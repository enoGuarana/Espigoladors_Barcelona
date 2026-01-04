import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Espigoladors Data Platform", layout="wide")

# --- BANCO DE DADOS SIMULADO (CSV) ---
DB_FILE = 'dados_espigoladors.csv'

def carregar_dados():
    try:
        return pd.read_csv(DB_FILE)
    except FileNotFoundError:
        # Cria um DataFrame vazio se o arquivo não existir
        return pd.DataFrame(columns=["Data", "Escola", "Alimento", "Peso_KG", "Metodo_Entrada"])

def salvar_dados(novo_dado):
    df = carregar_dados()
    novo_df = pd.DataFrame([novo_dado])
    # Concatena e salva
    df_final = pd.concat([df, novo_df], ignore_index=True)
    df_final.to_csv(DB_FILE, index=False)
    return df_final

# --- FUNÇÃO DE IA (SIMULADA PARA DEMO) ---
def processar_imagem_mock(imagem):
    """
    Simula o processamento de uma imagem pela OpenAI.
    Retorna dados fictícios para a demonstração na ONG não falhar.
    """
    time.sleep(2.5) # Fingindo que a IA está pensando
    return {
        "Data": datetime.now().strftime("%Y-%m-%d"),
        "Escola": "Escola Pau Casals (Detectado)",
        "Alimento": "Laranjas e Frutas Variadas",
        "Peso_KG": 45.5,
        "Metodo_Entrada": "IA Vision (OCR)"
    }

# --- INTERFACE (FRONTEND) ---
st.title("🥦 Espigoladors: Plataforma de Gestão Inteligente")
st.markdown("**Solução integrada para coleta, digitalização e análise de desperdício alimentar.**")

# Abas de Navegação
tab1, tab2, tab3 = st.tabs(["📝 Entrada Manual", "📸 Escanear Prancheta (IA)", "📊 Dashboard Gerencial"])

# --- ABA 1: MANUAL ---
with tab1:
    st.header("Nova Coleta Manual")
    col1, col2 = st.columns(2)
    
    with col1:
        escola_in = st.selectbox("Selecione a Escola", ["Escola Pau Casals", "Instituto Salvador Dalí", "Escola Joan Miró", "Centre Educatiu Poblenou"])
        alimento_in = st.text_input("Tipo de Alimento", "Pão")
    
    with col2:
        peso_in = st.number_input("Peso Resgatado (KG)", min_value=0.0, step=0.5)
        data_in = st.date_input("Data da Coleta")
        
    if st.button("💾 Salvar Registro Manual", use_container_width=True):
        novo = {
            "Data": data_in, "Escola": escola_in, 
            "Alimento": alimento_in, "Peso_KG": peso_in, 
            "Metodo_Entrada": "App Manual"
        }
        salvar_dados(novo)
        st.success("Registro salvo com sucesso!")

# --- ABA 2: IA / OCR ---
with tab2:
    st.header("Digitalização Inteligente")
    st.info("Tire uma foto da folha de controle manual. A IA extrairá os dados automaticamente.")
    
    # No iPad, isso abre a opção de Câmera nativa
    foto = st.file_uploader("Tirar Foto da Prancheta", type=["jpg", "png", "jpeg"])
    
    if foto:
        st.image(foto, caption="Imagem Carregada", width=300)
        
        if st.button("⚡ Processar com IA", type="primary"):
            with st.spinner("Analisando manuscrito com Vision AI..."):
                # Chama a função simulada
                dados_ai = processar_imagem_mock(foto)
                
                st.success("Dados Extraídos com Sucesso!")
                st.json(dados_ai) # Mostra o JSON bonitinho
                
                # Botão para confirmar
                if st.button("Confirmar e Integrar ao Banco de Dados"):
                    salvar_dados(dados_ai)
                    st.balloons()
                    st.success("Digitalização concluída!")

# --- ABA 3: DASHBOARD ---
with tab3:
    st.header("Painel de Controle em Tempo Real")
    df = carregar_dados()
    
    if not df.empty:
        # Métricas no topo
        total = df["Peso_KG"].sum()
        media = df["Peso_KG"].mean()
        contagem = len(df)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Resgatado (KG)", f"{total:.1f} kg", "+15% vs semana passada")
        m2.metric("Média por Coleta", f"{media:.1f} kg")
        m3.metric("Total de Registros", contagem)
        
        st.divider()
        
        # Gráficos Lado a Lado
        g1, g2 = st.columns(2)
        
        with g1:
            st.subheader("Desperdício por Escola")
            fig_bar = px.bar(df, x="Escola", y="Peso_KG", color="Alimento", text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with g2:
            st.subheader("Tendência Temporal")
            df["Data"] = pd.to_datetime(df["Data"]) # Garante formato data
            df_sorted = df.sort_values("Data")
            fig_line = px.line(df_sorted, x="Data", y="Peso_KG", markers=True)
            st.plotly_chart(fig_line, use_container_width=True)
            
        with st.expander("Ver Dados Brutos (Tabela)"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("Ainda não há dados. Use as abas anteriores para adicionar.")
