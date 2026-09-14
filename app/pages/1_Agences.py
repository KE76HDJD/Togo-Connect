import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import plotly.express as px
from streamlit_folium import st_folium
import folium
from utils import load_all, COULEURS, TUILES, apply_style, kpi_row, plotly_clean

st.set_page_config(page_title="Agences", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()
NB_MOOV, NB_TOGOCOM = sum(ag.operateur == "Moov"), sum(ag.operateur == "Togocom")
st.title("Agences des opérateurs")
st.caption(f"Moov : {NB_MOOV} - Togocom : {NB_TOGOCOM} - Total : {len(ag)} (fichier Télécom = union dédupliquée)")

kpi_row(st, [(str((ag.operateur == "Moov").sum()), "Agences Moov", "15 préfectures couvertes", "orange"),
             (str((ag.operateur == "Togocom").sum()), "Agences Togocom", "27 préfectures couvertes", "blue"),
             ("51/90", "En région Maritime", "Soit 57 % des agences", "red")])

f = st.multiselect("Opérateur", ["Moov", "Togocom"], default=["Moov", "Togocom"])
d = ag[ag.operateur.isin(f)]

c1, c2 = st.columns([1.25, 1])
with c1:
    m = folium.Map(location=[8.6, 1.0], zoom_start=7, tiles=TUILES)
    for _, r in d.iterrows():
        folium.CircleMarker([r.lat, r.lon], radius=6, color=COULEURS[r.operateur],
            fill=True, fill_opacity=0.85, weight=2,
            popup=f"{r.etab_nom} ({r.operateur}) - {r.prefecture_nom_bdd}").add_to(m)
    for _, r in dc.iterrows():
        folium.Marker([r.lat, r.lon], icon=folium.Icon(color="green", icon="server", prefix="fa"),
            popup=f"Datacenter : {r.etab_nom}").add_to(m)
    st_folium(m, height=500, use_container_width=True)
with c2:
    by_reg = d.groupby("region_nom_bdd").size().reset_index(name="n").sort_values("n")
    st.plotly_chart(plotly_clean(px.bar(by_reg, x="n", y="region_nom_bdd", orientation="h",
        color_discrete_sequence=["#00693E"]), "Agences par région"), width="stretch")
    by_pref = d.groupby("prefecture_nom_bdd").size().reset_index(name="n").sort_values("n", ascending=False).head(10)
    st.plotly_chart(plotly_clean(px.bar(by_pref, x="n", y="prefecture_nom_bdd", orientation="h",
        color_discrete_sequence=["#0066B3"]), "Dix premières préfectures"), width="stretch")

st.markdown('<div class="card"><h4>Analyse</h4><div>La région Maritime concentre 51 agences contre 6 en région des Savanes. '
    "Togocom assure le maillage de l'intérieur du pays tandis que le réseau Moov reste davantage urbain. "
    "Le fichier CANAL+ étant vide, ce segment reste à documenter.</div></div>", unsafe_allow_html=True)
