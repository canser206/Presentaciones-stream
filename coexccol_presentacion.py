"""
╔══════════════════════════════════════════════════════════════════════════════╗
║      COEXCCOL — INFORME CONTABILIDAD DE COSTOS 2026                          ║
║      Centro Costa Rica                               ║
║      Módulos: Nómina × Tonelada | Consumos | Costos vs Producción           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="COEXCCOL · Informe Contabilidad 2026",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fuente y fondo global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo de la app */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0f1722 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b27 100%);
        border-right: 1px solid #1e3a5f;
    }

    /* Tarjetas KPI */
    .kpi-card {
        background: linear-gradient(135deg, #1a2332 0%, #1e2d42 100%);
        border: 1px solid #2a4a6b;
        border-radius: 14px;
        padding: 20px 24px;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f5a623, #ff6b35);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 0.73rem;
        color: #8ba3c7;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-top: 4px;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #4ade80;
        margin-top: 6px;
        font-weight: 600;
    }
    .kpi-sub-red { color: #f87171; }
    .kpi-sub-yellow { color: #fbbf24; }

    /* Headers de sección */
    .section-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #1a2d4a 100%);
        border-left: 4px solid #f5a623;
        border-radius: 0 10px 10px 0;
        padding: 14px 20px;
        margin: 28px 0 18px 0;
    }
    .section-header h2 {
        color: #f5a623;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .section-header p {
        color: #8ba3c7;
        font-size: 0.82rem;
        margin: 4px 0 0 0;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #162032 50%, #0d1117 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 28px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #f5a623, #ff6b35, #f5a623);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: 2px;
    }
    .main-header .subtitle {
        color: #f5a623;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 6px;
    }
    .main-header .meta {
        color: #4a6fa5;
        font-size: 0.78rem;
        margin-top: 10px;
    }

    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a2332, #1e2d42);
        border: 1px solid #2a4a6b;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .insight-box.green { border-left: 4px solid #4ade80; }
    .insight-box.red   { border-left: 4px solid #f87171; }
    .insight-box.yellow{ border-left: 4px solid #fbbf24; }
    .insight-box.blue  { border-left: 4px solid #60a5fa; }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: #8ba3c7;
        font-weight: 600;
        font-size: 0.85rem;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #f5a623;
    }

    /* Plotly chart containers */
    .element-container .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Sidebar logo */
    .sidebar-logo {
        text-align: center;
        padding: 20px 16px;
        border-bottom: 1px solid #1e3a5f;
        margin-bottom: 20px;
    }
    .sidebar-logo h2 {
        color: #f5a623;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 3px;
    }
    .sidebar-logo p {
        color: #4a6fa5;
        font-size: 0.7rem;
        margin: 4px 0 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATOS — EXTRAÍDOS DE ARCHIVOS XLSX
# ─────────────────────────────────────────────────────────────────────────────

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO"]
MESES_SHORT = ["Ene", "Feb", "Mar", "Abr", "May"]

# Producción y Precios
produccion = [1150.22, 1830.15, 1898.77, 1800.91, 1964.11]
precio_vta = [290_000, 325_000, 290_000, 290_000, 290_000]
ingresos = [333_563_800, 594_798_750, 550_643_300, 522_263_900, 569_591_900]

# Costos totales y por categoría
total_costos = [484_201_441, 561_681_204, 591_548_765, 587_282_336, 539_115_150]
nomina       = [174_246_947, 198_767_663, 213_743_614, 210_197_785, 157_253_477]
carga_prest  = [70_442_617,  71_057_727,  76_527_947,  80_910_432,  81_142_044]
energia      = [29_603_230,  29_368_280,  38_315_850,  36_893_750,  31_502_690]
insumos_cst  = [23_584_638,  20_158_111,  20_658_931,  14_065_477,  19_639_124]
trans_carbon = [34_506_600,  54_904_500,  56_963_100,  54_027_300,  49_921_100]
cuota_ac     = [63_611_017,  63_611_017,  63_611_017,  63_611_017,  63_611_017]
regalias     = [13_626_958,  21_682_267,  22_495_226,  30_479_789,  33_241_894]
restaurante  = [17_914_000,  17_914_000,  21_459_750,  20_731_750,  23_087_468]
combustible  = [3_431_124,   12_535_782,  4_480_816,   4_609_346,   11_596_960]
madera       = [7_369_000,   8_182_000,   10_796_500,  10_794_500,  9_099_500]
servidumbre  = [16_850_707,  18_154_989,  18_835_699,  17_864_928,  19_483_078]
autorrenta   = [4_251_213,   6_368_922,   6_607_720,   6_267_167,   6_835_103]
otros_costos = [30_189_205,  38_856_747,  37_046_351,  47_819_625,  32_640_432]

# CF vs CV
costos_fijos     = [122_089_212, 147_495_464, 144_845_712, 140_734_212, 136_698_012]
costos_variables = [362_112_229, 414_185_741, 449_703_053, 451_548_124, 402_417_138]

# Punto de equilibrio
break_even = [-4_919, 2_316, 2_725, 3_149, 1_606]

# Costo por tonelada (total)
costo_x_ton = [tc / p for tc, p in zip(total_costos, produccion)]
ingreso_x_ton = precio_vta

# ---- NÓMINA LABOR DETAIL (RESUMEN 2026) ----
labor_data = {
    "ENERO": {
        "PICADA": 62_821_079, "BONO ALIMENTACIÓN": 34_100_750,
        "PERSONAL DE APOYO": 10_288_630, "MOV. ROCA": 11_699_399,
        "MALACATEROS": 5_432_956, "SOSTENIMIENTO": 5_045_450,
        "TURNOS": 3_831_630, "BONIFICACIÓN": 3_723_270,
        "OTROS": 117_331
    },
    "FEBRERO": {
        "PICADA": 65_801_446, "BONO ALIMENTACIÓN": 25_661_500,
        "PERSONAL DE APOYO": 13_384_885, "DOMINICALES": 13_306_878,
        "MALACATEROS": 6_392_748, "COCHES GUAYADOS": 5_939_500,
        "BONIFICACIÓN": 4_814_140, "MOV. ROCA": 4_131_000,
        "SOSTENIMIENTO": 3_170_410, "TURNOS": 3_382_000,
        "OTROS": 1_176_950
    },
    "MARZO": {
        "PICADA": 60_017_884, "ALIMENTACIÓN": 21_459_750,
        "DOMINICALES": 13_306_878, "COCHES GUAYADOS": 7_930_500,
        "METRO DE ROCA": 6_040_100, "TURNO": 4_796_050,
        "TOLVEROS": 4_672_087, "VENTANA": 4_400_000,
        "ALEMANA": 7_073_528, "MALACATEROS": 4_024_420,
        "PATIEROS": 3_641_067, "OTROS": 11_417_654
    },
    "ABRIL": {
        "PICADA": 58_199_567, "ALIMENTACIÓN": 30_371_250,
        "DOMINICALES": 12_633_452, "ALEMANA": 8_076_073,
        "COCHES GUAYADOS": 7_364_000, "TURNO": 5_741_275,
        "MALACATEROS": 5_603_350, "METRO DE ROCA": 4_674_800,
        "VENTANA": 4_550_000, "PATIEROS": 3_731_711,
        "TOLVEROS": 2_567_987, "OTROS": 9_395_140
    },
    "MAYO": {
        "PICADA": 63_934_306, "DOMINICALES": 15_000_000,
        "ALIMENTACIÓN": 15_487_750, "ALEMANA": 10_412_790,
        "COCHES GUAYADOS": 6_730_000, "MALACATEROS": 5_917_315,
        "VENTANA": 4_900_000, "PATIEROS": 3_794_196,
        "METRO DE ROCA": 2_988_300, "TOLVEROS": 2_799_334,
        "TURNO": 1_753_400, "OTROS": 4_769_830
    }
}

labor_totals = [137_060_495, 134_161_457, 148_779_918, 152_908_605, 93_487_221]
labor_x_ton  = [lt / p for lt, p in zip(labor_totals, produccion)]

# ---- CONSUMOS DETAIL ----
epp_cost  = [1_645_000, 3_818_000, 7_751_000, 7_743_200, 1_095_800]
epp_x_ton = [968.41, 2_086.17, 4_082.12, 4_299.60, 557.91]

insumos_total = [23_584_638, 20_158_111, 20_877_231, 14_315_477, 19_639_124]
insumos_x_ton = [13_884.26, 11_014.46, 10_995.13, 7_949.02, 9_998.99]

energia_kwh   = [28_260, 29_750, 37_142, 33_517, 31_155]
energia_total = [29_603_230, 29_368_280, 38_315_850, 36_893_750, 31_502_690]
energia_x_ton = [17_427.40, 16_046.93, 20_179.30, 20_486.17, 16_039.17]

combustible_total = [3_431_124, 12_535_782, 4_480_816, 4_609_346, 11_596_960]
combust_x_ton     = [2_019.90, 6_849.59, 2_359.85, 2_559.45, 5_904.44]

madera_total  = [35_216_000, 41_532_000, 44_356_000, 42_400_000, 34_996_000]
madera_x_ton  = [m/p for m,p in zip(madera_total, produccion)]

# ─────────────────────────────────────────────────────────────────────────────
# TEMA PLOTLY — PALETA OSCURA CORPORATIVA
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    "orange"  : "#f5a623",
    "amber"   : "#ff6b35",
    "blue"    : "#3b82f6",
    "teal"    : "#14b8a6",
    "green"   : "#4ade80",
    "red"     : "#f87171",
    "purple"  : "#a78bfa",
    "sky"     : "#38bdf8",
    "pink"    : "#f472b6",
    "indigo"  : "#818cf8",
    "emerald" : "#34d399",
    "yellow"  : "#fbbf24",
}

PALETTE = [COLORS["orange"], COLORS["blue"],    COLORS["teal"],    COLORS["purple"],
           COLORS["green"],  COLORS["amber"],   COLORS["sky"],     COLORS["pink"],
           COLORS["indigo"], COLORS["emerald"], COLORS["yellow"],  COLORS["red"],
           "#94a3b8"]  # 13.º — "Otros"

# ── Estilos reutilizables (sin duplicar claves en update_layout) ──
AXIS_STYLE = dict(
    showgrid=True, gridcolor="#1e293b", gridwidth=1,
    zeroline=False, color="#64748b",
    tickfont=dict(color="#94a3b8"),
)
LEGEND_STYLE = dict(
    bgcolor="rgba(15,23,42,0.8)",
    bordercolor="#1e3a5f",
    borderwidth=1,
    font=dict(size=11, color="#94a3b8"),
)
# LAYOUT_BASE solo con propiedades que nunca se repiten en los gráficos
LAYOUT_BASE = dict(
    paper_bgcolor="rgba(15,23,42,0)",
    plot_bgcolor="rgba(15,23,42,0)",
    font=dict(family="Inter", color="#cbd5e1", size=12),
)

def L(**kwargs):
    """Fusiona el estilo base con parámetros del gráfico.
    Hace deep-merge en dicts anidados (legend, xaxis, yaxis, margin)
    para evitar el TypeError 'got multiple values for keyword argument'."""
    base = {
        **LAYOUT_BASE,
        "margin" : dict(l=0, r=0, t=40, b=0),
        "xaxis"  : dict(AXIS_STYLE),
        "yaxis"  : dict(AXIS_STYLE),
        "legend" : dict(LEGEND_STYLE),
    }
    for k, v in kwargs.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            base[k] = {**base[k], **v}
        else:
            base[k] = v
    return base

def hex_to_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """Convierte color hex a rgba() válido para Plotly."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def fmt_m(val): return f"${val/1e6:.1f}M COP"
def fmt_k(val): return f"${val:,.0f} COP"
def pct_change(v1, v2): return (v2 - v1) / v1 * 100 if v1 else 0


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>⛏ COEXCCOL</h2>
        <p>Centro Costa Rica</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Navegación")
    modulo = st.radio(
        "",
        [
            "🏠 Resumen Ejecutivo",
            "👷 Nómina × Tonelada",
            "🔧 Costos de Consumos",
            "📊 Costos vs Producción",
            "🎯 Análisis de Incidencia",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🗓️ Período")
    mes_sel = st.multiselect(
        "Filtrar meses",
        MESES,
        default=MESES,
    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#4a6fa5; font-size:0.7rem; padding:10px;">
        <p style="margin:0">📁 Archivos fuente</p>
        <p style="margin:4px 0; color:#2a4a6b">Costos_nomina_Tonelada_2026</p>
        <p style="margin:4px 0; color:#2a4a6b">COSTOS_DE_CONSUMOS</p>
        <p style="margin:4px 0; color:#2a4a6b">COSTOS_VS_PRODUCCION_Real</p>
        <p style="margin:10px 0 0; color:#374151">Período: Ene–May 2026</p>
        <p style="margin:2px 0; color:#374151">Contabilidad · COEXCCOL</p>
    </div>
    """, unsafe_allow_html=True)

# Índices de meses seleccionados
idx_sel = [MESES.index(m) for m in mes_sel if m in MESES]
if not idx_sel:
    st.warning("⚠️ Selecciona al menos un mes en el panel izquierdo.")
    st.stop()

# Datos filtrados
prod_f    = [produccion[i]    for i in idx_sel]
ingr_f    = [ingresos[i]      for i in idx_sel]
tcst_f    = [total_costos[i]  for i in idx_sel]
meses_f   = [MESES[i]         for i in idx_sel]
meses_sf  = [MESES_SHORT[i]   for i in idx_sel]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>⛏ INFORME CONTABILIDAD DE COSTOS 2026</h1>
    <div class="subtitle">COMPAÑÍA EXPORTADORA DE CARBONES DE COLOMBIA SAS · COSTA RICA</div>
    <div class="meta">Enero – Mayo 2026 &nbsp;·&nbsp; Análisis Integral: Nómina · Consumos · Producción</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs GLOBALES (siempre visibles)
# ─────────────────────────────────────────────────────────────────────────────
total_prod_f   = sum(prod_f)
total_ingr_f   = sum(ingr_f)
total_tcst_f   = sum(tcst_f)
resultado_f    = total_ingr_f - total_tcst_f
cpt_prom       = total_tcst_f / total_prod_f if total_prod_f else 0
precio_prom    = total_ingr_f / total_prod_f if total_prod_f else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_prod_f:,.0f} t</div>
        <div class="kpi-label">⚖️ Producción Total</div>
        <div class="kpi-sub">Período seleccionado</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{fmt_m(total_ingr_f)}</div>
        <div class="kpi-label">💰 Ingresos Totales</div>
        <div class="kpi-sub">${precio_prom:,.0f} COP/ton promedio</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{fmt_m(total_tcst_f)}</div>
        <div class="kpi-label">🔴 Costos Totales</div>
        <div class="kpi-sub kpi-sub-{'red' if cpt_prom > precio_prom else 'yellow'}">${cpt_prom:,.0f} COP/ton</div>
    </div>""", unsafe_allow_html=True)

with c4:
    color = "red" if resultado_f < 0 else "green"
    icon  = "📉" if resultado_f < 0 else "📈"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{fmt_m(resultado_f)}</div>
        <div class="kpi-label">{icon} Resultado</div>
        <div class="kpi-sub kpi-sub-{color}">{'Déficit' if resultado_f<0 else 'Superávit'}</div>
    </div>""", unsafe_allow_html=True)

with c5:
    nom_total = sum(nomina[i]+carga_prest[i] for i in idx_sel)
    pct_nom   = nom_total / total_tcst_f * 100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{fmt_m(nom_total)}</div>
        <div class="kpi-label">👷 Nómina + Prestaciones</div>
        <div class="kpi-sub kpi-sub-yellow">{pct_nom:.1f}% del costo total</div>
    </div>""", unsafe_allow_html=True)

with c6:
    ener_total = sum(energia[i] for i in idx_sel)
    pct_ener   = ener_total / total_tcst_f * 100
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{fmt_m(ener_total)}</div>
        <div class="kpi-label">⚡ Energía Eléctrica</div>
        <div class="kpi-sub kpi-sub-blue">{pct_ener:.1f}% del costo total</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 0: RESUMEN EJECUTIVO
# ═══════════════════════════════════════════════════════════════════════════════
if modulo == "🏠 Resumen Ejecutivo":

    st.markdown('<div class="section-header"><h2>📊 Panorama General — Costos vs Producción 2026</h2><p>Visión consolidada de todos los indicadores clave de la operación</p></div>', unsafe_allow_html=True)

    # ── Gráfico 1: Ingresos vs Costos por mes ──
    col1, col2 = st.columns([3, 2])

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Ingresos",
            x=meses_sf,
            y=[ingresos[i]/1e6 for i in idx_sel],
            marker=dict(
                color=COLORS["green"],
                opacity=0.85,
                line=dict(color=COLORS["emerald"], width=1.5)
            ),
            hovertemplate="<b>%{x}</b><br>Ingresos: $%{y:.1f}M COP<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            name="Costos Totales",
            x=meses_sf,
            y=[total_costos[i]/1e6 for i in idx_sel],
            marker=dict(
                color=COLORS["red"],
                opacity=0.85,
                line=dict(color="#ef4444", width=1.5)
            ),
            hovertemplate="<b>%{x}</b><br>Costos: $%{y:.1f}M COP<extra></extra>",
        ))
        # Resultado
        resultado_mes = [(ingresos[i]-total_costos[i])/1e6 for i in idx_sel]
        colors_res = [COLORS["green"] if r >= 0 else COLORS["red"] for r in resultado_mes]
        fig.add_trace(go.Scatter(
            name="Resultado",
            x=meses_sf,
            y=resultado_mes,
            mode="lines+markers+text",
            line=dict(color=COLORS["orange"], width=2.5, dash="dot"),
            marker=dict(size=10, color=colors_res, line=dict(color="#fff", width=1.5)),
            text=[f"${r:.1f}M" for r in resultado_mes],
            textposition="top center",
            textfont=dict(size=10, color=COLORS["orange"]),
            hovertemplate="<b>%{x}</b><br>Resultado: $%{y:.1f}M COP<extra></extra>",
        ))
        fig.update_layout(**L(
            title=dict(text="<b>💰 Ingresos · Costos · Resultado Mensual</b>", font=dict(color="#f5a623", size=14)),
            barmode="group",
            height=340,
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            yaxis=dict(ticksuffix="M"),
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Donut de composición de costos
        cat_labels = ["Nómina", "Carga Prest.", "Cuota Acerías", "Trans. Carbón",
                      "Energía", "Regalías", "Restaurante", "Insumos", "Combustible", "Otros"]
        cat_vals = [
            sum(nomina[i]      for i in idx_sel),
            sum(carga_prest[i] for i in idx_sel),
            sum(cuota_ac[i]    for i in idx_sel),
            sum(trans_carbon[i]for i in idx_sel),
            sum(energia[i]     for i in idx_sel),
            sum(regalias[i]    for i in idx_sel),
            sum(restaurante[i] for i in idx_sel),
            sum(insumos_cst[i] for i in idx_sel),
            sum(combustible[i] for i in idx_sel),
            sum(otros_costos[i]for i in idx_sel),
        ]
        fig2 = go.Figure(go.Pie(
            labels=cat_labels,
            values=cat_vals,
            hole=0.55,
            marker=dict(colors=PALETTE, line=dict(color="#0a0e1a", width=2)),
            textinfo="label+percent",
            textfont=dict(size=10, color="#cbd5e1"),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
            pull=[0.04 if v == max(cat_vals) else 0 for v in cat_vals],
        ))
        fig2.add_annotation(
            text=f"<b>{fmt_m(sum(cat_vals))}</b><br><span style='font-size:10px'>Total Costos</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#f5a623", family="Inter"),
            align="center"
        )
        fig2.update_layout(**L(
            title=dict(text="<b>🥧 Composición del Costo</b>", font=dict(color="#f5a623", size=14)),
            showlegend=False,
            height=340,
            margin=dict(l=0, r=0, t=40, b=0),
        ))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico 2: Costo por Tonelada vs Precio de Venta ──
    col3, col4 = st.columns([2, 3])

    with col3:
        st.markdown("""
        <div class="section-header" style="margin-top:8px">
            <h2>🎯 Insights Ejecutivos</h2>
            <p>Hallazgos críticos del período</p>
        </div>""", unsafe_allow_html=True)

        mej_mes = MESES[idx_sel[np.argmin([costo_x_ton[i] for i in idx_sel])]]
        peo_mes = MESES[idx_sel[np.argmax([costo_x_ton[i] for i in idx_sel])]]
        max_prod_mes = MESES[idx_sel[np.argmax(prod_f)]]

        st.markdown(f"""
        <div class="insight-box green">
            ✅ <b>Mejor eficiencia:</b> {mej_mes} con el menor costo/ton del período
        </div>
        <div class="insight-box red">
            ⚠️ <b>Costos superiores a ingresos:</b> En TODOS los meses, los costos totales
            superan los ingresos. La operación require revisión de estructura de costos.
        </div>
        <div class="insight-box yellow">
            📌 <b>Nómina dominante:</b> La nómina + prestaciones representa
            <b>{sum(nomina[i]+carga_prest[i] for i in idx_sel)/sum(total_costos[i] for i in idx_sel)*100:.1f}%</b>
            del costo total, siendo el rubro más crítico a gestionar.
        </div>
        <div class="insight-box blue">
            ⚡ <b>Mayor producción:</b> {max_prod_mes} con <b>{max(prod_f):,.2f} t</b>
            es el mes más productivo — aprovechar para diluir costos fijos.
        </div>
        <div class="insight-box" style="border-left:4px solid #a78bfa">
            📈 <b>Regalías crecientes:</b> Las regalías pagadas aumentaron un
            <b>{pct_change(regalias[0], regalias[-1]):.0f}%</b> de enero a mayo,
            reflejando mayor formalización del proceso productivo.
        </div>
        """, unsafe_allow_html=True)

    with col4:
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Scatter(
            name="Costo/Ton COP",
            x=meses_sf,
            y=[costo_x_ton[i] for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["red"], width=3),
            marker=dict(size=10, color=COLORS["red"], line=dict(color="#fff", width=2)),
            fill="tozeroy",
            fillcolor="rgba(248,113,113,0.08)",
            hovertemplate="<b>%{x}</b><br>Costo/ton: $%{y:,.0f} COP<extra></extra>",
        ), secondary_y=False)
        fig3.add_trace(go.Scatter(
            name="Precio Vta/Ton COP",
            x=meses_sf,
            y=[precio_vta[i] for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["green"], width=3, dash="dash"),
            marker=dict(size=10, color=COLORS["green"], symbol="diamond", line=dict(color="#fff", width=2)),
            hovertemplate="<b>%{x}</b><br>Precio vta: $%{y:,.0f} COP<extra></extra>",
        ), secondary_y=False)
        fig3.add_trace(go.Bar(
            name="Producción (t)",
            x=meses_sf,
            y=[produccion[i] for i in idx_sel],
            marker=dict(color=COLORS["blue"], opacity=0.25),
            hovertemplate="<b>%{x}</b><br>Producción: %{y:,.2f} t<extra></extra>",
        ), secondary_y=True)

        fig3.update_layout(**L(
            title=dict(text="<b>📉 Costo/ton vs Precio Venta · Producción Mensual</b>", font=dict(color="#f5a623", size=14)),
            height=340,
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        ))
        fig3.update_yaxes(title_text="COP / Tonelada", secondary_y=False,
                          tickformat="$,.0f", title_font=dict(color="#94a3b8"),
                          showgrid=True, gridcolor="#1e293b")
        fig3.update_yaxes(title_text="Toneladas", secondary_y=True,
                          title_font=dict(color=COLORS["blue"]),
                          showgrid=False)
        st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 1: NÓMINA × TONELADA
# ═══════════════════════════════════════════════════════════════════════════════
elif modulo == "👷 Nómina × Tonelada":

    st.markdown('<div class="section-header"><h2>👷 Costos de Nómina por Tonelada Producida</h2><p>Análisis detallado por tipo de labor — Período Ene–May 2026</p></div>', unsafe_allow_html=True)

    # KPIs de nómina
    kn1, kn2, kn3, kn4 = st.columns(4)
    nom_t = [nomina[i]+carga_prest[i] for i in idx_sel]
    lt_f  = [labor_totals[i] for i in idx_sel]
    lxtn_f= [labor_x_ton[i] for i in idx_sel]

    with kn1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(sum(nom_t))}</div>
            <div class="kpi-label">💼 Nómina Total + Prestaciones</div>
        </div>""", unsafe_allow_html=True)
    with kn2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(sum(lt_f))}</div>
            <div class="kpi-label">⛏️ Costo Labor Directo</div>
        </div>""", unsafe_allow_html=True)
    with kn3:
        avg_lxtn = sum(lt_f) / sum(prod_f) if sum(prod_f) else 0
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">${avg_lxtn:,.0f} COP</div>
            <div class="kpi-label">📏 Costo Labor / Ton (prom.)</div>
        </div>""", unsafe_allow_html=True)
    with kn4:
        pct_nom2 = sum(nom_t) / sum(tcst_f) * 100 if sum(tcst_f) else 0
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{pct_nom2:.1f}%</div>
            <div class="kpi-label">📊 Incidencia en Costo Total</div>
        </div>""", unsafe_allow_html=True)

    col_n1, col_n2 = st.columns([3, 2])

    with col_n1:
        # Gráfico evolución nómina vs producción
        fig_nom = make_subplots(specs=[[{"secondary_y": True}]])
        fig_nom.add_trace(go.Bar(
            name="Nómina Base (labor)",
            x=meses_sf,
            y=[labor_totals[i]/1e6 for i in idx_sel],
            marker=dict(
                color=PALETTE[:len(idx_sel)],
                line=dict(color="#0a0e1a", width=1.5),
                opacity=0.88
            ),
            hovertemplate="<b>%{x}</b><br>Labor: $%{y:.2f}M COP<extra></extra>",
        ), secondary_y=False)
        fig_nom.add_trace(go.Bar(
            name="Carga Prestacional",
            x=meses_sf,
            y=[carga_prest[i]/1e6 for i in idx_sel],
            marker=dict(color=COLORS["indigo"], opacity=0.75),
            hovertemplate="<b>%{x}</b><br>Prest.: $%{y:.2f}M<extra></extra>",
        ), secondary_y=False)
        fig_nom.add_trace(go.Scatter(
            name="$/Tonelada (labor)",
            x=meses_sf,
            y=[labor_x_ton[i] for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["orange"], width=3),
            marker=dict(size=10, color=COLORS["orange"], line=dict(color="#fff", width=2)),
            hovertemplate="<b>%{x}</b><br>Labor/ton: $%{y:,.0f} COP<extra></extra>",
        ), secondary_y=True)

        fig_nom.update_layout(**L(
            title=dict(text="<b>Evolución de Costos de Nómina y Labor/Tonelada</b>", font=dict(color="#f5a623", size=14)),
            barmode="stack",
            height=360,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        fig_nom.update_yaxes(title_text="COP (Millones)", secondary_y=False,
                             ticksuffix="M", showgrid=True, gridcolor="#1e293b")
        fig_nom.update_yaxes(title_text="$/Tonelada", secondary_y=True,
                             tickformat="$,.0f", showgrid=False)
        st.plotly_chart(fig_nom, use_container_width=True)

    with col_n2:
        # Selector de mes para detalle de labor
        mes_detail = st.selectbox("🔍 Detalle de labor por mes:", [MESES[i] for i in idx_sel])
        ld = labor_data[mes_detail]
        sorted_ld = dict(sorted(ld.items(), key=lambda x: x[1], reverse=True))

        fig_labor = go.Figure(go.Bar(
            x=list(sorted_ld.values()),
            y=list(sorted_ld.keys()),
            orientation="h",
            marker=dict(
                color=PALETTE[:len(sorted_ld)],
                line=dict(color="#0a0e1a", width=1),
                opacity=0.88,
            ),
            text=[f"${v/1e6:.2f}M" for v in sorted_ld.values()],
            textposition="auto",
            textfont=dict(size=10, color="#fff"),
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f} COP<extra></extra>",
        ))
        fig_labor.update_layout(**L(
            title=dict(text=f"<b>📋 Desglose por Labor — {mes_detail}</b>", font=dict(color="#f5a623", size=13)),
            height=360,
            xaxis=dict(tickformat="$,.0f"),
            yaxis=dict(autorange="reversed"),
            margin=dict(l=0, r=20, t=40, b=0),
        ))
        st.plotly_chart(fig_labor, use_container_width=True)

    # Treemap de labores todos los meses
    st.markdown('<div class="section-header"><h2>🗺️ Mapa de Calor por Tipo de Labor</h2><p>Distribución acumulada del costo laboral por categoría</p></div>', unsafe_allow_html=True)

    # Consolidar labores de todos los meses seleccionados
    labor_acum = {}
    for i in idx_sel:
        mes_n = MESES[i]
        for lab, val in labor_data[mes_n].items():
            labor_acum[lab] = labor_acum.get(lab, 0) + val

    sorted_la = dict(sorted(labor_acum.items(), key=lambda x: x[1], reverse=True))

    col_tree1, col_tree2 = st.columns([3, 2])
    with col_tree1:
        fig_tree = go.Figure(go.Treemap(
            labels=list(sorted_la.keys()),
            parents=["" for _ in sorted_la],
            values=list(sorted_la.values()),
            marker=dict(
                colors=list(sorted_la.values()),
                colorscale=[[0, "#1e3a5f"], [0.5, "#f5a623"], [1, "#ff6b35"]],
                showscale=True,
                colorbar=dict(
                    title="COP",
                    tickformat="$,.0f",
                    thickness=12,
                    tickfont=dict(color="#94a3b8", size=9),
                ),
                line=dict(color="#0a0e1a", width=2),
            ),
            texttemplate="<b>%{label}</b><br>$%{value:,.0f}",
            textfont=dict(size=11, color="#fff"),
            hovertemplate="<b>%{label}</b><br>Costo: $%{value:,.0f} COP<br>%{percentRoot:.1%} del total<extra></extra>",
        ))
        fig_tree.update_layout(**L(
            title=dict(text="<b>💡 Treemap: Distribución del Costo por Labor (Período)</b>", font=dict(color="#f5a623", size=14)),
            height=380,
            margin=dict(l=0, r=0, t=40, b=0),
        ))
        st.plotly_chart(fig_tree, use_container_width=True)

    with col_tree2:
        # Radar chart de componentes por mes
        cats = ["PICADA", "ALIMENTACIÓN\n/BONO", "MOV. ROCA\n/METRO", "MALACATEROS",
                "COCHES\nGUAYADOS", "TURNOS\n/DOMINICALES"]
        mes_radar_keys = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO"]
        radar_map = {
            "PICADA":             ["PICADA"],
            "ALIMENTACIÓN\n/BONO":["BONO ALIMENTACIÓN","ALIMENTACIÓN"],
            "MOV. ROCA\n/METRO":  ["MOV. ROCA","MOVIMIENTO DE ROCA","METRO DE ROCA","MOV. ROCA"],
            "MALACATEROS":        ["MALACATEROS"],
            "COCHES\nGUAYADOS":   ["COCHES GUAYADOS"],
            "TURNOS\n/DOMINICALES":["TURNOS","DOMINICALES","TURNO"],
        }
        fig_radar = go.Figure()
        colors_r = [COLORS["orange"], COLORS["blue"], COLORS["teal"], COLORS["purple"], COLORS["green"]]
        for ii, i in enumerate(idx_sel):
            mes_n = MESES[i]
            ld2 = labor_data[mes_n]
            vals = []
            for cat, keys in radar_map.items():
                v = sum(ld2.get(k, 0) for k in keys)
                vals.append(v / 1e6)
            vals_c = vals + [vals[0]]
            cats_c = cats + [cats[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_c, theta=cats_c,
                name=mes_n[:3],
                line=dict(color=colors_r[ii % len(colors_r)], width=2),
                fill="toself",
                fillcolor=hex_to_rgba(colors_r[ii % len(colors_r)], 0.07),
                marker=dict(size=6, color=colors_r[ii % len(colors_r)]),
            ))
        fig_radar.update_layout(**L(
            title=dict(text="<b>🕸️ Radar de Labores por Mes</b>", font=dict(color="#f5a623", size=14)),
            polar=dict(
                bgcolor="rgba(15,23,42,0.5)",
                radialaxis=dict(visible=True, color="#4a6fa5", gridcolor="#1e293b",
                               ticksuffix="M", tickfont=dict(size=9)),
                angularaxis=dict(color="#64748b", gridcolor="#1e293b"),
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            height=380,
            margin=dict(l=20, r=20, t=40, b=40),
        ))
        st.plotly_chart(fig_radar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 2: COSTOS DE CONSUMOS
# ═══════════════════════════════════════════════════════════════════════════════
elif modulo == "🔧 Costos de Consumos":

    st.markdown('<div class="section-header"><h2>🔧 Análisis de Costos de Consumos</h2><p>EPP · Insumos · Energía Eléctrica · Combustible · Madera</p></div>', unsafe_allow_html=True)

    # KPIs de consumos
    kc1, kc2, kc3, kc4, kc5 = st.columns(5)
    epp_f  = sum(epp_cost[i]       for i in idx_sel)
    ins_f  = sum(insumos_total[i]  for i in idx_sel)
    ene_f  = sum(energia_total[i]  for i in idx_sel)
    comb_f = sum(combustible_total[i] for i in idx_sel)
    mad_f  = sum(madera_total[i]   for i in idx_sel)

    with kc1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(epp_f)}</div>
            <div class="kpi-label">🦺 EPP Total</div>
            <div class="kpi-sub">${sum(epp_x_ton[i] for i in idx_sel)/len(idx_sel):,.0f} COP/ton prom</div>
        </div>""", unsafe_allow_html=True)
    with kc2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(ins_f)}</div>
            <div class="kpi-label">🔩 Insumos Total</div>
            <div class="kpi-sub">${sum(insumos_x_ton[i] for i in idx_sel)/len(idx_sel):,.0f} COP/ton prom</div>
        </div>""", unsafe_allow_html=True)
    with kc3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(ene_f)}</div>
            <div class="kpi-label">⚡ Energía Total</div>
            <div class="kpi-sub">{sum(energia_kwh[i] for i in idx_sel):,} kWh</div>
        </div>""", unsafe_allow_html=True)
    with kc4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(comb_f)}</div>
            <div class="kpi-label">⛽ Combustible</div>
            <div class="kpi-sub">${sum(combust_x_ton[i] for i in idx_sel)/len(idx_sel):,.0f} COP/ton prom</div>
        </div>""", unsafe_allow_html=True)
    with kc5:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(mad_f)}</div>
            <div class="kpi-label">🪵 Madera (V. Comercial)</div>
            <div class="kpi-sub">Palancas + Tablas + Tacos</div>
        </div>""", unsafe_allow_html=True)

    # ── Costo × Tonelada de cada consumo ──
    col_c1, col_c2 = st.columns([3, 2])

    with col_c1:
        fig_c1 = go.Figure()
        consumos = {
            "EPP":         [epp_x_ton[i]       for i in idx_sel],
            "Insumos":     [insumos_x_ton[i]    for i in idx_sel],
            "Energía":     [energia_x_ton[i]    for i in idx_sel],
            "Combustible": [combust_x_ton[i]    for i in idx_sel],
            "Madera":      [madera_x_ton[i]     for i in idx_sel],
        }
        cols_c = [COLORS["amber"], COLORS["blue"], COLORS["teal"],
                  COLORS["red"],   COLORS["emerald"]]
        for ii, (name, vals) in enumerate(consumos.items()):
            fig_c1.add_trace(go.Scatter(
                name=name, x=meses_sf, y=vals,
                mode="lines+markers",
                line=dict(color=cols_c[ii], width=2.5),
                marker=dict(size=9, color=cols_c[ii], line=dict(color="#fff", width=1.5)),
                fill="tozeroy" if ii == 0 else "tonexty",
                fillcolor=hex_to_rgba(cols_c[ii], 0.06),
                hovertemplate=f"<b>%{{x}}</b><br>{name}: $%{{y:,.0f}} COP/ton<extra></extra>",
            ))
        fig_c1.update_layout(**L(
            title=dict(text="<b>📐 Costo por Tonelada — Todos los Consumos</b>", font=dict(color="#f5a623", size=14)),
            height=380,
            yaxis=dict(tickformat="$,.0f"),
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_c1, use_container_width=True)

    with col_c2:
        # Energía: kWh vs Costo
        fig_ener = make_subplots(specs=[[{"secondary_y": True}]])
        fig_ener.add_trace(go.Bar(
            name="kWh Consumidos",
            x=meses_sf,
            y=[energia_kwh[i] for i in idx_sel],
            marker=dict(color=COLORS["teal"], opacity=0.8,
                       line=dict(color="#0a0e1a", width=1)),
            hovertemplate="<b>%{x}</b><br>kWh: %{y:,}<extra></extra>",
        ), secondary_y=False)
        fig_ener.add_trace(go.Scatter(
            name="Costo Energía ($M)",
            x=meses_sf,
            y=[energia_total[i]/1e6 for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["yellow"], width=2.5),
            marker=dict(size=9, color=COLORS["yellow"], line=dict(color="#fff", width=2)),
            hovertemplate="<b>%{x}</b><br>Costo: $%{y:.2f}M<extra></extra>",
        ), secondary_y=True)
        fig_ener.update_layout(**L(
            title=dict(text="<b>⚡ Consumo Eléctrico vs Costo</b>", font=dict(color="#f5a623", size=13)),
            height=380,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        fig_ener.update_yaxes(title_text="kWh", secondary_y=False,
                              tickformat=",", showgrid=True, gridcolor="#1e293b")
        fig_ener.update_yaxes(title_text="$M COP", secondary_y=True,
                              ticksuffix="M", showgrid=False)
        st.plotly_chart(fig_ener, use_container_width=True)

    # ── Detalle de costos en barras agrupadas ──
    col_c3, col_c4 = st.columns([2, 3])

    with col_c3:
        # Madera desglose
        madera_labels  = ["Palancas", "Tablas", "Tacos/Riel"]
        madera_details = {
            "ENERO":   [21_866_000, 13_350_000, 0],
            "FEBRERO": [29_224_000, 12_260_000, 48_000],
            "MARZO":   [28_626_000, 15_730_000, 0],
            "ABRIL":   [27_170_000, 15_230_000, 0],
            "MAYO":    [22_646_000, 12_200_000, 150_000],
        }
        fig_mad = go.Figure()
        m_colors = [COLORS["emerald"], COLORS["orange"], COLORS["sky"]]
        for ii, lab in enumerate(madera_labels):
            vals = [madera_details.get(MESES[i], [0,0,0])[ii]/1e6 for i in idx_sel]
            fig_mad.add_trace(go.Bar(
                name=lab, x=meses_sf, y=vals,
                marker=dict(color=m_colors[ii], opacity=0.85),
                hovertemplate=f"<b>%{{x}}</b><br>{lab}: $%{{y:.2f}}M<extra></extra>",
            ))
        fig_mad.update_layout(**L(
            title=dict(text="<b>🪵 Consumo de Madera por Tipo</b>", font=dict(color="#f5a623", size=13)),
            barmode="stack", height=340,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_mad, use_container_width=True)

    with col_c4:
        # Heatmap de consumos por mes
        heat_data = pd.DataFrame({
            "EPP":         [epp_cost[i]/1e6        for i in idx_sel],
            "Insumos":     [insumos_total[i]/1e6   for i in idx_sel],
            "Energía":     [energia_total[i]/1e6   for i in idx_sel],
            "Combustible": [combustible_total[i]/1e6 for i in idx_sel],
            "Madera":      [madera_total[i]/1e6    for i in idx_sel],
        }, index=meses_sf)

        fig_heat = px.imshow(
            heat_data.T,
            color_continuous_scale=[[0, "#0d1117"], [0.3, "#1e3a5f"], [0.6, "#f5a623"], [1, "#ff3300"]],
            aspect="auto",
            text_auto=".1f",
        )
        fig_heat.update_traces(textfont=dict(color="#fff", size=11))
        fig_heat.update_layout(**L(
            title=dict(text="<b>🌡️ Heatmap de Consumos — $M COP por Mes</b>", font=dict(color="#f5a623", size=14)),
            height=340,
            coloraxis_colorbar=dict(
                title=dict(text="$M COP", font=dict(color="#94a3b8", size=11)),
                tickfont=dict(color="#94a3b8"),
            ),
            xaxis=dict(title=None),
            yaxis=dict(title=None),
        ))
        st.plotly_chart(fig_heat, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 3: COSTOS VS PRODUCCIÓN
# ═══════════════════════════════════════════════════════════════════════════════
elif modulo == "📊 Costos vs Producción":

    st.markdown('<div class="section-header"><h2>📊 Costos vs Producción Real — Análisis Estructural</h2><p>Estructura de costos · CF vs CV · Punto de equilibrio · Rentabilidad</p></div>', unsafe_allow_html=True)

    kp1, kp2, kp3, kp4 = st.columns(4)
    cf_f = [costos_fijos[i]     for i in idx_sel]
    cv_f = [costos_variables[i] for i in idx_sel]
    be_f = [break_even[i]       for i in idx_sel]

    with kp1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(sum(cf_f))}</div>
            <div class="kpi-label">🔒 Costos Fijos Totales</div>
            <div class="kpi-sub">{sum(cf_f)/sum(tcst_f)*100:.1f}% del costo total</div>
        </div>""", unsafe_allow_html=True)
    with kp2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{fmt_m(sum(cv_f))}</div>
            <div class="kpi-label">📈 Costos Variables Totales</div>
            <div class="kpi-sub">{sum(cv_f)/sum(tcst_f)*100:.1f}% del costo total</div>
        </div>""", unsafe_allow_html=True)
    with kp3:
        be_valid = [b for b in be_f if b > 0]
        pe_prom  = np.mean(be_valid) if be_valid else 0
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{pe_prom:,.0f} t</div>
            <div class="kpi-label">⚖️ Punto Equilibrio Prom.</div>
            <div class="kpi-sub kpi-sub-yellow">Meses con PE válido</div>
        </div>""", unsafe_allow_html=True)
    with kp4:
        margen = (sum(ingr_f) - sum(tcst_f)) / sum(ingr_f) * 100 if sum(ingr_f) else 0
        color  = "green" if margen >= 0 else "red"
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-value">{margen:.1f}%</div>
            <div class="kpi-label">📉 Margen Operacional</div>
            <div class="kpi-sub kpi-sub-{color}">{'Positivo' if margen >= 0 else 'Negativo'}</div>
        </div>""", unsafe_allow_html=True)

    # ── CF vs CV por mes ──
    col_p1, col_p2 = st.columns([3, 2])

    with col_p1:
        fig_cfcv = go.Figure()
        fig_cfcv.add_trace(go.Bar(
            name="Costos Fijos",
            x=meses_sf,
            y=[costos_fijos[i]/1e6 for i in idx_sel],
            marker=dict(
                color=COLORS["blue"],
                opacity=0.85,
                pattern=dict(shape="/", fgcolor="rgba(59,130,246,0.4)", size=6),
                line=dict(color="#0a0e1a", width=1),
            ),
            hovertemplate="<b>%{x}</b><br>CF: $%{y:.1f}M COP<extra></extra>",
        ))
        fig_cfcv.add_trace(go.Bar(
            name="Costos Variables",
            x=meses_sf,
            y=[costos_variables[i]/1e6 for i in idx_sel],
            marker=dict(
                color=COLORS["red"],
                opacity=0.85,
                line=dict(color="#0a0e1a", width=1),
            ),
            hovertemplate="<b>%{x}</b><br>CV: $%{y:.1f}M COP<extra></extra>",
        ))
        fig_cfcv.add_trace(go.Scatter(
            name="Ingresos",
            x=meses_sf,
            y=[ingresos[i]/1e6 for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["green"], width=3, dash="dash"),
            marker=dict(size=10, color=COLORS["green"], symbol="star",
                       line=dict(color="#fff", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Ingresos: $%{y:.1f}M<extra></extra>",
        ))
        fig_cfcv.update_layout(**L(
            title=dict(text="<b>🏗️ Estructura de Costos: Fijos vs Variables vs Ingresos</b>", font=dict(color="#f5a623", size=14)),
            barmode="stack",
            height=360,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
            yaxis=dict(ticksuffix="M"),
        ))
        st.plotly_chart(fig_cfcv, use_container_width=True)

    with col_p2:
        # Punto de equilibrio
        fig_be = go.Figure()
        be_colors = [COLORS["green"] if b > 0 and b <= produccion[idx_sel[ii]]
                     else COLORS["yellow"] if b > produccion[idx_sel[ii]]
                     else COLORS["red"]
                     for ii, b in enumerate(be_f)]
        fig_be.add_trace(go.Bar(
            name="Punto de Equilibrio",
            x=meses_sf,
            y=[max(b, 0) for b in be_f],
            marker=dict(color=be_colors, opacity=0.85, line=dict(color="#0a0e1a", width=1)),
            hovertemplate="<b>%{x}</b><br>PE: %{y:,.0f} tons<extra></extra>",
            text=[f"{b:,.0f} t" if b>0 else "⚠️ Sin PE" for b in be_f],
            textposition="auto",
            textfont=dict(size=10, color="#fff"),
        ))
        fig_be.add_trace(go.Scatter(
            name="Producción Real",
            x=meses_sf,
            y=[produccion[i] for i in idx_sel],
            mode="lines+markers",
            line=dict(color=COLORS["orange"], width=2.5, dash="dot"),
            marker=dict(size=10, color=COLORS["orange"], line=dict(color="#fff", width=2)),
            hovertemplate="<b>%{x}</b><br>Prod. real: %{y:,.2f} t<extra></extra>",
        ))
        fig_be.update_layout(**L(
            title=dict(text="<b>⚖️ Punto de Equilibrio vs Producción Real</b>", font=dict(color="#f5a623", size=13)),
            height=360,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_be, use_container_width=True)

    # ── Waterfall de costos por mes seleccionado ──
    st.markdown('<div class="section-header"><h2>💧 Cascada de Costos por Mes</h2><p>Composición del costo total con apertura por ítem</p></div>', unsafe_allow_html=True)

    mes_wf = st.selectbox("Seleccionar mes para cascada:", [MESES[i] for i in idx_sel], key="wf")
    i_wf   = MESES.index(mes_wf)

    items = [
        ("Nómina",       nomina[i_wf]),
        ("C. Prest.",    carga_prest[i_wf]),
        ("Cuota Acería", cuota_ac[i_wf]),
        ("Trans. Carbón",trans_carbon[i_wf]),
        ("Servidumbre",  servidumbre[i_wf]),
        ("Energía",      energia[i_wf]),
        ("Regalías",     regalias[i_wf]),
        ("Restaurante",  restaurante[i_wf]),
        ("Insumos",      insumos_cst[i_wf]),
        ("Combustible",  combustible[i_wf]),
        ("Madera",       madera[i_wf]),
        ("AutoRenta",    autorrenta[i_wf]),
        ("Otros",        otros_costos[i_wf]),
    ]
    items.sort(key=lambda x: x[1], reverse=True)

    fig_wf = go.Figure(go.Waterfall(
        name="Costos",
        orientation="v",
        measure=["relative"] * len(items) + ["total"],
        x=[it[0] for it in items] + ["TOTAL"],
        y=[it[1]/1e6 for it in items] + [0],
        text=[f"${it[1]/1e6:.1f}M" for it in items] + [f"${total_costos[i_wf]/1e6:.1f}M"],
        textposition="outside",
        textfont=dict(size=10, color="#cbd5e1"),
        connector=dict(line=dict(color="#1e3a5f", width=1, dash="dot")),
        increasing=dict(marker=dict(color=COLORS["red"], line=dict(color="#0a0e1a", width=1))),
        totals=dict(marker=dict(color=COLORS["orange"], line=dict(color="#0a0e1a", width=2))),
        hovertemplate="<b>%{x}</b><br>$%{y:.2f}M COP<extra></extra>",
    ))
    fig_wf.add_hline(
        y=ingresos[i_wf]/1e6, line_dash="dash", line_color=COLORS["green"], line_width=2,
        annotation_text=f"  Ingresos: ${ingresos[i_wf]/1e6:.1f}M",
        annotation_font=dict(color=COLORS["green"], size=12),
    )
    fig_wf.update_layout(**L(
        title=dict(text=f"<b>💧 Cascada de Costos — {mes_wf} 2026</b>", font=dict(color="#f5a623", size=14)),
        height=430,
        yaxis=dict(ticksuffix="M"),
        showlegend=False,
    ))
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── Tabla resumen ──
    st.markdown('<div class="section-header"><h2>📋 Tabla Comparativa Mensual</h2></div>', unsafe_allow_html=True)
    tabla = pd.DataFrame({
        "Mes":           [MESES[i] for i in idx_sel],
        "Producción (t)":[f"{produccion[i]:,.2f}" for i in idx_sel],
        "Precio VTA/t":  [f"${precio_vta[i]:,.0f}" for i in idx_sel],
        "Ingresos ($M)": [f"{ingresos[i]/1e6:.2f}" for i in idx_sel],
        "Costo Total ($M)":[f"{total_costos[i]/1e6:.2f}" for i in idx_sel],
        "Costo/ton":     [f"${costo_x_ton[i]:,.0f}" for i in idx_sel],
        "Resultado ($M)":[f"{(ingresos[i]-total_costos[i])/1e6:.2f}" for i in idx_sel],
        "CF ($M)":       [f"{costos_fijos[i]/1e6:.2f}" for i in idx_sel],
        "CV ($M)":       [f"{costos_variables[i]/1e6:.2f}" for i in idx_sel],
        "PE (tons)":     [f"{break_even[i]:,}" if break_even[i]>0 else "Sin PE" for i in idx_sel],
    })
    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  MÓDULO 4: ANÁLISIS DE INCIDENCIA
# ═══════════════════════════════════════════════════════════════════════════════
elif modulo == "🎯 Análisis de Incidencia":

    st.markdown('<div class="section-header"><h2>🎯 Incidencia de Costos en la Producción</h2><p>Análisis porcentual y de tendencias — cómo cada ítem impacta el costo total</p></div>', unsafe_allow_html=True)

    # ── Participación porcentual acumulada ──
    cat_names  = ["Nómina", "Carga Prest.", "Cuota Acería", "Trans. Carbón",
                  "Energía", "Regalías", "Restaurante", "Servidumbre",
                  "Insumos", "Combustible", "Madera", "AutoRenta", "Otros"]
    cat_series = [nomina, carga_prest, cuota_ac, trans_carbon, energia,
                  regalias, restaurante, servidumbre, insumos_cst,
                  combustible, madera, autorrenta, otros_costos]
    cat_colors = PALETTE

    col_inc1, col_inc2 = st.columns([3, 2])

    with col_inc1:
        # Barras 100% apiladas — incidencia relativa por mes
        fig_pct = go.Figure()
        for ii, (cat, series) in enumerate(zip(cat_names, cat_series)):
            pcts = [series[i] / total_costos[i] * 100 for i in idx_sel]
            fig_pct.add_trace(go.Bar(
                name=cat, x=meses_sf, y=pcts,
                marker=dict(color=cat_colors[ii % len(cat_colors)], opacity=0.88,
                           line=dict(color="#0a0e1a", width=0.5)),
                hovertemplate=f"<b>%{{x}}</b><br>{cat}: %{{y:.1f}}%<extra></extra>",
            ))
        fig_pct.update_layout(**L(
            title=dict(text="<b>📊 Composición % del Costo Total por Mes</b>", font=dict(color="#f5a623", size=14)),
            barmode="stack",
            height=420,
            yaxis=dict(ticksuffix="%", range=[0, 105]),
            legend=dict(
                orientation="h", y=-0.35, x=0.5, xanchor="center",
                font=dict(size=10), itemwidth=90
            )),
        )
        st.plotly_chart(fig_pct, use_container_width=True)

    with col_inc2:
        # Ordenar por incidencia acumulada
        tot_by_cat = [sum(s[i] for i in idx_sel) for s in cat_series]
        tot_total  = sum(tot_by_cat)
        pcts_tot   = [v / tot_total * 100 for v in tot_by_cat]

        sorted_pairs = sorted(zip(cat_names, pcts_tot, tot_by_cat), key=lambda x: x[1], reverse=True)
        sn, sp, sv = zip(*sorted_pairs)

        fig_rank = go.Figure()
        # Pareto
        acum = np.cumsum(sp)
        fig_rank.add_trace(go.Bar(
            name="% Incidencia",
            x=list(sn), y=list(sp),
            marker=dict(
                color=[PALETTE[i % len(PALETTE)] for i in range(len(sn))],
                opacity=0.88,
                line=dict(color="#0a0e1a", width=1),
            ),
            text=[f"{p:.1f}%" for p in sp],
            textposition="outside",
            textfont=dict(size=9, color="#94a3b8"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
        ))
        fig_rank.add_trace(go.Scatter(
            name="Acumulado",
            x=list(sn), y=list(acum),
            mode="lines+markers",
            line=dict(color=COLORS["orange"], width=2.5),
            marker=dict(size=7, color=COLORS["orange"]),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Acum: %{y:.1f}%<extra></extra>",
        ))
        fig_rank.add_hline(y=80, line_dash="dash", line_color=COLORS["yellow"],
                          annotation_text="  80% Pareto",
                          annotation_font=dict(color=COLORS["yellow"], size=10),
                          yref="y2")
        fig_rank.update_layout(**L(
            title=dict(text="<b>🏆 Diagrama de Pareto — Incidencia Acumulada</b>", font=dict(color="#f5a623", size=13)),
            height=420,
            yaxis=dict(ticksuffix="%", range=[0, max(sp)*1.2]),
            yaxis2=dict(
                overlaying="y", side="right",
                ticksuffix="%", range=[0, 120],
                showgrid=False, color="#64748b",
                tickfont=dict(color="#94a3b8"),
            ),
            xaxis=dict(tickangle=-45),
            legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_rank, use_container_width=True)

    # ── Tendencia de incidencia por ítem ──
    st.markdown('<div class="section-header"><h2>📈 Evolución de Incidencia — Ítems Críticos</h2></div>', unsafe_allow_html=True)

    cat_criticas = ["Nómina", "Carga Prest.", "Cuota Acería", "Trans. Carbón",
                    "Regalías", "Servidumbre"]
    cat_crit_series = [nomina, carga_prest, cuota_ac, trans_carbon,
                       regalias, servidumbre]

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        fig_tend = go.Figure()
        for ii, (cat, series) in enumerate(zip(cat_criticas, cat_crit_series)):
            pcts = [series[i] / total_costos[i] * 100 for i in idx_sel]
            fig_tend.add_trace(go.Scatter(
                name=cat, x=meses_sf, y=pcts,
                mode="lines+markers",
                line=dict(color=cat_colors[ii], width=2.5),
                marker=dict(size=8, color=cat_colors[ii], line=dict(color="#fff", width=1.5)),
                hovertemplate=f"<b>%{{x}}</b><br>{cat}: %{{y:.1f}}%<extra></extra>",
            ))
        fig_tend.update_layout(**L(
            title=dict(text="<b>Tendencia % de Ítems Críticos vs Costo Total</b>", font=dict(color="#f5a623", size=14)),
            height=360,
            yaxis=dict(ticksuffix="%"),
            legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
        ))
        st.plotly_chart(fig_tend, use_container_width=True)

    with col_t2:
        # Burbuja: Producción vs Costo/ton vs Total Costo
        fig_bub = go.Figure()
        for ii, i in enumerate(idx_sel):
            fig_bub.add_trace(go.Scatter(
                name=MESES[i],
                x=[produccion[i]],
                y=[costo_x_ton[i]],
                mode="markers+text",
                marker=dict(
                    size=[total_costos[i] / 4_000_000],
                    color=cat_colors[ii],
                    opacity=0.85,
                    line=dict(color="#fff", width=2),
                ),
                text=[MESES[i][:3]],
                textfont=dict(size=11, color="#fff"),
                textposition="middle center",
                hovertemplate=(
                    f"<b>{MESES[i]}</b><br>"
                    f"Producción: %{{x:,.2f}} t<br>"
                    f"Costo/ton: $%{{y:,.0f}} COP<br>"
                    f"Total costo: ${total_costos[i]/1e6:.1f}M COP<extra></extra>"
                ),
            ))
        fig_bub.add_hline(
            y=np.mean([precio_vta[i] for i in idx_sel]),
            line_dash="dash", line_color=COLORS["green"], line_width=2,
            annotation_text="  Precio VTA prom.",
            annotation_font=dict(color=COLORS["green"], size=11),
        )
        fig_bub.update_layout(**L(
            title=dict(text="<b>🔵 Burbuja: Producción × Costo/ton × Volumen</b>", font=dict(color="#f5a623", size=14)),
            height=360,
            xaxis=dict(title="Producción (tons)"),
            yaxis=dict(title="Costo/ton (COP)", tickformat="$,.0f"),
            showlegend=False,
        ))
        st.plotly_chart(fig_bub, use_container_width=True)

    # ── Tabla de incidencia ──
    st.markdown('<div class="section-header"><h2>📋 Incidencia por Ítem — Tabla Completa</h2></div>', unsafe_allow_html=True)
    # Tabla dinámica: columnas = meses seleccionados
    mes_cols_inc = {
        MESES_SHORT[i]: [f"{cat_series[ii][i]/1e6:.2f}" for ii in range(len(cat_names))]
        for i in idx_sel
    }
    grand_total_cat = sum(
        sum(cat_series[ii][i] for i in idx_sel)
        for ii in range(len(cat_names))
    ) or 1
    tab_inc_data = {"Ítem de Costo": cat_names}
    tab_inc_data.update(mes_cols_inc)
    tab_inc_data["Total (M COP)"] = [
        f"{sum(cat_series[ii][i] for i in idx_sel)/1e6:.2f}"
        for ii in range(len(cat_names))
    ]
    tab_inc_data["% Total"] = [
        f"{sum(cat_series[ii][i] for i in idx_sel)/grand_total_cat*100:.2f}%"
        for ii in range(len(cat_names))
    ]
    tab_inc = pd.DataFrame(tab_inc_data)
    st.dataframe(tab_inc, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#374151; font-size:0.72rem; padding:16px 0;">
    <p style="margin:0; color:#4a6fa5; font-weight:700; font-size:0.85rem; letter-spacing:2px">
        ⛏ COMPAÑÍA EXPORTADORA DE CARBONES DE COLOMBIA S.A.S · COEXCCOL
    </p>
    <p style="margin:4px 0">
        Centro Costa Rica · Informe Contabilidad 2026
    </p>
    <p style="margin:4px 0; color:#2a4a6b">
        Fuentes: Costos Nómina/Tonelada · Costos de Consumos · Costos vs Producción Real
    </p>
    <p style="margin:4px 0">
        Contabilidad · Elaborado con datos: Ene–May 2026
    </p>
</div>
""", unsafe_allow_html=True)
