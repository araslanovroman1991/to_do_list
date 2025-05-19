import os
import sys

from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.config.settings")
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../.."))


def first_migrate():
    """
    Выполнить django migrate
    """
    args = ["manage.py", "migrate"]
    execute_from_command_line(args)
