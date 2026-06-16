The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:URL_Formats.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Network Connection URL Directory

This runbook catalogs the specific network formats and port endpoints required to access the application and monitoring servers across different loopback, hostname, and address protocols.

## 1. Localhost Format (Loopback)
- **Streamlit Web Application UI**: `http://localhost:100` *(via Nginx)* or `http://localhost:8522` *(direct)*
- **Zabbix Web UI Console**: `http://localhost:8101`
- **Airflow Webserver DAG UI**: `http://localhost:8102`
- **Ollama AI Local Engine**: `http://localhost:11434`
- **SearXNG Meta-Search API**: `http://localhost:8105`
- **MySQL Database Server**: `localhost:3326` *(direct SQL connection)*

## 2. Hostname Format (assuming Hostname is `XYZZYX`)
- **Streamlit Web Application UI**: `http://XYZZYX:100` or `http://XYZZYX:8522`
- **Zabbix Web UI Console**: `http://XYZZYX:8101`
- **Airflow Webserver DAG UI**: `http://XYZZYX:8102`
- **Ollama AI Local Engine**: `http://XYZZYX:11434`
- **SearXNG Meta-Search API**: `http://XYZZYX:8105`
- **MySQL Database Server**: `XYZZYX:3326`

## 3. IPv4 Format (assuming Local Host IP is `192.168.1.50`)
- **Streamlit Web Application UI**: `http://192.168.1.50:100` or `http://192.168.1.50:8522` *(loopback: `http://127.0.0.1:100`)*
- **Zabbix Web UI Console**: `http://192.168.1.50:8101` *(loopback: `http://127.0.0.1:8101`)*
- **Airflow Webserver DAG UI**: `http://192.168.1.50:8102` *(loopback: `http://127.0.0.1:8102`)*
- **Ollama AI Local Engine**: `http://192.168.1.50:11434` *(loopback: `http://127.0.0.1:11434`)*
- **SearXNG Meta-Search API**: `http://192.168.1.50:8105` *(loopback: `http://127.0.0.1:8105`)*
- **MySQL Database Server**: `192.168.1.50:3326` *(loopback: `127.0.0.1:3326`)*

## 4. IPv6 Format (using loopback `[::1]` or link-local address)
- **Streamlit Web Application UI**: `http://[::1]:100` or `http://[::1]:8522`
- **Zabbix Web UI Console**: `http://[::1]:8101`
- **Airflow Webserver DAG UI**: `http://[::1]:8102`
- **Ollama AI Local Engine**: `http://[::1]:11434`
- **SearXNG Meta-Search API**: `http://[::1]:8105`
- **MySQL Database Server**: `[::1]:3326`
