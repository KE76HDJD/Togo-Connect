# Togo — Diagnostic connectivité & inclusion numérique (Défi 1)

Préparé par ANKOU Yaokouma Kevin.

Dashboard Streamlit + rapport 10 slides. Données : geodata.gouv.tg uniquement.

## Prérequis

- Python 3.10 ou supérieur (`python3 --version`)
- pip à jour (`pip install --upgrade pip`)
- Connexion internet uniquement pour l'installation des dépendances (ensuite 100 % hors-ligne)

## Lancement

```bash
cd Data_lab
pip install -r requirements.txt
streamlit run app/Home.py
```

Variante recommandée (environnement isolé) :

```bash
cd Data_lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Home.py
```

Puis ouvrir `http://localhost:8501`.

## Régénérer les livrables (optionnel)

```bash
python3 clean.py         # data/raw -> data/processed
python3 make_figures.py  # figures + tables dans outputs/
python3 make_ppt.py      # rapport/Togo_Diagnostic_Connectivite_10slides.pptx
```

## Données sources (`data/raw/` incluses)

- Agences Moov 28, Togocom 62, Télécom 90 (= union), CANAL+ 0 ligne, MoMo 19 788, Datacenters 3.
- Fichier Télécom dédupliqué ; CANAL+ vide assumé ; `Nsp` → Inconnu.
- `data/processed/` est déjà généré : le dashboard fonctionne sans relancer `clean.py`.

## Méthode

- Parsing `POINT(lon lat)`, recodage `Grand Lomé = Golfe + Agoè-Nyivé`.
- Indicateurs par préfecture : `nb_agences, nb_momo, momo_par_agence, priorite P1/P2/P3`.
- P1 = 0 agence (12/39) ; ratio national 220 MoMo/1 agence.

## Livrables

- `app/` : accueil + 5 pages (Agences, MoMo, Adéquation, Zones blanches, Recommandations).
- `rapport/Togo_Diagnostic_Connectivite_10slides.pptx` : 10 slides.
- `outputs/` : figures + tables.

## Dépannage

| Symptôme | Solution |
|---|---|
| `pip` refuse l'installation (PEP 668, Debian/Ubuntu) | `pip install -r requirements.txt --break-system-packages` ou utiliser un `venv` |
| `FileNotFoundError: .../data/processed/...` | Lancer depuis la racine `Data_lab`, ou relancer `python3 clean.py` |
| Port 8501 occupé | `streamlit run app/Home.py --server.port 8502` |
| Ancien code affiché après modification | Arrêter le serveur (`Ctrl+C`), supprimer `app/__pycache__`, relancer |
| `python-pptx` absent pour `make_ppt.py` | `pip install -r requirements.txt` (inclut `python-pptx`, `Pillow`, `lxml`) |

## Limites

Pas de population RGPH ni d'antennes BTS fournies → pas de ratio /hab ni de vraie carte 2G/3G/4G. Recommandation R4 : publier pour V2.
