# Import from the database service module at services level
from services.database import database, get_database, get_db, create_tables, drop_tables

__all__ = ['database', 'get_database', 'get_db', 'create_tables', 'drop_tables']
