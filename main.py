import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Основная логика приложения ---

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.filename = "books.json"

        # Создание виджетов
        self.create_widgets()
        self.load_books()  # Загрузка данных при старте

    def create_widgets(self):
        # --- Рамка для ввода ---
        input_frame = tk.LabelFrame(self.root, text="Добавить книгу", padx=10, pady=10)
        input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Поля ввода
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="e")
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="e")
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Страниц:").grid(row=3, column=0, sticky="e")
        self.pages_entry = tk.Entry(input_frame, width=10)
        self.pages_entry.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Таблица для отображения книг ---
        columns = ("#1", "#2", "#3", "#4")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("#1", text="Название")
        self.tree.heading("#2", text="Автор")
        self.tree.heading("#3", text="Жанр")
        self.tree.heading("#4", text="Страниц")
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        # --- Рамка для фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтр", padx=10, pady=10)
        filter_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Больше страниц:").grid(row=1, column=0)
        self.filter_pages = tk.Entry(filter_frame)
        self.filter_pages.grid(row=1, column=1, padx=5)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=2, columnspan=2)

        # --- Кнопки сохранения и загрузки ---
        save_btn = tk.Button(self.root, text="Сохранить в JSON", command=self.save_books)
        save_btn.grid(row=3, column=0, padx=(10, 5), pady=(0, 10))

        load_btn = tk.Button(self.root, text="Загрузить из JSON", command=self.load_books)
        load_btn.grid(row=3, column=1, padx=(5, 10), pady=(0, 10))

        # Настройка размеров сетки
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_raw = self.pages_entry.get().strip()

        # Валидация ввода
        if not (title and author and genre and pages_raw):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages_raw.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть целым числом!")
            return

        pages = int(pages_raw)

        # Добавление в список и обновление таблицы
        self.books.append({"title": title, "author": author, "genre": genre.lower(), "pages": pages})
        self.update_table(self.books) # Показываем все книги после добавления

    def update_table(self, data):
        """Очищает и заполняет таблицу новыми данными."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in data:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        pages_filter_raw = self.filter_pages.get().strip()

        filtered_books = []

        for book in self.books:
            match_genre = True
            match_pages = True

            if genre_filter:
                match_genre = (book["genre"] == genre_filter)
            
            if pages_filter_raw.isdigit():
                match_pages = (book["pages"] > int(pages_filter_raw))
            
            if match_genre and match_pages:
                filtered_books.append(book)
        
        if not filtered_books and (genre_filter or pages_filter_raw.isdigit()):
            messagebox.showinfo("Фильтр", "Книги по заданным критериям не найдены.")
        
        self.update_table(filtered_books or [])

    def save_books(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные сохранены в {self.filename}")
            print(f"[LOG] Файл {self.filename} сохранен.")
            # Здесь можно добавить вызов git commit/push через subprocess при необходимости
            os.system('git add .')
            os.system('git commit -m "Обновление данных книг"')
            os.system('git push')
            print("[LOG] Изменения отправлены в Git.")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            


    def load_books(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
            messagebox.showinfo("Успех", f"Данные загружены из {self.filename}")
            print(f"[LOG] Файл {self.filename} загружен.")
            self.update_table(self.books)
            return True
        except FileNotFoundError:
            messagebox.showinfo("Информация", f"Файл {self.filename} не найден. Будет создан при сохранении.")
            return False

# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
