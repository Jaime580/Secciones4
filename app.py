
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.title("📊 Comparativa de Ventas por Familia (2024 vs 2025)")

# Cargar el archivo Excel
df = pd.read_excel("datos.xlsx")

# Normalizar nombres de columnas para trabajar fácilmente
df.columns = [col.strip().upper() for col in df.columns]

# Selector de familias
familias = df["FAMILIA"].unique().tolist()
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias)

# Filtro de datos
df_filtrado = df[df["FAMILIA"].isin(familias_seleccionadas)]

# Gráfico de barras: Totales 2024 vs 2025
st.subheader("📊 Total de ventas por familia")
df_totales = df_filtrado[["FAMILIA", "TOTAL 2024", "TOTAL 2025"]].set_index("FAMILIA")
df_totales.plot(kind="bar", figsize=(10, 5))
plt.ylabel("€")
plt.xticks(rotation=45)
for i, col in enumerate(df_totales.columns):
    for x, y in enumerate(df_totales[col]):
        plt.text(x + i*0.25 - 0.15, y + max(df_totales.max()) * 0.01, f"{int(y):,} €", ha="center", fontsize=8)
st.pyplot(plt.gcf())

# Gráfico de líneas: Evolución mensual
st.subheader("📈 Evolución mensual de ventas por familia")
columnas_mensuales = [col for col in df.columns if "2024" in col or "2025" in col and "TOTAL" not in col]
df_lineas = df_filtrado.set_index("FAMILIA")[columnas_mensuales].T
df_lineas.index.name = "Mes"
df_lineas = df_lineas.reset_index()

for familia in df_filtrado["FAMILIA"]:
    plt.plot(df_lineas["Mes"], df_lineas[familia], marker='o', label=familia)
    for i, valor in enumerate(df_lineas[familia]):
        plt.text(i, valor, f"{int(valor):,} €", fontsize=7, ha='center', va='bottom')

plt.legend()
plt.xticks(rotation=45)
plt.ylabel("€")
plt.tight_layout()
st.pyplot(plt.gcf())
