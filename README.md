# Telegram Бот для Управління Бібліотекою

Цей бот є інформаційною системою для бібліотеки, реалізованою на Python з використанням `aiogram`. Він дозволяє здійснювати повне управління бібліотечною базою даних, включаючи книги, авторів, жанри, користувачів, а також відстеження видачі книг та боргів.

---

## 📁 Структура Проєкту
```
.
├── config_bot.py # Конфігурація токена, адміністраторів
├── create_bot.py # Створення та запуск бота
├── database/ # Модулі роботи з базою даних
│ ├── authors_db.py
│ ├── backup_db.py
│ ├── book_author_db.py
│ ├── book_genre_db.py
│ ├── books_db.py
│ ├── borrows_db.py
│ ├── config_db.py
│ ├── connection_db.py
│ ├── genres_db.py
│ └── users_db.py
├── fsm/ # Машини станів для введення даних
│ ├── authors_fsm.py
│ ├── book_author_fsm.py
│ ├── book_genre_fsm.py
│ ├── books_fsm.py
│ ├── borrows_fsm.py
│ ├── genres_fsm.py
│ └── users_fsm.py
├── handlers/ # Обробники команд бота
│ ├── authors.py
│ ├── book_author.py
│ ├── book_genre.py
│ ├── books.py
│ ├── borrows.py
│ ├── general.py
│ ├── genres.py
│ ├── users.py
│ └── validation.py
├── keyboards/ # Клавіатури та тексти кнопок
│ ├── authors_kb.py
│ ├── book_author_kb.py
│ ├── book_genre_kb.py
│ ├── books_kb.py
│ ├── borrows_kb.py
│ ├── general_kb.py
│ ├── genres_kb.py
│ ├── users_kb.py
│ ├── keyboards_text.py
├── main.py # Точка входу у програму
├── README.md # Документація
└── requirements.txt # Залежності
```

---

## ⚙️ Функціональність

### 📚 Робота з Книгами
- Додавання, редагування, видалення книг
- Пошук книг за автором, назвою, жанром

### 👨‍💼 Робота з Авторами та Жанрами
- CRUD-операції з авторами та жанрами
- Прив'язка книг до авторів та жанрів

### 👥 Користувачі
- Додавання нових користувачів
- Перегляд усіх користувачів

### 📖 Видача Книг
- Видача книг користувачам
- Облік повернень
- Визначення прострочених книг

### 📊 Статистика
- Найпопулярніші книги
- Статистика за видачами

---

## 🔌 Технології

- Python 3.x
- Aiogram
- MySQL
- `mysql-connector-python`
- FSM (Finite State Machine) для покрокового введення

---

## 📦 Встановлення

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/hanashiko/library-bot.git
   cd library-telegram-bot
   ```
2. Створіть .env файл або відредагуйте config_bot.py для додавання токена та конфігурації БД.
3. Встановіть залежності:
  ```bash
  pip install -r requirements.txt
  ```
4. Запустіть бота:
  ```bash
  python main.py
  ```

## 🔐 Доступ

Доступ до бота обмежений через config_bot.py, де задаються ID адміністраторів.

## 🛠 Резервне Копіювання

Скрипт backup_db.py дозволяє зробити дамп бази даних у файл для резервного збереження.

## 📂 База Даних

Бот використовує MySQL базу даних зі зв'язками між таблицями:

- books, authors, genres
- Зв’язувальні таблиці: book_author, book_genre
- users, borrows (видачі), debts (прострочення)
