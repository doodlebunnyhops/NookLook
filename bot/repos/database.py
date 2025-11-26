import aiosqlite
import pathlib
import logging
import asyncio
from typing import Optional, List, Dict, Any

logger = logging.getLogger("bot.database")

class Database:
    """Base database class for handling SQLite operations with connection pooling"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db_dir = pathlib.Path(db_path).parent
        self._connection: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()
        
        # Debug logging for database initialization
        logger.debug(f" Database __init__: db_path = {db_path}")
        logger.debug(f" Database __init__: absolute path = {pathlib.Path(db_path).resolve()}")
        logger.debug(f" Database __init__: db_path exists = {pathlib.Path(db_path).exists()}")
    
    async def _get_connection(self) -> aiosqlite.Connection:
        """Get or create a persistent database connection"""
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
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