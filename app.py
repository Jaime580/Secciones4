
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparativa de Ventas por Familia", layout="centered")

st.title("📈 Comparativa de Ventas por Familia (2024 vs 2025)")

# Cargar datos
df = pd.read_excel("App ventas secciones.xlsx")

# Selector de Familias
familias = df["Familia"].tolist()
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:3])

# Filtrado
df_filtrado = df[df["Familia"].isin(familias_seleccionadas)]

# Gráfico de líneas mensual
st.subheader("📉 Evolución mensual de ventas por familia")
columnas_mensuales = [col for col in df.columns if "Enero" in col or "Febrero" in col or "Marzo" in col or "Abril" in col]
df_melted = df_filtrado.melt(id_vars=["Familia"], value_vars=columnas_mensuales, var_name="Mes", value_name="Ventas")
fig, ax = plt.subplots()
for fam in familias_seleccionadas:
    datos = df_melted[df_melted["Familia"] == fam]
    ax.plot(datos["Mes"], datos["Ventas"], label=fam, marker='o')
ax.set_ylabel("€")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Gráfico de barras
st.subheader("📊 Total de ventas por familia (2024 vs 2025)")
df_totales = df_filtrado[["Familia", "Total 2024", "Total 2025"]].set_index("Familia")
fig2, ax2 = plt.subplots()
df_totales.plot(kind="bar", ax=ax2)
ax2.set_ylabel("€")
ax2.legend()
st.pyplot(fig2)
