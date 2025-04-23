
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

st.set_page_config(layout="wide")

st.title("📊 Comparativa de Ventas por Familia (dinámica por meses)")

uploaded_file = st.file_uploader("Por favor, sube tu archivo Excel con los datos actualizados. Si no lo haces, se usará el último archivo que subiste.", type=["xlsx"])

if uploaded_file is not None:
    with open("ultimo_archivo.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

if not os.path.exists("ultimo_archivo.xlsx"):
    st.warning("No hay ningún archivo cargado todavía. Por favor, sube uno para comenzar.")
else:
    df = pd.read_excel("ultimo_archivo.xlsx")
    df.columns = df.columns.str.strip()
    df["Familia"] = df["Familia"].str.strip()

    familias = df["Familia"].tolist()
    familias_seleccionadas = st.multiselect("Selecciona una o varias familias:", familias, default=familias[:1])

    # Detectar columnas mensuales dinámicamente
    patron_mes = re.compile(r"^(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre) (2024|2025)$")
    columnas_mensuales = [col for col in df.columns if patron_mes.match(col)]
    
    # Ordenar las columnas cronológicamente
    meses_orden = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
                   "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
    columnas_mensuales.sort(key=lambda x: (int(x.split()[1]), meses_orden[x.split()[0]]))

    if familias_seleccionadas:
        df_filt = df[df["Familia"].isin(familias_seleccionadas)]

        st.subheader("📈 Evolución mensual de ventas por familia")
        fig, ax = plt.subplots(figsize=(12, 5))

        for fam in familias_seleccionadas:
            valores = df_filt[df_filt["Familia"] == fam][columnas_mensuales].values.flatten()
            ax.plot(columnas_mensuales, valores, label=fam, linewidth=2)

            for i, val in enumerate(valores):
                ax.text(i, val, f"{int(val):,} €", ha='center', va='bottom', fontsize=8)

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.yaxis.set_visible(False)
        ax.legend()
        st.pyplot(fig)

        st.subheader("📊 Total de ventas por familia")
        columnas_totales = ["Total 2024", "Total 2025"]
        if all(col in df.columns for col in columnas_totales):
            df_totales = df[df["Familia"].isin(familias_seleccionadas)][["Familia"] + columnas_totales]
            fig2, ax2 = plt.subplots()
            x = df_totales["Familia"]
            bar_width = 0.35
            index = range(len(x))

            b1 = ax2.bar(index, df_totales["Total 2024"], bar_width, label="Total 2024")
            b2 = ax2.bar([i + bar_width for i in index], df_totales["Total 2025"], bar_width, label="Total 2025")

            for rect in b1 + b2:
                height = rect.get_height()
                ax2.text(rect.get_x() + rect.get_width() / 2, height, f"{height:,.0f} €", ha='center', va='bottom', fontsize=8)

            ax2.set_xticks([i + bar_width / 2 for i in index])
            ax2.set_xticklabels(x, rotation=0)
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.yaxis.set_visible(False)
            ax2.set_xlabel("")
            ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=2)
            st.pyplot(fig2)

            st.subheader("📋 Análisis de variación total por familia")
            for _, row in df_totales.iterrows():
                nombre = row["Familia"]
                total_2024 = row["Total 2024"]
                total_2025 = row["Total 2025"]
                dif = total_2025 - total_2024
                pct = (dif / total_2024) * 100 if total_2024 else 0
                if dif > 0:
                    st.markdown(f"✅ **{nombre}** ha crecido en **{dif:,.0f} €**, lo que supone un incremento del **{pct:.2f}%**.")
                elif dif < 0:
                    st.markdown(f"🔻 **{nombre}** ha bajado en **{abs(dif):,.0f} €**, lo que supone una caída del **{abs(pct):.2f}%**.")
                else:
                    st.markdown(f"⚖️ **{nombre}** mantiene las mismas ventas que en 2024.")
        else:
            st.info("El archivo aún no contiene las columnas 'Total 2024' y 'Total 2025'.")
