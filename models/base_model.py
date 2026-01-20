from database.connection import db
from contextlib import contextmanager


class BaseModel:
    _table_name = None  # protected
    _fields = []  # protected
    
    @staticmethod
    @contextmanager
    def get_cursor(dictionary=False):
        conn = db.get_connection()
        try:
            cursor = conn.cursor(dictionary=dictionary)
            yield cursor
            conn.commit()
        finally:
            db.close_connection(conn)
    
    @staticmethod
    def execute_query(query, params=None, dictionary=True):
        with BaseModel.get_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    
    @staticmethod
    def execute_query_one(query, params=None, dictionary=True):
        with BaseModel.get_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    
    @staticmethod
    def execute_insert(query, params=None):
        with BaseModel.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid
    
    @staticmethod
    def execute_update(query, params=None):
        with BaseModel.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount > 0
    
    @staticmethod
    def execute_count(query, params=None):
        result = BaseModel.execute_query_one(query, params, dictionary=True)
        return result['count'] if result else 0
    
    @staticmethod
    def build_update_query(table_name, updates_dict, where_field='id'):
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

