# Quiz Application

Ứng dụng thi trắc nghiệm với giao diện đồ họa và cơ sở dữ liệu MySQL.

## Đặc điểm nổi bật

### 1. Chức năng

- ✅ Ngân hàng câu hỏi với CRUD đầy đủ
- ✅ Random câu hỏi từ ngân hàng
- ✅ Chấm điểm tự động
- ✅ Ma trận độ khó (Easy/Medium/Hard)
- ✅ Timer đếm ngược trong bài thi
- ✅ Review đáp án chi tiết sau khi thi

### 2. Cơ sở dữ liệu MySQL

- ✅ **5 bảng chính**: `questions`, `options`, `quizzes`, `attempts`, `attempt_answers`
- ✅ **Engine InnoDB** với charset UTF8MB4 và collation utf8mb4_unicode_ci
- ✅ **Foreign Keys** với ON DELETE CASCADE và ON DELETE SET NULL
- ✅ **Indexes** trên các cột thường xuyên truy vấn (difficulty, category, quiz_id, etc.)
- ✅ **AUTO_INCREMENT** cho primary keys
- ✅ **UNIQUE constraint** trên title của quizzes
- ✅ **Connection pooling** để quản lý kết nối hiệu quả
- ✅ **100 câu hỏi mẫu** với 3 độ khó (Easy/Medium/Hard) và nhiều danh mục

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

### 1. Cài đặt MySQL Server hoặc MariaDB

**Tùy chọn 1: MySQL Server**

