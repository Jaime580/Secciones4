
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración general de la app
st.set_page_config(page_title="Ventas por Familia", layout="centered")

st.title("📈 Comparativa de Ventas por Familia (2024 vs 2025)")

# Cargar los datos
df = pd.read_excel("Datos.xlsx")

# Selector de familia
familias = df["Familia"].unique().tolist()
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

# Gráfico de líneas - evolución mensual
st.subheader("📉 Evolución mensual de ventas por familia")
columnas_mensuales = [col for col in df.columns if "TOTAL" not in col and col != "Familia"]

fig, ax = plt.subplots()
for familia in familias_seleccionadas:
    datos = df[df["Familia"] == familia][columnas_mensuales].values.flatten()
    ax.plot(columnas_mensuales, datos, label=f"{familia}")

ax.legend()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.set_ylabel("€")
ax.tick_params(axis="y", labelleft=False)
st.pyplot(fig)

# Gráfico de barras - totales
st.subheader("📊 Total de ventas por familia")
columnas_totales = ["TOTAL 2024", "TOTAL 2025"]
df_totales = df[df["Familia"].isin(familias_seleccionadas)][["Familia"] + columnas_totales]

fig_bar, ax_bar = plt.subplots()
bar_width = 0.35
x = range(len(df_totales))
ax_bar.bar(x, df_totales["TOTAL 2024"], width=bar_width, label="Total 2024")
ax_bar.bar([i + bar_width for i in x], df_totales["TOTAL 2025"], width=bar_width, label="Total 2025")
ax_bar.set_xticks([i + bar_width/2 for i in x])
ax_bar.set_xticklabels(df_totales["Familia"], rotation=0)
ax_bar.legend()
ax_bar.spines["right"].set_visible(False)
ax_bar.spines["top"].set_visible(False)
ax_bar.tick_params(axis="y", labelleft=False)
for i, valor in enumerate(df_totales["TOTAL 2024"]):
    ax_bar.text(i, valor + 500, f"{valor:,.0f} €", ha='center', fontsize=8)
for i, valor in enumerate(df_totales["TOTAL 2025"]):
    ax_bar.text(i + bar_width, valor + 500, f"{valor:,.0f} €", ha='center', fontsize=8)
st.pyplot(fig_bar)

# Comentario explicativo
st.subheader("📝 Análisis de variación")
for index, row in df_totales.iterrows():
    total_2024 = row["TOTAL 2024"]
    total_2025 = row["TOTAL 2025"]
    diferencia = total_2025 - total_2024
    variacion_pct = (diferencia / total_2024 * 100) if total_2024 != 0 else 0
    signo = "aumentado" if diferencia > 0 else "disminuido"
    st.markdown(f"**{row['Familia']}** ha {signo} en **{abs(diferencia):,.0f} €**, lo que representa un cambio del **{abs(variacion_pct):.2f}%** respecto al 2024.")
