"""Quiz model"""
from mysql.connector import Error as MySQLError
from models.base_model import BaseModel
from database.connection import db


class Quiz(BaseModel):
    """Quiz model"""

    def __init__(self, id=None, title='', description='', time_limit=600, 
                 total_questions=0, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.time_limit = time_limit
        self.total_questions = total_questions
        self.created_at = created_at

    @classmethod
    def _from_row(cls, row):
        """Create Quiz instance from database row"""
        if not row:
            return None
        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            time_limit=row['time_limit'],
            total_questions=row['total_questions'],
            created_at=row['created_at']
        )

    @classmethod
    def _from_rows(cls, rows):
        """Create list of Quiz instances from database rows"""
        return [cls._from_row(row) for row in rows]

    @staticmethod
    def create(title, description='', time_limit=600, total_questions=10):
        """Create a new quiz (returns existing quiz_id if title already exists)"""
        # Need special handling for duplicate title check
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                'INSERT INTO quizzes (title, description, time_limit, total_questions) VALUES (%s, %s, %s, %s)',
                (title, description, time_limit, total_questions)
            )
            conn.commit()
            quiz_id = cursor.lastrowid
            db.close_connection(conn)
            return quiz_id
        except MySQLError:
            # Title already exists, return existing quiz ID
            cursor.execute('SELECT id FROM quizzes WHERE title = %s', (title,))
            row = cursor.fetchone()
            db.close_connection(conn)
            return row['id'] if row else None

    @classmethod
    def get_by_id(cls, quiz_id):
        """Get quiz by ID"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM quizzes WHERE id = %s',
            (quiz_id,)
        )
        return cls._from_row(row)

    @classmethod
    def get_by_title(cls, title):
        """Get quiz by title"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM quizzes WHERE title = %s',
            (title,)
        )
        return cls._from_row(row)

    @classmethod
    def get_all(cls):
        """Get all quizzes"""
        rows = BaseModel.execute_query('SELECT * FROM quizzes ORDER BY created_at DESC')
        return cls._from_rows(rows)

    @staticmethod
    def update(quiz_id, title=None, description=None, time_limit=None, total_questions=None):
        """Update quiz"""
        query, params = BaseModel.build_update_query(
            'quizzes',
            {
                'title': title,
                'description': description,
                'time_limit': time_limit,
                'total_questions': total_questions
            }
        )
        if query:
            params.append(quiz_id)
            return BaseModel.execute_update(query, params)
        return False

    @staticmethod
    def delete(quiz_id):
        """Delete quiz"""
        return BaseModel.execute_update(
            'DELETE FROM quizzes WHERE id = %s',
            (quiz_id,)
        )

    @staticmethod
    def count():
        """Count total quizzes"""
        return BaseModel.execute_count('SELECT COUNT(*) as count FROM quizzes')
