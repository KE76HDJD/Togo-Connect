import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from utils import load_all, apply_style, badge

st.set_page_config(page_title="Recommandations", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()
st.title("Recommandations et plan d'action")
st.caption("Quatre actions priorisées selon l'impact et le coût de mise en oeuvre")
p1 = ", ".join(ind[ind.priorite == 1].sort_values("nb_momo", ascending=False)["prefecture"].head(6).tolist())

cards = [
    ("R1 - Agences mobiles mutualisées", "P1", "Horizon 0-12 mois - Coût faible",
     f"Unités itinérantes Moov et Togocom sur les 12 préfectures P1 ({p1}). Indicateur : 12 tournées mensuelles."),
    ("R2 - 200 relais Mobile Money labellisés", "P1", "Horizon 6-18 mois - Coût modéré",
     "Équipement et formation des points à fort trafic en relais de services. Indicateur : +40 % d'actes hors Lomé."),
    ("R3 - Datacenter secondaire à Kara ou Sokodé", "P2", "Horizon 12-36 mois - Investissement structurant",
     "Site redondant adossé à la fibre. Indicateur : reprise sous 4 heures, latence du nord réduite de 40 %."),
    ("R4 - Transparence des données ouvertes", "P3", "Horizon 3 mois - Coût nul",
     "Publication des données CANAL+, de la population RGPH et des antennes BTS pour une version 2 en ratio pour 10 000 habitants."),
]
for t, b, d, desc in cards:
    cls = "p1" if b == "P1" else ("p2" if b == "P2" else "p3")
    st.markdown(f'<div class="card"><h4>{t} {badge(b, cls)}</h4><div>{d}</div><div>{desc}</div></div>',
        unsafe_allow_html=True)
st.download_button("Télécharger les indicateurs par préfecture (CSV)", ind.to_csv(index=False),
    "indicateurs_prefecture.csv", width="stretch")
