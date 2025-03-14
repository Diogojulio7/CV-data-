import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *

# Configuração da página
st.set_page_config(page_title="Dashboard de Distribuições Probabilísticas", layout="wide")

# Adicionando o logo
st.logo("image.jpg")

# Adicionando o logo
st.image("image.jpg", width=150)

# Criando as sub-abas (pages)
pages = st.sidebar.selectbox("Escolha a Distribuição:", [
    "Analise seus Dados"
])

st.sidebar.markdown("Desenvolvido por Diogo Julio Oliveira")

# Função para exibir gráfico Plotly
def plot_distribution(x, y, title, xlabel, ylabel):
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    st.plotly_chart(fig)


if pages == "Analise seus Dados":
    st.header("Análise de Dados")

    
    
    df = pd.read_excel("balanco-regime-tributario-unificado-2017-2023.xlsx", index_col= None)
    st.write("Amostra dos dados:")
    st.write(df.head())
    
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    if colunas_numericas:

        st.write("Quando selecionamos a coluna númerica: Valor  dos Tributos (em R$) ; e utilizamos a distribuição para análise: Normal. ")
        st.write("Conseguimos analisar o cálculo da média, mediana, o desvio padrâo e outros . Assim conseguimos ver os valores dos tributos anuais e ter uma noção de como manipulalos ao nosso favor.")

        st.write("Quando selecionamos a coluna númerica: Quantidade de Importadores ; e utilizamos a distribuição para análise: Poisson. ")
        st.write("Conseguimos analisar o cálculo da média, mediana e outros . Assim conseguimos analisar a probabilidade de quantos importadores teremos no decorrer dos anos.")

        coluna_escolhida = st.selectbox("Escolha uma coluna numérica:", colunas_numericas)
        
        if coluna_escolhida:
            st.write("Distribuição dos dados:")
            st.write(df[coluna_escolhida].describe())
            
            dist = st.selectbox("Escolha a distribuição para análise:", ["Poisson", "Normal", "Binomial"])
            
            if dist == "Poisson":
                
                col1, col2 = st.columns([0.3,0.7])
                
                lambda_est = df[coluna_escolhida].mean()

                x_min = col1.number_input("Número mínimo de eventos",value=0)
                x_max = col1.number_input("Número máximo de eventos desejado",value=2*lambda_est)
                
                x = np.arange(x_min, x_max)
                y = stats.poisson.pmf(x, lambda_est)
                y_cdf = stats.poisson.cdf(x,lambda_est)

                df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),"P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")

                col2.write("Tabela de probabilidades:")
                col2.write(df_poisson)
                
                st.subheader(f"Estimativa de λ (Taxa média de Ocorrência): {lambda_est:.2f}")
                prob_acum = st.toggle("Probabilidade Acumulada")
                if prob_acum:
                    st.write("Probabilidades 'somadas' desde a origem!")
                    y_selec = y_cdf
                    fig = go.Figure(data=[go.Line(x=x, y=y_selec)])
                    fig.update_layout(title="Distribuição de Poisson Acumulada", xaxis_title="Número de eventos", yaxis_title="Probabilidade Acumulada")
                    st.plotly_chart(fig)
                else:
                    y_selec = y
                    plot_distribution(x, y_selec, "Distribuição de Poisson", "Número de eventos", "Probabilidade")
                


                
            elif dist == "Normal":
                
                n = df[coluna_escolhida].count()
                mu_est = df[coluna_escolhida].mean()
                sigma_est = df[coluna_escolhida].std()
                st.subheader(f"Estimativa de μ: {mu_est:.2f}, σ: {sigma_est:.2f}")


                # Create distplot with custom bin_size
                #colunas_categoricas = df.select_dtypes(include=[np.character]).#columns.tolist()
                
                #st.selectbox("Escolha uma variável qualitativa",colunas_categoricas)


                hist_data = [df[coluna_escolhida].dropna().tolist()]
                group_labels=['distplot']
                b_size = st.number_input("Largura de Classe - Histograma",min_value=0.1,value=10000.00)

                fig = ff.create_distplot(
                    hist_data, group_labels, bin_size=b_size)
                
                teorica = st.checkbox("Curva teórica")
                if teorica:

                    # Adicionando a curva da distribuição normal teórica com média e desvio padrão da amostra
                    x = np.linspace(mu_est - 4*sigma_est, mu_est + 4*sigma_est, 100)
                    y = stats.norm.pdf(x, mu_est, sigma_est)

                    # Criando um trace da curva normal
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva Normal', line=dict(color='red')))
                
                st.plotly_chart(fig)

                p = ggplot(df, aes(sample=coluna_escolhida)) + geom_qq(size=3,colour='red',alpha=0.7) + geom_qq_line()+theme_bw()+labs(x="Quantis Teóricos",y = "Quantis Amostrais", title="Gráfico QQPlot")
                st.pyplot(ggplot.draw(p))





            
            elif dist in ["Binomial"]:
                threshold = st.number_input("Defina o limiar para True/False:")
                p_est = (df[coluna_escolhida] > threshold).mean()
                k = st.slider("Número de sucessos (k):", min_value=0, max_value=50, value=5, step=1)
                st.write(f"Estimativa de p: {p_est:.2f}")
                valores = np.arange(0, k + 1)
                probabilidades = stats.binom.pmf(valores, k, p_est)
                plot_distribution(valores, probabilidades, f"Distribuição {dist}", "Resultado", "Probabilidade")
                df_binomial = pd.DataFrame({"X": valores, "P(X)": probabilidades})
                st.write("Tabela de probabilidades:")
                st.write(df_binomial)