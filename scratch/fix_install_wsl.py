import re
import os

file_path = "INSTALL_WSL.md"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace the encoding artifact in the first line if present
content = content.replace("Franois", "Francois")
content = content.replace("FranA ois", "Francois")
content = content.replace("Françoise", "Francois")

# 1. Update Step 3 (.env template)
old_step3 = """cat <<EOF > .env
MYSQL_ROOT_PASSWORD=your_db_password_here
DB_READER_PASS=your_db_password_here
DB_LOADER_PASS=your_db_password_here
DB_APP_AUTH_PASS=your_db_password_here
MYSQL_ZABBIX_PASSWORD=your_db_password_here
EOF"""

new_step3 = """Configure your database credentials, active network mode, and the target model name in a `.env` file at the root of the repository. A generic template is provided below:

```ini
# NETWORK_MODE: local (offline) or server (online)
NETWORK_MODE=local
LLM_MODEL=llama3.2:3b

# DATABASE CREDENTIALS (MySQL)
MYSQL_ROOT_PASSWORD=your_secure_root_password
DB_READER_PASS=your_secure_reader_password
DB_LOADER_PASS=your_secure_loader_password
DB_APP_AUTH_PASS=your_secure_auth_password
MYSQL_ZABBIX_PASSWORD=your_secure_zabbix_password

# ZABBIX & SNMP CREDENTIALS
ZABBIX_USER=Admin
ZABBIX_PASS=zabbix
ZABBIX_SNMP_USER=zabbix_snmp
ZABBIX_SNMP_AUTHKEY=authkey123
ZABBIX_SNMP_PRIVKEY=privkey123
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your_webhook_id

# EMAIL ALERTS CONFIGURATION
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password

# TAIGA CREDENTIALS
TAIGA_URL=https://192.168.130.161/taiga
TAIGA_USER=your_taiga_user
TAIGA_PASS=your_taiga_password
```"""

# Remove the extra code fence that would follow the old cat block
content = content.replace(f"```bash\n{old_step3}\n```", new_step3)

# 2. Update Step 5 (model pulling command)
old_step5 = "docker exec -it $(docker ps -q -f name=ollama) ollama pull qwen2.5:7b"
new_step5 = "docker exec -it $(docker ps -q -f name=ollama) ollama pull $( grep '^[ \\t]*LLM_MODEL[ \t]*=' .env | sed 's/^.*=//' )"

content = content.replace(old_step5, new_step5)
content = content.replace("model **`qwen2.5:7b`**", "model")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("INSTALL_WSL.md successfully updated and encoding sanitized.")
