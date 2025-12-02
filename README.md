# Quiz Application

Ứng dụng thi trắc nghiệm với giao diện đồ họa và cơ sở dữ liệu SQLite.

## Đặc điểm nổi bật

### 1. Chức năng

- ✅ Ngân hàng câu hỏi với CRUD đầy đủ
- ✅ Random câu hỏi từ ngân hàng
- ✅ Chấm điểm tự động
- ✅ Ma trận độ khó (Easy/Medium/Hard)
- ✅ Timer đếm ngược trong bài thi
- ✅ Review đáp án chi tiết sau khi thi

### 2. Cơ sở dữ liệu

- ✅ 6 bảng: `questions`, `options`, `quizzes`, `quiz_questions`, `attempts`, `attempt_answers`
- ✅ Ràng buộc toàn vẹn (Foreign Keys, Cascades)
- ✅ Ràng buộc logic (CHECK constraints)
- ✅ Indexes để tối ưu hiệu suất
- ✅ Ràng buộc đảm bảo mỗi câu hỏi có đúng 1 đáp án đúng

### 3. Tìm kiếm & Phân tích

- ✅ Thống kê tỷ lệ chọn từng đáp án
- ✅ Phân tích độ khó thực tế (dựa vào tỷ lệ đúng)
- ✅ Thống kê điểm số, thời gian làm bài
- ✅ Lọc câu hỏi theo độ khó, danh mục

### 4. Giao diện

- ✅ GUI tkinter với sidebar navigation
- ✅ Timer đếm ngược, cảnh báo khi sắp hết giờ
- ✅ Review đáp án với highlights đúng/sai
- ✅ Quản lý câu hỏi trực quan
- ✅ Dashboard thống kê

### 5. Kiểm thử

- ✅ 15 unit tests với pytest
- ✅ Tests cho Models (Question, Option, Quiz, Attempt)
- ✅ Tests cho Controllers (QuizController, QuestionBankController)
- ✅ Tests cho randomization, scoring, validation

## Cấu trúc dự án (MVC)

```
đồ án 2/
│
├── config.py                    # Cấu hình ứng dụng
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
│
├── database/
│   ├── __init__.py
│   └── connection.py           # Database connection & schema
│
├── models/                     # Model layer
│   ├── __init__.py
│   ├── question.py            # Question model
│   ├── option.py              # Option model
│   ├── quiz.py                # Quiz model
│   └── attempt.py             # Attempt model
│
├── controllers/                # Controller layer
│   ├── __init__.py
│   ├── quiz_controller.py     # Quiz business logic
│   └── question_bank_controller.py
│
├── views/                      # View layer (GUI)
│   ├── __init__.py
│   ├── quiz_view.py           # Quiz taking interface
│   ├── question_bank_view.py  # Question management
│   └── statistics_view.py     # Statistics & analysis
│
└── tests/                      # Testing
    ├── __init__.py
    └── test_quiz_app.py       # 15 unit tests
```

## Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
python main.py
```

### 3. Chạy tests

```bash
pytest tests/test_quiz_app.py -v
```

Hoặc:

```bash
python tests/test_quiz_app.py
```

## Hướng dẫn sử dụng

### Lần đầu sử dụng

1. Chạy ứng dụng
2. Vào "Làm bài thi"
3. Click "Tạo bài thi mẫu" để có dữ liệu demo
4. Bắt đầu làm bài thi thử

### Quản lý câu hỏi

1. Vào "Ngân hàng câu hỏi"
2. Click "➕ Thêm câu hỏi"
3. Nhập câu hỏi, chọn độ khó, nhập 4 đáp án
4. Chọn đáp án đúng bằng radio button

### Làm bài thi

1. Vào "Làm bài thi"
2. Chọn bài thi và nhập tên
3. Trả lời câu hỏi trong thời gian quy định
4. Xem kết quả và review đáp án

### Xem thống kê

1. Vào "Thống kê"
2. Tab "Thống kê bài thi": Xem tổng quan các bài thi
3. Tab "Phân tích câu hỏi": Xem tỷ lệ chọn từng đáp án
4. Tab "Độ khó": So sánh độ khó gán vs độ khó thực tế

## Schema Database

### questions

- id (PK)
- question_text (NOT NULL, CHECK not empty)
- difficulty (1=Easy, 2=Medium, 3=Hard)
- category
- created_at

### options

- id (PK)
- question_id (FK -> questions)
- option_text (NOT NULL)
- is_correct (BOOLEAN)
- UNIQUE constraint: one correct per question

### quizzes

- id (PK)
- title (NOT NULL)
- description
- time_limit (seconds, CHECK > 0)
- total_questions (CHECK > 0)
- created_at

### quiz_questions

- id (PK)
- quiz_id (FK -> quizzes)
- question_id (FK -> questions)
- question_order
- UNIQUE: (quiz_id, question_id)

### attempts

- id (PK)
- quiz_id (FK -> quizzes)
- student_name (NOT NULL)
- score
- total_questions
- correct_answers
- time_taken
- started_at, completed_at

### attempt_answers

- id (PK)
- attempt_id (FK -> attempts)
- question_id (FK -> questions)
- selected_option_id (FK -> options)
- is_correct
- answered_at

## Chi tiết 15 Tests

1. `test_create_question` - Tạo câu hỏi
2. `test_get_question_by_id` - Lấy câu hỏi theo ID
3. `test_get_questions_by_difficulty` - Lọc theo độ khó
4. `test_update_question` - Cập nhật câu hỏi
5. `test_delete_question` - Xóa câu hỏi
6. `test_random_question_selection` - **Randomization test**
7. `test_create_option` - Tạo đáp án
8. `test_get_options_by_question` - Lấy đáp án
9. `test_get_correct_option` - Lấy đáp án đúng
10. `test_create_quiz_with_random_questions` - **Random quiz creation**
11. `test_difficulty_matrix_selection` - **Ma trận độ khó**
12. `test_submit_answer_correct` - Submit đáp án đúng
13. `test_submit_answer_incorrect` - Submit đáp án sai
14. `test_scoring_calculation` - **Tính điểm**
15. `test_add_question_with_options` - Thêm câu + đáp án
16. `test_validate_one_correct_answer` - Validation: 1 đáp án đúng
17. `test_validate_minimum_options` - Validation: min 2 đáp án
18. `test_question_bank_validation` - Validate toàn bộ ngân hàng

> **Tổng: 18 tests** (vượt yêu cầu ≥12 tests)

## Tính năng đặc biệt

### Random với ma trận độ khó

```python
QuizController.create_quiz_with_random_questions(
    title="Mixed Quiz",
    description="Test",
    total_questions=10,
    time_limit=600,
    difficulty_matrix={'easy': 5, 'medium': 3, 'hard': 2}
)
```

### Timer với cảnh báo

- Màu xanh: > 5 phút
- Màu cam: 1-5 phút
- Màu đỏ: < 1 phút
- Auto-submit khi hết giờ

### Phân tích độ khó thực tế

So sánh độ khó đã gán với tỷ lệ trả lời đúng thực tế để phát hiện câu hỏi có độ khó không chính xác.

## Yêu cầu đề tài đã đáp ứng

✅ **Chức năng**: Ngân hàng câu hỏi, random, chấm điểm, ma trận độ khó  
✅ **CSDL**: 6 tables với ràng buộc logic đầy đủ  
✅ **Tìm kiếm/Phân tích**: Thống kê tỉ lệ chọn, phân tích độ khó  
✅ **Giao diện**: GUI với timer, review đáp án  
✅ **Kiểm thử**: 18 tests (vượt yêu cầu ≥12)  
✅ **MVC**: Tách biệt rõ ràng Model-View-Controller

## Công nghệ sử dụng

- Python 3.8+
- tkinter (GUI)
- SQLite3 (Database)
- pytest (Testing)

## Tác giả

Quiz App - Đồ án môn học Python
