
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_excel("Datos.xlsx")

# Mostrar título
st.title("📊 Comparativa de Ventas por Familia (2024 vs 2025)")

# Selector de familias
familias = df["Familia"].unique().tolist()
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:2])

# Filtrado del DataFrame
df_filtro = df[df["Familia"].isin(familias_seleccionadas)]

# Gráfico de líneas - evolución mensual
st.subheader("📈 Evolución mensual de ventas por familia")

meses = ["Enero", "Febrero", "Marzo", "Abril"]
col_2024 = [f"{mes} 2024" for mes in meses]
col_2025 = [f"{mes} 2025" for mes in meses]

fig, ax = plt.subplots(figsize=(10, 4))

for _, row in df_filtro.iterrows():
    ax.plot(meses, row[col_2024], marker='o', label=f"{row['Familia']} (2024)")
    ax.plot(meses, row[col_2025], marker='o', linestyle='--', label=f"{row['Familia']} (2025)")

ax.set_ylabel("€")
ax.legend()
st.pyplot(fig)

# Gráfico de barras - Totales
st.subheader("📊 Total de ventas por familia")

fig2, ax2 = plt.subplots(figsize=(10, 4))
x = range(len(familias_seleccionadas))
ventas_2024 = df_filtro["Total 2024"]
ventas_2025 = df_filtro["Total 2025"]

bar1 = ax2.bar([i - 0.2 for i in x], ventas_2024, width=0.4, label="Total 2024")
bar2 = ax2.bar([i + 0.2 for i in x], ventas_2025, width=0.4, label="Total 2025")

ax2.set_xticks(list(x))
ax2.set_xticklabels(familias_seleccionadas, rotation=45)
ax2.set_ylabel("€")
ax2.legend()

for i in range(len(familias_seleccionadas)):
    ax2.text(i - 0.2, ventas_2024.iloc[i], f"{ventas_2024.iloc[i]:,.0f} €", ha='center', va='bottom')
    ax2.text(i + 0.2, ventas_2025.iloc[i], f"{ventas_2025.iloc[i]:,.0f} €", ha='center', va='bottom')

st.pyplot(fig2)
