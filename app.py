
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

st.title("📊 Comparativa de Ventas por Familia (2024 vs 2025)")

uploaded_file = st.file_uploader("Por favor, sube tu archivo Excel con los datos actualizados. Si no lo haces, se usará el último archivo que subiste.", type=["xlsx"])

if uploaded_file is not None:
    with open("ultimo_archivo.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

# Verificar si hay un archivo previo
if not os.path.exists("ultimo_archivo.xlsx"):
    st.warning("No hay ningún archivo cargado todavía. Por favor, sube uno para comenzar.")
else:
    df = pd.read_excel("ultimo_archivo.xlsx")

    # Mostrar selector de familias
    familias = df["Familia"].tolist()
    familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

    # Gráfico de evolución mensual
    st.subheader("📉 Evolución mensual de ventas por familia")
    meses = ["Enero", "Febrero", "Marzo", "Abril"]
    fig, ax = plt.subplots()
    for familia in familias_seleccionadas:
        valores_2024 = df[df["Familia"] == familia][[f"{mes} 2024" for mes in meses]].values.flatten()
        valores_2025 = df[df["Familia"] == familia][[f"{mes} 2025" for mes in meses]].values.flatten()
        ax.plot(meses, valores_2024, label=f"{familia} (2024)", linestyle="-")
        ax.plot(meses, valores_2025, label=f"{familia} (2025)", linestyle="--")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend()
    ax.set_ylabel("€")
    st.pyplot(fig)

    # Gráfico de barras con totales
    st.subheader("📊 Total de ventas por familia")
    columnas_totales = ["Total 2024", "Total 2025"]
    df_totales = df[df["Familia"].isin(familias_seleccionadas)][["Familia"] + columnas_totales]

    fig2, ax2 = plt.subplots()
    x = df_totales["Familia"]
    bar_width = 0.35
    index = range(len(x))
    barras1 = ax2.bar(index, df_totales["Total 2024"], bar_width, label="Total 2024")
    barras2 = ax2.bar([i + bar_width for i in index], df_totales["Total 2025"], bar_width, label="Total 2025")

    # Eliminar líneas innecesarias
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_xticks([i + bar_width / 2 for i in index])
    ax2.set_xticklabels(x, rotation=0)
    ax2.set_yticklabels([])
    ax2.set_xlabel("")  # No mostrar "Familia"
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=2)

    for bar in barras1:
        height = bar.get_height()
        ax2.annotate(f'{height:,.0f} €', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    for bar in barras2:
        height = bar.get_height()
        ax2.annotate(f'{height:,.0f} €', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig2)

    # Análisis explicativo
    st.subheader("🧾 Análisis de variación total por familia")
    for _, row in df_totales.iterrows():
        nombre = row["Familia"]
        total_2024 = row["Total 2024"]
        total_2025 = row["Total 2025"]
        dif = total_2025 - total_2024
        pct = (dif / total_2024) * 100 if total_2024 else 0
        if dif > 0:
            st.markdown(f"✅ La familia **{nombre}** ha **crecido** en **{dif:,.0f} €** respecto a 2024, lo que supone un incremento del **{pct:.2f}%**.")
        elif dif < 0:
            st.markdown(f"🔻 La familia **{nombre}** ha **disminuido** en **{abs(dif):,.0f} €** respecto a 2024, lo que supone una caída del **{abs(pct):.2f}%**.")
        else:
            st.markdown(f"⚖️ La familia **{nombre}** mantiene exactamente las mismas ventas que en 2024.")

