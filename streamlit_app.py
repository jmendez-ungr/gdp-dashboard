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

