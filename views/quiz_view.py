"""Quiz Taking View"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time
from controllers.quiz_controller import QuizController
from models.quiz import Quiz
from config import FONT_FAMILY, COLOR_SUCCESS, COLOR_DANGER, COLOR_PRIMARY


class QuizView:
    """View for taking quizzes"""

    def __init__(self, parent):
        self.parent = parent
        self.current_quiz = None
        self.current_attempt = None
        self.current_question_index = 0
        self.answers = {}
        self.start_time = None
        self.timer_running = False
        self.time_remaining = 0
        
        self.show_quiz_list()

    def show_quiz_list(self):
        """Show list of available quizzes"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header with title and action button
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=30, pady=20)
        
        ttk.Label(header, text="📝 Danh sách bài thi", 
                 font=(FONT_FAMILY, 20, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Quiz list with better container
        container = ttk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        list_frame = ttk.Frame(container)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        quizzes = Quiz.get_all()
        
        if not quizzes:
            empty_frame = ttk.Frame(list_frame)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="📋",
                     font=(FONT_FAMILY, 48)).pack(pady=20)
            ttk.Label(empty_frame, text="Chưa có bài thi nào",
                     font=(FONT_FAMILY, 16)).pack(pady=10)
            ttk.Button(empty_frame, text="🎯 Tạo bài thi mẫu",
                      command=self.create_sample_quiz,
                      bootstyle="success",
                      width=20).pack(pady=20)
            return
        
        # Create quiz cards
        for quiz in quizzes:
            self.create_quiz_card(list_frame, quiz)

    def create_quiz_card(self, parent, quiz):
        """Create a card for each quiz"""
        card = ttk.Frame(parent, bootstyle="light")
        card.pack(fill=tk.X, pady=8, padx=5)
        
        # Inner card with border
        inner = ttk.Frame(card, relief=tk.SOLID, borderwidth=1)
        inner.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(inner)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Title with icon
        ttk.Label(info_frame, text=f"📚 {quiz.title}",
                 font=(FONT_FAMILY, 14, 'bold'),
                 bootstyle="primary").pack(anchor=tk.W)
        
        # Description
        ttk.Label(info_frame, text=quiz.description or "Không có mô tả",
                 font=(FONT_FAMILY, 10),
                 bootstyle="secondary").pack(anchor=tk.W, pady=(5, 8))
        
        # Info badges
        info_container = ttk.Frame(info_frame)
        info_container.pack(anchor=tk.W)
        
        ttk.Label(info_container, 
                 text=f"⏱ {quiz.time_limit//60} phút",
                 font=(FONT_FAMILY, 9),
                 bootstyle="info").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Label(info_container, 
                 text=f"📝 {quiz.total_questions} câu",
                 font=(FONT_FAMILY, 9),
                 bootstyle="info").pack(side=tk.LEFT)
        
        # Button
        btn_frame = ttk.Frame(inner)
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        ttk.Button(btn_frame, text="Bắt đầu làm bài",
                  command=lambda q=quiz: self.start_quiz(q),
                  bootstyle="success",
                  width=15).pack()

    def start_quiz(self, quiz):
        """Start taking a quiz"""
        # Get student name
        name_dialog = tk.Toplevel(self.parent)
        name_dialog.title("Thông tin sinh viên")
        name_dialog.geometry("400x200")
        name_dialog.transient(self.parent)
        name_dialog.grab_set()
        
        # Center the dialog
        name_dialog.update_idletasks()
        x = (name_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (name_dialog.winfo_screenheight() // 2) - (200 // 2)
        name_dialog.geometry(f"400x200+{x}+{y}")
        
        container = ttk.Frame(name_dialog)
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        ttk.Label(container, text="👤 Nhập tên của bạn:",
                 font=(FONT_FAMILY, 13, 'bold'),
                 bootstyle="primary").pack(pady=(0, 15))
        
        name_entry = ttk.Entry(container, font=(FONT_FAMILY, 12), width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def submit_name():
            student_name = name_entry.get().strip()
            if not student_name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên!")
                return
            
            name_dialog.destroy()
            self.initialize_quiz(quiz, student_name)
        
        ttk.Button(container, text="🚀 Bắt đầu làm bài",
                  command=submit_name,
                  bootstyle="success",
                  width=20).pack(pady=15)
        name_entry.bind('<Return>', lambda e: submit_name())

    def initialize_quiz(self, quiz, student_name):
        """Initialize quiz session"""
        # Get quiz data with questions
        quiz_data = QuizController.get_quiz_with_questions(quiz.id)
        if not quiz_data:
            messagebox.showerror("Lỗi", "Không thể tải bài thi!")
            return
        
        # Start attempt
        attempt_id = QuizController.start_attempt(quiz.id, student_name)
        
        self.current_quiz = quiz_data
        self.current_attempt = attempt_id
        self.current_question_index = 0
        self.answers = {}
        self.start_time = time.time()
        self.time_remaining = quiz.time_limit
        
        self.show_quiz_interface()

    def show_quiz_interface(self):
        """Show quiz taking interface"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header with gradient-like styling
        header = ttk.Frame(self.parent, bootstyle="primary")
        header.pack(fill=tk.X, padx=30, pady=(20, 15))
        
        header_inner = ttk.Frame(header)
        header_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        ttk.Label(header_inner, text=f"📝 {self.current_quiz['quiz'].title}",
                 font=(FONT_FAMILY, 16, 'bold'),
                 bootstyle="inverse-primary").pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(header_inner, text="",
                                     font=(FONT_FAMILY, 16, 'bold'),
                                     bootstyle="inverse-primary")
        self.timer_label.pack(side=tk.RIGHT)
        
        # Question container with card styling
        container_outer = ttk.Frame(self.parent)
        container_outer.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        self.question_container = ttk.Frame(container_outer, bootstyle="light")
        self.question_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Navigation buttons with better styling
        nav_frame = ttk.Frame(self.parent)
        nav_frame.pack(fill=tk.X, padx=30, pady=(10, 20))
        
        self.prev_btn = ttk.Button(nav_frame, text="◀ Câu trước",
                                   command=self.previous_question,
                                   bootstyle="secondary-outline",
                                   width=15)
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = ttk.Button(nav_frame, text="Câu sau ▶",
                                   command=self.next_question,
                                   bootstyle="primary",
                                   width=15)
        self.next_btn.pack(side=tk.RIGHT)
        
        self.submit_btn = ttk.Button(nav_frame, text="✅ Nộp bài",
                                     command=self.submit_quiz,
                                     bootstyle="success",
                                     width=15)
        
        # Show first question
        self.show_question()
        
        # Start timer
        self.timer_running = True
        self.update_timer()

    def show_question(self):
        """Display current question"""
        for widget in self.question_container.winfo_children():
            widget.destroy()
        
        question_data = self.current_quiz['questions'][self.current_question_index]
        question = question_data['question']
        options = question_data['options']
        
        # Question card
        q_card = ttk.Frame(self.question_container)
        q_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Question header
        header = ttk.Frame(q_card)
        header.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header,
                 text=f"📝 Câu {self.current_question_index + 1}/{len(self.current_quiz['questions'])}",
                 font=(FONT_FAMILY, 14, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Difficulty badge
        difficulty_text = {1: "Dễ", 2: "Trung bình", 3: "Khó"}
        difficulty_style = {1: "success", 2: "warning", 3: "danger"}
        ttk.Label(header,
                 text=difficulty_text.get(question.difficulty, 'N/A'),
                 font=(FONT_FAMILY, 9),
                 bootstyle=difficulty_style.get(question.difficulty, "secondary")).pack(side=tk.RIGHT)
        
        # Question text
        ttk.Label(q_card,
                 text=question.question_text,
                 font=(FONT_FAMILY, 13),
                 wraplength=900).pack(anchor=tk.W, pady=(0, 20))
        
        # Options with better styling
        options_label = ttk.Label(q_card, text="Chọn đáp án:",
                                 font=(FONT_FAMILY, 11, 'bold'),
                                 bootstyle="secondary")
        options_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.selected_option = tk.IntVar(value=self.answers.get(question.id, -1))
        
        for i, option in enumerate(options, 1):
            option_frame = ttk.Frame(q_card, bootstyle="light")
            option_frame.pack(fill=tk.X, pady=4, padx=10)
            
            rb = ttk.Radiobutton(option_frame,
                                text=f"{chr(64+i)}. {option.option_text}",
                                variable=self.selected_option,
                                value=option.id,
                                bootstyle="primary",
                                command=lambda q=question.id, o=option.id: self.save_answer(q, o))
            rb.pack(anchor=tk.W, pady=8, padx=15)
        
        # Update navigation buttons
        self.prev_btn.config(state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED)
        
        if self.current_question_index == len(self.current_quiz['questions']) - 1:
            self.next_btn.pack_forget()
            self.submit_btn.pack(side=tk.RIGHT)
        else:
            self.submit_btn.pack_forget()
            self.next_btn.pack(side=tk.RIGHT)

    def save_answer(self, question_id, option_id):
        """Save selected answer"""
        self.answers[question_id] = option_id

    def previous_question(self):
        """Go to previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        """Go to next question"""
        if self.current_question_index < len(self.current_quiz['questions']) - 1:
            self.current_question_index += 1
            self.show_question()

    def update_timer(self):
        """Update countdown timer"""
        if not self.timer_running:
            return
        
        self.time_remaining -= 1
        
        if self.time_remaining <= 0:
            self.timer_running = False
            messagebox.showinfo("Hết giờ", "Đã hết thời gian làm bài!")
            self.submit_quiz()
            return
        
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"⏱ {minutes:02d}:{seconds:02d}")
        
        # Change color when time is running out
        if self.time_remaining < 60:
            self.timer_label.config(foreground=COLOR_DANGER)
        elif self.time_remaining < 300:
            self.timer_label.config(foreground='orange')
        
        self.parent.after(1000, self.update_timer)

    def submit_quiz(self):
        """Submit quiz answers"""
        if len(self.answers) < len(self.current_quiz['questions']):
            unanswered = len(self.current_quiz['questions']) - len(self.answers)
            if not messagebox.askyesno("Xác nhận",
                                       f"Bạn còn {unanswered} câu chưa trả lời.\nBạn có chắc muốn nộp bài?"):
                return
        
        self.timer_running = False
        
        # Submit all answers
        for question_data in self.current_quiz['questions']:
            question_id = question_data['question'].id
            selected_option = self.answers.get(question_id)
            QuizController.submit_answer(self.current_attempt, question_id, selected_option)
        
        # Calculate time taken
        time_taken = int(time.time() - self.start_time)
        
        # Complete attempt
        result = QuizController.complete_attempt(self.current_attempt, time_taken)
        
        # Show results
        self.show_results(result)

    def show_results(self, result):
        """Show quiz results"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        container = ttk.Frame(self.parent)
        container.pack(expand=True)
        
        ttk.Label(container, text="🎉 Kết quả bài thi",
                 font=(FONT_FAMILY, 18, 'bold'),
                 bootstyle="primary").pack(pady=20)
        
        # Score card
        score_card = ttk.Frame(container, bootstyle="light")
        score_card.pack(pady=10, padx=50)
        
        score_inner = ttk.Frame(score_card)
        score_inner.pack(padx=40, pady=30)
        
        # Score with color based on percentage
        percentage = result['correct'] / result['total'] * 100
        score_color = COLOR_SUCCESS if percentage >= 50 else COLOR_DANGER
        score_style = "success" if percentage >= 50 else "danger"
        
        score_label = tk.Label(score_inner,
                              text=f"{result['score']}/10",
                              font=(FONT_FAMILY, 48, 'bold'),
                              fg=score_color)
        score_label.pack(pady=10)
        
        ttk.Label(score_inner, text="điểm",
                 font=(FONT_FAMILY, 14),
                 bootstyle="secondary").pack()
        
        # Stats
        stats_frame = ttk.Frame(container)
        stats_frame.pack(pady=20)
        
        ttk.Label(stats_frame,
                 text=f"✓ Số câu đúng: {result['correct']}/{result['total']}",
                 font=(FONT_FAMILY, 13),
                 bootstyle=score_style).pack(pady=5)
        
        ttk.Label(stats_frame,
                 text=f"📊 Tỷ lệ đúng: {percentage:.1f}%",
                 font=(FONT_FAMILY, 13),
                 bootstyle="info").pack(pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="📋 Xem chi tiết",
                  command=lambda: self.show_review(),
                  bootstyle="info",
                  width=15).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(btn_frame, text="📝 Làm bài khác",
                  bootstyle="success-outline",
                  width=15,
                  command=self.show_quiz_list).pack(side=tk.LEFT, padx=10)

    def show_review(self):
        """Show detailed answer review"""
        review_data = QuizController.get_attempt_review(self.current_attempt)
        
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Title
        ttk.Label(self.parent, text="Xem lại đáp án",
                 font=(FONT_FAMILY, 16, 'bold')).pack(pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling only when hovering over canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Show each answer
        for i, answer in enumerate(review_data['answers'], 1):
            self.create_review_item(scrollable_frame, i, answer)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Back button
        ttk.Button(self.parent, text="Quay lại",
                  command=self.show_quiz_list).pack(pady=10)

    def create_review_item(self, parent, number, answer):
        """Create review item for one question"""
        frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Question
        status = "✓" if answer['is_correct'] else "✗"
        color = COLOR_SUCCESS if answer['is_correct'] else COLOR_DANGER
        
        header = tk.Label(frame, text=f"{status} Câu {number}",
                         font=(FONT_FAMILY, 12, 'bold'),
                         fg=color)
        header.pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text=answer['question'].question_text,
                 wraplength=700).pack(anchor=tk.W, padx=20, pady=5)
        
        # Options
        for option in answer['all_options']:
            option_frame = ttk.Frame(frame)
            option_frame.pack(fill=tk.X, padx=30, pady=2)
            
            prefix = ""
            fg_color = 'black'
            
            if option.id == answer['correct_option_id']:
                prefix = "✓ "
                fg_color = COLOR_SUCCESS
            elif option.id == answer['selected_option_id'] and not answer['is_correct']:
                prefix = "✗ "
                fg_color = COLOR_DANGER
            
            tk.Label(option_frame, text=f"{prefix}{option.option_text}",
                    fg=fg_color).pack(anchor=tk.W)

    def create_sample_quiz(self):
        """Create sample quiz with sample questions"""
        from utils.sample_data import create_sample_questions_and_quizzes
        
        result = create_sample_questions_and_quizzes()
        messagebox.showinfo("Thành công", 
                          f"Đã tạo {result['questions_count']} câu hỏi và {result['quizzes_count']} bài thi mẫu!")
        self.show_quiz_list()
