from django.db import models
from django.utils import timezone

from app.config.settings import DB_SCHEMA


class MetaFields(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk and not kwargs.get("force_insert", False):
            self.update_time = timezone.now()
        super().save(*args, **kwargs)


class Categories(MetaFields):
    """У каждого проекта есть своя функция
    Категория	                Цель проекта
    Экзистенциальные	        Найти смысл, идентичность, самореализацию
    Социальные	                Принадлежность, отношения, семья, дружба
    Профессиональные	        Реализация навыков, карьера, признание
    Эволюционные (родовые)	    Продление рода, воспитание, генетическое наследие
    Духовные	                Вера, трансцендентность, внутренний путь
    Гедонистические	            Удовольствие, отдых, красота, эмоции
    Этические/моральные	        Помощь другим, служение, справедливость
    Материальные	            Деньги, имущество, безопасность, накопления
    """

    category_title = models.CharField(max_length=300, null=False, unique=True)
    category_description = models.CharField(max_length=300, null=False)
    category_number = models.IntegerField(null=False, unique=True)

    class Meta:
        db_table = f'"{DB_SCHEMA}"."categories"'

    def __str__(self):
        return f"{self.category_number}. {self.category_title}"


class User(MetaFields):
    username = models.CharField(max_length=150, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    hashed_password = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = f'"{DB_SCHEMA}"."user_data"'

    def __str__(self):
        return self.username


class Projects(MetaFields):
    """Описание проектов"""

    project_title = models.CharField(max_length=300, null=False, unique=True)
    project_description = models.CharField(max_length=300, null=False)
    project_category = models.ForeignKey(
        "Categories", on_delete=models.PROTECT, related_name="projects", null=False
    )

    class Meta:
        db_table = f'"{DB_SCHEMA}"."projects"'

    def __str__(self):
        return self.project_title


class Tasks(MetaFields):
    """Описание задач"""

    task_title = models.CharField(max_length=300, null=False, unique=True)
    task_description = models.CharField(max_length=300, null=False)
    task_status = models.BooleanField(default=False)

    class Meta:
        db_table = f'"{DB_SCHEMA}"."tasks"'

    def __str__(self):
        return self.task_title


class TasksAssociation(MetaFields):
    """Связь задач, проектов и пользователей"""

    project = models.ForeignKey(
        "Projects", on_delete=models.PROTECT, related_name="task_links", null=False
    )

    task = models.ForeignKey(
        "Tasks", on_delete=models.PROTECT, related_name="project_links", null=False
    )

    user = models.ForeignKey(
        "User", on_delete=models.PROTECT, related_name="task_assignments", null=False
    )

    # Например, статус выполнения можно добавить:
    is_done = models.BooleanField(default=False)

    class Meta:
        db_table = f'"{DB_SCHEMA}"."tasks_association"'
        unique_together = ("project", "task", "user")

    def __str__(self):
        return f"{self.task.task_title} — {self.project.project_title} by {self.user.username}"
