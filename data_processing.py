import pandas as pd

def data_precessing(df_raw):
    df_geral = df_raw.rename(columns={
        '# RELATÓRIO':'RELATÓRIO',
        'DATA DA DESPESA':'MES_ANO'
    })

    df_geral = df_geral[['RELATÓRIO','USUÁRIO','MES_ANO','VALOR',
             'CATEGORIA','SUBCATEGORIA','PROJETO',
             'DESCRIÇÃO','APROVADORES']]
    
    df_geral["MES_ANO"] = pd.to_datetime(df_geral["MES_ANO"], format="%d/%m/%Y") # Cria coluna mes_ano
    df_geral["MES_ANO"] = df_geral["MES_ANO"].dt.strftime("%m/%Y")

    df_geral = df_geral.fillna("Outros") # Subistitui NaN por "Outros"
    df_geral["VALOR"] = pd.to_numeric(df_geral["VALOR"], errors="coerce") # Garante valores numéricos
    df_geral["PROJETO"] = (df_geral["PROJETO"].str.strip()) # Tira espaços da celulas da coluna PROJETO
    
    # 6 - SUBISTITUI TEXTOS DESNECESSÁRIOS DA COLUNA "SUBCATEGORIA"
    substituicoes = {
    "Lavanderia - obrigatório inserir o período":"Lavanderia",
    "Material ou Suprimento (CUSTO CLIENTE - OBRIGATÓRIO JUSTIFICATIVA)":"Material ou Suprimento",
    "Passagem Aérea (OBRIGATÓRIO JUSTIFICATIVA)":"Passagem Aérea",
    "Outro (Obrigatório Justificativa)":"Outro",
    "Material ou Suprimento (CUSTO EMPRESA - OBRIGATÓRIO JUSTIFICATIVA)":"Material ou Suprimento",
    "Hotel (OBRIGATÓRIO JUSTIFICATIVA)":"Hotel",
    "Passagens de Ônibus (OBRIGATÓRIO JUSTIFICATIVA)":"Passagens de Ônibus",
    "Locação de casa - OBRIGATÓRIO NOME DE QUEM AUTORIZOU":"Locação de casa",
    "Treinamento Interno - custo Projexa":"Treinamento Interno",
    "Material de Limpeza - somente para casa alugada - obrigatório NOME DE QUEM AUTORIZOU":"Material de Limpeza",
    "EPIs - inserir nome de quem autorizou":"EPIs",
    "Estacionamento - descrever o período":"Estacionamento",
    "Locação de Veículo (OBRIGATÓRIO JUSTIFICATIVA)":"Locação de Veículo",
    "Manutenção de Equipamentos - Inserir quem autorizou":"Manutenção de Equipamentos",
    "Marketing - inserir nome de quem autorizou":"Marketing",
}
    df_geral["SUBCATEGORIA"] = df_geral["SUBCATEGORIA"].replace(substituicoes)
    
    df_graf = df_geral[['MES_ANO', 'VALOR', 'SUBCATEGORIA', 'PROJETO']]

    return(df_geral, df_graf)