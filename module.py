import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, ttk



class LibraryManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.books = pd.DataFrame(columns=['Назва книги', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників'])
        self.load_books()

    def load_books(self):
        try:
            self.books = pd.read_csv(self.file_path, encoding='utf-8')
        except FileNotFoundError:
            print("CSV файл не знайдено")
            self.books = pd.DataFrame(columns=['Назва книги', 'Автор', 'Рік видання', 'Жанр', 'Кількість примірників'])

    def save_books(self):
        self.books.to_csv(self.file_path, index=False, encoding='utf-8')

    def add_book(self, title, author, year, genre, quantity):
        new_book = pd.DataFrame([{
            'Назва книги': title,
            'Автор': author,
            'Рік видання': int(year),
            'Жанр': genre,
            'Кількість примірників': int(quantity)
        }])
        self.books = pd.concat([self.books, new_book], ignore_index=True)
        print(f"Книга '{title}' додана")
        self.save_books()

    def edit_book(self, title, field, new_value):
        if title in self.books['Назва книги'].values:
            idx = self.books.index[self.books['Назва книги'] == title].tolist()[0]
            self.books.at[idx, field] = new_value
            print(f"Книга '{title}' оновлена")
            self.save_books()
        else:
            print(f"Книга '{title}' не знайдена.")
        self.save_books()

    def delete_book(self, title):
        if title in self.books['Назва книги'].values:
            self.books = self.books[self.books['Назва книги'] != title]
            print(f"Книга '{title}' успішно видалена!")
            self.save_books()
        else:
            print(f"Книга '{title}' не знайдена.")
        self.save_books()

    def display_books(self):
        if not self.books.empty:
            print(self.books)
        else:
            print("Бібліотека порожня.")

    def total_books(self):
        total = self.books['Кількість примірників'].sum()
        print(f"Загальна кількість книг: {total}")

    def popular_genres(self):
        genre_counts = self.books['Жанр'].value_counts()
        print("Найпопулярніші жанри:")
        print(genre_counts)

    def search_books_by_auther(self, author=None, year=None):
        if author:
            print(f"Книги автора '{author}':")
            print(self.books[self.books['Автор'] == author])
        if year:
            print(f"Книги, видані у {year} році:")
            print(self.books[self.books['Рік видання'] == int(year)])

    def genre_pie_chart(self):
        genre_counts = self.books['Жанр'].value_counts()
        if genre_counts.empty:
            messagebox.showinfo("Інформація", "Немає даних для побудови діаграми.")
            return

        plt.figure(figsize=(8, 8))
        genre_counts.plot.pie(autopct='%1.1f%%', startangle=140, cmap='tab20c', wedgeprops={'edgecolor': 'black'})
        plt.title('Розподіл книг за жанрами')
        plt.ylabel('')

        plt.show()

    def year_histogram(self):
        if self.books.empty:
            messagebox.showinfo("Інформація", "Немає даних для побудови гістограми.")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(self.books['Рік видання'], bins=15, color='skyblue', edgecolor='black')
        plt.title('Розподіл книг за роками видання')
        plt.xlabel('Рік видання')
        plt.ylabel('Кількість книг')
        plt.show()

class LibraryGUI:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Бібліотека книг")

        tk.Button(root, text="Завантажити CSV", command=self.load_file).pack(pady=5)
        tk.Button(root, text="Додати книгу", command=self.add_book).pack(pady=5)
        tk.Button(root, text="Показати книги", command=self.show_books).pack(pady=5)
        tk.Button(root, text="Кругова діаграма жанрів", command=self.manager.genre_pie_chart).pack(pady=5)
        tk.Button(root, text="Гістограма за роками", command=self.manager.year_histogram).pack(pady=5)
        tk.Button(root, text="Обчислити кількість книг", command=self.show_total_books).pack(pady=5)
        tk.Button(root, text="Найпопулярніші жанри", command=self.show_popular_genres).pack(pady=5)
        tk.Button(root, text="Пошук книг", command=self.search_books).pack(pady=5)
        tk.Button(root, text="Видалення книги за назвою", command=self.delete_book).pack(pady=5)
        tk.Button(root, text="Вийти", command=root.quit).pack(pady=5)

    def delete_book(self):
        def delete():
            title = entry_title.get()
            if title:
                self.manager.delete_book(title)
                messagebox.showinfo("Успіх", f"Книга '{title}' видалена.")
                delete_window.destroy()
            else:
                messagebox.showerror("Помилка", "Назва книги не вказана!")

        delete_window = tk.Toplevel(self.root)
        delete_window.title("Видалити книгу")

        tk.Label(delete_window, text="Назва книги").grid(row=0, column=0, padx=5, pady=5)
        entry_title = tk.Entry(delete_window)
        entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(delete_window, text="Видалити", command=delete).grid(row=1, column=0, columnspan=2, pady=10)

    def show_total_books(self):
        total = self.manager.books['Кількість примірників'].sum()
        if pd.isna(total) or total == 0:
            total = 0
        messagebox.showinfo("Загальна кількість книг", f"Загальна кількість книг: {int(total)}")

    def show_popular_genres(self):
        genres = self.manager.books['Жанр'].value_counts()
        if not genres.empty:
            result = "\n".join([f"{genre}: {count}" for genre, count in genres.items()])
            messagebox.showinfo("Найпопулярніші жанри", result)
        else:
            messagebox.showinfo("Популярні жанри", "У бібліотеці ще немає книг.")

    def search_books(self):
        def search():
            author = entry_author.get()
            year = entry_year.get()
            if author:
                result = self.manager.books[self.manager.books['Автор'] == author]
            elif year:
                result = self.manager.books[self.manager.books['Рік видання'] == int(year)]
            else:
                result = pd.DataFrame()

            if not result.empty:
                result_window = tk.Toplevel(self.root)
                result_window.title("Результати пошуку")
                text = tk.Text(result_window, wrap="word")
                text.pack(expand=True, fill="both")
                text.insert("1.0", result.to_string())
            else:
                messagebox.showinfo("Результати пошуку", "Книги не знайдено.")
            search_window.destroy()

        search_window = tk.Toplevel(self.root)
        search_window.title("Пошук книг")

        tk.Label(search_window, text="Автор").grid(row=0, column=0, padx=5, pady=5)
        entry_author = tk.Entry(search_window)
        entry_author.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(search_window, text="Рік видання").grid(row=1, column=0, padx=5, pady=5)
        entry_year = tk.Entry(search_window)
        entry_year.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(search_window, text="Пошук", command=search).grid(row=2, column=0, columnspan=2, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV файли", "*.csv")])
        if file_path:
            self.manager.file_path = file_path
            self.manager.load_books()
            messagebox.showinfo("Успіх", "Дані завантажено успішно!")

    def add_book(self):
        def save():
            try:
                title = entry_title.get()
                author = entry_author.get()
                year = int(entry_year.get())
                genre = entry_genre.get()
                quantity = int(entry_quantity.get())
                self.manager.add_book(title, author, year, genre, quantity)
                messagebox.showinfo("Успіх", "Книгу додано!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Помилка", "Некоректні дані!")

        add_window = tk.Toplevel(self.root)
        add_window.title("Додати книгу")

        tk.Label(add_window, text="Назва книги").grid(row=0, column=0, padx=5, pady=5)
        entry_title = tk.Entry(add_window)
        entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Автор").grid(row=1, column=0, padx=5, pady=5)
        entry_author = tk.Entry(add_window)
        entry_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Рік видання").grid(row=2, column=0, padx=5, pady=5)
        entry_year = tk.Entry(add_window)
        entry_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Жанр").grid(row=3, column=0, padx=5, pady=5)
        entry_genre = tk.Entry(add_window)
        entry_genre.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Кількість примірників").grid(row=4, column=0, padx=5, pady=5)
        entry_quantity = tk.Entry(add_window)
        entry_quantity.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(add_window, text="Зберегти", command=save).grid(row=5, column=0, columnspan=2, pady=10)

    def show_books(self):
        books_window = tk.Toplevel(self.root)
        books_window.title("Список книг")

        tree = ttk.Treeview(books_window, columns=("Назва", "Автор", "Рік видання", "Жанр", "Кількість примірників"),
                            show="headings")
        tree.pack(expand=True, fill="both")

        tree.heading("Назва", text="Назва книги")
        tree.heading("Автор", text="Автор")
        tree.heading("Рік видання", text="Рік видання")
        tree.heading("Жанр", text="Жанр")
        tree.heading("Кількість примірників", text="Кількість примірників")

        tree.column("Назва")
        tree.column("Автор")
        tree.column("Рік видання")
        tree.column("Жанр")
        tree.column("Кількість примірників")

        for _, row in self.manager.books.iterrows():
            tree.insert("", "end", values=(
            row['Назва книги'], row['Автор'], row['Рік видання'], row['Жанр'], row['Кількість примірників']))


if __name__ == "__main__":
    library_manager = LibraryManager("boоoks.csv")
    main_window = tk.Tk()
    app = LibraryGUI(main_window, library_manager)
    main_window.mainloop()

