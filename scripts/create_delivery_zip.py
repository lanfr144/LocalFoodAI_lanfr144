#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:create_delivery_zip.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import zipfile
import pathspec

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gitignore_path = os.path.join(repo_root, ".gitignore")
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, f)
    else:
        spec = pathspec.PathSpec([])
        
    # Standard ignores
    spec.patterns.append(pathspec.patterns.GitWildMatchPattern('.git/'))
    spec.patterns.append(pathspec.patterns.GitWildMatchPattern('*.zip'))

    zip_path = os.path.join(repo_root, "delivery.zip")
    print(f"Building {zip_path}...")
    
    network_mode = 'server'
    llm_model = 'your_llm_model'
    env_path = os.path.join(repo_root, ".env")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('NETWORK_MODE='):
                    network_mode = line.strip().split('=', 1)[1]
                elif line.startswith('LLM_MODEL='):
                    llm_model = line.strip().split('=', 1)[1]
    
    dummy_env = f"""# ==========================================
# LOCAL FOOD AI - DUMMY CONFIGURATION
# ==========================================

# ------------------------------------------
# 1. NETWORK & ENVIRONMENT MODE
# ------------------------------------------
# NETWORK_MODE: Controls network call execution.
# Possible values: 'local' (or 'server')
NETWORK_MODE={network_mode}
LLM_MODEL={llm_model}

# ------------------------------------------
# 2. DATABASE CREDENTIALS (MySQL)
# ------------------------------------------
MYSQL_ROOT_PASSWORD=your_mysql_root_pass
DB_READER_PASS=your_db_reader_pass
DB_LOADER_PASS=your_db_loader_pass
DB_APP_AUTH_PASS=your_db_auth_pass
MYSQL_ZABBIX_PASSWORD=your_mysql_zabbix_pass

# ------------------------------------------
# 3. ZABBIX & SNMP CREDENTIALS
# ------------------------------------------
ZABBIX_USER=Admin
ZABBIX_PASS=your_zabbix_pass
ZABBIX_SNMP_USER=zabbix_snmp
ZABBIX_SNMP_AUTHKEY=your_snmp_authkey
ZABBIX_SNMP_PRIVKEY=your_snmp_privkey
DISCORD_WEBHOOK=your_discord_webhook

# ------------------------------------------
# 4. EMAIL ALERTS CONFIGURATION
# ------------------------------------------
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password

# ------------------------------------------
# 5. TAIGA PROJECT MANAGEMENT CREDENTIALS
# ------------------------------------------
TAIGA_URL=your_taiga_url
TAIGA_USER=your_taiga_user
TAIGA_PASS=your_taiga_pass
"""
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('.env', dummy_env)
        for root, dirs, files in os.walk(repo_root):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_root)
                posix_path = rel_path.replace(os.sep, '/')
                
                # Check against .gitignore rules
                if not spec.match_file(posix_path):
                    zipf.write(full_path, rel_path)
                    
    print(f"Successfully created: delivery.zip")

if __name__ == "__main__":
    main()
