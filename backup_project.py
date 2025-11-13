import os
import shutil
from datetime import datetime

PROJECT_DIR = "."
BACKUP_ROOT = "./backups"

# Files and folders to exclude from backup
EXCLUDE = ['venv', 'backups', '__pycache__', '.git', '*.pyc']

def should_exclude(name):
    """Check if file/folder should be excluded"""
    for pattern in EXCLUDE:
        if pattern in name or name.startswith('.'):
            return True
    return False

def make_backup():
    """Create timestamped backup of project"""
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(BACKUP_ROOT, f"backup_{timestamp}")
    
    print(f"Creating backup: {backup_dir}")
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy files
    copied_files = 0
    for item in os.listdir(PROJECT_DIR):
        if should_exclude(item):
            continue
        
        src = os.path.join(PROJECT_DIR, item)
        dst = os.path.join(backup_dir, item)
        
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
                print(f"  Copied folder: {item}/")
            else:
                shutil.copy2(src, dst)
                print(f"  Copied file: {item}")
            copied_files += 1
        except Exception as e:
            print(f"  Warning: Could not copy {item}: {e}")
    
    print(f"\nBackup complete!")
    print(f"Location: {backup_dir}")
    print(f"Files/folders backed up: {copied_files}")
    print(f"\nTo restore: Copy files from backup folder back to project")

if __name__ == "__main__":
    make_backup()