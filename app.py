import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o modelo treinado
model = joblib.load('best_model.pkl')

# Carregar os nomes das colunas usadas no treinamento do modelo
trained_columns = joblib.load('trained_columns.pkl')

# Título
st.title('Monitoramento e Conservação de Recifes de Coral')

# Função para processar os dados carregados pelo usuário
def process_user_data(data):
    # Lista de espécies para criar variáveis binárias
    especies = [
        'Montastraea annularis',
        'Acropora',
        'Acropora palmata',
        'Montastraea sp. (= annularis complex)',
        'Porites',
        'Pocillopora',
        'Montastraea faveolata'
    ]

    if 'CORAL_SPECIES' not in data.columns:
        st.error("Coluna 'CORAL_SPECIES' não encontrada nos dados carregados.")
        return None

    # Converter a coluna CORAL_SPECIES para string e lidar com valores nulos
    data['CORAL_SPECIES'] = data['CORAL_SPECIES'].astype(str).fillna('')

    # Criar variáveis binárias para cada espécie
    for especie in especies:
        if especie in ['Montastraea annularis', 'Montastraea sp. (= annularis complex)']:
            data['Montastraea_annularis_complex'] = data['CORAL_SPECIES'].str.contains('Montastraea annularis|Montastraea sp. (= annularis complex)', case=False, na=False).astype(int)
        else:
            data[especie] = data['CORAL_SPECIES'].str.contains(especie, case=False, na=False).astype(int)

    # Criar variável binária para outras espécies
    data['Other_species'] = (~data['CORAL_SPECIES'].str.contains('|'.join(especies), case=False, na=False)).astype(int)

    # Lista de famílias de corais para criar variáveis binárias
    familias = [
        'Acroporidae',
        'Poritidae',
        'Faviidae',
        'Pocilloporidae',
        'Siderastreidae',
        'Agariciidae'
    ]

    if 'CORAL_FAMILY' not in data.columns:
        st.error("Coluna 'CORAL_FAMILY' não encontrada nos dados carregados.")
        return None

    # Converter a coluna CORAL_FAMILY para string e lidar com valores nulos
    data['CORAL_FAMILY'] = data['CORAL_FAMILY'].astype(str).fillna('')

    # Criar variáveis binárias para cada família
    for familia in familias:
        data[familia] = data['CORAL_FAMILY'].str.contains(familia, case=False, na=False).astype(int)

    # Criar variável binária para outras famílias
    data['Other_families'] = (~data['CORAL_FAMILY'].str.contains('|'.join(familias), case=False, na=False)).astype(int)

    # Remover colunas desnecessárias
    columns_to_drop = ['ID', 'REGION', 'SUBREGION', 'LOCATION', 'MONTH', 'COUNTRY_CODE', 'WATER_TEMPERATURE', 'CORAL_SPECIES', 'CORAL_FAMILY', 'YEAR', 'DEPTH', 'BLEACHING_SEVERITY', 'PERCENTAGE_AFFECTED', 'BLEACHING_DURATION', 'MORTALITY', 'MORTALITY_CODE', 'RECOVERY_CODE', 'RECOVERY', 'SURVEY_TYPE', 'SURVEY_AREA', 'OTHER_FACTORS', 'REFERENCE_CODE', 'SOURCE', 'REMARKS']
    data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Converter variáveis categóricas em variáveis dummy
    data = pd.get_dummies(data)

    # Garantir que as colunas correspondam às do treinamento
    for col in trained_columns:
        if col not in data.columns:
            data[col] = 0

    data = data[trained_columns]

    return data

def process_user_input(country, lat, lon, depth_mean, species, family):
    species_map = {
        'Montastraea annularis': 'Montastraea_annularis_complex',
        'Montastraea sp. (= annularis complex)': 'Montastraea_annularis_complex',
        'Acropora': 'Acropora',
        'Acropora palmata': 'Acropora palmata',
        'Porites': 'Porites',
        'Pocillopora': 'Pocillopora',
        'Montastraea faveolata': 'Montastraea faveolata',
        'Outros': 'Other_species'
    }

    family_map = {
        'Acroporidae': 'Acroporidae',
        'Poritidae': 'Poritidae',
        'Faviidae': 'Faviidae',
        'Pocilloporidae': 'Pocilloporidae',
        'Siderastreidae': 'Siderastreidae',
        'Agariciidae': 'Agariciidae',
        'Outros': 'Other_families'
    }

    user_data = {
        'COUNTRY': country,
        'LAT': lat,
        'LON': lon,
        'DEPTH_MEAN': depth_mean,
        species_map[species]: 1,
        family_map[family]: 1
    }

    for col in trained_columns:
        if col not in user_data:
            user_data[col] = 0

    user_df = pd.DataFrame(user_data, index=[0])
    user_df = user_df[trained_columns]  # Garantir que as colunas estejam na mesma ordem

    return user_df

