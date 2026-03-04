# IMPORTANDO BIBLIOTECAS E CONFIGURAÇÕES INICIAIS
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # locale - Brasil

# LEITURA DA BASE DE DADOS
df = pd.read_excel(r"C:\Users\Projexa\OneDrive - projexa.com.br\Área de Trabalho\Estudos_python\1.Dashboard_gastos_projetos\data\03-03-2026 20_19_16.xlsx")

# TRATAMENTO DE DADOS
# 1 - EXCLUI COLUNAS DESNECESSÁRIAS
df1 = df.drop(['E-MAIL', 
              'CPF', 'TIME', 'MOEDA', 'NÃO REEMBOLSÁVEL',
              'CARTÃO', 'STATUS', 'DATA DE ENVIO', 
              'DATA DE APROVAÇÃO', 'DATA DE CONCLUSÃO', 'CONCLUIDORES', 
              'URL DO COMPROVANTE', 'URL DO RELATÓRIO', 'MOTIVO 1'], axis=1)

# 2 - CORREÇÃO DE NOME COLUNA
df2 = df1.rename(columns={'# RELATÓRIO':'RELATÓRIO', 'DATA DA DESPESA':'MES_ANO'})

# 3 - REORGANIZAÇÃO DAS CONLUNAS
df3 = df2[['RELATÓRIO','USUÁRIO','MES_ANO','VALOR','CATEGORIA','SUBCATEGORIA','PROJETO','DESCRIÇÃO','APROVADORES']]

# 4 - SUBSTITUI NaN POR NADA
#   - GARANTE QUE COLUNA VALOR SEJA BRL - USANDO BIBLIOTECA LOCALE 
df4 = df3.fillna("Outros")
#df4["VALOR"] = df4["VALOR"].apply(lambda x: locale.currency(x, grouping=True))

# 5 - CRIA COLUNA MES_ANO
df5 = df4
df5["MES_ANO"] = pd.to_datetime(df5["MES_ANO"], format="%d/%m/%Y")
df5["MES_ANO"] = df5["MES_ANO"].dt.strftime("%m/%Y")

# 6 - GARANTE VALORES NUMERICOS
df6 = df5
df6["VALOR"] = pd.to_numeric(df6["VALOR"], errors="coerce")


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide")
st.title("📊 Dashboard de Gastos por Subcategoria")

# FILTROS (PILLS STYLE)
st.subheader("Filtros")

col1, col2 = st.columns(2) # layout dos filtros

with col1:
    projetos = st.pills(
        "Projetos:",
        df6["PROJETO"].dropna().unique(),
        selection_mode = "multi",
        label_visibility = "collapsed"
    )

with col2:
    meses = st.pills(
        "Meses:", 
        df6["MES_ANO"].dropna().unique(),
        selection_mode = "multi",
        label_visibility = "collapsed"
    )

# TRATAMENTO SE NADA FOR SELECIONADO
if not projetos or not meses:
    st.warning("Selecione ao menos um projeto e um mês.")
    st.stop()

# DATA FRAME COM OS VALORES FILTRADOS
df_filtrado = df6[
    (df6["PROJETO"].isin(projetos)) &
    (df6["MES_ANO"].isin(meses))
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