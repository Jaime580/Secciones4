import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

st.title("📈 Comparativa de Ventas por Familia (2024 vs 2025)")

uploaded_file = st.file_uploader("📂 Sube tu archivo Excel con datos de ventas", type=["xlsx"])
if uploaded_file:
    with open("ultimo_archivo.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Archivo subido correctamente.")

# Usar el último archivo subido
if os.path.exists("ultimo_archivo.xlsx"):
    df = pd.read_excel("ultimo_archivo.xlsx")

    familias = df["Familia"].unique().tolist()
    familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

    if familias_seleccionadas:
        df_seleccionado = df[df["Familia"].isin(familias_seleccionadas)].copy()
        
        # Columnas de meses para evolución mensual
        columnas_mensuales = [col for col in df.columns if "TOTAL" not in col and "Familia" not in col]
        meses_2024 = [col for col in columnas_mensuales if "2024" in col]
        meses_2025 = [col for col in columnas_mensuales if "2025" in col]

        fig, ax = plt.subplots()
        for familia in familias_seleccionadas:
            datos_2024 = df[df["Familia"] == familia][meses_2024].values.flatten()
            datos_2025 = df[df["Familia"] == familia][meses_2025].values.flatten()
            ax.plot(meses_2024, datos_2024, label=f"{familia} (2024)", linewidth=2)
            ax.plot(meses_2025, datos_2025, label=f"{familia} (2025)", linewidth=2, linestyle='--')

            for i, value in enumerate(datos_2024):
                ax.text(i, value, f"{value:,.0f} €", ha='center', va='bottom', fontsize=8)
            for i, value in enumerate(datos_2025):
                ax.text(i, value, f"{value:,.0f} €", ha='center', va='bottom', fontsize=8)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_title("📉 Evolución mensual de ventas por familia")
        ax.legend()
        st.pyplot(fig)

        # Gráfico de barras totales
        fig2, ax2 = plt.subplots()
        for i, familia in enumerate(familias_seleccionadas):
            total_2024 = df[df["Familia"] == familia]["TOTAL 2024"].values[0]
            total_2025 = df[df["Familia"] == familia]["TOTAL 2025"].values[0]
            ax2.bar(i - 0.2, total_2024, width=0.4, label="Total 2024" if i == 0 else "", color='#1f77b4')
            ax2.bar(i + 0.2, total_2025, width=0.4, label="Total 2025" if i == 0 else "", color='#ff7f0e')
            ax2.text(i - 0.2, total_2024, f"{total_2024:,.0f} €", ha='center', va='bottom', fontsize=8)
            ax2.text(i + 0.2, total_2025, f"{total_2025:,.0f} €", ha='center', va='bottom', fontsize=8)

        ax2.set_xticks(range(len(familias_seleccionadas)))
        ax2.set_xticklabels(familias_seleccionadas, rotation=0)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.yaxis.set_visible(False)
        ax2.set_title("📊 Total de ventas por familia")
        ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
        st.pyplot(fig2)

        # Análisis explicativo
        for familia in familias_seleccionadas:
            total_2024 = df[df["Familia"] == familia]["TOTAL 2024"].values[0]
            total_2025 = df[df["Familia"] == familia]["TOTAL 2025"].values[0]
            diferencia = total_2025 - total_2024
            variacion = (diferencia / total_2024 * 100) if total_2024 else 0
            st.markdown(f"**🔍 Análisis para {familia}:**")
            st.markdown(f"- Variación absoluta: **{diferencia:,.0f} €**")
            st.markdown(f"- Variación relativa: **{variacion:.2f}%**")
else:
    st.warning("📤 Por favor, sube un archivo Excel para comenzar.")