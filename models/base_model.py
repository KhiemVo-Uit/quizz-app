"""Base Model with common database operations (DRY principle)"""
from database.connection import db
from contextlib import contextmanager


class BaseModel:
    """Base class providing common database operations to reduce code duplication"""
    
    # Subclasses should override these
    _table_name = None
    _fields = []
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=False):
        """
        Context manager for database operations.
        Automatically handles connection open/close.
        
        Usage:
            with BaseModel.get_cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM table')
                result = cursor.fetchall()
        """
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=dictionary)
            yield cursor
            conn.commit()
        finally:
            db.close_connection(conn)
    
    @staticmethod
    def execute_query(query, params=None, dictionary=True):
        """
        Execute a SELECT query and return all results.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or None)
            dictionary: If True, return dict rows; else tuple rows
            
        Returns:
            List of rows
        """
        with BaseModel.get_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    
    @staticmethod
    def execute_query_one(query, params=None, dictionary=True):
        """
        Execute a SELECT query and return one result.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or None)
            dictionary: If True, return dict row; else tuple row
            
        Returns:
            Single row or None
        """
        with BaseModel.get_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    
    @staticmethod
    def execute_insert(query, params=None):
        """
        Execute an INSERT query and return the last inserted ID.
        
        Args:
            query: SQL INSERT query string
            params: Query parameters (tuple or None)
            
        Returns:
            Last inserted row ID
        """
        with BaseModel.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid
    
    @staticmethod
    def execute_update(query, params=None):
        """
        Execute an UPDATE/DELETE query and return affected row count.
        
        Args:
            query: SQL UPDATE/DELETE query string
            params: Query parameters (tuple or None)
            
        Returns:
            True if at least one row was affected, False otherwise
        """
        with BaseModel.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount > 0
    
    @staticmethod
    def execute_count(query, params=None):
        """
        Execute a COUNT query and return the count value.
        
        Args:
            query: SQL COUNT query string
            params: Query parameters (tuple or None)
            
        Returns:
            Integer count value
        """
        result = BaseModel.execute_query_one(query, params, dictionary=True)
        return result['count'] if result else 0
    
    @staticmethod
    def build_update_query(table_name, updates_dict, where_field='id'):
        """
        Build an UPDATE query dynamically from a dictionary.
        
        Args:
            table_name: Name of the table to update
            updates_dict: Dictionary of {field_name: value} to update (None values are skipped)
            where_field: Field name for WHERE clause
            
        Returns:
            Tuple of (query_string, params_list) or (None, None) if no updates
        """
        updates = []
        params = []
        
        for field, value in updates_dict.items():
            if value is not None:
                updates.append(f'{field} = %s')
                params.append(value)
        
        if not updates:
            return None, None
            
        query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE {where_field} = %s"
        return query, params

