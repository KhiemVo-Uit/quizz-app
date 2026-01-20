"""Database connection and initialization for MySQL"""
import mysql.connector
from mysql.connector import pooling, Error
from config import MYSQL_CONFIG


class Database:
    """Singleton database connection handler for MySQL"""
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def _create_pool(self):
        """Create connection pool"""
        if self._connection_pool is None:
            try:
                # Tạo database nếu chưa tồn tại
                temp_config = MYSQL_CONFIG.copy()
                db_name = temp_config.pop('database')
                temp_config.pop('pool_name', None)
                temp_config.pop('pool_size', None)
                
                temp_conn = mysql.connector.connect(**temp_config)
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                temp_conn.close()
                
                # Tạo connection pool
                self._connection_pool = pooling.MySQLConnectionPool(**MYSQL_CONFIG)
            except Error as e:
                print(f"Error creating connection pool: {e}")
                raise

    def get_connection(self):
        """Get database connection from pool"""
        self._create_pool()
        try:
            conn = self._connection_pool.get_connection()
            return conn
        except Error as e:
            print(f"Error getting connection: {e}")
            raise

    def close_connection(self, conn):
        """Return connection to pool"""
        if conn and conn.is_connected():
            conn.close()

    def initialize_database(self):
        """Create all tables with constraints"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT NOT NULL,
                difficulty INT NOT NULL,
                category VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT chk_difficulty CHECK (difficulty IN (1, 2, 3)),
                INDEX idx_questions_difficulty (difficulty),
                INDEX idx_questions_category (category)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # Options table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question_id INT NOT NULL,
                option_text TEXT NOT NULL,
                is_correct BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                INDEX idx_options_question (question_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # Quizzes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL UNIQUE,
                description TEXT,
                time_limit INT NOT NULL DEFAULT 600,
                total_questions INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT chk_time_limit CHECK (time_limit > 0),
                CONSTRAINT chk_total_questions CHECK (total_questions > 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # Attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                quiz_id INT NOT NULL,
                student_name VARCHAR(255) NOT NULL,
                score DECIMAL(5,2) NOT NULL DEFAULT 0,
                total_questions INT NOT NULL,
                correct_answers INT NOT NULL DEFAULT 0,
                time_taken INT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
                CONSTRAINT chk_score CHECK (score >= 0),
                CONSTRAINT chk_correct_answers CHECK (correct_answers >= 0),
                INDEX idx_attempts_quiz (quiz_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # Attempt answers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attempt_answers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                attempt_id INT NOT NULL,
                question_id INT NOT NULL,
                selected_option_id INT,
                is_correct BOOLEAN NOT NULL DEFAULT FALSE,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (attempt_id) REFERENCES attempts(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                FOREIGN KEY (selected_option_id) REFERENCES options(id) ON DELETE SET NULL,
                UNIQUE KEY unique_question_per_attempt (attempt_id, question_id),
                INDEX idx_attempt_answers_attempt (attempt_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        conn.commit()
        self.close_connection(conn)

    def reset_database(self):
        """Drop all tables and reinitialize (for testing)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Disable foreign key checks for dropping tables
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
        
        tables = ['attempt_answers', 'attempts', 'quizzes', 'options', 'questions']
        for table in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')

        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
        conn.commit()
        self.close_connection(conn)
        
        self.initialize_database()


# Create global database instance
db = Database()
