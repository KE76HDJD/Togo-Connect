import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import plotly.express as px
from utils import load_all, apply_style, kpi_row, plotly_clean

st.set_page_config(page_title="Adéquation", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()
st.title("Adéquation entre agences et Mobile Money")
st.caption("Indicateur de substitution sans population RGPH : points Mobile Money par agence")

kpi_row(st, [("220/1", "Ratio national", "Points par agence", "blue"),
             ("741/0", "Préfecture des Lacs", "Aucune agence", "red"),
             ("476/0", "Préfecture de Vo", "Aucune agence", "red")])

st.plotly_chart(plotly_clean(px.scatter(ind, x="nb_agences", y="nb_momo", color="region",
    size="nb_momo", hover_name="prefecture",
    color_discrete_sequence=px.colors.qualitative.Set2),
    "Chaque point représente une préfecture (en haut à gauche : tension maximale)"), width="stretch")
st.dataframe(ind[["prefecture", "region", "nb_agences", "nb_momo", "momo_par_agence", "priorite"]]
    .sort_values("momo_par_agence", ascending=False).head(15), width="stretch", hide_index=True)
st.caption("Lecture : les préfectures sans agence mais à forte densité Mobile Money sont les candidates naturelles à un relais de services.")
