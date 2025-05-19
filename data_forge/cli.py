import typer
import sys
from loguru import logger

from data_forge.commands import first_migrate
from data_forge.commands import insert_data
from create_super_user import create_super_user

app = typer.Typer(name="data_forge")


@app.command(name="first-migrate")
def first_migrate_data():
    """
    Create first_migrate in DB
    """
    first_migrate.first_migrate()
    
    
@app.command(name="insert-data")
def create_directories():
    """
    Insert data to db from json
    
    """
    insert_data.insert_data()
    
@app.command(name="create-super-user")
def create_super():
    """
    Create super user for django admin
    
    """
    create_super_user()
    
        
def main():
    if "--help" in sys.argv:
        app()
        
    else:
        create_directories_command = None
        for command_info in app.registered_commands:
            if command_info.name == sys.argv[1]:
                create_directories_command = command_info.callback
                
        if create_directories_command:
            create_directories_command()
            
        else:
            logger.warning(f"Command {sys.argv[1]} not found.")
        

if __name__ == "__main__":
    main()