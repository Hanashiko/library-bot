import os
import time
import subprocess
from database.connection_db import get_connection, close_connection
from database.config_db import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def create_backup() -> str:
    connection = get_connection()
    if connection is None:
        print("Failed to create backup: unable to connect to database.")
        return ""
    
    backup_dir = 'database/backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    backup_filename = f"{backup_dir}/backup_{int(time.time())}.sql"
    
    try:
        command = f"mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {backup_filename}"
        subprocess.run(command, shell=True, check=True)
        print(f"Backup created: {backup_filename}")
        return backup_filename
    except subprocess.CalledProcessError as err:
        print(f"Error creating backup: {err}")
        return ""
    finally:
        close_connection(connection)
