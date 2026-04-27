import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Desigualdades Raciais no Mercado de Trabalho - Brasil 2021",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# CARREGAMENTO DOS DADOS COM CACHE
# ------------------------------
@st.cache_data
def load_data():
    """Cria o DataFrame final com os dados do IBGE (PNAD Contínua 2021)"""
    dados_finais = {
        'Caracteristicas': [
            'Total', 'Sem instrução ou Ensino Fundamental incompleto',
            'Ensino Fundamental completo ou Ensino Médio incompleto',
            'Ensino Médio completo ou Ensino Superior Incompleto',
            'Ensino Superior completo',
            'Branca', 'Preta', 'Parda', 'Preta ou parda'
        ],
        'Pop_idade_trabalhar': [171714, 53722, 29365, 61268, 27359, 74715, 16569, 78735, 95304],
        'Pop_forca_trabalho': [104070, 21742, 15894, 44284, 22150, 45569, 10656, 46815, 57471],
        'Pop_ocupada': [89495, 18793, 12839, 37291, 20572, 40432, 8900, 39224, 48124],
        'Pop_trab_formal': [53619, 7117, 6182, 24195, 16125, 27221, 5035, 20788, 25823],
        'Pop_desocupada': [14575, 2948, 3055, 6994, 1578, 5137, 1756, 7591, 9347],
        'Pop_forca_potencial': [10524, 3555, 2468, 3711, 791, 3280, 1121, 6025, 7147],
        'Pop_subutilizada': [32652, 8824, 6902, 13496, 3431, 10968, 3769, 17656, 21425],
        'Taxa_participacao': [60.6, 40.5, 54.1, 72.3, 81.0, 61.0, 64.3, 59.5, 60.3],
        'Nivel_ocupacao': [52.1, 35.0, 43.7, 60.9, 75.2, 54.1, 53.7, 49.8, 50.5],
        'Taxa_formalizacao': [59.9, 37.9, 48.2, 64.9, 78.4, 67.3, 56.6, 53.0, 53.7],
        'Taxa_desocupacao': [14.0, 13.6, 19.2, 15.8, 7.1, 11.3, 16.5, 16.2, 16.3],
        'Taxa_subutilizacao': [28.5, 34.9, 37.6, 28.1, 15.0, 22.5, 32.0, 33.4, 33.2]
    }
    df = pd.DataFrame(dados_finais)
    return df

@st.cache_data
def load_educacao_data():
    """Dados de formalização por nível educacional (separados por raça) - construídos manualmente a partir da tabela original"""
    niveis = [
        'Sem instrução ou Fundamental incompleto',
        'Fundamental completo ou Médio incompleto',
        'Médio completo ou Superior incompleto',
        'Superior completo'
    ]
    df_brancos = pd.DataFrame({
        'Nivel': niveis,
        'Taxa_formalizacao': [45.5, 53.8, 70.2, 79.5],
        'Pop_ocupada': [6427, 4777, 16292, 12937],
        'Raca': 'Branca'
    })
    df_negros = pd.DataFrame({
        'Nivel': niveis,
        'Taxa_formalizacao': [33.9, 44.8, 60.8, 76.4],
        'Pop_ocupada': [12228, 7955, 20617, 7325],
        'Raca': 'Negra (preta ou parda)'
    })
    return pd.concat([df_brancos, df_negros], ignore_index=True)

# ------------------------------
# FUNÇÕES DE PLOT (reutilizáveis)
# ------------------------------
def plot_comparacao_geral(df, grupos):
    """Gráfico de barras comparando formalização e desocupação entre grupos raciais"""
    df_filtrado = df[df['Caracteristicas'].isin(grupos)].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtrado['Caracteristicas'],
        y=df_filtrado['Taxa_formalizacao'],
        name='Formalização (%)',
        marker_color='#2ecc71',
        text=df_filtrado['Taxa_formalizacao'].round(1),
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=df_filtrado['Caracteristicas'],
        y=df_filtrado['Taxa_desocupacao'],
        name='Desocupação (%)',
        marker_color='#e74c3c',
        text=df_filtrado['Taxa_desocupacao'].round(1),
        textposition='outside'
    ))
    fig.update_layout(
        title='Comparação de Indicadores por Raça (2021)',
        xaxis_title='Grupo Racial',
        yaxis_title='Taxa (%)',
        barmode='group',
        template='plotly_white',
        height=500
    )
    return fig

def plot_formalizacao_por_educacao(df_educ):
    """Gráfico de linhas mostrando evolução da formalização por nível educacional"""
    fig = go.Figure()
    for raca in df_educ['Raca'].unique():
        subset = df_educ[df_educ['Raca'] == raca]
        fig.add_trace(go.Scatter(
            x=subset['Nivel'],
            y=subset['Taxa_formalizacao'],
            mode='lines+markers+text',
            name=raca,
            text=subset['Taxa_formalizacao'].round(1),
            textposition='top center',
            marker=dict(size=10)
        ))
    fig.update_layout(
        title='Taxa de Formalização por Nível de Instrução e Raça',
        xaxis_title='Nível de Instrução',
        yaxis_title='Taxa de Formalização (%)',
        template='plotly_white',
        height=500
    )
    return fig

