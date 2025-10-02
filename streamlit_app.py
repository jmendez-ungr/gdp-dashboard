# app_streamlit_ugr_notas_if.py
# -------------------------------------------------------------
# Streamlit (sin ML): Predicción simple de nota (0-10)
# Variables:
#   - Total de clases (FIJO = 16)
#   - Cantidad de tests completos (0 a 5)
#   - Clases asistidas (0 a 16)
#   - Participación (Nula, Media, Alta, Muy alta)
# Lógica interna con reglas IF (NO se muestran en UI).
# Autor: ChatGPT para Joa — 2025
# -------------------------------------------------------------

import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="UGR • Predicción de Nota (Validación)",
    page_icon="🎓",
    layout="wide",
)

# ---------------- ESTILO ----------------
st.markdown("""
<style>
  .metric-card {
    border-radius: 16px; padding: 18px 22px;
    border: 1px solid rgba(120,120,120,0.15);
    box-shadow: 0 2px 10px rgba(30,30,30,0.05);
    background: #ffffff;
  }
  .pill { display:inline-block; padding:4px 10px; border-radius:999px;
          border:1px solid rgba(120,120,120,0.25); font-size:.9rem; margin-left:8px; }
  .good { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
  .warn { background:#FEF3C7; color:#92400E; border-color:#FDE68A; }
  .bad  { background:#FEE2E2; color:#991B1B; border-color:#FCA5A5; }
  .big-number { font-size: 3rem; font-weight: 800; line-height: 1; }
  .muted { color:#6B7280; }
  .section { margin-top: .5rem; }
  h1, h2, h3 { letter-spacing: -0.02em; }
  .kpi { font-size: .95rem; color:#374151; }
  .stProgress > div > div > div { background-color: #10B981; }
</style>
""", unsafe_allow_html=True)

# ---------------- ENCABEZADO ----------------
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown("## 🎓 Predicción de Nota — UGR (Validación)")
    st.markdown("<span class='muted'>Proyecto demostrativo: asistencia + participación + tests → nota (0–10)</span>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='pill muted'>Streamlit • Reglas internas • Demo académica</div>", unsafe_allow_html=True)

st.divider()

# ---------------- CONTEXTO (modo proyecto de ciencia de datos) ----------------
st.markdown("### 🧭 Introducción (formato proyecto)")
col_l, col_r = st.columns([1.6, 1.1])

with col_l:
    st.markdown("**Objetivo de investigación**")
    st.write(
        "- Estimar de manera rápida una **nota final (0–10)** usando señales simples del cursado.\n"
        "- Proveer una **validación operativa** para simulaciones y seguimiento académico."
    )

    st.markdown("**Origen de la fuente de datos**")
    st.write(
        "- Parámetros declarados por cátedra/gestión académica.\n"
        "- Sin datos sensibles de estudiantes; este demo no usa históricos reales.\n"
        "- El total de clases se fija en **16** por cohorte estándar."
    )

    st.markdown("**Desarrollo del modelo**")
    st.write(
        "- En esta fase usamos una **heurística determinística** (reglas internas) para validar criterios.\n"
        "- La lógica combina **asistencia (sobre 16 clases)**, **participación** y **tests completos (0–5)**.\n"
        "- En producción podría reemplazarse por un **modelo estadístico/ML** con datos reales."
    )

with col_r:
    st.markdown("**Consideraciones**")
    st.write(
        "- El resultado es **orientativo** para decisiones operativas.\n"
        "- Se prioriza la **interpretabilidad** y la **simplicidad**.\n"
        "- La UI busca uso docente y comunicación con dirección."
    )
    st.markdown("**Alcance de esta app**")
    st.write(
        "- Brinda un **interactivo** para experimentar escenarios.\n"
        "- No persiste datos ni identifica alumnos."
    )

st.divider()

# ---------------- INTERACTIVO ----------------
st.markdown("### ⚙️ Interactivo")
TOTAL_CLASES = 16  # Fijo

ci1, ci2, ci3, ci4 = st.columns([1, 1, 1, 1])
with ci1:
    st.metric("Total de clases (fijo)", TOTAL_CLASES)
with ci2:
    tests_completos = st.slider("Cantidad de tests completos (0–5)", min_value=0, max_value=5, value=3, step=1)
with ci3:
    asistidas = st.slider("Clases asistidas por el alumno (0–16)", min_value=0, max_value=TOTAL_CLASES, value=12, step=1)
with ci4:
    participacion = st.selectbox("Participación", ["Nula", "Media", "Alta", "Muy alta"], index=1)

asistencia_rate = asistidas / TOTAL_CLASES if TOTAL_CLASES > 0 else 0.0
st.caption(f"📝 Asistencia efectiva: {asistidas}/{TOTAL_CLASES} · {asistencia_rate:.1%} — Tests completos: {tests_completos}/5 — Participación: {participacion}")

st.divider()

# ---------------- LÓGICA INTERNA (NO VISIBLE) ----------------
# Base por asistencia
if asistencia_rate >= 0.9:
    base = 8.5
elif asistencia_rate >= 0.8:
    base = 7.5
elif asistencia_rate >= 0.7:
    base = 6.5
elif asistencia_rate >= 0.6:
    base = 5.5
elif asistencia_rate >= 0.5:
    base = 4.5
else:
    base = 3.5

# Bonus por participación
if participacion == "Muy alta":
    bonus_part = 1.5
elif participacion == "Alta":
    bonus_part = 1.0
elif participacion == "Media":
    bonus_part = 0.5
