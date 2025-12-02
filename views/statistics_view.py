"""Statistics and Analysis View"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers.quiz_controller import QuizController
from models.quiz import Quiz
from models.attempt import Attempt
from config import FONT_FAMILY


class StatisticsView:
    """View for statistics and analysis"""

    def __init__(self, parent):
        self.parent = parent
        self.show_statistics()

    def show_statistics(self):
        """Show statistics overview"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=30, pady=20)
        
        ttk.Label(header, text="📊 Thống kê & Phân tích",
                 font=(FONT_FAMILY, 20, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Tabs with better styling
        notebook = ttk.Notebook(self.parent, bootstyle="primary")
        notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Quiz statistics tab
        quiz_tab = ttk.Frame(notebook)
        notebook.add(quiz_tab, text="📝 Thống kê bài thi")
        self.show_quiz_statistics(quiz_tab)
        
        # Question analysis tab
        question_tab = ttk.Frame(notebook)
        notebook.add(question_tab, text="🔍 Phân tích câu hỏi")
        self.show_question_analysis(question_tab)
        
        # Difficulty analysis tab
        difficulty_tab = ttk.Frame(notebook)
        notebook.add(difficulty_tab, text="🎯 Phân tích độ khó")
        self.show_difficulty_analysis(difficulty_tab)

    def show_quiz_statistics(self, parent):
        """Show quiz statistics"""
        quizzes = Quiz.get_all()
        
        if not quizzes:
            empty_frame = ttk.Frame(parent)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="📊",
                     font=(FONT_FAMILY, 48)).pack(pady=20)
            ttk.Label(empty_frame, text="Chưa có dữ liệu thống kê",
                     font=(FONT_FAMILY, 14)).pack(pady=10)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
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
        
        for quiz in quizzes:
            self.create_quiz_stats_card(scrollable_frame, quiz)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_quiz_stats_card(self, parent, quiz):
        """Create statistics card for a quiz"""
        card = ttk.Labelframe(parent, text=quiz.title, padding=10, bootstyle="info")
        card.pack(fill=tk.X, pady=10, padx=10)
        
        stats = Attempt.get_statistics(quiz.id)
        
        if not stats or stats['total_attempts'] == 0:
            ttk.Label(card, text="📭 Chưa có lượt thi nào",
                     font=(FONT_FAMILY, 11),
                     bootstyle="secondary").pack(pady=10)
            return
        
        # Statistics in modern card layout
        stats_grid = ttk.Frame(card)
        stats_grid.pack(fill=tk.X, pady=10)
        
        # Metric cards
        metrics = [
            ("👥 Tổng lượt thi", str(stats['total_attempts']), "primary"),
            ("📊 Điểm TB", f"{stats['avg_score']:.1f}", "info"),
            ("🏆 Cao nhất", f"{stats['max_score']:.1f}", "success"),
            ("📉 Thấp nhất", f"{stats['min_score']:.1f}", "warning")
        ]
        
        for i, (label, value, style) in enumerate(metrics):
            metric_frame = ttk.Frame(stats_grid)
            metric_frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
            
            ttk.Label(metric_frame, text=label,
                     font=(FONT_FAMILY, 9),
                     bootstyle="secondary").pack(anchor=tk.W)
            ttk.Label(metric_frame, text=value,
                     font=(FONT_FAMILY, 13, 'bold'),
                     bootstyle=style).pack(anchor=tk.W)
        
        # Average time
        if stats['avg_time']:
            time_frame = ttk.Frame(card)
            time_frame.pack(fill=tk.X, pady=5, padx=10)
            
            avg_minutes = int(stats['avg_time']) // 60
            avg_seconds = int(stats['avg_time']) % 60
            
            ttk.Label(time_frame, text="⏱ Thời gian trung bình:",
                     font=(FONT_FAMILY, 9),
                     bootstyle="secondary").pack(anchor=tk.W)
            ttk.Label(time_frame, text=f"{avg_minutes}:{avg_seconds:02d}",
                     font=(FONT_FAMILY, 13, 'bold'),
                     bootstyle="secondary").pack(anchor=tk.W)
        
        # Show recent attempts button
        ttk.Button(card, text="📋 Xem chi tiết",
                  command=lambda q=quiz: self.show_attempt_details(q),
                  bootstyle="info-outline",
                  width=15).pack(pady=10)

    def show_attempt_details(self, quiz):
        """Show detailed attempt history"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Chi tiết - {quiz.title}")
        dialog.geometry("700x500")
        dialog.transient(self.parent)
        
        attempts = Attempt.get_by_quiz(quiz.id)
        
        # Create treeview with better styling
        tree_frame = ttk.Frame(dialog)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ('student', 'score', 'correct', 'time', 'date')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('student', text='Sinh viên', anchor=tk.W)
        tree.heading('score', text='Điểm', anchor=tk.CENTER)
        tree.heading('correct', text='Số câu đúng', anchor=tk.CENTER)
        tree.heading('time', text='Thời gian', anchor=tk.CENTER)
        tree.heading('date', text='Ngày thi', anchor=tk.W)
        
        tree.column('student', width=150, anchor=tk.W)
        tree.column('score', width=80, anchor=tk.CENTER)
        tree.column('correct', width=100, anchor=tk.CENTER)
        tree.column('time', width=90, anchor=tk.CENTER)
        tree.column('date', width=200, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for attempt in attempts:
            time_str = ""
            if attempt.time_taken:
                minutes = attempt.time_taken // 60
                seconds = attempt.time_taken % 60
                time_str = f"{minutes}:{seconds:02d}"
            
            tree.insert('', tk.END, values=(
                attempt.student_name,
                f"{attempt.score:.0f}",
                f"{attempt.correct_answers}/{attempt.total_questions}",
                time_str,
                attempt.completed_at or "Chưa hoàn thành"
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_question_analysis(self, parent):
        """Show question-level analysis"""
        from models.question import Question
        
        questions = Question.get_all()
        
        if not questions:
            ttk.Label(parent, text="Chưa có câu hỏi nào",
                     font=(FONT_FAMILY, 12)).pack(pady=20)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling only when hovering over canvas
        def _on_mousewheel_qa(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel_qa(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel_qa)
        
        def _unbind_mousewheel_qa(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _bind_mousewheel_qa)
        canvas.bind("<Leave>", _unbind_mousewheel_qa)
        
        # Header
        header_frame = ttk.Frame(scrollable_frame)
        header_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(header_frame, text="Phân tích tỷ lệ chọn đáp án",
                 font=(FONT_FAMILY, 12, 'bold')).pack()
        
        # Analyze each question
        for question in questions[:50]:  # Limit to first 20 for performance
            stats = QuizController.get_question_statistics(question.id)
            
            if stats['total_answers'] > 0:
                self.create_question_analysis_card(scrollable_frame, question, stats)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_question_analysis_card(self, parent, question, stats):
        """Create analysis card for a question"""
        card = ttk.Labelframe(parent, text=f"Câu {question.id}", padding=10, bootstyle="primary")
        card.pack(fill=tk.X, pady=5, padx=10)
        
        # Question text (truncated)
        q_text = question.question_text[:100] + "..." if len(question.question_text) > 100 else question.question_text
        ttk.Label(card, text=q_text, wraplength=600).pack(anchor=tk.W, pady=5)
        
        # Statistics
        stats_frame = ttk.Frame(card)
        stats_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stats_frame, text=f"Tổng lượt trả lời: {stats['total_answers']}",
                 font=(FONT_FAMILY, 9)).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(stats_frame, text=f"Tỷ lệ đúng: {stats['correct_rate']:.1f}%",
                 font=(FONT_FAMILY, 9, 'bold'),
                 foreground='green' if stats['correct_rate'] >= 50 else 'red').pack(side=tk.LEFT, padx=10)
        
        # Option distribution
        if stats['option_distribution']:
            dist_frame = ttk.Frame(card)
            dist_frame.pack(fill=tk.X, pady=5)
            
            for opt in stats['option_distribution']:
                percentage = (opt['selection_count'] / stats['total_answers'] * 100) if stats['total_answers'] > 0 else 0
                marker = "✓" if opt['is_correct'] else " "
                
                opt_label = ttk.Label(dist_frame, 
                                     text=f"{marker} {opt['option_text'][:50]}: {percentage:.1f}% ({opt['selection_count']} lượt)",
                                     font=(FONT_FAMILY, 8))
                opt_label.pack(anchor=tk.W, padx=20)

    def show_difficulty_analysis(self, parent):
        """Show difficulty analysis"""
        ttk.Label(parent, text="Phân tích độ khó thực tế",
                 font=(FONT_FAMILY, 14, 'bold')).pack(pady=20)
        
        difficulty_data = QuizController.analyze_difficulty()
        
        if not difficulty_data:
            ttk.Label(parent, text="Chưa có dữ liệu để phân tích",
                     font=(FONT_FAMILY, 12)).pack(pady=20)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling only when hovering over canvas
        def _on_mousewheel_da(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel_da(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel_da)
        
        def _unbind_mousewheel_da(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _bind_mousewheel_da)
        canvas.bind("<Leave>", _unbind_mousewheel_da)
        
        # Create treeview
        columns = ('id', 'labeled', 'success_rate', 'total', 'question')
        tree = ttk.Treeview(scrollable_frame, columns=columns, show='headings', height=20)
        
        tree.heading('id', text='ID')
        tree.heading('labeled', text='Độ khó gán')
        tree.heading('success_rate', text='Tỷ lệ đúng')
        tree.heading('total', text='Tổng câu TL')
        tree.heading('question', text='Câu hỏi')
        
        tree.column('id', width=50)
        tree.column('labeled', width=100)
        tree.column('success_rate', width=100)
        tree.column('total', width=100)
        tree.column('question', width=400)
        
        difficulty_names = {1: 'Dễ', 2: 'Trung bình', 3: 'Khó'}
        
        for data in difficulty_data:
            q_text = data['question_text'][:50] + "..." if len(data['question_text']) > 50 else data['question_text']
            
            tree.insert('', tk.END, values=(
                data['id'],
                difficulty_names.get(data['labeled_difficulty'], 'N/A'),
                f"{data['success_rate']:.1f}%",
                data['total_answers'],
                q_text
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Legend
        legend = ttk.Frame(parent)
        legend.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(legend, text="Ghi chú: Câu hỏi được sắp xếp từ khó nhất (tỷ lệ đúng thấp) đến dễ nhất",
                 font=(FONT_FAMILY, 9, 'italic')).pack()
