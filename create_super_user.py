from django.contrib.auth import get_user_model
import os 
from loguru import logger
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.config.settings')

django.setup()

def create_super_user():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        logger.success("Суперпользователь создан")
    else:
        logger.warning("Суперпользователь уже существует")