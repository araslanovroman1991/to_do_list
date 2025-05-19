import os

import django
from django.contrib.auth import get_user_model
from loguru import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")

django.setup()


def create_super_user():
    user = get_user_model()
    if not user.objects.filter(username="admin").exists():
        user.objects.create_superuser("admin", "admin@example.com", "admin")
        logger.success("Суперпользователь создан")
    else:
        logger.warning("Суперпользователь уже существует")