def detect_delimiter(file_content):
    first_line = file_content.split('\n')[0]
    if ',' in first_line:
        return ','
    elif ';' in first_line:
        return ';'
    elif '\t' in first_line:
        return '\t'
    return None

# Seção: Carregar dados
st.sidebar.header('Escolha uma opção')
option = st.sidebar.radio('Como você gostaria de fornecer os dados?', ('Carregar CSV', 'Inserir Manualmente'))

if option == 'Carregar CSV':
    uploaded_file = st.sidebar.file_uploader('Carregar um arquivo CSV', type='csv')
    if uploaded_file:
        encodings = ['utf-8', 'latin1', 'iso-8859-1']
        success = False
        for encoding in encodings:
            try:
                file_content = uploaded_file.getvalue().decode(encoding)
                delimiter = detect_delimiter(file_content)
                if delimiter:
                    st.write(f"Arquivo carregado com codificação {encoding} e delimitador '{delimiter}'")
                    uploaded_file.seek(0)  # Reset file pointer after read
                    user_data = pd.read_csv(uploaded_file, encoding=encoding, delimiter=delimiter, on_bad_lines='skip')
                    st.write("Dados carregados:")
                    st.write(user_data.head())
                    st.write("Colunas dos dados carregados:")
                    st.write(user_data.columns.tolist())
                    
                    # Processar dados carregados
                    processed_data = process_user_data(user_data)
                    if processed_data is not None:
                        # Fazer previsões
                        predictions = model.predict(processed_data)
                        probabilities = model.predict_proba(processed_data)
                        processed_data['Predicted_SEVERITY_CODE'] = predictions
                        st.write("Previsões:")
                        st.write(processed_data)
                        st.write("Probabilidades:")
                        st.write(probabilities)

                        # Seção: Visualização de dados
                        st.subheader('Visualização de Dados')

                        # Importância das variáveis
                        importances = model.feature_importances_
                        features = processed_data.columns[:-1]  # Excluindo a coluna de previsão

                        # Criar um DataFrame para facilitar a visualização
                        feature_importances = pd.DataFrame({'Feature': features, 'Importance': importances})

                        # Ordenar por importância
                        feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

                        # Plotar a importância das variáveis
                        plt.figure(figsize=(12, 8))
                        sns.barplot(x='Importance', y='Feature', data=feature_importances)
                        plt.title('Importância das Variáveis')
                        plt.xlabel('Importância')
                        plt.ylabel('Variável')
                        st.pyplot(plt)
                    success = True
                    break
            except UnicodeDecodeError:
                continue
        if not success:
            st.error("Não foi possível detectar o delimitador ou a codificação do arquivo. Tente outro arquivo.")

elif option == 'Inserir Manualmente':
    st.sidebar.header('Insira as informações necessárias')
    country = st.sidebar.text_input('País')
    lat = st.sidebar.number_input('Latitude', format="%.6f")
    lon = st.sidebar.number_input('Longitude', format="%.6f")
    depth_mean = st.sidebar.number_input('Profundidade Média', format="%.2f")

    species = st.sidebar.selectbox('Espécie', [
        'Montastraea annularis',
        'Acropora',
        'Acropora palmata',
        'Montastraea sp. (= annularis complex)',
        'Porites',
        'Pocillopora',
        'Montastraea faveolata',
        'Outros'
    ])

    family = st.sidebar.selectbox('Família', [
        'Acroporidae',
        'Poritidae',
        'Faviidae',
        'Pocilloporidae',
        'Siderastreidae',
        'Agariciidae',
        'Outros'
    ])

    if st.sidebar.button('Prever'):
        user_data = process_user_input(country, lat, lon, depth_mean, species, family)
        
        # Remover a coluna 'COUNTRY' se ela estiver presente no DataFrame
        if 'COUNTRY' in user_data.columns:
            user_data = user_data.drop(columns=['COUNTRY'])
        
        # Fazer previsões
        prediction = model.predict(user_data)
        probabilities = model.predict_proba(user_data)

        st.write(f'Previsão de SEVERITY_CODE: {prediction[0]}')
        st.write('Probabilidades de cada classe:')
        for i, prob in enumerate(probabilities[0]):
            st.write(f'Classe {i}: {prob * 100:.2f}%')

        # Seção: Visualização de Dados
        st.subheader('Visualização de Dados')

        # Importância das variáveis
        importances = model.feature_importances_
        features = user_data.columns

        # Criar um DataFrame para facilitar a visualização
        feature_importances = pd.DataFrame({'Feature': features, 'Importance': importances})

        # Ordenar por importância
        feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

        # Plotar a importância das variáveis
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Feature', data=feature_importances)
        plt.title('Importância das Variáveis')
        plt.xlabel('Importância')
        plt.ylabel('Variável')
        st.pyplot(plt)
