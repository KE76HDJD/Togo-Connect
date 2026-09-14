"""Nettoyage des donnees brutes (data/raw) vers data/processed.

Lancer depuis la racine du projet : python3 clean.py
"""
from pathlib import Path
import os, re
import pandas as pd

BASE = Path(__file__).resolve().parent
SRC = str(BASE / "data" / "raw")
DST = str(BASE / "data" / "processed")
REF = str(BASE / "data" / "referentiels")
os.makedirs(DST, exist_ok=True)
os.makedirs(REF, exist_ok=True)

def parse_point(s):
    if pd.isna(s): return (None, None)
    m = re.match(r"POINT\s*\(\s*([-\d\.]+)\s+([-\d\.]+)\s*\)", str(s))
    if m: return (float(m.group(1)), float(m.group(2)))
    return (None, None)

def load(name):
    p = os.path.join(SRC, name)
    return pd.read_csv(p, encoding="utf-8")

f_moov = "file-Agences - Moov-14-09-2026 18_55_37.csv"
f_togo = "file-Agences - Togocom-14-09-2026 18_55_52.csv"
f_tele = "file-Agences - Télécom-14-09-2026 18_51_24.csv"
f_momo = "file-Agents mobile money-14-09-2026 18_57_11.csv"
f_dc = "file-Datacenter - Établissements-14-09-2026 18_56_44.csv"

moov = load(f_moov); togo = load(f_togo); momo = load(f_momo); dc = load(f_dc)

# Harmonisation agences : union dédupliquée sur geometry
moov["operateur"] = "Moov"
togo["operateur"] = "Togocom"
agences = pd.concat([moov, togo], ignore_index=True).drop_duplicates(subset=["geometry"]).reset_index(drop=True)
agences[["lon","lat"]] = pd.DataFrame(agences["geometry"].apply(parse_point).tolist(), index=agences.index)

# Recodage Grand Lomé = Golfe + Agoè-Nyivé (référentiel INSEED RGPH-5)
def zone_metropole(pref):
    if pref in ["Golfe","Agoè-Nyivé"]: return "Grand Lomé"
    return None
agences["zone"] = agences["prefecture_nom_bdd"].apply(lambda x: zone_metropole(x) or "Intérieur")
momo[["lon","lat"]] = pd.DataFrame(momo["geometry"].apply(parse_point).tolist(), index=momo.index)
momo["operateur_clean"] = momo["operateur"].replace({"Nsp":"Inconnu"}).fillna("Inconnu")
momo["zone"] = momo["prefecture_nom_bdd"].apply(lambda x: zone_metropole(x) or "Intérieur")
dc[["lon","lat"]] = pd.DataFrame(dc["geometry"].apply(parse_point).tolist(), index=dc.index)

# Référentiel préfecture -> région (observé dans données)
ref = pd.DataFrame({
    "prefecture": sorted(set(agences["prefecture_nom_bdd"].dropna().tolist()) | set(momo["prefecture_nom_bdd"].dropna().tolist())),
})
# mapping région via mode observé dans momo+agences
map_reg = {}
for pref in ref["prefecture"]:
    s = pd.concat([agences[agences["prefecture_nom_bdd"]==pref]["region_nom_bdd"],
                   momo[momo["prefecture_nom_bdd"]==pref]["region_nom_bdd"]]).mode()
    map_reg[pref] = s.iloc[0] if len(s)>0 else "Nsp"
ref["region_source"] = ref["prefecture"].map(map_reg)
ref["grand_lome"] = ref["prefecture"].isin(["Golfe","Agoè-Nyivé"])
ref.to_csv(os.path.join(REF,"correspondance_pref_region.csv"), index=False, encoding="utf-8")

# Indicateurs par préfecture
agg_ag = agences.groupby("prefecture_nom_bdd").size().rename("nb_agences")
agg_momo = momo.groupby("prefecture_nom_bdd").size().rename("nb_momo")
ind = pd.DataFrame({"prefecture": ref["prefecture"]}).set_index("prefecture")
ind = ind.join(agg_ag).join(agg_momo).fillna(0).astype(int)
ind["region"] = ind.index.map(map_reg)
ind["grand_lome"] = ind.index.isin(["Golfe","Agoè-Nyivé"])
ind["momo_par_agence"] = (ind["nb_momo"] / ind["nb_agences"].replace(0, float("nan"))).round(1)
ind["momo_par_agence"] = ind["momo_par_agence"].fillna(ind["nb_momo"])  # si 0 agence -> tout le MoMo sans relais
ind["flag_zero_agence"] = (ind["nb_agences"]==0).astype(int)
# Score priorité : normalisé nb_momo élevé + zéro agence = urgent
# priorité 1 = zéro agence & momo élevé ; priorité 2 = 1 agence & momo élevé ; sinon 3
def prio(r):
    if r["nb_agences"]==0 and r["nb_momo"]>=150: return 1
    if r["nb_agences"]==0: return 1
    if r["nb_agences"]<=1 and r["nb_momo"]>=200: return 2
    if r["nb_agences"]<=1: return 2
    return 3
ind["priorite"] = ind.apply(prio, axis=1)
ind = ind.sort_values(["priorite","nb_momo"], ascending=[True, False]).reset_index()

# Sauvegardes
agences.to_parquet(os.path.join(DST,"agences_clean.parquet"), index=False)
momo.to_parquet(os.path.join(DST,"momo_clean.parquet"), index=False)
dc.to_parquet(os.path.join(DST,"datacenters_clean.parquet"), index=False)
ind.to_csv(os.path.join(DST,"indicateurs_prefecture.csv"), index=False, encoding="utf-8")
agences.to_csv(os.path.join(DST,"agences_clean.csv"), index=False, encoding="utf-8")
momo.to_csv(os.path.join(DST,"momo_clean.csv"), index=False, encoding="utf-8")
dc.to_csv(os.path.join(DST,"datacenters_clean.csv"), index=False, encoding="utf-8")

print(f"Agences: {len(agences)} (Moov {(agences.operateur=='Moov').sum()}, Togocom {(agences.operateur=='Togocom').sum()})")
print(f"MoMo: {len(momo)} | prefectures: {momo.prefecture_nom_bdd.nunique()}")
print(f"Datacenters: {len(dc)}")
print(f"Zero-agence prefectures: {(ind.nb_agences==0).sum()} / {len(ind)}")
print(ind.head(12).to_string(index=False))
print("OK clean")
