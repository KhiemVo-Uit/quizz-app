"""Database connection and initialization"""
import sqlite3
from config import DATABASE_PATH


class Database:
    """Singleton database connection handler"""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        """Get database connection"""
        if self._connection is None:
            conn = sqlite3.connect(DATABASE_PATH)  
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            self._connection = conn
        return self._connection

    def close_connection(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def initialize_database(self):
        """Create all tables with constraints"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                difficulty INTEGER NOT NULL CHECK(difficulty IN (1, 2, 3)),
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT question_text_not_empty CHECK(length(trim(question_text)) > 0)
            )
        ''')

        # Options table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                option_text TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                CONSTRAINT option_text_not_empty CHECK(length(trim(option_text)) > 0)
            )
        ''')

        # Quizzes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                time_limit INTEGER NOT NULL DEFAULT 600,
                total_questions INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT title_not_empty CHECK(length(trim(title)) > 0),
                CONSTRAINT time_limit_positive CHECK(time_limit > 0),
                CONSTRAINT total_questions_positive CHECK(total_questions > 0)
            )
        ''')

        # Quiz questions mapping (for specific question selection)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                question_order INTEGER NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                CONSTRAINT unique_question_in_quiz UNIQUE(quiz_id, question_id),
                CONSTRAINT unique_order_in_quiz UNIQUE(quiz_id, question_order)
            )
        ''')

        # Attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                score REAL NOT NULL DEFAULT 0,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                time_taken INTEGER,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
                CONSTRAINT student_name_not_empty CHECK(length(trim(student_name)) > 0),
                CONSTRAINT score_valid CHECK(score >= 0),
                CONSTRAINT correct_answers_valid CHECK(correct_answers >= 0 AND correct_answers <= total_questions)
            )
        ''')

        # Attempt answers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempt_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                selected_option_id INTEGER,
                is_correct BOOLEAN NOT NULL DEFAULT 0,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attempt_id) REFERENCES attempts(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                FOREIGN KEY (selected_option_id) REFERENCES options(id) ON DELETE SET NULL,
                CONSTRAINT unique_question_per_attempt UNIQUE(attempt_id, question_id)
            )
        ''')

        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_options_question ON options(question_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_quiz_questions_quiz ON quiz_questions(quiz_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempts_quiz ON attempts(quiz_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempt_answers_attempt ON attempt_answers(attempt_id)')

        conn.commit()

    def reset_database(self):
        """Drop all tables and reinitialize (for testing)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        tables = ['attempt_answers', 'attempts', 'quiz_questions', 'quizzes', 'options', 'questions']
        for table in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')

        conn.commit()
        self.initialize_database()


# Create global database instance
db = Database()
