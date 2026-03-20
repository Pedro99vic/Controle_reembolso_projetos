# IMPORTANDO BIBLIOTECAS E CONFIGURAÇÕES INICIAIS
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # locale - Brasil

# LEITURA DA BASE DE DADOS
from data_loader import load_data
df_raw = load_data(r"C:\Users\Projexa\OneDrive - projexa.com.br\Área de Trabalho\Estudos_python\1.Dashboard_reembolso_projetos\data\base_de_dados_geral.xlsx")


# TRATAMENTO DE DADOS
from data_processing import data_precessing
df_geral, df = data_precessing(df_raw)


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide")
st.title("📊 Controle de Gastos e Reembolsos - PROJEXA")

# FILTROS
st.subheader("Filtros")

col1, col2 = st.columns(2) # layout dos filtros

with col1:
    projetos = st.multiselect(
    "Projetos",
    options=sorted(df["PROJETO"].dropna().unique()),
    placeholder="Selecione o projeto"
    )

with col2:
    meses = st.multiselect(
        "Meses:", 
        options=sorted(df["MES_ANO"].dropna().unique()),
        default=df["MES_ANO"].unique(),
        placeholder="Data"
    )

# TRATAMENTO SE NADA FOR SELECIONADO
if not projetos or not meses:
    st.warning("Selecione ao menos um projeto e um mês.")
    st.stop()

# DATA FRAME COM OS VALORES FILTRADOS
df_filtrado = df[
    (df["PROJETO"].isin(projetos)) &
    (df["MES_ANO"].isin(meses))
]

# AGRUPAMENTO GRÁFICO 1
df_graf1 = (
    df_filtrado
    .groupby("SUBCATEGORIA", as_index=False)["VALOR"]
    .sum()
    .sort_values("VALOR", ascending=False)
)

# AGRUPAMENTO METRIC
df_soma = (df_filtrado["VALOR"].sum())

col3, col4 = st.columns([3,1]) # layout dados

# GRÁFICO DE BARRAS (COM PLOTLY)
with col3:
    fig = px.bar(
        df_graf1,
        x="SUBCATEGORIA",
        y="VALOR",
        title="Gastos por Subcategoria",
        labels={
            "SUBCATEGORIA": "Subcategoria",
            "VALOR": "Total de Gastos (R$)"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_tickformat=",.2f"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.metric(
        label="Total Gasto",
        value=f"R$ {df_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        border=True
    )


# TABELA AO FINAL DA PAGINA (RAW DATA)
st.subheader("Raw data - Filtrado")
st.dataframe(df_filtrado)