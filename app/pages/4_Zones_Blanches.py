import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from streamlit_folium import st_folium
import folium
from utils import load_all, TUILES, apply_style, kpi_row

st.set_page_config(page_title="Zones blanches", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()
st.title("Zones blanches relatives")
st.caption("P1 : aucune agence (12 préfectures) - P2 : une seule agence - P3 : desservie")

kpi_row(st, [(str(int((ind.priorite == 1).sum())), "Priorité P1", "Aucune agence", "red"),
             (str(int((ind.priorite == 2).sum())), "Priorité P2", "Agence unique, situation fragile", "orange"),
             ("3/3", "Datacenters à Lomé", "Site unique, risque de concentration", "")])

p = st.selectbox("Filtrer par priorité", ["Toutes", "P1", "P2", "P3"], index=0)
d = ind if p == "Toutes" else ind[ind.priorite == int(p[1])]

m = folium.Map(location=[8.6, 1.0], zoom_start=7, tiles=TUILES)
for _, r in ag.iterrows():
    folium.CircleMarker([r.lat, r.lon], radius=4, color="#00693E", fill=True,
        fill_opacity=0.6, popup=f"{r.etab_nom}").add_to(m)
cent = mo.groupby("prefecture_nom_bdd")[["lat", "lon"]].mean().reset_index()
cent = cent.merge(ind[["prefecture", "priorite", "nb_momo", "nb_agences"]],
    left_on="prefecture_nom_bdd", right_on="prefecture", how="left")
if p != "Toutes":
    cent = cent[cent.priorite == int(p[1])]
cols = {1: "#D7263D", 2: "#B96A00", 3: "#00693E"}
for _, r in cent.iterrows():
    folium.CircleMarker([r.lat, r.lon], radius=max(6, min(18, r.nb_momo / 150)),
        color=cols[int(r.priorite)], fill=True, fill_opacity=0.45, weight=2,
        popup=f"{r.prefecture_nom_bdd} : {int(r.nb_momo)} points Mobile Money / {int(r.nb_agences)} agences").add_to(m)
st_folium(m, height=500, use_container_width=True)

st.dataframe(d[["prefecture", "region", "nb_agences", "nb_momo", "priorite"]]
    .sort_values(["priorite", "nb_momo"], ascending=[True, False]), width="stretch", hide_index=True)
st.markdown('<div class="card"><h4>Datacenters et couverture radio</h4><div>Les 3 datacenters sont localisés à Lomé : '
    "une redondance à Kara ou Sokodé est recommandée. "
    "La couverture 2G/3G/4G, non fournie dans les jeux de données, reste à valider par une campagne de mesures ARCEP.</div></div>",
    unsafe_allow_html=True)
