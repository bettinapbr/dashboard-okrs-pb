import streamlit as st
 
# --- Page Config ---
st.set_page_config(
    page_title="OKRs PagBrasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- AUTENTICAÇÃO ---
def check_password():
    """Retorna True se o usuário digitou a senha correta."""
    
    def password_entered():
        """Verifica se a senha está correta."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style='text-align: center; padding: 100px 0;'>
            <h1 style='color: #2ECC71;'>🔒 OKRs PagBrasil</h1>
            <p style='color: #7B9BAF;'>Acesso restrito - Digite a senha</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "Senha", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: center; padding: 100px 0;'>
            <h1 style='color: #2ECC71;'>🔒 OKRs PagBrasil</h1>
            <p style='color: #7B9BAF;'>Acesso restrito - Digite a senha</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "Senha", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Senha incorreta. Tente novamente.")
        return False
    else:
        return True

if not check_password():
    st.stop()
 
# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
 
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0F1923 0%, #152736 50%, #0F1923 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
 
    /* Hide Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
 
    /* Dashboard Title */
    .dashboard-header {
        text-align: center;
        margin-bottom: 2.5rem;
        position: relative;
    }
    .dashboard-header h1 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 3px;
        margin: 0;
        display: inline-block;
        position: relative;
    }
    .dashboard-header h1::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #2ECC71, #1ABC9C);
        border-radius: 2px;
    }
    .dashboard-subtitle {
        color: #7B9BAF;
        font-size: 0.9rem;
        margin-top: 1rem;
        letter-spacing: 1px;
    }
 
    /* OKR Card */
    .okr-card {
        background: linear-gradient(145deg, #1A3A4A 0%, #15303E 100%);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    .okr-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2ECC71, #1ABC9C);
        border-radius: 16px 16px 0 0;
    }
    .okr-card:hover {
        border-color: rgba(46, 204, 113, 0.35);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
 
    /* Card Title */
    .card-title-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.2rem;
    }
    .card-title-badge {
        background: rgba(214, 232, 236, 0.12);
        border: 1px solid rgba(214, 232, 236, 0.2);
        color: #D6E8EC;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        padding: 6px 14px;
        border-radius: 8px;
    }
    .status-dot {
        width: 10px;
        height: 10px;
        background: #2ECC71;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px rgba(46, 204, 113, 0.5);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 8px rgba(46, 204, 113, 0.5); }
        50% { box-shadow: 0 0 16px rgba(46, 204, 113, 0.8); }
    }
 
    /* KR Row */
    .kr-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        transition: background 0.2s ease;
    }
    .kr-row:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    .kr-name {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.82rem;
        font-weight: 500;
    }
    .kr-value {
        color: #FFFFFF;
        font-size: 0.85rem;
        font-weight: 700;
        white-space: nowrap;
    }
 
    /* Streamlit column gap fix */
    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
        align-items: stretch;
    }
    [data-testid="stColumn"] > div {
        height: 100%;
    }
    [data-testid="stColumn"] > div > div {
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)
 
# --- Data ---
okrs = {
    "CRESCIMENTO": [
        ("Receita", "R$ 12.4M"),
        ("Receita NB", "R$ 8.7M"),
        ("Receita XB", "R$ 3.7M"),
    ],
    "INOVAÇÃO / PRODUTO": [
        ("Receita prod. <24m", "R$ 3.1M"),
        ("% clientes c/ novos produtos", "34%"),
        ("% clientes c/ novas func.", "28%"),
        ("Taxa Falhas Críticas", "0.12%"),
        ("Índice inovação percebida", "8.1"),
        ("Taxa de conversão", "72.5%"),
    ],
    "EXCELÊNCIA OPERACIONAL": [
        ("Receita por pessoa", "R$ 285K"),
        ("Tempo onboarding NB", "12 dias"),
        ("Tempo onboarding XB", "18 dias"),
        ("% processos documentados", "67%"),
    ],
    "PESSOAS": [
        ("Índice de engajamento", "81%"),
        ("% certificação interna", "63%"),
        ("eNPS", "72"),
        ("Pontuação GPTW", "84"),
    ],
    "CLIENTES": [
        ("NPS", "+68"),
        ("% Contas Não Ativadas", "15%"),
        ("MRR Churn Rate", "1.8%"),
        ("% atendimentos no SLA", "94%"),
        ("Taxa chargeback", "R$ 142K"),
        ("CSAT", "4.3/5"),
        ("Indicador branding", "A construir"),
        ("Nº solic./contas ativas", "0.32"),
    ],
}
 
 
def render_card(title: str, krs: list):
    """Render a single OKR card as HTML."""
    kr_html = ""
    for name, value in krs:
        kr_html += f"""
<div class="kr-row">
<span class="kr-name">{name}</span>
<span class="kr-value">{value}</span>
</div>"""
 
    st.markdown(f"""
<div class="okr-card">
<div class="card-title-row">
<span class="card-title-badge">{title}</span>
<span class="status-dot"></span>
</div>
        {kr_html}
</div>
    """, unsafe_allow_html=True)
 
 
# --- Header ---
st.markdown("""
<div class="dashboard-header">
<h1>OKRs PAGBRASIL</h1>
<div class="dashboard-subtitle">PAINEL DE OBJETIVOS E RESULTADOS-CHAVE</div>
</div>
""", unsafe_allow_html=True)
 
# --- Row 1: 3 cards ---
cols1 = st.columns(3)
titles = list(okrs.keys())
 
for i, col in enumerate(cols1):
    with col:
        render_card(titles[i], okrs[titles[i]])
 
# --- Row 2: 2 cards centered ---
spacer_left, col_p, col_c, spacer_right = st.columns([0.5, 1, 1, 0.5])
 
with col_p:
    render_card(titles[3], okrs[titles[3]])
 
with col_c:
    render_card(titles[4], okrs[titles[4]])