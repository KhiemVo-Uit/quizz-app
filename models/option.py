"""Option model"""
from models.base_model import BaseModel


class Option(BaseModel):
    """Option model for question choices"""

    def __init__(self, id=None, question_id=None, option_text='', is_correct=False, created_at=None):
        self.id = id
        self.question_id = question_id
        self.option_text = option_text
        self.is_correct = is_correct
        self.created_at = created_at

    @classmethod
    def _from_row(cls, row):
        """Create Option instance from database row"""
        if not row:
            return None
        return cls(
            id=row['id'],
            question_id=row['question_id'],
            option_text=row['option_text'],
            is_correct=bool(row['is_correct']),
            created_at=row['created_at']
        )

    @classmethod
    def _from_rows(cls, rows):
        """Create list of Option instances from database rows"""
        return [cls._from_row(row) for row in rows]

    @staticmethod
    def create(question_id, option_text, is_correct=False):
        """Create a new option"""
        return BaseModel.execute_insert(
            'INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)',
            (question_id, option_text, is_correct)
        )

    @classmethod
    def get_by_id(cls, option_id):
        """Get option by ID"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM options WHERE id = %s',
            (option_id,)
        )
        return cls._from_row(row)

    @classmethod
    def get_by_question(cls, question_id):
        """Get all options for a question"""
        rows = BaseModel.execute_query(
            'SELECT * FROM options WHERE question_id = %s ORDER BY id',
            (question_id,)
        )
        return cls._from_rows(rows)

    @classmethod
    def get_correct_option(cls, question_id):
        """Get the correct option for a question"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM options WHERE question_id = %s AND is_correct = 1',
            (question_id,)
        )
        return cls._from_row(row)

    @staticmethod
    def update(option_id, option_text=None, is_correct=None):
        """Update option"""
        query, params = BaseModel.build_update_query(
            'options',
            {'option_text': option_text, 'is_correct': is_correct}
        )
        if query:
            params.append(option_id)
            return BaseModel.execute_update(query, params)
        return False

    @staticmethod
    def delete(option_id):
        """Delete option"""
        return BaseModel.execute_update(
            'DELETE FROM options WHERE id = %s',
            (option_id,)
        )

    @staticmethod
    def delete_by_question(question_id):
        """Delete all options for a question"""
        return BaseModel.execute_update(
            'DELETE FROM options WHERE question_id = %s',
            (question_id,)
        )
