"""Regenere les figures et tables dans outputs/.

Lancer depuis la racine du projet : python3 make_figures.py
"""
from pathlib import Path
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
PROC = os.path.join(BASE, "data", "processed")
FIG = os.path.join(BASE, "outputs", "figures")
TAB = os.path.join(BASE, "outputs", "tables")
os.makedirs(FIG, exist_ok=True); os.makedirs(TAB, exist_ok=True)

ag = pd.read_parquet(os.path.join(PROC, "agences_clean.parquet"))
mo = pd.read_parquet(os.path.join(PROC, "momo_clean.parquet"))
ind = pd.read_csv(os.path.join(PROC, "indicateurs_prefecture.csv"))

plt.rcParams.update({"figure.dpi": 150, "font.size": 9})

# 1 agences par région
by = ag.groupby("region_nom_bdd").size().sort_values()
plt.figure(figsize=(6,3.5)); by.plot(kind="barh", color="#0066B3")
plt.title("Agences par région (n=90)"); plt.xlabel("Agences"); plt.tight_layout()
plt.savefig(os.path.join(FIG, "01_agences_region.png")); plt.close()

# 2 momo par région
by2 = mo.groupby("region_nom_bdd").size().sort_values()
plt.figure(figsize=(6,3.5)); by2.plot(kind="barh", color="#7B2CBF")
plt.title("Points Mobile Money par région (n=19 788)"); plt.xlabel("Points"); plt.tight_layout()
plt.savefig(os.path.join(FIG, "02_momo_region.png")); plt.close()

# 3 top 15 momo
t15 = ind.sort_values("nb_momo", ascending=False).head(15).sort_values("nb_momo")
plt.figure(figsize=(6.5,4.5)); plt.barh(t15["prefecture"], t15["nb_momo"], color="#FF7900")
plt.title("Top 15 préfectures Mobile Money"); plt.xlabel("Points"); plt.tight_layout()
plt.savefig(os.path.join(FIG, "03_top_momo.png")); plt.close()

# 4 scatter agences vs momo
plt.figure(figsize=(6,4))
for reg, g in ind.groupby("region"):
    plt.scatter(g["nb_agences"], g["nb_momo"], label=reg, s=60)
plt.xlabel("Nb agences"); plt.ylabel("Nb points MoMo"); plt.title("Adéquation par préfecture")
plt.legend(fontsize=7); plt.tight_layout()
plt.savefig(os.path.join(FIG, "04_adequation.png")); plt.close()

# 5 operateurs momo
op = mo["operateur_clean"].value_counts()
plt.figure(figsize=(5,3.5)); op.plot(kind="bar", color=["#00693E","#0066B3","#FF7900","#B0BEC5"])
plt.title("Points MoMo par opérateur"); plt.ylabel("Points"); plt.xticks(rotation=15); plt.tight_layout()
plt.savefig(os.path.join(FIG, "05_operateurs.png")); plt.close()

# 6 datacenters par prefecture (concentration Lome)
dc = pd.read_parquet(os.path.join(PROC, "datacenters_clean.parquet"))
bydc = dc.groupby("prefecture_nom_bdd").size().sort_values()
plt.figure(figsize=(5,2.6)); bydc.plot(kind="barh", color="#00693E")
plt.title("Datacenters par préfecture (n=3, tous à Lomé)"); plt.xlabel("Datacenters"); plt.tight_layout()
plt.savefig(os.path.join(FIG, "06_datacenters.png")); plt.close()

# tables
ind.sort_values(["priorite","nb_momo"], ascending=[True,False]).to_csv(os.path.join(TAB,"priorites_prefectures.csv"), index=False)
ind.sort_values("nb_momo", ascending=False).head(10).to_csv(os.path.join(TAB,"top10_momo.csv"), index=False)
print("figures + tables OK:", os.listdir(FIG), os.listdir(TAB))
