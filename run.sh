#!/bin/bash
# Lancement du dashboard - a executer depuis la racine du projet.
# Sur Debian/Ubuntu recents, si pip refuse l'installation (PEP 668),
# relancer avec : pip install -r requirements.txt --break-system-packages
set -e
cd "$(dirname "$0")"
pip install -r requirements.txt
streamlit run app/Home.py
