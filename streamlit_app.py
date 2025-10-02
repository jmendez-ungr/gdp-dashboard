# app_streamlit_ugr_notas_if.py
# -------------------------------------------------------------
# Streamlit demo (sin ML): Predicción simple de nota (0-10)
# basado en asistencia y participación con reglas IF.
# Autor: ChatGPT para Joa — 2025
# -------------------------------------------------------------

import streamlit as st

# ---------- CONFIG ----------
st.set_page_config(
    page_title="UGR • Predicción de Nota (Reglas IF)",
    page_icon="🎓",
    layout="wide",
)

# ---------- ESTILO SENCILLO ----------
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
</style>
""", unsafe_allow_html=True)

# ---------- ENCABEZADO ----------
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown("## 🎓 Predicción de Nota — UGR (Reglas IF)")
    st.markdown("<span class='muted'>Validación simple: asistencia + participación → nota (0–10)</span>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='pill muted'>Streamlit • Reglas IF • Demo didáctico</div>", unsafe_allow_html=True)

st.divider()

# ---------- ENTRADAS ----------
st.markdown("### Ingresá las variables")
col_a, col_b, col_c = st.columns([1.2, 1.2, 1])

with col_a:
    total = st.slider("Total de clases del curso", min_value=10, max_value=40, value=30, step=1)
with col_b:
    asistidas = st.slider("Clases asistidas por el alumno", min_value=0, max_value=40, value=24, step=1)
    if asistidas > total:
        st.warning("Las clases asistidas no pueden superar el total. Ajustando al máximo permitido.")
        asistidas = total
with col_c:
    participacion = st.selectbox("Participación", ["Nula", "Media", "Alta", "Muy alta"], index=1)

asistencia_rate = asistidas / total if total > 0 else 0.0
st.markdown(f"**Asistencia efectiva:** {asistidas}/{total} → {asistencia_rate:.1%}")

st.divider()

# ---------- LÓGICA DE NEGOCIO (IFs) ----------
# Regla base por asistencia
# (Podés ajustar estos tramos y puntajes fácilmente)
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

# Ajuste por participación
if participacion == "Muy alta":
    bonus = 1.5
elif participacion == "Alta":
    bonus = 1.0
elif participacion == "Media":
    bonus = 0.5
else:  # Nula
    bonus = 0.0

nota_predicha = max(0.0, min(10.0, base + bonus))

# ---------- SALIDA ----------
m1, m2 = st.columns([1.3, 1])
with m1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("#### Predicción de nota")
    st.markdown(f"<div class='big-number'>{nota_predicha:.1f}</div>", unsafe_allow_html=True)

    if nota_predicha >= 6.0:
        status_class, status_txt = "good", "APROBADO"
    elif nota_predicha >= 5.0:
        status_class, status_txt = "warn", "LÍMITE (recuperatorio/ajustes)"
    else:
        status_class, status_txt = "bad", "DESAPROBADO"
    st.markdown(f"<div class='pill {status_class}'>{status_txt}</div>", unsafe_allow_html=True)

    st.progress(min(1.0, nota_predicha/10.0))
    st.markdown("</div>", unsafe_allow_html=True)

with m2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("#### Señales (reglas aplicadas)")
    # Feedback por asistencia
    if asistencia_rate >= 0.85:
        st.markdown("• ✅ **Asistencia alta**: base de nota favorable.")
    elif asistencia_rate >= 0.65:
        st.markdown("• ⚠️ **Asistencia media**: impacto moderado en la base.")
    else:
        st.markdown("• ❌ **Asistencia baja**: principal riesgo para aprobar.")
    # Feedback por participación
    if participacion in ["Alta", "Muy alta"]:
        st.markdown("• ✅ **Participación elevada**: suma puntos significativos.")
    elif participacion == "Media":
        st.markdown("• ⚠️ **Participación media**: mejora leve; hay margen.")
    else:
        st.markdown("• ❌ **Participación nula**: no agrega al puntaje.")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------- DETALLE DE LAS REGLAS ----------
with st.expander("🔎 Ver detalle de reglas IF"):
    st.write("""
**Asistencia → base de nota**
- ≥ 90% → 8.5
- 80–89% → 7.5
- 70–79% → 6.5
- 60–69% → 5.5
- 50–59% → 4.5
- < 50%   → 3.5

**Participación → bonus**
- Muy alta → +1.5
- Alta     → +1.0
- Media    → +0.5
- Nula     → +0.0

**Nota final:** `nota = clamp(base + bonus, 0, 10)`  
*(Clamp = acotar entre 0 y 10)*
    """)

# ---------- FOOTER ----------
st.caption("⚠️ Demo educativa: reglas simples para validación rápida. Ajustá tramos/bonos según tu rúbrica.")

