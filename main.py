"""
Главный модуль приложения TaskMate.
Запускает графический интерфейс и управляет основным циклом программы.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from task import Task
from storage import TaskStorage


class TaskMateApp:
    """
    Главный класс приложения TaskMate.
    
    Управляет интерфейсом и логикой работы с задачами.
    """
    
    def __init__(self):
        """Инициализация приложения: загрузка задач и создание окна."""
        self.storage = TaskStorage()
        self.tasks = self.storage.load()
        self.next_id = max([t.id for t in self.tasks], default=0) + 1
        
        # Создание главного окна
        self.root = tk.Tk()
        self.root.title("TaskMate - Планировщик задач")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка пользовательского интерфейса."""
        # Заголовок
        tk.Label(
            self.root,
            text=f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Список задач (рамка с прокруткой)
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(self.tasks_frame)
        scrollbar = tk.Scrollbar(self.tasks_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Поле для новой задачи
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.task_entry = tk.Entry(input_frame)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        tk.Button(
            input_frame,
            text="Добавить",
            command=self.add_task
        ).pack(side=tk.RIGHT)
        
        # Кнопки фильтров
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        
        tk.Button(filter_frame, text="Все задачи", command=self.show_all).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="На сегодня", command=self.show_today).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Выполненные", command=self.show_completed).pack(side=tk.LEFT, padx=5)
        
        # Отображаем задачи
        self.show_all()
    
    def add_task(self):
        """Добавляет новую задачу из поля ввода."""
        title = self.task_entry.get().strip()
        if title:
            task = Task(
                id=self.next_id,
                title=title
            )
            self.next_id += 1
            self.tasks.append(task)
            self.storage.save(self.tasks)
            self.task_entry.delete(0, tk.END)
            self.show_all()
        else:
            messagebox.showwarning("Ошибка", "Введите название задачи")
    
    def toggle_task(self, task_id: int):
        """Переключает статус выполнения задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.complete()
                break
        self.storage.save(self.tasks)
        self.show_all()
    
    def delete_task(self, task_id: int):
        """Удаляет задачу."""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.storage.save(self.tasks)
        self.show_all()
    
    def show_all(self):
        """Показывает все задачи."""
        self._render_tasks(self.tasks)
    
    def show_today(self):
        """Показывает только задачи на сегодня."""
        today = datetime.now().date()
        filtered = [
            t for t in self.tasks
            if t.created_at.date() == today and not t.is_completed
        ]
        self._render_tasks(filtered)
    
    def show_completed(self):
        """Показывает только выполненные задачи."""
        filtered = [t for t in self.tasks if t.is_completed]
        self._render_tasks(filtered)
    
    def _render_tasks(self, tasks: list):
        """
        Отображает список задач в интерфейсе.
        
        Args:
            tasks: список задач для отображения
        """
        # Очищаем текущий список
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not tasks:
            tk.Label(self.scrollable_frame, text="Нет задач", fg="gray").pack(pady=20)
            return
        
        for task in tasks:
            frame = tk.Frame(self.scrollable_frame, bd=1, relief=tk.RAISED)
            frame.pack(fill=tk.X, pady=2)
            
            # Чекбокс
            var = tk.BooleanVar(value=task.is_completed)
            cb = tk.Checkbutton(
                frame,
                text=task.title,
                variable=var,
                command=lambda tid=task.id: self.toggle_task(tid),
                font=("Arial", 11)
            )
            cb.pack(side=tk.LEFT, padx=5)
            
            if task.is_completed:
                cb.config(fg="green", font=("Arial", 11, "overstrike"))
            
            # Время
            time_label = tk.Label(frame, text=task.due_time, fg="blue", font=("Arial", 9))
            time_label.pack(side=tk.LEFT, padx=10)
            
            # Кнопка удаления
            tk.Button(
                frame,
                text="✖",
                command=lambda tid=task.id: self.delete_task(tid),
                fg="red",
                bd=0,
                font=("Arial", 10)
            ).pack(side=tk.RIGHT, padx=5)
    
    def run(self):
        """Запускает главный цикл приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskMateApp()
    app.run()
