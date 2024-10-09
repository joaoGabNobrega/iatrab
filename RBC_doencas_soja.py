
import pandas as pd
import numpy as np
import streamlit as st

# Função para calcular a similaridade usando distância euclidiana ponderada
def calcular_similaridade(novo_caso, df_casos, df_pesos):
    similaridades = []
    for index, row in df_casos.iterrows():
        # Calcular a distância ponderada
        distancia = np.sqrt(np.sum([
            ((novo_caso[attr] == row[attr]) * df_pesos.loc[df_pesos['Atributo'] == attr, 'Peso'].values[0]) ** 2
            for attr in df_pesos['Atributo'] if attr in novo_caso and pd.notna(row[attr])
        ]))
        similaridades.append((row['DescDoenca'], row, distancia))  # Usar o nome da doença
    
    similaridades.sort(key=lambda x: x[2])
    return similaridades[:3]  # Retornar os 3 casos mais semelhantes

# Função para adaptar o caso
def adaptar_caso(caso_similar, novo_caso):
    caso_adaptado = caso_similar.copy()
    for atributo in novo_caso:
        if novo_caso[atributo] != caso_similar[atributo]:
            caso_adaptado[atributo] = novo_caso[atributo]
    return caso_adaptado

# Função para revisar a solução aplicada
def revisar_solucao(caso_adaptado):
    # Neste exemplo, a revisão sempre será positiva, mas pode ser ajustada
    return True

# Função para reter o novo caso na base de casos
def reter_novo_caso(caso_adaptado, df_casos):
    df_casos = df_casos.append(caso_adaptado, ignore_index=True)
    return df_casos

# Carregar os dados das planilhas
df_casos = pd.read_excel('base.xlsx', sheet_name='Casos')
df_pesos = pd.read_excel('base.xlsx', sheet_name='Pesos')

# Interface com Streamlit
st.title('Sistema RBC de Doenças da Soja')

# Lista de atributos relevantes
atributos_relevantes = df_pesos['Atributo'].dropna().tolist()

# Input dos dados do novo caso, dinamicamente baseado nos atributos relevantes
novo_caso = {}

# Criar caixas de seleção para todos os atributos
for atributo in atributos_relevantes:
    opcoes = df_casos[atributo].dropna().unique().tolist()  # Extrair as opções disponíveis
    if len(opcoes) > 0:
        novo_caso[atributo] = st.selectbox(atributo, opcoes)

# Quando o usuário clicar no botão
if st.button('Buscar Casos Semelhantes'):
    # 1. Recuperação dos casos semelhantes
    casos_semelhantes = calcular_similaridade(novo_caso, df_casos, df_pesos)
    
    # Exibir os resultados
    st.write('Casos mais semelhantes encontrados:')
    for caso in casos_semelhantes:
        st.write(f'Doença: {caso[0]}, Similaridade: {caso[2]}')
    
    # Selecionar o caso mais semelhante
    caso_similar = casos_semelhantes[0][1]
    
    # 2. Adaptação do caso semelhante
    caso_adaptado = adaptar_caso(caso_similar, novo_caso)
    st.write('Caso adaptado:')
    st.write(caso_adaptado)
    
    # 3. Reutilização da solução (neste caso, estamos exibindo o caso adaptado como a solução)
    st.write('Solução reutilizada com base no caso adaptado:')
    st.write(caso_adaptado)
    
    # 4. Revisão da solução
    sucesso = revisar_solucao(caso_adaptado)
    if sucesso:
        st.success('Solução revisada e considerada bem-sucedida.')
    
    # 5. Retenção do novo caso
    df_casos = reter_novo_caso(caso_adaptado, df_casos)
    st.write('Novo caso adicionado à base de casos.')
