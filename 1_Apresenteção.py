import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

if "data" not in st.session_state:
    df = pd.read_excel("balanco-regime-tributario-unificado-2017-2023.xlsx", index_col= None)
    df = df.sort_values(by="Valor dos Tributos (em R$)")
    st.session_state["data"] = df

# Configuração da página
st.set_page_config(page_title="CV Diogo Julio", layout="wide")
st.sidebar.markdown("Desenvolvido por Diogo Julio Oliveira")

# Adicionando logo com streamlit-extras


# Adicionando o logo
st.logo("image.jpg")

# Adicionando o logo no body
st.image("image.jpg", width=150)

st.title("Introdução Pessoal e Objetivo Profissional")

st.write("Prazer me chamo Diogo Julio Oliveira sou um estudante de Engenharia de Software apaixonado por tecnologia e inovação. Sempre tive interesse em resolver problemas por meio da programação e do desenvolvimento de sistemas, buscando aprender e aprimorar minhas habilidades continuamente. Durante minha trajetória acadêmica, venho adquirindo conhecimentos em linguagens de programação, banco de dados, desenvolvimento web e metodologias ágeis.")

st.write("Meu objetivo profissional é ingressar no mercado de tecnologia, contribuindo para projetos desafiadores e ampliando minha experiência prática. Busco oportunidades como estágio ou trainee para aplicar meus conhecimentos, desenvolver novas competências e crescer profissionalmente na área de desenvolvimento de software. Estou motivado a aprender com profissionais experientes e a colaborar em equipes para criar soluções eficientes e inovadoras.")