else:
    bonus_part = 0.0

# Bonus por tests completos (lineal simple 0..1.5)
bonus_tests = tests_completos * 0.3  # 5 tests -> +1.5

nota_pred = max(0.0, min(10.0, base + bonus_part + bonus_tests))

# ---------------- SALIDA ----------------
col_pred, col_info = st.columns([1.3, 1])

with col_pred:
    st.subheader("Predicción de nota")
    st.markdown(f"<div class='big-number'>{nota_pred:.1f}</div>", unsafe_allow_html=True)

    if nota_pred >= 6.0:
        cls, txt = "good", "APROBADO"
    elif nota_pred >= 5.0:
        cls, txt = "warn", "LÍMITE (recuperatorio/ajustes)"
    else:
        cls, txt = "bad", "DESAPROBADO"

    st.markdown(f"<div class='pill {cls}'>{txt}</div>", unsafe_allow_html=True)
    st.progress(min(1.0, nota_pred/10.0))

with col_info:
    st.subheader("Lectura rápida")
    if asistencia_rate >= 0.85:
        st.markdown("• ✅ **Asistencia alta**: buen soporte para la calificación final.")
    elif asistencia_rate >= 0.65:
        st.markdown("• ⚠️ **Asistencia media**: conviene sostener o mejorar presencia.")
    else:
        st.markdown("• ❌ **Asistencia baja**: principal factor de riesgo.")

    if participacion in ["Alta", "Muy alta"]:
        st.markdown("• ✅ **Participación elevada**: contribuye positivamente al resultado.")
    elif participacion == "Media":
        st.markdown("• ⚠️ **Participación media**: hay margen para sumar.")
    else:
        st.markdown("• ❌ **Participación nula**: no aporta al desempeño.")

    if tests_completos >= 4:
        st.markdown("• ✅ **Tests casi completos**: refuerzan el aprendizaje.")
    elif tests_completos >= 2:
        st.markdown("• ⚠️ **Tests parciales**: completar evaluaciones podría elevar la nota.")
    else:
        st.markdown("• ❌ **Tests escasos**: completar instancias mejora la proyección.")


# ---------------- ----- GRAFICO ----- ----------------
st.markdown("### 📈 ----- GRAFICO -----")

import numpy as np
import pandas as pd

# (1) Distribución de notas simuladas vs. media y tu valor (sin plotly)
rng = np.random.default_rng(7)
muestras = 400

# Simulamos alrededor de los valores actuales
asis_sim = np.clip(asistidas + rng.integers(-4, 5, size=muestras), 0, TOTAL_CLASES)
rate_sim = asis_sim / TOTAL_CLASES
tests_sim = np.clip(tests_completos + rng.integers(-2, 3, size=muestras), 0, 5)
niveles = ["Nula", "Media", "Alta", "Muy alta"]
p_idx = niveles.index(participacion)
choices = [niveles[np.clip(p_idx + d, 0, len(niveles)-1)] for d in rng.integers(-1, 2, size=muestras)]

def predecir_nota(asistencia_rate: float, participacion: str, tests: int) -> float:
    if asistencia_rate >= 0.9:   base = 8.5
    elif asistencia_rate >= 0.8: base = 7.5
    elif asistencia_rate >= 0.7: base = 6.5
    elif asistencia_rate >= 0.6: base = 5.5
    elif asistencia_rate >= 0.5: base = 4.5
    else:                        base = 3.5

    if participacion == "Muy alta":   bonus_part = 1.5
    elif participacion == "Alta":     bonus_part = 1.0
    elif participacion == "Media":    bonus_part = 0.5
    else:                             bonus_part = 0.0

    bonus_tests = tests * 0.3
    return float(max(0.0, min(10.0, base + bonus_part + bonus_tests)))

notas_sim = np.array([predecir_nota(rate_sim[i], choices[i], int(tests_sim[i])) for i in range(muestras)])
media = float(notas_sim.mean())

# Histograma con numpy + st.bar_chart
bins = np.linspace(0, 10, 21)  # 20 bins
counts, edges = np.histogram(notas_sim, bins=bins)
mids = 0.5 * (edges[:-1] + edges[1:])

df_hist = pd.DataFrame({"Nota": mids, "Frecuencia": counts}).set_index("Nota")
st.subheader("Distribución de notas simuladas")
st.bar_chart(df_hist)  # Streamlit interno, sin dependencias

# Mostramos media y tu nota como métricas debajo del histograma
mcol1, mcol2 = st.columns(2)
with mcol1:
    st.metric("Media simulada", f"{media:.1f}")
with mcol2:
    st.metric("Tu nota", f"{nota_pred:.1f}")

st.divider()

# (2) Barras de escenarios (¿qué pasaría si...?) sin plotly
escenarios = [
    ("Actual", nota_pred),
    ("Completa 5 tests", predecir_nota(asistencia_rate, participacion, 5)),
    ("Asistencia ≥80%", predecir_nota(max(asistidas, 13)/TOTAL_CLASES, participacion, tests_completos)),
    (f"Participación → {niveles[min(p_idx+1, len(niveles)-1)]}",
     predecir_nota(asistencia_rate, niveles[min(p_idx+1, len(niveles)-1)], tests_completos)),
]
df_esc = pd.DataFrame(escenarios, columns=["Escenario", "Nota"]).set_index("Escenario")

st.subheader("Comparativa de escenarios (¿qué pasaría si...?)")
st.bar_chart(df_esc)  # Streamlit interno

