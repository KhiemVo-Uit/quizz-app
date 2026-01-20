"""Option model"""
from database.connection import db


class Option:
    """Option model for question choices"""

    def __init__(self, id=None, question_id=None, option_text='', is_correct=False, created_at=None):
        self.id = id
        self.question_id = question_id
        self.option_text = option_text
        self.is_correct = is_correct
        self.created_at = created_at

    @staticmethod
    def create(question_id, option_text, is_correct=False):
        """Create a new option"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO options (question_id, option_text, is_correct)
            VALUES (%s, %s, %s)
        ''', (question_id, option_text, is_correct))

        conn.commit()
        option_id = cursor.lastrowid
        db.close_connection(conn)
        return option_id

    @staticmethod
    def get_by_id(option_id):
        """Get option by ID"""
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM options WHERE id = %s', (option_id,))
        row = cursor.fetchone()
        db.close_connection(conn)

        if row:
            return Option(
                id=row['id'],
                question_id=row['question_id'],
                option_text=row['option_text'],
                is_correct=bool(row['is_correct']),
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def get_by_question(question_id):
        """Get all options for a question"""
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM options WHERE question_id = %s ORDER BY id', (question_id,))
        rows = cursor.fetchall()
        db.close_connection(conn)

        return [Option(
            id=row['id'],
            question_id=row['question_id'],
            option_text=row['option_text'],
            is_correct=bool(row['is_correct']),
            created_at=row['created_at']
        ) for row in rows]

    @staticmethod
    def get_correct_option(question_id):
        """Get the correct option for a question"""
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
            SELECT * FROM options 
            WHERE question_id = %s AND is_correct = 1
        ''', (question_id,))
        row = cursor.fetchone()
        db.close_connection(conn)

        if row:
            return Option(
                id=row['id'],
                question_id=row['question_id'],
                option_text=row['option_text'],
                is_correct=bool(row['is_correct']),
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def update(option_id, option_text=None, is_correct=None):
        """Update option"""
        conn = db.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if option_text is not None:
            updates.append('option_text = %s')
            params.append(option_text)
        if is_correct is not None:
            updates.append('is_correct = %s')
            params.append(is_correct)

        if updates:
            params.append(option_id)
            query = f"UPDATE options SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
            result = cursor.rowcount > 0
            db.close_connection(conn)
            return result
        db.close_connection(conn)
        return False

    @staticmethod
    def delete(option_id):
        """Delete option"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM options WHERE id = %s', (option_id,))
        conn.commit()
        result = cursor.rowcount > 0
        db.close_connection(conn)
        return result

    @staticmethod
    def delete_by_question(question_id):
        """Delete all options for a question"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM options WHERE question_id = %s', (question_id,))
        conn.commit()
        result = cursor.rowcount > 0
        db.close_connection(conn)
        return result