- Tải và cài đặt MySQL Server từ [mysql.com](https://dev.mysql.com/downloads/mysql/)

**Tùy chọn 2: XAMPP (khuyến nghị)**

- Tải và cài đặt [XAMPP](https://www.apachefriends.org/) (đã bao gồm MariaDB/MySQL và phpMyAdmin)
- Mở XAMPP Control Panel và Start MySQL

**Tùy chọn 3: WAMP**

- Tải và cài đặt [WAMP](https://www.wampserver.com/) (đã bao gồm MySQL và phpMyAdmin)

### 2. Cấu hình database

1. Mở file [config.py](config.py) và cập nhật thông tin kết nối MySQL:

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Nhập mật khẩu MySQL của bạn
    'database': 'quiz_app',
    'port': 3306,
}
```

2. **Import database mẫu** (file `quiz_app.sql` có sẵn 100 câu hỏi):

**Cách 1: Dùng phpMyAdmin (khuyến nghị)**

- Truy cập http://localhost/phpmyadmin
- Tạo database mới tên `quiz_app` (hoặc database sẽ tự động tạo khi import)
- Chọn tab "Import" (Nhập)
- Chọn file `quiz_app.sql` và click "Go" (Thực hiện)

**Cách 2: Dùng Command Line**

```bash
mysql -u root -p < quiz_app.sql
```

> **Lưu ý**: File SQL bao gồm:
>
> - 100 câu hỏi (Easy: 40, Medium: 40, Hard: 20)
> - 400 đáp án (mỗi câu 4 đáp án)
> - 1 bài thi mẫu "Kỹ thuật lập trình Python" (30 câu, 30 phút)
> - 25 lượt thi mẫu với điểm số và thời gian thực tế

### 3. Cài đặt dependencies Python

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

**Trên Windows:**

```bash
py main.py
```

**Trên Linux/macOS:**

```bash
python3 main.py
```

> **Lưu ý**: Ứng dụng sẽ tự động:
>
> - Tạo database `quiz_app` nếu chưa tồn tại
> - Tạo các bảng cần thiết
> - Tạo dữ liệu mẫu nếu database trống

### 5. Chạy tests

**Trên Windows:**

```bash
pytest tests/test_quiz_app.py -v
# hoặc
py tests/test_quiz_app.py
```

**Trên Linux/macOS:**

```bash
pytest tests/test_quiz_app.py -v
# hoặc
python3 tests/test_quiz_app.py
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

## Schema Database (MySQL)

### questions

```sql
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` text NOT NULL,
  `difficulty` int(11) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_questions_difficulty` (`difficulty`),
  KEY `idx_questions_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Mô tả:**

- `id`: Mã câu hỏi (Primary Key, Auto Increment)
- `question_text`: Nội dung câu hỏi
- `difficulty`: Độ khó (1=Easy, 2=Medium, 3=Hard)
- `category`: Danh mục câu hỏi
- `created_at`: Thời gian tạo

### options

```sql
CREATE TABLE `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `option_text` text NOT NULL,
  `is_correct` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_options_question` (`question_id`),
  CONSTRAINT `options_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Mô tả:**

- `id`: Mã đáp án (Primary Key, Auto Increment)
- `question_id`: Mã câu hỏi (Foreign Key)
- `option_text`: Nội dung đáp án
- `is_correct`: Đáp án đúng (0=sai, 1=đúng)
- `created_at`: Thời gian tạo

### quizzes

```sql
CREATE TABLE `quizzes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `time_limit` int(11) NOT NULL DEFAULT 600,
  `total_questions` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Mô tả:**

- `id`: Mã bài thi (Primary Key, Auto Increment)
- `title`: Tiêu đề bài thi (UNIQUE)
- `description`: Mô tả bài thi
- `time_limit`: Thời gian làm bài (giây)
- `total_questions`: Tổng số câu hỏi
- `created_at`: Thời gian tạo

### attempts

```sql
CREATE TABLE `attempts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `student_name` varchar(255) NOT NULL,
  `score` decimal(5,2) NOT NULL DEFAULT 0.00,
  `total_questions` int(11) NOT NULL,
  `correct_answers` int(11) NOT NULL DEFAULT 0,
  `time_taken` int(11) DEFAULT NULL,
  `started_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `completed_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_attempts_quiz` (`quiz_id`),
  CONSTRAINT `attempts_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Mô tả:**

- `id`: Mã lượt thi (Primary Key, Auto Increment)
- `quiz_id`: Mã bài thi (Foreign Key)
- `student_name`: Tên học sinh
- `score`: Điểm số (0.00 - 10.00)
- `total_questions`: Tổng số câu hỏi
- `correct_answers`: Số câu trả lời đúng
- `time_taken`: Thời gian làm bài (giây)
- `started_at`: Thời gian bắt đầu
- `completed_at`: Thời gian hoàn thành

### attempt_answers

```sql
CREATE TABLE `attempt_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attempt_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `selected_option_id` int(11) DEFAULT NULL,
  `is_correct` tinyint(1) NOT NULL DEFAULT 0,
  `answered_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_attempt_answers_attempt` (`attempt_id`),
  KEY `idx_attempt_answers_question` (`question_id`),
  KEY `attempt_answers_ibfk_3` (`selected_option_id`),
  CONSTRAINT `attempt_answers_ibfk_1` FOREIGN KEY (`attempt_id`) REFERENCES `attempts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attempt_answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attempt_answers_ibfk_3` FOREIGN KEY (`selected_option_id`) REFERENCES `options` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Mô tả:**

- `id`: Mã câu trả lời (Primary Key, Auto Increment)
- `attempt_id`: Mã lượt thi (Foreign Key)
- `question_id`: Mã câu hỏi (Foreign Key)
- `selected_option_id`: Mã đáp án được chọn (Foreign Key, NULL nếu không trả lời)
- `is_correct`: Trả lời đúng (0=sai, 1=đúng)
- `answered_at`: Thời gian trả lời

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
✅ **CSDL MySQL**: 5 bảng với InnoDB engine, Foreign Keys, CHECK constraints  
✅ **Connection Pooling**: Quản lý kết nối database hiệu quả  
✅ **Tìm kiếm/Phân tích**: Thống kê tỉ lệ chọn, phân tích độ khó  
✅ **Giao diện**: GUI hiện đại với ttkbootstrap, timer, review đáp án  
✅ **Kiểm thử**: 18 tests (vượt yêu cầu ≥12)  
✅ **MVC**: Tách biệt rõ ràng Model-View-Controller  
✅ **UTF8MB4**: Hỗ trợ đầy đủ Unicode và emoji

## Công nghệ sử dụng

- **Python 3.8+** - Ngôn ngữ lập trình chính
- **MySQL 8.0+ / MariaDB 10.4+** - Hệ quản trị cơ sở dữ liệu quan hệ
- **mysql-connector-python** - MySQL driver cho Python
- **tkinter + ttkbootstrap** - Giao diện đồ họa hiện đại
- **pytest** - Framework testing
- **Pillow** - Xử lý hình ảnh

> **Lưu ý**: Ứng dụng tương thích với cả MySQL và MariaDB (XAMPP sử dụng MariaDB)