# ------------------------------
# MAIN - INTERFACE STREAMLIT
# ------------------------------
def main():
    st.title("📊 Desigualdades Raciais no Mercado de Trabalho Brasileiro")
    st.markdown("**Fonte:** PNAD Contínua - IBGE (2021) | Dados reais sobre formalização, desocupação e subutilização da força de trabalho.")

    # Carregar dados
    df = load_data()
    df_educ = load_educacao_data()

    # Sidebar com controles
    st.sidebar.header("🔍 Filtros e Configurações")
    grupos_disponiveis = ['Branca', 'Preta', 'Parda', 'Preta ou parda']
    grupos_selecionados = st.sidebar.multiselect(
        "Selecione os grupos raciais para comparar:",
        grupos_disponiveis,
        default=['Branca', 'Preta ou parda']
    )

    if not grupos_selecionados:
        st.warning("Selecione pelo menos um grupo racial na barra lateral.")
        st.stop()

    # Abas para organizar o conteúdo
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Comparação Geral", 
        "🎓 Impacto da Educação", 
        "📋 Relatório Detalhado",
        "📊 Dados Brutos"
    ])

    with tab1:
        st.subheader("Desigualdades nos principais indicadores")
        fig1 = plot_comparacao_geral(df, grupos_selecionados)
        st.plotly_chart(fig1, use_container_width=True)

        # Exibir números em métricas
        col1, col2, col3 = st.columns(3)
        branca = df[df['Caracteristicas'] == 'Branca'].iloc[0] if 'Branca' in df['Caracteristicas'].values else None
        negra = df[df['Caracteristicas'] == 'Preta ou parda'].iloc[0]

        if branca is not None:
            with col1:
                st.metric("Formalização - Brancos", f"{branca['Taxa_formalizacao']:.1f}%")
                st.metric("Formalização - Negros", f"{negra['Taxa_formalizacao']:.1f}%",
                          delta=f"{branca['Taxa_formalizacao'] - negra['Taxa_formalizacao']:.1f} p.p.")
            with col2:
                st.metric("Desocupação - Brancos", f"{branca['Taxa_desocupacao']:.1f}%")
                st.metric("Desocupação - Negros", f"{negra['Taxa_desocupacao']:.1f}%",
                          delta=f"{negra['Taxa_desocupacao'] - branca['Taxa_desocupacao']:.1f} p.p.", delta_color="inverse")
            with col3:
                st.metric("Subutilização - Brancos", f"{branca['Taxa_subutilizacao']:.1f}%")
                st.metric("Subutilização - Negros", f"{negra['Taxa_subutilizacao']:.1f}%",
                          delta=f"{negra['Taxa_subutilizacao'] - branca['Taxa_subutilizacao']:.1f} p.p.", delta_color="inverse")

    with tab2:
        st.subheader("A educação reduz a desigualdade, mas não a elimina")
        fig2 = plot_formalizacao_por_educacao(df_educ)
        st.plotly_chart(fig2, use_container_width=True)

        st.info("""
        **Análise**: Mesmo entre trabalhadores com Ensino Superior completo, negros têm formalização menor (76,4% vs 79,5% dos brancos).  
        A diferença persiste em todos os níveis, indicando fatores estruturais além da educação.
        """)

        # Gap por nível
        niveis = df_educ['Nivel'].unique()
        gap_data = []
        for nivel in niveis:
            branco_val = df_educ[(df_educ['Raca']=='Branca') & (df_educ['Nivel']==nivel)]['Taxa_formalizacao'].values[0]
            negro_val = df_educ[(df_educ['Raca']=='Negra (preta ou parda)') & (df_educ['Nivel']==nivel)]['Taxa_formalizacao'].values[0]
            gap_data.append({'Nível': nivel, 'Gap (p.p.)': branco_val - negro_val})
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True)

    with tab3:
        st.subheader("Relatório Executivo das Desigualdades")
        if st.checkbox("Mostrar relatório completo"):
            st.markdown("""
            ### 1. Contexto
            Análise da PNAD Contínua 2021, comparando população branca e negra (pretos+ pardos).

            ### 2. Principais Desigualdades
            - **Formalização**: Brancos 67,3% | Negros 53,7% → **Gap de 13,6 p.p.**  
            - **Desocupação**: Brancos 11,3% | Negros 16,3% → **44% maior** entre negros  
            - **Subutilização**: Brancos 22,5% | Negros 33,2% → **Gap de 10,7 p.p.**

            ### 3. Impacto da Educação
            O gap de formalização diminui com a escolaridade, mas não desaparece:
            - Sem instrução: 11,6 p.p.  
            - Superior completo: 3,1 p.p. (ainda significativo)

            ### 4. Impacto de políticas públicas
            Se a formalização negra alcançasse o nível da branca, **+6,5 milhões** de trabalhadores negros passariam a ter emprego formal.

            ### 5. Recomendações
            - Políticas afirmativas para formalização de negros  
            - Fiscalização antirracista em todos os níveis de qualificação  
            - Metas anuais específicas por raça
            """)

        # Cálculo do impacto potencial (dinâmico)
        st.subheader("💰 Impacto Potencial de Políticas Públicas")
        pop_negra_ocupada = negra['Pop_ocupada']
        gap_formal = branca['Taxa_formalizacao'] - negra['Taxa_formalizacao'] if branca is not None else 0
        formais_adicionais = pop_negra_ocupada * (gap_formal / 100)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("População negra ocupada", f"{pop_negra_ocupada:,.0f}")
            st.metric("Gap de formalização", f"{gap_formal:.1f} p.p.")
        with col_b:
            st.metric("Trabalhadores negros adicionais em empregos formais", 
                      f"{formais_adicionais:,.0f}", 
                      delta="se igualar à taxa dos brancos")

    with tab4:
        st.subheader("Base de dados completa (PNAD Contínua 2021 - tratada)")
        st.dataframe(df, use_container_width=True)
        st.download_button(
            label="📥 Baixar dados como CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='desigualdade_racial_2021.csv',
            mime='text/csv'
        )

    # Rodapé com explicação técnica
    st.markdown("---")
    st.caption("Projeto desenvolvido por Luara Maciel | Dados oficiais do IBGE | Visualizações interativas com Plotly.")

if __name__ == "__main__":
    main()