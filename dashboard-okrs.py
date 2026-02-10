import streamlit as st
import pandas as pd

# ─── Page Config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="OKRs PagBrasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Autenticação ────────────────────────────────────────────────────
def check_password():
    """Retorna True se o usuário digitou a senha correta."""

    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown(
            '<div style="text-align:center;padding:100px 0;">'
            '<h1 style="color:#34D399;">🔒 OKRs PagBrasil</h1>'
            '<p style="color:#6B7B94;">Acesso restrito — Digite a senha</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False

    elif not st.session_state["password_correct"]:
        st.markdown(
            '<div style="text-align:center;padding:100px 0;">'
            '<h1 style="color:#34D399;">🔒 OKRs PagBrasil</h1>'
            '<p style="color:#6B7B94;">Acesso restrito — Digite a senha</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("😕 Senha incorreta. Tente novamente.")
        return False

    return True


if not check_password():
    st.stop()


# ─── Constants ───────────────────────────────────────────────────────
STATUS_COLORS = {"green": "#34D399", "yellow": "#FBBF24", "red": "#F87171"}
STATUS_LABELS = {"green": "On Track", "yellow": "Atenção", "red": "Em Risco"}

# ─── Data ────────────────────────────────────────────────────────────
OKRS = [
    {
        "title": "CRESCIMENTO",
        "subtitle": "Impulsionar o crescimento sustentável e rentável",
        "accent": "#0058B5",
        "status": "green",
        "chart": [8.1, 8.5, 9.2, 9.0, 9.8, 10.2, 10.5, 11.0, 11.3, 11.8, 12.0, 12.4],
        "krs": [
            {"name": "Receita", "val": "R$ 12.4M", "ant": "R$ 11.8M", "meta": "R$ 12.0M", "pct": 100},
            {"name": "Receita Nacional (NB)", "val": "R$ 8.7M", "ant": "R$ 8.2M", "meta": "R$ 8.5M", "pct": 100},
            {"name": "Receita Internacional (XB)", "val": "R$ 3.7M", "ant": "R$ 3.5M", "meta": "R$ 4.0M", "pct": 93},
        ],
    },
    {
        "title": "INOVAÇÃO / PRODUTO",
        "subtitle": "Consolidar liderança em inovação e diferenciação",
        "accent": "#4B36F8",
        "status": "green",
        "chart": [1.2, 1.4, 1.6, 1.8, 2.0, 2.1, 2.3, 2.5, 2.7, 2.8, 2.9, 3.1],
        "krs": [
            {"name": "Receita prod. < 24 meses", "val": "R$ 3.1M", "ant": "R$ 2.9M", "meta": "R$ 3.0M", "pct": 100},
            {"name": "% clientes c/ novos prod.", "val": "34%", "ant": "31%", "meta": "35%", "pct": 97},
            {"name": "% clientes c/ novas func.", "val": "28%", "ant": "25%", "meta": "30", "pct": 93},
            {"name": "Taxa de Falhas Críticas", "val": "0.12%", "ant": "0.15%", "meta": "≤ 0.10%", "pct": 83},
            {"name": "Índice inovação percebida", "val": "8.1", "ant": "7.8", "meta": "8.0", "pct": 100},
            {"name": "Taxa de conversão", "val": "72.5%", "ant": "70.1%", "meta": "72.0%", "pct": 100},
        ],
    },
    {
        "title": "EXCELÊNCIA OPERACIONAL",
        "subtitle": "Elevar a excelência operacional e eficiência",
        "accent": "#FFB035",
        "status": "yellow",
        "chart": [310, 305, 298, 295, 290, 288, 285, 283, 280, 282, 284, 285],
        "krs": [
            {"name": "Receita por pessoa", "val": "R$ 285K", "ant": "R$ 290K", "meta": "R$ 300K", "pct": 95},
            {"name": "Tempo onboarding NB", "val": "12 dias", "ant": "14 dias", "meta": "≤ 10 dias", "pct": 83},
            {"name": "Tempo onboarding XB", "val": "18 dias", "ant": "20 dias", "meta": "≤ 15 dias", "pct": 83},
            {"name": "% processos documentados", "val": "67%", "ant": "62%", "meta": "75%", "pct": 89},
        ],
    },
    {
        "title": "PESSOAS",
        "subtitle": "Desenvolver pessoas e lideranças para o próximo ciclo",
        "accent": "#54CA30",
        "status": "green",
        "chart": [58, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72],
        "krs": [
            {"name": "Índice de engajamento", "val": "81%", "ant": "78%", "meta": "80%", "pct": 100},
            {"name": "% de certificação interna", "val": "63%", "ant": "58%", "meta": "70%", "pct": 90},
            {"name": "eNPS", "val": "72", "ant": "68", "meta": "70", "pct": 100},
            {"name": "Pontuação GPTW", "val": "84", "ant": "81", "meta": "85", "pct": 99},
        ],
    },
    {
        "title": "CLIENTES",
        "subtitle": "Garantir experiências fluidas que impulsionem satisfação",
        "accent": "#007BFF",
        "status": "red",
        "chart": [72, 71, 70, 69, 70, 69, 68, 69, 68, 67, 68, 68],
        "krs": [
            {"name": "NPS", "val": "+68", "ant": "+71", "meta": "+75", "pct": 91},
            {"name": "% Contas Não Ativadas", "val": "15%", "ant": "17%", "meta": "≤ 10%", "pct": 67},
            {"name": "MRR Churn Rate", "val": "1.8%", "ant": "2.1%", "meta": "≤ 1.5%", "pct": 83},
            {"name": "% atendimentos no SLA", "val": "94%", "ant": "92%", "meta": "97%", "pct": 97},
            {"name": "Taxa de chargeback", "val": "R$ 142K", "ant": "R$ 155K", "meta": "≤ R$ 120K", "pct": 85},
            {"name": "CSAT", "val": "4.3/5", "ant": "4.2/5", "meta": "4.5/5", "pct": 96},
            {"name": "Indicador de branding", "val": "—", "ant": "—", "meta": "A definir", "pct": 0},
            {"name": "Nº solic./contas ativas", "val": "0.32", "ant": "0.35", "meta": "≤ 0.25", "pct": 78},
        ],
    },
]

# ─── Helpers ─────────────────────────────────────────────────────────
def pct_color(pct: int) -> str:
    if pct >= 95:
        return "#34D399"
    if pct >= 70:
        return "#FBBF24"
    return "#F87171"


def okr_status_from_krs(krs: list[dict]) -> str:
    pcts = [kr.get("pct", 0) for kr in krs if kr.get("pct", 0) > 0]
    if not pcts:
        return "yellow"
    if any(p < 70 for p in pcts):
        return "red"
    if any(p < 95 for p in pcts):
        return "yellow"
    return "green"


def open_okr(idx: int):
    st.session_state["selected_okr"] = idx


def close_okr():
    st.session_state["selected_okr"] = None


# ─── Dialog (NÚMEROS EM CIMA, GRÁFICO EMBAIXO) ───────────────────────
@st.dialog("Detalhes do OKR", width="large")
def okr_dialog(okr: dict, idx: int):
    accent = okr["accent"]
    status = okr_status_from_krs(okr["krs"])
    sc = STATUS_COLORS[status]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(160deg, #181D2C 0%, #141822 100%);
            border: 1px solid #2B3350;
            border-left: 6px solid {accent};
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 12px;
        ">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
            <div>
              <div style="color:{accent};font-weight:800;letter-spacing:1.3px;font-size:0.85rem;">
                {okr["title"]}
              </div>
              <div style="color:#6B7B94;margin-top:6px;line-height:1.35;">
                {okr["subtitle"]}
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;white-space:nowrap;">
              <span style="width:10px;height:10px;border-radius:50%;background:{sc};display:inline-block;"></span>
              <span style="color:#9DB2CC;font-size:0.85rem;">{STATUS_LABELS[status]}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Key Results")
    for kr in okr["krs"]:
        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pct_text = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"
        st.markdown(
            f"""
            <div style="padding:10px 6px;border-top:1px solid rgba(255,255,255,0.06);">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
                <span style="color:#8090A8;font-size:0.85rem;font-weight:600;">{kr["name"]}</span>
                <span style="color:#FFF;font-size:0.95rem;font-weight:800;white-space:nowrap;">{kr["val"]}</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <div style="flex:1;height:4px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;">
                  <div style="width:{w}%;height:100%;background:{pc};"></div>
                </div>
                <span style="min-width:36px;text-align:right;color:{pc};font-weight:800;font-size:0.8rem;">{pct_text}</span>
              </div>
              <div style="color:#4A5670;font-size:0.75rem;">Ant: {kr["ant"]} · Meta: {kr["meta"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    series = okr.get("chart", [])
    df = pd.DataFrame({"Mês": months[: len(series)], "Valor": series})

    st.subheader("Evolução (últimos 12 meses)")
    st.line_chart(df, x="Mês", y="Valor", use_container_width=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    if st.button("Fechar", use_container_width=True, key=f"close_{idx}"):
        close_okr()
        st.rerun()


# ─── Session State: open dialog if selected ───────────────────────────
if "selected_okr" not in st.session_state:
    st.session_state["selected_okr"] = None

if st.session_state["selected_okr"] is not None:
    i = int(st.session_state["selected_okr"])
    if 0 <= i < len(OKRS):
        okr_dialog(OKRS[i], i)

# ─── CSS ─────────────────────────────────────────────────────────────
st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');

/* === GLOBAL === */
.stApp {
    background: radial-gradient(ellipse at 12% 8%, #141B2D 0%, #0F1117 50%, #0B0E14 100%);
    font-family: 'Nunito', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1500px; }
[data-testid="stHorizontalBlock"] { gap: 1.1rem; align-items: stretch; }
[data-testid="stColumn"] > div,
[data-testid="stColumn"] > div > div { height: 100%; }

/* (opcional) esconde ícones de expandir do Streamlit */
[data-testid="stElementToolbar"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* === HEADER === */
.hdr {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #1C2132;
}
.hdr-title {
    font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #FFF;
    margin: 0;
    letter-spacing: -0.3px;
}
.hdr-sub{
    font-size: 1.7rem;
    font-weight: 800;
    line-height: 1.05;
    margin-top: 0;
    color: rgba(246,246,246,0.92);
    font-family: 'Montserrat','Segoe UI',system-ui,sans-serif;
    letter-spacing: -0.3px;
}
.hdr-logo-right{
  height: 48px;
  width: auto;
  opacity: 0.95;
  background: transparent;
  border: none;
  padding: 0;
  border-radius: 0;
  margin-left: 12px;
}

/* === SUMMARY === */
.sum-row { display: flex; gap: 0.8rem; margin-bottom: 1.4rem; }
.sum-card {
    flex: 1;
    background: rgba(255,255,255,0.035);
    border: 1px solid #1C2132;
    border-radius: 12px;
    padding: 14px 0;
    text-align: center;
    transition: background 0.2s;
}
.sum-card:hover { background: rgba(255,255,255,0.06); }
.sum-val { font-size: 1.5rem; font-weight: 800; color: #FFF; }
.sum-lbl {
    font-size: 0.68rem;
    color: #5E6E85;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 2px;
}

/* === OKR CARD === */
.okr-card {
    background: linear-gradient(160deg, #181D2C 0%, #141822 100%);
    border: 1px solid #232940;
    border-radius: 16px;
    padding: 20px 20px 16px;
    height: 420px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}
.okr-card:hover { transform: translateY(-3px); border-color: #384060; box-shadow: 0 16px 48px rgba(0,0,0,0.4); }

/* cabeçalho do card com botão */
.c-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 4px; }
.c-head-left { display:flex; align-items:center; gap:10px; min-width:0; }
.c-title { font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
.c-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; flex-shrink: 0; animation: dot-pulse 2.5s ease-in-out infinite; }
@keyframes dot-pulse {
    0%, 100% { box-shadow: 0 0 4px 1px currentColor; }
    50% { box-shadow: 0 0 12px 3px currentColor; }
}
.c-sub { color: #6B7B94; font-size: 0.76rem; margin-bottom: 14px; line-height: 1.35; }

/* estilo do botão "Veja mais" do Streamlit (só dentro do card) */
.card-action [data-testid="stButton"] button{
    border-radius: 999px !important;
    padding: 6px 12px !important;
    font-size: 0.75rem !important;
    font-weight: 800 !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    color: rgba(246,246,246,0.92) !important;
    line-height: 1 !important;
}
.card-action [data-testid="stButton"] button:hover{
    background: rgba(255,255,255,0.10) !important;
    border-color: rgba(255,255,255,0.28) !important;
}

/* Card body */
.c-body { display: grid; grid-template-columns: 1fr; gap: 12px; flex: 1; min-height: 0; }
.c-krs { display: flex; flex-direction: column; overflow-y: auto; padding-right: 6px; }
.c-krs::-webkit-scrollbar { width: 4px; }
.c-krs::-webkit-scrollbar-track { background: transparent; }
.c-krs::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 2px; }
.c-krs::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

/* KR row */
.kr { padding: 9px 0 8px; border-top: 1px solid rgba(255,255,255,0.05); }
.kr:first-child { border-top: none; padding-top: 0; }
.kr-top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
.kr-nm { color: #8090A8; font-size: 0.76rem; font-weight: 500; }
.kr-vl { color: #FFF; font-size: 0.92rem; font-weight: 700; white-space: nowrap; }
.kr-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
.kr-track { flex: 1; height: 3px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; }
.kr-fill { height: 100%; border-radius: 2px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); }
.kr-pct { font-size: 0.68rem; font-weight: 600; min-width: 30px; text-align: right; }
.kr-meta { color: #4A5670; font-size: 0.65rem; letter-spacing: 0.2px; }

/* === FOOTER === */
.ftr {
    text-align: center;
    color: #3D4A60;
    font-size: 0.72rem;
    padding-top: 1.2rem;
    margin-top: 1.8rem;
    border-top: 1px solid #1C2132;
    letter-spacing: 0.5px;
}

/* === RESPONSIVE === */
@media (max-width: 1100px) { .hdr { flex-direction: column; align-items: flex-start; gap: 0.8rem; } }
@media (max-width: 768px) {
    .sum-row { flex-wrap: wrap; }
    .sum-card { min-width: 45%; }
    .hdr-title { font-size: 1.3rem; }
    .block-container { padding-top: 1.2rem; }
}
</style>""",
    unsafe_allow_html=True,
)

# ─── Header ──────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hdr">
    <div>
        <div class="hdr-title">OKRs Estratégicos</div>
        <div class="hdr-sub">PagBrasil &middot; Indicadores de Performance</div>
    </div>
    <img class="hdr-logo-right" src="https://i.imgur.com/CYyv2PD.png" alt="PagBrasil" />
</div>
""",
    unsafe_allow_html=True,
)

# ─── Summary Metrics ─────────────────────────────────────────────────
total_krs = sum(len(o["krs"]) for o in OKRS)
okr_statuses = [okr_status_from_krs(o["krs"]) for o in OKRS]
on_track = sum(1 for s in okr_statuses if s == "green")
attention = sum(1 for s in okr_statuses if s == "yellow")
at_risk = sum(1 for s in okr_statuses if s == "red")
valid_pcts = [kr["pct"] for o in OKRS for kr in o["krs"] if kr.get("pct", 0) > 0]
avg_pct = round(sum(valid_pcts) / len(valid_pcts)) if valid_pcts else 0

st.markdown(
    f"""
<div class="sum-row">
    <div class="sum-card">
        <div class="sum-val">{total_krs}</div>
        <div class="sum-lbl">Key Results</div>
    </div>
    <div class="sum-card">
        <div class="sum-val" style="color:#34D399">{on_track}</div>
        <div class="sum-lbl">On Track</div>
    </div>
    <div class="sum-card">
        <div class="sum-val" style="color:#FBBF24">{attention}</div>
        <div class="sum-lbl">Atenção</div>
    </div>
    <div class="sum-card">
        <div class="sum-val" style="color:#F87171">{at_risk}</div>
        <div class="sum-lbl">Em Risco</div>
    </div>
    <div class="sum-card">
        <div class="sum-val">{avg_pct}%</div>
        <div class="sum-lbl">Progresso Médio</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ─── Card Renderer ───────────────────────────────────────────────────
def render_card(okr: dict, idx: int) -> None:
    accent = okr["accent"]
    status = okr_status_from_krs(okr["krs"])
    sc = STATUS_COLORS[status]

    rows = ""
    for kr in okr["krs"]:
        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pct_text = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"
        rows += (
            f'<div class="kr">'
            f'  <div class="kr-top">'
            f'    <span class="kr-nm">{kr["name"]}</span>'
            f'    <span class="kr-vl">{kr["val"]}</span>'
            f'  </div>'
            f'  <div class="kr-bar-row">'
            f'    <div class="kr-track">'
            f'      <div class="kr-fill" style="width:{w}%;background:{pc}"></div>'
            f'    </div>'
            f'    <span class="kr-pct" style="color:{pc}">{pct_text}</span>'
            f'  </div>'
            f'  <div class="kr-meta">Ant: {kr["ant"]}  ·  Meta: {kr["meta"]}</div>'
            f'</div>'
        )

    # layout do topo do card (titulo + sinaleira)
    st.markdown(
        f"""
        <div class="okr-card" style="border-left:4px solid {accent};">
          <div class="c-head">
            <div class="c-head-left">
              <span class="c-title" style="color:{accent}">{okr["title"]}</span>
              <span class="c-dot" style="background:{sc};color:{sc}"></span>
            </div>
            <div class="card-action" id="card-action-{idx}"></div>
          </div>
          <div class="c-sub">{okr["subtitle"]}</div>
          <div class="c-body">
            <div class="c-krs">{rows}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # botão "Veja mais" (fica ao lado do título)
    # (renderizado depois, mas posicionado no topo via HTML slot acima)
    # solução simples: renderiza o botão logo após o card e usa CSS pra ficar estilizado;
    # fica visualmente no card porque o Streamlit coloca no fluxo, então usamos container abaixo.
    with st.container():
        # um container só pra aplicar a classe do CSS no botão
        st.markdown('<div class="card-action">', unsafe_allow_html=True)
        if st.button("Veja mais", key=f"open_{idx}"):
            open_okr(idx)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ─── Layout: Row 1 (3 cards) ────────────────────────────────────────
row1 = st.columns(3)
for i in range(3):
    with row1[i]:
        render_card(OKRS[i], i)

st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

# ─── Layout: Row 2 (2 cards centered) ───────────────────────────────
_, col_p, col_c, _ = st.columns([0.5, 1, 1, 0.5])
with col_p:
    render_card(OKRS[3], 3)
with col_c:
    render_card(OKRS[4], 4)

# ─── Footer ──────────────────────────────────────────────────────────
st.markdown(
    """
<div class="ftr">
    PagBrasil &nbsp;·&nbsp; Dashboard Estratégico de OKRs &nbsp;·&nbsp; People &amp; Development
</div>
""",
    unsafe_allow_html=True,
)
