"""Main GUI Application"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.connection import db
from views.quiz_view import QuizView
from views.question_bank_view import QuestionBankView
from views.statistics_view import StatisticsView
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_FAMILY, FONT_SIZE_TITLE


class QuizApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Initialize database
        db.initialize_database()
        
        # Create main container
        # Auto-create sample questions if database is empty
        self.check_and_create_sample_data()
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar and content area
        self.create_sidebar()
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show home view by default
        self.show_home()

    def setup_style(self):
        """Configure application styles - not needed with ttkbootstrap"""
        pass

    def check_and_create_sample_data(self):
        """Check if database has data, create sample questions if empty"""
        try:
            from models.question import Question
        except Exception:
            return

        # Check if questions exist
        try:
            question_count = Question.count()
        except Exception:
            question_count = 0

        if question_count == 0:
            print("📝 Database is empty. Creating sample questions...")
            try:
                from utils.sample_data import create_sample_questions_and_quizzes
                result = create_sample_questions_and_quizzes()
                created_q = result.get('questions_count') if isinstance(result, dict) else None
                print(f"✅ Created {created_q or 'N/A'} sample questions")
            except Exception as e:
                print(f"⚠️ Error creating sample data: {e}")
                try:
                    messagebox.showwarning(
                        "Cảnh báo",
                        f"Không thể tạo dữ liệu mẫu: {e}\nBạn có thể thêm câu hỏi thủ công trong Ngân hàng câu hỏi."
                    )
                except Exception:
                    pass
        else:
            print(f"✅ Database has {question_count} questions")

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = ttk.Frame(self.main_container, bootstyle="dark", width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # App title
        title_frame = ttk.Frame(sidebar, bootstyle="dark")
        title_frame.pack(pady=(25, 5))
        
        ttk.Label(title_frame, text="QUIZ APP", 
                 font=(FONT_FAMILY, 19, 'bold'),
                 bootstyle="inverse-dark").pack()

        
        ttk.Separator(sidebar, bootstyle="secondary").pack(fill=tk.X, padx=15, pady=(5, 20))
        
        # Navigation buttons
        nav_frame = ttk.Frame(sidebar, bootstyle="dark")
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=15)
        
        buttons = [
            ("🏠 Trang chủ", self.show_home, "primary"),
            ("📝 Làm bài thi", self.show_quiz, "success"),
            ("📚 Ngân hàng câu hỏi", self.show_question_bank, "info"),
            ("📊 Thống kê", self.show_statistics, "warning"),
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(nav_frame, text=text, command=command,
                          bootstyle=style,
                          width=22,
                          padding=(12, 12))
            btn.pack(fill=tk.X, pady=(0, 10))
            btn.configure(cursor="hand2")
        
        # Spacer
        ttk.Frame(nav_frame, bootstyle="dark", height=10).pack()
        
        # Exit button (separated at bottom)
        ttk.Separator(sidebar, bootstyle="secondary").pack(fill=tk.X, padx=15, pady=(0, 15))
        exit_btn = ttk.Button(sidebar, text="❌ Thoát", command=self.quit_app,
                            bootstyle="danger",
                            width=22,
                            padding=(12, 12))
        exit_btn.pack(fill=tk.X, padx=15, pady=(0, 20))
        exit_btn.configure(cursor="hand2")

    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Show home view"""
        self.clear_content()

        # Outer container
        outer = ttk.Frame(self.content_frame)
        outer.pack(fill=tk.BOTH, expand=True)

        # Hero card (centered)
        hero = ttk.Frame(outer, bootstyle="light")
        hero.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        hero_inner = ttk.Frame(hero)
        hero_inner.pack(expand=True, fill=tk.BOTH)

        ttk.Label(
            hero_inner,
            text="🎓",
            font=(FONT_FAMILY, 72),
            bootstyle="secondary"
        ).pack(pady=(10, 0))

        ttk.Label(
            hero_inner,
            text="Chào mừng đến với Quiz App",
            font=(FONT_FAMILY, FONT_SIZE_TITLE + 14, 'bold'),
            bootstyle="primary"
        ).pack(pady=(10, 6))

        ttk.Label(
            hero_inner,
            text="Luyện tập trắc nghiệm nhanh chóng • Quản lý ngân hàng câu hỏi • Theo dõi thống kê",
            font=(FONT_FAMILY, 13),
            bootstyle="secondary",
            justify=tk.CENTER,
            wraplength=860,
        ).pack(pady=(0, 18))

        ttk.Separator(hero_inner).pack(fill=tk.X, padx=60, pady=(0, 22))

        # Small stats row
        try:
            from models.question import Question
            total_questions = Question.count()
        except Exception:
            total_questions = 0

        try:
            from models.quiz import Quiz
            total_quizzes = Quiz.count()
        except Exception:
            total_quizzes = 0

        stats = ttk.Frame(hero_inner)
        stats.pack(pady=(0, 22))

        def _stat_item(parent, value, label, style):
            card = ttk.Frame(parent, bootstyle="light", padding=(22, 14))
            card.pack(side=tk.LEFT, padx=8)
            ttk.Label(card, text=str(value), font=(FONT_FAMILY, 24, 'bold'), bootstyle=style).pack()
            ttk.Label(card, text=label, font=(FONT_FAMILY, 11), bootstyle="secondary").pack(pady=(4, 0))

        _stat_item(stats, total_questions, "Câu hỏi", "info")
        _stat_item(stats, total_quizzes, "Bài thi", "warning")

        # Primary actions
        actions = ttk.Frame(hero_inner)
        actions.pack(pady=(0, 8))

        ttk.Button(
            actions,
            text="📝 Bắt đầu làm bài",
            command=self.show_quiz,
            bootstyle="success",
            width=24,
            padding=(18, 10),
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            actions,
            text="📚 Ngân hàng câu hỏi",
            command=self.show_question_bank,
            bootstyle="info",
            width=24,
            padding=(18, 10),
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            actions,
            text="📊 Xem thống kê",
            command=self.show_statistics,
            bootstyle="warning",
            width=24,
            padding=(18, 10),
        ).pack(side=tk.LEFT, padx=10)

        ttk.Label(
            hero_inner,
            font=(FONT_FAMILY, 11),
            bootstyle="secondary",
        ).pack(pady=(14, 0))

    def show_quiz(self):
        """Show quiz view"""
        self.clear_content()
        QuizView(self.content_frame)

    def show_question_bank(self):
        """Show question bank view"""
        self.clear_content()
        QuestionBankView(self.content_frame)

    def show_statistics(self):
        """Show statistics view"""
        self.clear_content()
        StatisticsView(self.content_frame)

    def quit_app(self):
        """Quit application"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.root.destroy()


def main():
    """Main entry point"""
    # Create ttkbootstrap window with theme
    root = ttk.Window(
        title="Quiz Application",
        themename="cosmo",  # Available: cosmo, flatly, litera, minty, lumen, sandstone, yeti, pulse, united, morph, journal, darkly, superhero, solar, cyborg, vapor, simplex, cerculean
        size=(WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    app = QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
