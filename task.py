"""
Модуль для работы с задачей.
Содержит класс Task и основные операции над ним.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Класс, представляющий одну задачу пользователя.
    
    Attributes:
        id: уникальный идентификатор задачи
        title: краткий заголовок задачи (обязательный)
        description: подробное описание (опционально)
        due_time: время выполнения задачи (часы:минуты)
        is_completed: статус выполнения задачи
        created_at: дата и время создания задачи
    """
    
    title: str
    id: Optional[int] = None
    description: str = ""
    due_time: str = "23:59"
    is_completed: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Инициализация после создания объекта."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def complete(self) -> None:
        """Отмечает задачу как выполненную."""
        self.is_completed = True
    
    def to_dict(self) -> dict:
        """
        Преобразует задачу в словарь для сохранения.
        
        Returns:
            dict: словарь с полями задачи
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Создает задачу из словаря (при загрузке из файла).
        
        Args:
            data: словарь с данными задачи
            
        Returns:
            Task: восстановленный объект задачи
        """
        task = cls(
            title=data['title'],
            description=data['description'],
            due_time=data['due_time'],
            is_completed=data['is_completed']
        )
        task.id = data['id']
        task.created_at = datetime.fromisoformat(data['created_at'])
        return task
