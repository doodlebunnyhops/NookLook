# Database Migrations

This directory contains database migration files for schema updates.

## Naming Convention
Migrations should be named: `YYYYMMDD_HHMMSS_description.sql`

For example: `20241114_120000_add_user_favorites.sql`

## Migration Format
Each migration file should contain:
1. Comments describing the change
2. SQL statements to apply the migration
3. Proper error handling where applicable

## Current Schema
The current base schema is in the parent directory `items.sql`.