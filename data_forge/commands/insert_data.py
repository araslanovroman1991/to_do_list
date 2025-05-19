import json
import os
import sys
from pathlib import Path
from typing import Any

import django
from django.db import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../.."))
base_path = Path(__file__).resolve().parent.parent
django.setup()

from app.models.models import Categories, Projects, Tasks, TasksAssociation, User  # type: ignore


def get_js_data(name: str) -> Any:
    """get js_data for table"""
    full_path = os.path.join(base_path, "data", f"{name}.json")
    with open(full_path, encoding="utf-8") as f:
        return json.load(f)


def insert_directory_data(
    model: type[models.Model], data: list, lookup_fields: list
) -> None:
    """
    Универсальная функция для вставки справочников (idempotent insert)

    :param model: Django-модель (например, Categories)
    :param data: список словарей с данными
    :param lookup_field: поле, по которому искать (обычно уникальное)
    """
    for item in data:
        item = item.copy()  # type: ignore

        # Автоматически разрешаем ForeignKey
        for field in model._meta.fields:
            if isinstance(field, models.ForeignKey):
                fk_field = field.name  # project_category
                fk_model = field.related_model  # Categories
                if fk_field in item and isinstance(item[fk_field], int):
                    try:
                        item[fk_field] = fk_model.objects.get(pk=item[fk_field])
                    except fk_model.DoesNotExist as err:
                        raise ValueError(
                            f"{fk_model.__name__} with id={item[fk_field]} not found"
                        ) from err

                # Также поддержка *_id
                fk_id_field = f"{fk_field}_id"
                if fk_id_field in item:
                    try:
                        item[fk_field] = fk_model.objects.get(pk=item[fk_id_field])
                        del item[fk_id_field]
                    except fk_model.DoesNotExist as err:
                        raise ValueError(
                            f"{fk_model.__name__} with id={item[fk_id_field]} not found"
                        ) from err

        # Вычисляем поля для get_or_create
        lookup_value = {field: item[field] for field in lookup_fields}
        defaults = {k: v for k, v in item.items() if k not in lookup_fields}

        model.objects.get_or_create(**lookup_value, defaults=defaults)


def insert_data():
    insert_directory_data(
        Categories,
        get_js_data(Categories.__name__.lower()),
        lookup_fields=["category_number"],
    )
    insert_directory_data(
        User, get_js_data(User.__name__.lower()), lookup_fields=["username"]
    )
    insert_directory_data(
        Projects,
        get_js_data(Projects.__name__.lower()),
        lookup_fields=["project_title"],
    )
    insert_directory_data(
        Tasks, get_js_data(Tasks.__name__.lower()), lookup_fields=["task_title"]
    )
    insert_directory_data(
        TasksAssociation,
        get_js_data(TasksAssociation.__name__.lower()),
        lookup_fields=["project", "task", "user"],
    )
