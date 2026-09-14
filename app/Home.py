"""Accueil - Diagnostic territorial de la connectivité au Togo."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from utils import load_all, apply_style, kpi_row

st.set_page_config(page_title="Togo - Diagnostic de la connectivité", layout="wide")
apply_style(st)
ag, mo, dc, ind = load_all()

# Indicateurs calcules (jamais de chiffres en dur)
NB_AG, NB_MOMO, NB_DC = len(ag), len(mo), len(dc)
NB_P1 = int((ind.nb_agences == 0).sum())
NB_PREF = len(ind)
PART_MARITIME = (ag.region_nom_bdd == "Maritime").sum() / NB_AG * 100
RATIO_MOMO = NB_MOMO / NB_AG

st.title("Togo - Diagnostic territorial de la connectivité et des services numériques")
st.caption("Préparé par ANKOU Yaokouma Kevin - Données ouvertes geodata.gouv.tg - Échelle Région / Préfecture")

kpi_row(st, [
    (f"{NB_AG}", "Agences recensées", f"Moov {sum(ag.operateur=='Moov')} - Togocom {sum(ag.operateur=='Togocom')}", "blue"),
    (f"{NB_MOMO:,}".replace(",", " "), "Points Mobile Money", f"{NB_PREF} préfectures couvertes", "orange"),
    (f"{NB_DC}", "Datacenters", "Localisés à Lomé (Golfe)", ""),
    (f"{NB_P1}/{NB_PREF}", "Préfectures sans agence", "Zones blanches relatives", "red"),
])

NB_MOMO_TXT = f"{NB_MOMO:,}".replace(",", " ")
st.markdown('<div class="card"><h4>Synthèse exécutive</h4>'
    f"<div>L'offre physique reste concentrée : {PART_MARITIME:.0f} % des agences se situent en région Maritime "
    f"et les {NB_DC} datacenters recensés sont localisés à Lomé (Golfe). "
    f"Avec {NB_MOMO_TXT} points Mobile Money répartis sur {NB_PREF} préfectures "
    f"(ratio de {RATIO_MOMO:.0f} points pour une agence), "
    "le Mobile Money constitue le maillage de proximité le plus structurant. "
    f"{NB_P1} préfectures ne disposent d'aucune agence et requièrent une intervention prioritaire.</div></div>",
    unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Préfectures prioritaires (P1)")
    p1 = (ind[ind.priorite == 1].sort_values("nb_momo", ascending=False).head(5)
          [["prefecture", "region", "nb_agences", "nb_momo", "priorite"]])
    st.dataframe(p1, width="stretch", hide_index=True)
    st.caption("Classées par nombre de points Mobile Money sans relais d'agence.")
with c2:
    st.subheader("Sommaire")
    st.markdown("- **Agences** : couverture par opérateur et par territoire\n"
                "- **Mobile Money** : densité et répartition des opérateurs\n"
                "- **Adéquation** : points Mobile Money par agence et par préfecture\n"
                "- **Zones blanches** : priorisation P1, P2, P3\n"
                "- **Recommandations** : quatre actions opérationnelles")
st.caption("Limites méthodologiques : fichier CANAL+ vide, population RGPH et tracé des antennes BTS non fournis. "
           "Indicateurs relatifs uniquement. Fichier Télécom = union dédupliquée Moov et Togocom.")
st.divider()
st.caption("ANKOU Yaokouma Kevin - Défi 1 Économie Numérique Togo")
