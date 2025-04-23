
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparativa de Ventas por Familia", layout="centered")

st.title("📊 Comparativa de Ventas por Familia (2024 vs 2025)")

df = pd.read_excel("ventas_familias_app/App ventas secciones.xlsx")

# Asegurarse que todos los nombres de columnas estén bien formateados
df.columns = df.columns.str.strip()

familias = df["Familia"].tolist()
selector_familias = st.multiselect("Selecciona una o varias familias", familias, default=[])

if selector_familias:
    df_filtrado = df[df["Familia"].isin(selector_familias)]

    # Gráfico 1 - Evolución mensual
    st.subheader("📈 Evolución mensual de ventas por familia")

    columnas_mensuales = ["ENERO 2024", "ENERO 2025", "FEBRERO 2024", "FEBRERO 2025",
                          "MARZO 2024", "MARZO 2025", "ABRIL 2024", "ABRIL 2025"]
    df_mensual = df_filtrado[["Familia"] + columnas_mensuales].set_index("Familia").T

    fig, ax = plt.subplots()
    df_mensual.plot(ax=ax, marker="o")
    ax.set_ylabel("€")
    ax.set_title("Evolución mensual de ventas")
    ax.legend(title="Familia")
    st.pyplot(fig)

    # Gráfico 2 - Comparativa total
    st.subheader("📊 Total de ventas por familia (2024 vs 2025)")
    df_totales = df_filtrado[["Familia", "TOTAL 2024", "TOTAL 2025"]].set_index("Familia")

    fig2, ax2 = plt.subplots()
    df_totales.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("€")
    ax2.set_title("Total de ventas por familia (2024 vs 2025)")
    ax2.bar_label(ax2.containers[0], fmt="%.0f", padding=3)
    ax2.bar_label(ax2.containers[1], fmt="%.0f", padding=3)
    st.pyplot(fig2)
else:
    st.info("Selecciona al menos una familia para visualizar los gráficos.")
