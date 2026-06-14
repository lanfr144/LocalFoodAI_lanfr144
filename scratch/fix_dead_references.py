import os

# 1. Update start_batch_ingest.sh
file1 = "start_batch_ingest.sh"
if os.path.exists(file1):
    with open(file1, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    content = content.replace("Lange FranA ois", "Francois Lange")
    content = content.replace("Lange FranAois", "Francois Lange")
    content = content.replace("Lange François", "Francois Lange")
    
    old_block = """echo "dYs? Starting database wipe and reset..."
# Automatically run the new DB setup to drop the rigid table
venv/bin/python3 setup_db.py"""
    
    new_block = """echo "dYs? Running database migrations to ensure schema health..."
venv/bin/python3 -m alembic upgrade head"""
    
    content = content.replace(old_block, new_block)
    with open(file1, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated start_batch_ingest.sh")

# 2. Update master_trigger.sh
file2 = "master_trigger.sh"
if os.path.exists(file2):
    with open(file2, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    content = content.replace("Lange FranA ois", "Francois Lange")
    content = content.replace("Lange FranAois", "Francois Lange")
    content = content.replace("Lange François", "Francois Lange")
    
    content = content.replace("python3 setup_db.py", "python3 -m alembic upgrade head")
    with open(file2, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated master_trigger.sh")

# 3. Update deploy.sh
file3 = "deploy.sh"
if os.path.exists(file3):
    with open(file3, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    content = content.replace("Lange FranA ois", "Francois Lange")
    content = content.replace("Lange FranAois", "Francois Lange")
    content = content.replace("Lange François", "Francois Lange")
    
    old_deploy_end = """echo "Next steps:"
echo "1. Activate your virtual environment manually:  source venv/bin/activate"
echo "2. Check your config.ini file details."
echo "3. Run your setup script to configure database users:  python setup_db.py\""""

    new_deploy_end = """echo "Next steps:"
echo "1. Activate your virtual environment manually:  source venv/bin/activate"
echo "2. Check your .env file details."
echo "3. Run database migrations:  alembic upgrade head\""""

    content = content.replace(old_deploy_end, new_deploy_end)
    with open(file3, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated deploy.sh")
