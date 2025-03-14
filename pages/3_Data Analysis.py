import streamlit as st
import pandas as pd
import numpy as np



st.set_page_config(
    page_title="Dados",
    page_icon="🏃🏼", 
    layout="wide"
)

st.logo("image.jpg")

# Adicionando o logo no body
st.image("image.jpg", width=150)

df = st.session_state["data"]

tipos='Todos'
tipos = np.append(tipos,df["Ano"].unique())
tipo = st.sidebar.selectbox("Ano", tipos)
st.sidebar.markdown("Desenvolvido por Diogo Julio Oliveira")

if tipo == 'Todos':
    df_filtered = df
else:
    df_filtered = df[(df["Ano"]==tipo)]

st.title("O que conseguimos analisar com os dados fornecidos")

st.write("A planilha contém dados sobre declarações e valores financeiros organizados por ano e mês. Aqui está o que cada coluna representa:")

st.write("Ano - O ano correspondente aos dados registrados.")
st.write("Mês - Código do mês no formato AAAAMM (AnoMês), por exemplo, 201206 representa junho de 2012.")
st.write("Total de Declarações (DRTU) - Quantidade de declarações registradas no período.   ")
st.write("Valor total desembaraçado (em R$) - O valor total das mercadorias ou bens desembaraçados.")
st.write("Valor dos Tributos Federais (em R$) - O total de tributos federais pagos no período.")

st.write("Com base nos dados, é possível realizar diversas análises relevantes relacionadas a declarações e valores tributários ao longo do tempo. Aqui estão algumas das principais interpretações que podem ser feitas:")

st.write("1. Análise Temporal das Declarações")
st.write("Avaliar como o número de declarações (DRTU) varia ao longo dos meses e anos.")
st.write("Identificar tendências, como aumento ou queda nas declarações em determinados períodos.")
st.write("Detectar sazonalidades, por exemplo, se há meses com maior volume de declarações.")
st.write("2. Análise de Valores Desembaraçados")
st.write("Examinar a evolução do valor total desembaraçado ao longo do tempo.")
st.write("Identificar picos ou quedas que podem indicar variações no volume de mercadorias ou transações.")
st.write("Comparar o valor desembaraçado com o número de declarações para verificar se há meses em que menos declarações envolvem valores mais altos.")
st.write("3. Análise de Tributos Federais")
st.write("Avaliar quanto foi arrecadado em tributos federais ao longo dos anos.")
st.write("Identificar a relação entre o valor desembaraçado e os tributos pagos (exemplo: qual a porcentagem média de tributos sobre o valor desembaraçado).")
st.write("Verificar se há variações significativas na arrecadação de impostos em determinados períodos.")
st.write("4. Comparação entre Declarações, Valores e Tributos")
st.write("Verificar se há correlação entre o número de declarações e os valores desembaraçados (por exemplo, um aumento no número de declarações sempre significa mais valor desembaraçado?).")
st.write("Comparar meses com alto volume de declarações e arrecadação para entender se há padrões específicos.")
st.write("Identificar anomalias - meses em que houve poucas declarações, mas valores muito altos (ou vice-versa).")

#df_filtered
st.dataframe(df_filtered,
             column_config={
                 "Valor dos Tributos (em R$)": st.column_config.ProgressColumn(
                     "Valor dos Tributos (em R$)", format="%f", min_value=0, max_value=int(df_filtered["Valor dos Tributos (em R$)"].max()))
                 })