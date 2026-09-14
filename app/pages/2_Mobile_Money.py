import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import plotly.express as px
from utils import load_all, apply_style, kpi_row, plotly_clean

st.set_page_config(page_title="Mobile Money", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()
NB_MOMO = len(mo)
st.title("Mobile Money : le réseau de proximité")
st.caption(f"{NB_MOMO:,} points recensés - {mo.prefecture_nom_bdd.nunique()} préfectures couvertes".replace(",", " "))

mixte = int((mo.operateur_clean == "Moov, Togocom").sum())
seul_tgc = int((mo.operateur_clean == "Togocom").sum())
top_pref = ind.sort_values("nb_momo", ascending=False).iloc[0]
kpi_row(st, [(f"{mixte:,}".replace(",", " "), "Points mixtes Moov et Togocom", f"{mixte / NB_MOMO:.0%} des points", "blue"),
             (f"{seul_tgc:,}".replace(",", " "), "Points Togocom seul", f"{seul_tgc / NB_MOMO:.0%} des points", "orange"),
             (f"{int(top_pref.nb_momo):,}".replace(",", " "), f"Préfecture de {top_pref.prefecture}", "Premier territoire", "")])

c1, c2 = st.columns(2)
with c1:
    op = mo.operateur_clean.value_counts().reset_index()
    op.columns = ["operateur", "n"]
    st.plotly_chart(plotly_clean(px.pie(op, names="operateur", values="n", hole=0.55,
        color_discrete_sequence=["#00693E", "#0066B3", "#FF7900", "#B0BEC5"]), "Répartition par opérateur"), width="stretch")
with c2:
    rg = mo.groupby("region_nom_bdd").size().reset_index(name="n").sort_values("n")
    st.plotly_chart(plotly_clean(px.bar(rg, x="n", y="region_nom_bdd", orientation="h",
        color_discrete_sequence=["#00693E"]), "Points par région"), width="stretch")

top15 = ind.sort_values("nb_momo", ascending=False).head(15).sort_values("nb_momo")
st.plotly_chart(plotly_clean(px.bar(top15, x="nb_momo", y="prefecture", orientation="h",
    color_discrete_sequence=["#0066B3"]), "Quinze premières préfectures - Golfe 5 121 contre Mô 32"), width="stretch")
st.markdown('<div class="card"><h4>Analyse</h4><div>Le Mobile Money couvre les 39 préfectures, '
    "y compris les 12 territoires sans agence (Lacs : 741 points, Vo : 476). "
    "Il constitue le principal levier d'inclusion numérique.</div></div>", unsafe_allow_html=True)
