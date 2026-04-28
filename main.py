import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        
        # Предопределенные задачи с категориями
        self.default_tasks = [
            {"task": "Прочитать статью", "category": "учёба"},
            {"task": "Решить 5 задач", "category": "учёба"},
            {"task": "Сделать конспект", "category": "учёба"},
            {"task": "Выучить 10 новых слов", "category": "учёба"},
            {"task": "Сделать зарядку", "category": "спорт"},
            {"task": "Пробежать 3 км", "category": "спорт"},
            {"task": "Сделать 50 приседаний", "category": "спорт"},
            {"task": "Растяжка 15 минут", "category": "спорт"},
            {"task": "Ответить на письма", "category": "работа"},
            {"task": "Подготовить отчёт", "category": "работа"},
            {"task": "Провести встречу", "category": "работа"},
            {"task": "Обновить документацию", "category": "работа"}
        ]
        
        self.tasks = self.default_tasks.copy()
        self.history = []
        self.history_file = "task_history.json"
        
        self.create_widgets()
        self.load_history()
        
    def create_widgets(self):
        # Фрейм для добавления новых задач
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(add_frame, text="Задача:").grid(row=0, column=0, sticky="w")
        self.new_task_entry = ttk.Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Категория:").grid(row=0, column=2, sticky="w")
        self.category_combo = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], width=10)
        self.category_combo.grid(row=0, column=3, padx=5)
        self.category_combo.set("учёба")
        
        ttk.Button(add_frame, text="Добавить задачу", command=self.add_task).grid(row=0, column=4, padx=5)
        
        # Фрейм для генерации задачи
        generate_frame = ttk.LabelFrame(self.root, text="Генерация задачи", padding=10)
        generate_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(generate_frame, text="Фильтр по категории:").grid(row=0, column=0, sticky="w")
        self.filter_combo = ttk.Combobox(generate_frame, values=["Все", "учёба", "спорт", "работа"], width=10)
        self.filter_combo.grid(row=0, column=1, padx=5)
        self.filter_combo.set("Все")
        
        ttk.Button(generate_frame, text="Сгенерировать задачу", 
                  command=self.generate_task).grid(row=0, column=2, padx=5)
        
        self.result_label = ttk.Label(generate_frame, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Фрейм для истории
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создаем Treeview для отображения истории
        columns = ("#", "Дата", "Задача", "Категория")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("#", text="#")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Задача", text="Задача")
        self.tree.heading("Категория", text="Категория")
        
        self.tree.column("#", width=30)
        self.tree.column("Дата", width=150)
        self.tree.column("Задача", width=250)
        self.tree.column("Категория", width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка очистки истории
        ttk.Button(self.root, text="Очистить историю", command=self.clear_history).pack(pady=5)
        
    def add_task(self):
        task = self.new_task_entry.get().strip()
        category = self.category_combo.get()
        
        if not task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return
        
        new_task = {"task": task, "category": category}
        self.tasks.append(new_task)
        messagebox.showinfo("Успех", f"Задача '{task}' добавлена в категорию '{category}'")
        self.new_task_entry.delete(0, tk.END)
        
    def generate_task(self):
        filter_category = self.filter_combo.get()
        
        if filter_category == "Все":
            available_tasks = self.tasks
        else:
            available_tasks = [task for task in self.tasks if task["category"] == filter_category]
        
        if not available_tasks:
            messagebox.showwarning("Предупреждение", "Нет доступных задач для выбранной категории")
            return
        
        selected_task = random.choice(available_tasks)
        self.result_label.config(text=f"Задача: {selected_task['task']} ({selected_task['category']})")
        
        # Добавляем в историю
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": selected_task["task"],
            "category": selected_task["category"]
        }
        
        self.history.append(history_entry)
        self.update_history_display()
        self.save_history()
        
    def update_history_display(self):
        # Очищаем текущее отображение
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем элементы из истории
        for i, entry in enumerate(self.history, 1):
            self.tree.insert("", "end", values=(i, entry["date"], entry["task"], entry["category"]))
        
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.update_history_display()
            self.save_history()
            
    def save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
            
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_history_display()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
