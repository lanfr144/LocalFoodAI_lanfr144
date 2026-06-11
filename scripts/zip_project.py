#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# Alias for create_delivery_zip.py
import os
import sys

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"python {os.path.join(script_dir, 'create_delivery_zip.py')}")