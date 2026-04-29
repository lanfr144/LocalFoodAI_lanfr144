import os

def parse(login_path: str):
    """Very simple fallback parser.
    It looks for environment variables matching the login_path name.
    For example, for 'app_loader' it expects:
        APP_LOADER_HOST, APP_LOADER_USER, APP_LOADER_PASSWORD
    If those variables are missing, returns defaults pointing to localhost.
    """
    prefix = login_path.upper()
    host = os.getenv(f"{prefix}_HOST", "127.0.0.1")
    user = os.getenv(f"{prefix}_USER", "root")
    password = os.getenv(f"{prefix}_PASSWORD", "")
    return {"host": host, "user": user, "password": password}
