"""
Модуль для сохранения и загрузки задач в JSON файл.
"""

import json
import os
from typing import List
from task import Task


class TaskStorage:
    """
    Класс для работы с постоянным хранением задач.
    
    Tasks are stored in a JSON file. Each task is saved as a dictionary.
    """
    
    def __init__(self, filename: str = "tasks.json"):
        """
        Инициализация хранилища.
        
        Args:
            filename: имя файла для сохранения задач
        """
        self.filename = filename
    
    def save(self, tasks: List[Task]) -> None:
        """
        Сохраняет список задач в файл.
        
        Args:
            tasks: список задач для сохранения
        """
        data = [task.to_dict() for task in tasks]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> List[Task]:
        """
        Загружает список задач из файла.
        
        Returns:
            List[Task]: список восстановленных задач
        """
        if not os.path.exists(self.filename):
            return []
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Task.from_dict(item) for item in data]
