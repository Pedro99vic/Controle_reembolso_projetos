# IMPORTANDO BIBLIOTECAS E CONFIGURAÇÕES INICIAIS
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # locale - Brasil

# LEITURA DA BASE DE DADOS
df = pd.read_excel(r"C:\Users\Projexa\OneDrive - projexa.com.br\Área de Trabalho\Estudos_python\1.Dashboard_reembolso_projetos\data\base_de_dados_geral.xlsx")

###################################################################################################

# TRATAMENTO DE DADOS

df = df.rename(columns={'# RELATÓRIO':'RELATÓRIO',
                        'DATA DA DESPESA':'MES_ANO'}) # Correção dos nomes de algumas colunas

df = df[['RELATÓRIO','USUÁRIO','MES_ANO',
         'VALOR','CATEGORIA','SUBCATEGORIA',
         'PROJETO','DESCRIÇÃO','APROVADORES']] # Seleção de colunas que serão utilizadas

df["MES_ANO"] = pd.to_datetime(df["MES_ANO"], format="%d/%m/%Y") # Cria coluna mes_ano
df["MES_ANO"] = df["MES_ANO"].dt.strftime("%m/%Y")

# 3 - SUBSTITUI NaN POR "Outros"
df = df.fillna("Outros") # Subistitui NaN por "Outros"
df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce") # Garante valores numéricos
df["PROJETO"] = (df["PROJETO"].str.strip()) # Tira espaços da celulas da coluna PROJETO

# 6 - SUBISTITUI TEXTOS DESNECESSÁRIOS DA COLUNA "SUBCATEGORIA"
substituicoes = {
    "Hotel (OBRIGATÓRIO JUSTIFICATIVA)": "Hotel",
    "Lavanderia - obrigatório inserir o período": "Lavanderia",
    "Material ou Suprimento (CUSTO EMPRESA - OBRIGATÓRIO JUSTIFICATIVA)" : "Material ou Suprimento",
    "Passagem Aérea (OBRIGATÓRIO JUSTIFICATIVA)":"Passagem Aérea",
    "Material de Limpeza - somente para casa alugada - obrigatório NOME DE QUEM AUTORIZOU":"Material de Limpeza",
    "Passagens de Ônibus (OBRIGATÓRIO JUSTIFICATIVA)":"Passagens de Ônibus",
    "Locação de casa - OBRIGATÓRIO NOME DE QUEM AUTORIZOU":"Locação de casa",
    "Outro (Obrigatório Justificativa)":"Outros"
}
df["SUBCATEGORIA"] = df["SUBCATEGORIA"].replace(substituicoes)

###################################################################################################

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide")
st.title("📊 Controle de Gastos e Reembolsos - PROJEXA")

# FILTROS (PILLS STYLE)
st.subheader("Filtros")

col1, col2 = st.columns(2) # layout dos filtros

with col1:
    projetos = st.multiselect(
    "Projetos",
    options=sorted(df["PROJETO"].dropna().unique()),
    placeholder="Selecione o projeto"
    )

with col2:
    meses = st.pills(
        "Meses:", 
        df["MES_ANO"].dropna().unique(),
        selection_mode = "multi"
        #label_visibility = "collapsed"
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

col3, col4 = st.columns([4,1]) # layout dados

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
        value=f"R$ {df_soma:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )