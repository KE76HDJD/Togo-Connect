"""Utils partagés dashboard."""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(BASE, "data", "processed")

COULEURS = {"Moov": "#FF7900", "Togocom": "#0066B3", "Datacenter": "#0B7A55", "MoMo": "#7B2CBF"}
TUILES = "CartoDB positron"

def apply_style(st):
    css = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    if os.path.exists(css):
        st.markdown(f"<style>{open(css, encoding='utf-8').read()}</style>", unsafe_allow_html=True)

def kpi_row(st, items):
    html = '<div class="kpi-row">' + "".join(
        f'<div class="kpi {c}"><div class="v">{v}</div><div class="l">{l}</div><div class="s">{s}</div></div>'
        for v, l, s, c in items) + "</div>"
    st.markdown(html, unsafe_allow_html=True)

def badge(txt, cls="info"):
    return f'<span class="badge {cls}">{txt}</span>'

def plotly_clean(fig, title=""):
    fig.update_layout(title=title, paper_bgcolor="white", plot_bgcolor="white",
        font=dict(color="#0B2C4D"), margin=dict(l=10, r=10, t=50, b=10))
    return fig

def _read(name):
    pq = os.path.join(PROC, name + ".parquet")
    cs = os.path.join(PROC, name + ".csv")
    if os.path.exists(pq):
        return pd.read_parquet(pq)
    if os.path.exists(cs):
        return pd.read_csv(cs)
    raise RuntimeError(f"Fichier introuvable : {pq} (ni {cs}). Relancez clean.py depuis {BASE}.")

def load_all():
    ag = _read("agences_clean")
    mo = _read("momo_clean")
    dc = _read("datacenters_clean")
    ind = pd.read_csv(os.path.join(PROC, "indicateurs_prefecture.csv"))
    return ag, mo, dc, ind
