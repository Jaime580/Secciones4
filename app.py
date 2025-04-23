
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparativa de Ventas por Familia", layout="centered")

# Cargar datos
df = pd.read_excel("Datos.xlsx")

# Configurar columnas
df.columns = [col.strip() for col in df.columns]
meses = ["Enero", "Febrero", "Marzo", "Abril"]
familias = df["Familia"].tolist()

# Selector de familias
familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

# Filtrar por familias
df_filtrado = df[df["Familia"].isin(familias_seleccionadas)].copy()

# GRÁFICO DE LÍNEAS
st.markdown("### 📉 Evolución mensual de ventas por familia")
fig, ax = plt.subplots()
for familia in familias_seleccionadas:
    fila = df[df["Familia"] == familia].iloc[0]
    y_2024 = [fila[f"{mes} 2024"] for mes in meses]
    y_2025 = [fila[f"{mes} 2025"] for mes in meses]
    ax.plot(meses, y_2024, label=f"{familia} (2024)", linewidth=2)
    ax.plot(meses, y_2025, label=f"{familia} (2025)", linestyle="--", linewidth=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_ylabel("€")
ax.legend()
st.pyplot(fig)

# GRÁFICO DE BARRAS
st.markdown("### 📊 Total de ventas por familia")
df_totales = df_filtrado[["Familia", "Total 2024", "Total 2025"]].set_index("Familia")
fig2, ax2 = plt.subplots()
df_totales.plot(kind="bar", ax=ax2, width=0.6, color=["#1f77b4", "#ff7f0e"])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.set_ylabel("€")
ax2.set_xticklabels(df_totales.index, rotation=0)
ax2.legend(["Total 2024", "Total 2025"])
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():,.0f} €", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom')
st.pyplot(fig2)

# EXPLICACIÓN DE VARIACIÓN
st.markdown("### 📌 Análisis de variación")
for i, row in df_totales.iterrows():
    total_2024 = row["Total 2024"]
    total_2025 = row["Total 2025"]
    diferencia = total_2025 - total_2024
    porcentaje = (diferencia / total_2024) * 100 if total_2024 != 0 else 0
    signo = "aumento" if diferencia > 0 else "descenso" if diferencia < 0 else "sin variación"
    st.write(f"➡️ **{i}** ha tenido un {signo} de **{abs(diferencia):,.0f} €** "
             f"(**{porcentaje:+.2f}%**) en 2025 respecto a 2024.")
