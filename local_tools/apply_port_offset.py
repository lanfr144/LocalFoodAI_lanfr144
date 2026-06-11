#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import socket
import sys

DEFAULT_PORTS = {
    "BACKEND_PORT": 5000,
    "MYSQL_PORT": 3306,
    "AIRFLOW_PORT": 8080,
    "ZABBIX_PORT": 8081,
    "JENKINS_PORT": 8088
}

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        return s.connect_ex(('127.0.0.1', port)) == 0

def load_env(env_path):
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

def write_env(env_path, updates):
    if not os.path.exists(env_path):
        with open(env_path, 'w', encoding='utf-8') as f:
            for k, v in updates.items():
                f.write(f"{k}={v}\n")
        return

    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_keys = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key, _ = stripped.split('=', 1)
            key = key.strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    for k, v in updates.items():
        if k not in updated_keys:
            new_lines.append(f"{k}={updates[k]}\n")

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if not os.path.exists(env_path):
        print(f"[ERROR] .env file not found at {env_path}")
        sys.exit(1)
        
    env_vars = load_env(env_path)
    offset_str = env_vars.get("PORT_OFFSET", "0")
    try:
        offset = int(offset_str)
    except ValueError:
        print(f"[ERROR] PORT_OFFSET in .env is not a valid integer: '{offset_str}'")
        sys.exit(1)
        
    print(f"[INFO] Using PORT_OFFSET={offset} loaded from .env")
    
    # Calculate ports and check availability
    calculated_ports = {}
    in_use_ports = []
    
    for name, default_port in DEFAULT_PORTS.items():
        target_port = default_port + offset
        calculated_ports[name] = target_port
        
        print(f"Checking target port {name}: {target_port} ... ", end="")
        sys.stdout.flush()
        if is_port_in_use(target_port):
            print("IN USE")
            in_use_ports.append((name, target_port))
        else:
            print("FREE")
            
    if in_use_ports:
        print("\n[ERROR] The following calculated ports are already in use on the host:")
        for name, port in in_use_ports:
            print(f"  - {name}: {port}")
        print("Please resolve the conflict or change PORT_OFFSET in .env before proceeding.")
        sys.exit(1)
        
    # Write updates to .env
    updates = {name: str(port) for name, port in calculated_ports.items()}
    write_env(env_path, updates)
    print("\n[SUCCESS] Successfully verified and updated .env with offsetted ports:")
    for name, port in calculated_ports.items():
        print(f"  - {name}: {port}")

if __name__ == "__main__":
    main()