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

    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = ttk.Frame(self.main_container, bootstyle="dark", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # App title
        title = ttk.Label(sidebar, text="QUIZ APP", 
                        font=(FONT_FAMILY, 16, 'bold'),
                        bootstyle="inverse-dark")
        title.pack(pady=20)
        
        # Navigation buttons
        buttons = [
            ("🏠 Trang chủ", self.show_home, "primary"),
            ("📝 Làm bài thi", self.show_quiz, "success"),
            ("📚 Ngân hàng câu hỏi", self.show_question_bank, "info"),
            ("📊 Thống kê", self.show_statistics, "warning"),
            ("❌ Thoát", self.quit_app, "danger")
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(sidebar, text=text, command=command,
                          bootstyle=style, width=20)
            btn.pack(fill=tk.X, padx=10, pady=5)

    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Show home view"""
        self.clear_content()
        
        container = ttk.Frame(self.content_frame)
        container.pack(expand=True)
        
        # Welcome message
        welcome = ttk.Label(container, 
                           text="Chào mừng đến với Quiz App",
                           font=(FONT_FAMILY, FONT_SIZE_TITLE, 'bold'),
                           bootstyle="primary")
        welcome.pack(pady=20)
        
        description = ttk.Label(container,
                               text="Hệ thống thi trắc nghiệm trực tuyến",
                               font=(FONT_FAMILY, 12))
        description.pack(pady=10)
        
        # Quick actions
        actions_frame = ttk.Frame(container)
        actions_frame.pack(pady=30)
        
        ttk.Button(actions_frame, text="Bắt đầu làm bài",
                  command=self.show_quiz,
                  bootstyle="success-outline",
                  width=20).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(actions_frame, text="Quản lý câu hỏi",
                  command=self.show_question_bank,
                  bootstyle="info-outline",
                  width=20).pack(side=tk.LEFT, padx=10)

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
            db.close_connection()
            self.root.quit()


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
