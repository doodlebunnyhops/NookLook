import aiosqlite
import pathlib
import logging
import asyncio
from typing import Optional, List, Dict, Any, ClassVar

logger = logging.getLogger("bot.database")

class Database:
    """Base database class for handling SQLite operations with connection pooling
    
    Uses a singleton pattern per db_path to share connections across repositories.
    """
    
    # Class-level registry of all Database instances
    _instances: ClassVar[Dict[str, 'Database']] = {}
    
    def __new__(cls, db_path: str):
        """Return existing instance for this db_path or create new one"""
        # Normalize path for consistent key
        normalized_path = str(pathlib.Path(db_path).resolve())
        
        if normalized_path not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[normalized_path] = instance
        
        return cls._instances[normalized_path]
    
    def __init__(self, db_path: str):
        # Only initialize once
        if getattr(self, '_initialized', False):
            return
            
        self.db_path = db_path
        self.db_dir = pathlib.Path(db_path).parent
        self._connection: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()
        self._initialized = True
        
        # Debug logging for database initialization
        logger.debug(f" Database __init__: db_path = {db_path}")
        logger.debug(f" Database __init__: absolute path = {pathlib.Path(db_path).resolve()}")
        logger.debug(f" Database __init__: db_path exists = {pathlib.Path(db_path).exists()}")
    
    @classmethod
    async def close_all(cls):
        """Close all database connections (call on shutdown)"""
        for path, instance in cls._instances.items():
            if instance._connection is not None:
                try:
                    await instance._connection.close()
                    instance._connection = None
                    logger.info(f"Closed database connection: {path}")
                except Exception as e:
                    logger.error(f"Error closing database {path}: {e}")
        cls._instances.clear()
    
    async def _get_connection(self) -> aiosqlite.Connection:
        """Get or create a persistent database connection"""
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
            # Enable foreign key constraints (required for ON DELETE CASCADE)
            await self._connection.execute("PRAGMA foreign_keys=ON")
            # Enable WAL mode for better concurrent read performance
            await self._connection.execute("PRAGMA journal_mode=WAL")
            await self._connection.execute("PRAGMA synchronous=NORMAL")
            logger.info(f"Database connection established: {self.db_path}")
        return self._connection
    
    async def close(self):
        """Close the persistent connection"""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None
            logger.info("Database connection closed")
        
    async def ensure_db_directory(self):
        """Ensure the database directory exists"""
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
    async def init_from_schema(self, schema_path: str):
        """Initialize database from a schema file"""
        schema_file = pathlib.Path(schema_path)
        
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
            
        await self.ensure_db_directory()
        
        # Read schema file
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        async with aiosqlite.connect(self.db_path) as db:
            for statement in statements:
                try:
                    await db.execute(statement)
                    logger.debug(f"Executed schema statement: {statement[:50]}...")
                except Exception as e:
                    logger.error(f"Error executing schema statement: {e}")
                    logger.error(f"Statement: {statement}")
                    raise
            
            await db.commit()
            logger.info(f"Database initialized from schema: {schema_path}")
    
    async def ensure_schema(self, schema_path: str = None):
        """Ensure all tables from schema exist (uses CREATE TABLE IF NOT EXISTS)
        
        This is safe to call on every startup - it will only create missing tables.
        """
        if schema_path is None:
            # Default to project schema
            schema_path = pathlib.Path(self.db_path).parent.parent / "schemas" / "nooklook_schema.sql"
        
        schema_file = pathlib.Path(schema_path)
        
        if not schema_file.exists():
            logger.warning(f"Schema file not found: {schema_path}")
            return
        
        # Read schema file
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Parse statements properly - handle triggers with embedded semicolons
        # Split on semicolons but rejoin trigger bodies
        statements = []
        current_stmt = []
        in_trigger = False
        
        for line in schema_sql.split('\n'):
            stripped = line.strip().upper()
            
            # Track if we're inside a trigger
            if 'CREATE TRIGGER' in stripped:
                in_trigger = True
            
            current_stmt.append(line)
            
            # Check for end of trigger or regular statement
            if in_trigger and stripped == 'END;':
                statements.append('\n'.join(current_stmt))
                current_stmt = []
                in_trigger = False
            elif not in_trigger and line.rstrip().endswith(';'):
                statements.append('\n'.join(current_stmt))
                current_stmt = []
        
        # Add any remaining statement
        if current_stmt:
            remaining = '\n'.join(current_stmt).strip()
            if remaining:
                statements.append(remaining)
        
        async with self._lock:
            db = await self._get_connection()
            created_count = 0
            
            for statement in statements:
                statement = statement.strip()
                if not statement:
                    continue
                    
                # Only process CREATE IF NOT EXISTS statements for safety
                stmt_upper = statement.upper()
                if not ('CREATE TABLE IF NOT EXISTS' in stmt_upper or 
                        'CREATE INDEX IF NOT EXISTS' in stmt_upper or
                        'CREATE TRIGGER IF NOT EXISTS' in stmt_upper or
                        'CREATE VIRTUAL TABLE IF NOT EXISTS' in stmt_upper):
                    continue
                
                try:
                    await db.execute(statement)
                    created_count += 1
                except Exception as e:
                    # Log but don't fail - table might already exist
                    if "already exists" not in str(e).lower():
                        logger.debug(f"Schema statement skipped: {e}")
            
            await db.commit()
            if created_count > 0:
                logger.info(f"Schema check complete: processed {created_count} CREATE statements")
            
            # Handle migrations for existing tables that need new columns
            await self._run_migrations(db)
    
    async def _run_migrations(self, db):
        """Run any necessary migrations for existing tables"""
        
        # Check if stash_items needs migration to REMOVE the unique constraint (allow duplicates for TI orders)
        await self._migrate_stash_items_allow_duplicates(db)

    async def _migrate_stash_items_allow_duplicates(self, db):
        """
        Migrate stash_items table to REMOVE the UNIQUE constraint.
        This allows users to add duplicate items for TI orders.
        SQLite doesn't support ALTER TABLE to modify constraints, so we must recreate the table.
        """
        try:
            # Check if table exists
            cursor = await db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='stash_items'"
            )
            table_exists = await cursor.fetchone()
            await cursor.close()

            if not table_exists:
                return  # Table doesn't exist yet, schema will create it correctly

            # Check current table schema for the UNIQUE constraint
            cursor = await db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='stash_items'")
            result = await cursor.fetchone()
            await cursor.close()

            if not result:
                logger.error("Failed to retrieve stash_items table schema for migration check")
                return

            table_sql = result[0] or ""

            # If there's NO UNIQUE constraint, we're good (duplicates allowed)
            if "UNIQUE" not in table_sql:
                logger.info("stash_items table already allows duplicates (no UNIQUE constraint)")
                return

            logger.info("Migrating stash_items table to allow duplicate items for TI orders...")

            # Create new table WITHOUT the UNIQUE constraint
            await db.execute("""
                CREATE TABLE IF NOT EXISTS stash_items_new (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    stash_id            INTEGER NOT NULL REFERENCES user_stashes(id) ON DELETE CASCADE,
                    ref_table           TEXT NOT NULL,
                    ref_id              INTEGER NOT NULL,
                    variant_id          INTEGER,
                    display_name        TEXT NOT NULL,
                    added_at            DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)            # Copy data from old table
            await db.execute("""
                INSERT INTO stash_items_new (id, stash_id, ref_table, ref_id, variant_id, display_name, added_at)
                SELECT id, stash_id, ref_table, ref_id, variant_id, display_name, added_at
                FROM stash_items
            """)
            
            # Drop old table
            await db.execute("DROP TABLE stash_items")
            
            # Rename new table
            await db.execute("ALTER TABLE stash_items_new RENAME TO stash_items")

            # Recreate index
            await db.execute("CREATE INDEX IF NOT EXISTS idx_stash_items_stash_id ON stash_items(stash_id)")

            await db.commit()
            logger.info("Successfully migrated stash_items table to allow duplicates for TI orders")

        except Exception as e:
            logger.error(f"Failed to migrate stash_items table: {e}")
            # Don't fail - the table will still work

    async def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        async with self._lock:
            db = await self._get_connection()
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            await cursor.close()
            return [dict(row) for row in rows]
    
    async def execute_query_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Execute a SELECT query and return first result as dictionary"""
        async with self._lock:
            db = await self._get_connection()
            cursor = await db.execute(query, params)
            row = await cursor.fetchone()
            await cursor.close()
            return dict(row) if row else None
    
    async def execute_command(self, command: str, params: tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE command and return affected rows"""
        async with self._lock:
            db = await self._get_connection()
            cursor = await db.execute(command, params)
            await db.commit()
            affected_rows = cursor.rowcount
            await cursor.close()
            return affected_rows