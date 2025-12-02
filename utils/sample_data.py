"""Sample data generator for quiz application"""
from controllers.question_bank_controller import QuestionBankController
from controllers.quiz_controller import QuizController


def create_sample_questions_and_quizzes():
    """Create sample questions and quizzes"""
    
    # Sample questions - Python Basic (Easy)
    sample_questions = [
        ("Python là ngôn ngữ lập trình gì?", 1, "Python Cơ bản", 
         [("Ngôn ngữ bậc cao", True), ("Ngôn ngữ bậc thấp", False), ("Ngôn ngữ máy", False), ("Assembly", False)]),
        ("Câu lệnh nào dùng để in ra màn hình trong Python?", 1, "Python Cơ bản",
         [("print()", True), ("echo()", False), ("printf()", False), ("cout", False)]),
        ("Phần mở rộng file Python là gì?", 1, "Python Cơ bản",
         [(".py", True), (".python", False), (".pt", False), (".pyt", False)]),
        ("Câu lệnh nào dùng để nhận input từ người dùng?", 1, "Python Cơ bản",
         [("input()", True), ("get()", False), ("scanf()", False), ("read()", False)]),
        ("Comment một dòng trong Python dùng ký tự gì?", 1, "Python Cơ bản",
         [("#", True), ("//", False), ("/*", False), ("--", False)]),
        ("Để kiểm tra kiểu dữ liệu dùng hàm nào?", 1, "Python Cơ bản",
         [("type()", True), ("typeof()", False), ("check()", False), ("datatype()", False)]),
        
        # Python Medium
        ("Kiểu dữ liệu nào lưu số thực trong Python?", 2, "Kiểu dữ liệu",
         [("float", True), ("int", False), ("string", False), ("boolean", False)]),
        ("List trong Python có thể thay đổi không?", 2, "Kiểu dữ liệu",
         [("Có", True), ("Không", False), ("Tùy trường hợp", False), ("Không biết", False)]),
        ("Tuple trong Python được khai báo bằng?", 2, "Kiểu dữ liệu",
         [("()", True), ("[]", False), ("{}", False), ("<>", False)]),
        ("Dictionary trong Python lưu trữ dữ liệu dạng?", 2, "Kiểu dữ liệu",
         [("key-value", True), ("array", False), ("list", False), ("queue", False)]),
        ("Phương thức nào để thêm phần tử vào cuối list?", 2, "List & Tuple",
         [("append()", True), ("add()", False), ("insert()", False), ("push()", False)]),
        ("Để lấy độ dài của một list, dùng hàm nào?", 2, "List & Tuple",
         [("len()", True), ("length()", False), ("size()", False), ("count()", False)]),
        ("Set trong Python có cho phép phần tử trùng lặp không?", 2, "Kiểu dữ liệu",
         [("Không", True), ("Có", False), ("Tùy trường hợp", False), ("Không xác định", False)]),
        ("Cách nào để tạo string nhiều dòng?", 2, "String",
         [('"""text"""', True), ("'text'", False), ('"text"', False), ("(text)", False)]),
        
        # Python Hard
        ("Decorator trong Python được ký hiệu bằng?", 3, "Advanced",
         [("@", True), ("#", False), ("&", False), ("$", False)]),
        ("Lambda function trong Python là gì?", 3, "Functions",
         [("Hàm vô danh", True), ("Hàm thông thường", False), ("Hàm tĩnh", False), ("Hàm đệ quy", False)]),
        ("Generator trong Python sử dụng từ khóa nào?", 3, "Advanced",
         [("yield", True), ("return", False), ("generate", False), ("next", False)]),
        ("*args trong Python dùng để làm gì?", 3, "Functions",
         [("Nhận số lượng tham số không xác định", True), ("Nhận mảng", False), ("Nhận dictionary", False), ("Nhận tuple", False)]),
        ("__init__ trong Python là gì?", 3, "OOP",
         [("Constructor", True), ("Destructor", False), ("Method thường", False), ("Static method", False)]),
        ("List comprehension nào sau đây đúng?", 3, "Advanced",
         [("[x*2 for x in range(5)]", True), ("{x*2 for x in range(5)}", False), ("(x*2 in range(5))", False), ("[x*2 in range(5)]", False)]),
        ("Để bắt ngoại lệ trong Python dùng từ khóa?", 3, "Exception",
         [("try-except", True), ("try-catch", False), ("catch-throw", False), ("handle-error", False)]),
        ("Module nào để làm việc với JSON?", 3, "Modules",
         [("json", True), ("jsonlib", False), ("jsonparser", False), ("simplejson", False)]),
        
        # Data Structures
        ("Stack hoạt động theo nguyên tắc nào?", 2, "Data Structures",
         [("LIFO", True), ("FIFO", False), ("LILO", False), ("FILO", False)]),
        ("Queue hoạt động theo nguyên tắc nào?", 2, "Data Structures",
         [("FIFO", True), ("LIFO", False), ("LILO", False), ("Random", False)]),
        
        # OOP
        ("Tính kế thừa trong OOP tiếng Anh là?", 2, "OOP",
         [("Inheritance", True), ("Polymorphism", False), ("Encapsulation", False), ("Abstraction", False)]),
        ("Từ khóa nào để kế thừa class trong Python?", 2, "OOP",
         [("class Child(Parent):", True), ("class Child extends Parent:", False), ("class Child inherits Parent:", False), ("class Child <- Parent:", False)]),
        
        # File Handling
        ("Mode nào để mở file để đọc?", 2, "File Handling",
         [("'r'", True), ("'w'", False), ("'a'", False), ("'x'", False)]),
        ("Mode nào để mở file để ghi (xóa nội dung cũ)?", 2, "File Handling",
         [("'w'", True), ("'r'", False), ("'a'", False), ("'r+'", False)]),
    ]
    
    # Add questions to database
    for q_text, diff, cat, options in sample_questions:
        try:
            QuestionBankController.add_question_with_options(q_text, diff, cat, options)
        except Exception:
            # Skip if question already exists
            pass
    
    # Create multiple quizzes
    try:
        QuizController.create_quiz_with_random_questions(
            "Bài thi Python cơ bản",
            "Kiểm tra kiến thức Python cơ bản",
            10,
            600,
            {'easy': 6, 'medium': 3, 'hard': 1}
        )
    except Exception:
        pass
    
    try:
        QuizController.create_quiz_with_random_questions(
            "Bài thi Python nâng cao",
            "Kiểm tra kiến thức Python nâng cao",
            15,
            900,
            {'easy': 3, 'medium': 7, 'hard': 5}
        )
    except Exception:
        pass
    
    try:
        QuizController.create_quiz_with_random_questions(
            "Bài thi Python toàn diện",
            "Kiểm tra toàn diện kiến thức Python",
            20,
            1200,
            {'easy': 6, 'medium': 8, 'hard': 6}
        )
    except Exception:
        pass
    
    try:
        QuizController.create_quiz_with_random_questions(
            "Bài thi nhanh - 5 phút",
            "Bài thi ngắn 5 câu",
            5,
            300,
            {'easy': 2, 'medium': 2, 'hard': 1}
        )
    except Exception:
        pass
    
    return {
        'questions_count': len(sample_questions),
        'quizzes_count': 4
    }
