
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_excel("Datos.xlsx")

# Limpiar y preparar nombres
df.columns = df.columns.str.strip()
df["Familia"] = df["Familia"].str.strip()

# Selector de familias
familias = df["Familia"].tolist()
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

# Gráfico de líneas
st.markdown("### 📉 Evolución mensual de ventas por familia")
meses = ["Enero", "Febrero", "Marzo", "Abril"]
fig, ax = plt.subplots()

for familia in familias_seleccionadas:
    fila = df[df["Familia"] == familia]
    valores_2024 = fila[[f"{mes} 2024" for mes in meses]].values.flatten()
    valores_2025 = fila[[f"{mes} 2025" for mes in meses]].values.flatten()

    ax.plot(meses, valores_2024, label=f"{familia} (2024)", linewidth=2)
    ax.plot(meses, valores_2025, label=f"{familia} (2025)", linestyle='--', linewidth=2)

    # Añadir etiquetas en cada punto
    for i, (x, y) in enumerate(zip(meses, valores_2024)):
        ax.text(i, y, f"{int(y):,} €", ha='center', va='bottom', fontsize=8)
    for i, (x, y) in enumerate(zip(meses, valores_2025)):
        ax.text(i, y, f"{int(y):,} €", ha='center', va='bottom', fontsize=8)

# Estética del gráfico de líneas
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.yaxis.set_visible(False)
ax.legend()
st.pyplot(fig)

# Gráfico de barras
st.markdown("### 📊 Total de ventas por familia")
fig2, ax2 = plt.subplots()
totales_2024 = df[df["Familia"].isin(familias_seleccionadas)]["Total 2024"]
totales_2025 = df[df["Familia"].isin(familias_seleccionadas)]["Total 2025"]
etiquetas = df[df["Familia"].isin(familias_seleccionadas)]["Familia"]

bar_width = 0.35
index = range(len(etiquetas))

b1 = ax2.bar(index, totales_2024, bar_width, label="Total 2024")
b2 = ax2.bar([i + bar_width for i in index], totales_2025, bar_width, label="Total 2025")

# Etiquetas encima de las barras
for rect in b1 + b2:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width() / 2, height, f"{int(height):,} €", ha='center', va='bottom', fontsize=8)

# Estética del gráfico de barras
ax2.set_xticks([i + bar_width / 2 for i in index])
ax2.set_xticklabels(etiquetas, rotation=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.yaxis.set_visible(False)
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
st.pyplot(fig2)

# Explicación final
st.markdown("### 📋 Análisis de variación total por familia")

for i, fam in enumerate(familias_seleccionadas):
    fila = df[df["Familia"] == fam]
    v2024 = fila["Total 2024"].values[0]
    v2025 = fila["Total 2025"].values[0]
    dif = v2025 - v2024
    pct = (dif / v2024) * 100 if v2024 else 0
    if dif > 0:
        st.markdown(f"**{fam}** ha aumentado en **{dif:,.0f} €** respecto a 2024, lo que supone un incremento del **{pct:.2f}%**.")
    elif dif < 0:
        st.markdown(f"**{fam}** ha disminuido en **{abs(dif):,.0f} €** respecto a 2024, lo que supone una bajada del **{abs(pct):.2f}%**.")
    else:
        st.markdown(f"**{fam}** mantiene exactamente las mismas ventas que en 2024.")
