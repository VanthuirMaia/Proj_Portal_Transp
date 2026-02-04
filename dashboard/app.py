import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Portal Transparência - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Caminho do banco
db_path = Path("../data/warehouse/portal_transparencia.duckdb")

# Conexão com DuckDB
@st.cache_resource
def get_connection():
    return duckdb.connect(str(db_path), read_only=True)

con = get_connection()

# Título
st.title("📊 Dashboard - Portal da Transparência")
st.markdown("Análise de despesas por órgão do Governo Federal")

# Métricas principais
st.header("📈 Visão Geral")

col1, col2, col3 = st.columns(3)

# Total empenhado
total_empenhado = con.execute("""
    SELECT SUM(valor_empenhado) as total
    FROM fct_despesas
""").fetchone()[0]

col1.metric("Total Empenhado", f"R$ {total_empenhado:,.2f}")

# Total liquidado
total_liquidado = con.execute("""
    SELECT SUM(valor_liquidado) as total
    FROM fct_despesas
""").fetchone()[0]

col2.metric("Total Liquidado", f"R$ {total_liquidado:,.2f}")

# Total pago
total_pago = con.execute("""
    SELECT SUM(valor_pago) as total
    FROM fct_despesas
""").fetchone()[0]

col3.metric("Total Pago", f"R$ {total_pago:,.2f}")

# Top 10 órgãos
st.header("🏛️ Top 10 Órgãos por Despesa")

df_top10 = con.execute("""
    SELECT 
        d.nome_orgao,
        SUM(f.valor_empenhado) as empenhado,
        SUM(f.valor_liquidado) as liquidado,
        SUM(f.valor_pago) as pago
    FROM fct_despesas f
    INNER JOIN dim_orgaos d ON f.sk_orgao = d.sk_orgao
    GROUP BY d.nome_orgao
    ORDER BY empenhado DESC
    LIMIT 10
""").df()

fig = px.bar(
    df_top10, 
    x='nome_orgao', 
    y='empenhado',
    title='Top 10 Órgãos - Valor Empenhado',
    labels={'empenhado': 'Valor (R$)', 'nome_orgao': 'Órgão'}
)
st.plotly_chart(fig, use_container_width=True)

# Evolução temporal
st.header("📅 Evolução por Ano")

df_evolucao = con.execute("""
    SELECT 
        ano,
        SUM(valor_empenhado) as empenhado,
        SUM(valor_liquidado) as liquidado,
        SUM(valor_pago) as pago
    FROM fct_despesas
    GROUP BY ano
    ORDER BY ano
""").df()

fig2 = px.line(
    df_evolucao,
    x='ano',
    y=['empenhado', 'liquidado', 'pago'],
    title='Evolução das Despesas ao Longo dos Anos',
    labels={'value': 'Valor (R$)', 'ano': 'Ano', 'variable': 'Tipo'}
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
# Rodapé com informações do autor
st.markdown("---")
st.markdown("### 👨‍💻 Sobre o Projeto")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Desenvolvido por: Vanthuir Maia**
    
    Engenheiro de Dados | Especialista em IA Generativa
    
    Pipeline completo de dados públicos do Portal da Transparência:
    - Ingestão automatizada via API REST
    - Transformação e modelagem dimensional (dbt)
    - Testes de qualidade automatizados
    - Visualização interativa (Streamlit + Plotly)
    """)

with col2:
    st.markdown("""
    📧 **Contato:**
    - [LinkedIn](https://www.linkedin.com/in/vanthuir-maia-47767810b/)
    - [GitHub](https://github.com/VanthuirMaia)
    - [WhatsApp](https://wa.me/5587996075897)           
    - vanmaiasf@gmail.com | vanthuir.dev@gmail.com
    """)
st.caption("Dados: Portal da Transparência | Pipeline: Python + dbt + DuckDB")