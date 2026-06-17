#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "Criando ambiente virtual .venv..."
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install selenium webdriver-manager
python assistente-virtual/whatsapp.py
