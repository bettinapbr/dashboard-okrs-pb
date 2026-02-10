import re

import pandas as pd
import streamlit as st

# â”€â”€â”€ Page Config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(
    page_title="OKRs PagBrasil",
    page_icon="ðŸ“Š",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# â”€â”€â”€ AutenticaÃ§Ã£o â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def check_password():
    """Retorna True se o usuÃ¡rio digitou a senha correta."""

    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown(
            '<div style="text-align:center;padding:100px 0;">'
            '<h1 style="color:#34D399;">ðŸ”’ OKRs PagBrasil</h1>'
            '<p style="color:#6B7B94;">Acesso restrito â€” Digite a senha</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        return False

    elif not st.session_state["password_correct"]:
        st.markdown(
            '<div style="text-align:center;padding:100px 0;">'
            '<h1 style="color:#34D399;">ðŸ”’ OKRs PagBrasil</h1>'
            '<p style="color:#6B7B94;">Acesso restrito â€” Digite a senha</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.text_input("Senha", type="password", on_change=password_entered, key="password")
        st.error("ðŸ˜• Senha incorreta. Tente novamente.")
        return False

    return True


if not check_password():
    st.stop()


# â”€â”€â”€ Constants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
STATUS_COLORS = {"green": "#34D399", "yellow": "#FBBF24", "red": "#F87171"}
STATUS_LABELS = {"green": "On Track", "yellow": "AtenÃ§Ã£o", "red": "Em Risco"}

# â”€â”€â”€ Data â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
OKRS = [
    {
        "title": "CRESCIMENTO",
        "subtitle": "Impulsionar o crescimento sustentÃ¡vel e rentÃ¡vel",
        "accent": "#4A9EFF",
        "status": "green",
        "chart": [8.1, 8.5, 9.2, 9.0, 9.8, 10.2, 10.5, 11.0, 11.3, 11.8, 12.0, 12.4],
        "krs": [
            {"name": "Receita", "val": "R$ 12.4M", "ant": "R$ 11.8M", "meta": "R$ 12.0M", "pct": 100},
            {"name": "Receita Nacional (NB)", "val": "R$ 8.7M", "ant": "R$ 8.2M", "meta": "R$ 8.5M", "pct": 100},
            {"name": "Receita Internacional (XB)", "val": "R$ 3.7M", "ant": "R$ 3.5M", "meta": "R$ 4.0M", "pct": 93},
        ],
    },
    {
        "title": "INOVAÃ‡ÃƒO / PRODUTO",
        "subtitle": "Consolidar lideranÃ§a em inovaÃ§Ã£o e diferenciaÃ§Ã£o",
        "accent": "#A78BFA",
        "status": "green",
        "chart": [1.2, 1.4, 1.6, 1.8, 2.0, 2.1, 2.3, 2.5, 2.7, 2.8, 2.9, 3.1],
        "krs": [
            {"name": "Receita prod. < 24 meses", "val": "R$ 3.1M", "ant": "R$ 2.9M", "meta": "R$ 3.0M", "pct": 100},
            {"name": "% clientes c/ novos prod.", "val": "34%", "ant": "31%", "meta": "35%", "pct": 97},
            {"name": "% clientes c/ novas func.", "val": "28%", "ant": "25%", "meta": "30", "pct": 93},
            {"name": "Taxa de Falhas CrÃ­ticas", "val": "0.12%", "ant": "0.15%", "meta": "â‰¤ 0.10%", "pct": 83},
            {"name": "Ãndice inovaÃ§Ã£o percebida", "val": "8.1", "ant": "7.8", "meta": "8.0", "pct": 100},
            {"name": "Taxa de conversÃ£o", "val": "72.5%", "ant": "70.1%", "meta": "72.0%", "pct": 100},
        ],
    },
    {
        "title": "EXCELÃŠNCIA OPERACIONAL",
        "subtitle": "Elevar a excelÃªncia operacional e eficiÃªncia",
        "accent": "#FBBF24",
        "status": "yellow",
        "chart": [310, 305, 298, 295, 290, 288, 285, 283, 280, 282, 284, 285],
        "krs": [
            {"name": "Receita por pessoa", "val": "R$ 285K", "ant": "R$ 290K", "meta": "R$ 300K", "pct": 95},
            {"name": "Tempo onboarding NB", "val": "12 dias", "ant": "14 dias", "meta": "â‰¤ 10 dias", "pct": 83},
            {"name": "Tempo onboarding XB", "val": "18 dias", "ant": "20 dias", "meta": "â‰¤ 15 dias", "pct": 83},
            {"name": "% processos documentados", "val": "67%", "ant": "62%", "meta": "75%", "pct": 89},
        ],
    },
    {
        "title": "PESSOAS",
        "subtitle": "Desenvolver pessoas e lideranÃ§as para o prÃ³ximo ciclo",
        "accent": "#F472B6",
        "status": "green",
        "chart": [58, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72],
        "krs": [
            {"name": "Ãndice de engajamento", "val": "81%", "ant": "78%", "meta": "80%", "pct": 100},
            {"name": "% de certificaÃ§Ã£o interna", "val": "63%", "ant": "58%", "meta": "70%", "pct": 90},
            {"name": "eNPS", "val": "72", "ant": "68", "meta": "70", "pct": 100},
            {"name": "PontuaÃ§Ã£o GPTW", "val": "84", "ant": "81", "meta": "85", "pct": 99},
        ],
    },
    {
        "title": "CLIENTES",
        "subtitle": "Garantir experiÃªncias fluidas que impulsionem satisfaÃ§Ã£o",
        "accent": "#22D3EE",
        "status": "red",
        "chart": [72, 71, 70, 69, 70, 69, 68, 69, 68, 67, 68, 68],
        "krs": [
            {"name": "NPS", "val": "+68", "ant": "+71", "meta": "+75", "pct": 91},
            {"name": "% Contas NÃ£o Ativadas", "val": "15%", "ant": "17%", "meta": "â‰¤ 10%", "pct": 67},
            {"name": "MRR Churn Rate", "val": "1.8%", "ant": "2.1%", "meta": "â‰¤ 1.5%", "pct": 83},
            {"name": "% atendimentos no SLA", "val": "94%", "ant": "92%", "meta": "97%", "pct": 97},
            {"name": "Taxa de chargeback", "val": "R$ 142K", "ant": "R$ 155K", "meta": "â‰¤ R$ 120K", "pct": 85},
            {"name": "CSAT", "val": "4.3/5", "ant": "4.2/5", "meta": "4.5/5", "pct": 96},
            {"name": "Indicador de branding", "val": "â€”", "ant": "â€”", "meta": "A definir", "pct": 0},
            {"name": "NÂº solic./contas ativas", "val": "0.32", "ant": "0.35", "meta": "â‰¤ 0.25", "pct": 78},
        ],
    },
]

# â”€â”€â”€ Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def pct_color(pct: int) -> str:
    if pct >= 95:
        return "#34D399"
    if pct >= 70:
        return "#FBBF24"
    return "#F87171"

def okr_status_from_krs(krs: list[dict]) -> str:
    """
    Calcula o status do OKR baseado nos KRs.
    Regras:
      - ignora pct == 0 (ex.: 'A definir')
      - se algum pct < 70 => red
      - senÃ£o se algum pct < 95 => yellow
      - senÃ£o => green
    """
    pcts = [kr.get("pct", 0) for kr in krs if kr.get("pct", 0) > 0]
    if not pcts:
        return "yellow"  # fallback quando tudo estiver "A definir"
    if any(p < 70 for p in pcts):
        return "red"
    if any(p < 95 for p in pcts):
        return "yellow"
    return "green"

def kr_status_from_pct(pct: int) -> str:
    if pct >= 95:
        return "green"
    if pct >= 70:
        return "yellow"
    return "red"

def parse_metric_value(raw_value: str) -> tuple[float | None, str]:
    text = str(raw_value or "").strip()
    if text in {"", "-", "â€”"}:
        return None, "generic"

    unit = "generic"
    if "R$" in text:
        unit = "currency"
    elif "%" in text:
        unit = "percent"
    elif "dia" in text.lower():
        unit = "days"

    cleaned = (
        text.replace("R$", "")
        .replace("%", "")
        .replace("â‰¤", "")
        .replace("+", "")
        .replace("dias", "")
        .replace("dia", "")
        .replace("/5", "")
        .strip()
    )
    match = re.search(r"-?\d+(?:[.,]\d+)?", cleaned)
    if not match:
        return None, unit

    value = float(match.group(0).replace(",", "."))
    if "M" in text:
        value *= 1_000_000
    elif "K" in text:
        value *= 1_000
    return value, unit

def format_delta(delta: float | None, unit: str) -> str:
    if delta is None:
        return "n/d"

    sign = "+" if delta >= 0 else "-"
    abs_delta = abs(delta)

    if unit == "currency":
        if abs_delta >= 1_000_000:
            return f"{sign}R$ {abs_delta / 1_000_000:.2f}M"
        if abs_delta >= 1_000:
            return f"{sign}R$ {abs_delta / 1_000:.1f}K"
        return f"{sign}R$ {abs_delta:.0f}"
    if unit == "percent":
        return f"{sign}{abs_delta:.1f} p.p."
    if unit == "days":
        return f"{sign}{abs_delta:.1f} dias"
    return f"{sign}{abs_delta:.2f}"

def build_kr_dataframe(okr: dict) -> pd.DataFrame:
    rows = []
    for kr in okr["krs"]:
        current, unit = parse_metric_value(kr["val"])
        previous, _ = parse_metric_value(kr["ant"])
        delta = current - previous if current is not None and previous is not None else None
        pct = kr.get("pct", 0)
        status = STATUS_LABELS[kr_status_from_pct(pct)] if pct > 0 else "A definir"
        rows.append(
            {
                "KR": kr["name"],
                "Atual": kr["val"],
                "Anterior": kr["ant"],
                "Meta": kr["meta"],
                "Vs anterior": format_delta(delta, unit),
                "Progresso (%)": pct,
                "Status": status,
            }
        )

    frame = pd.DataFrame(rows)
    return frame.sort_values(by="Progresso (%)", ascending=False)


# â”€â”€â”€ CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* === GLOBAL === */
.stApp {
    background: radial-gradient(ellipse at 12% 8%, #141B2D 0%, #0F1117 50%, #0B0E14 100%);
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
[data-testid="stHorizontalBlock"] {
    gap: 1.1rem;
    align-items: stretch;
}
[data-testid="stColumn"] > div,
[data-testid="stColumn"] > div > div { height: 100%; }

/* === HEADER === */
.hdr {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #1C2132;
}
.hdr-left { display: flex; align-items: center; gap: 14px; }
.hdr-logo { height: 38px; opacity: 0.92; }
.hdr-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: #FFF;
    margin: 0;
    letter-spacing: -0.3px;
}
.hdr-sub { color: #6B7B94; font-size: 0.82rem; margin-top: 2px; }
.hdr-badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid #262D40;
    color: #7B8CA6;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 500;
    white-space: nowrap;
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
.okr-link {
    text-decoration: none;
    color: inherit;
    display: block;
    height: 100%;
}
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
.okr-card:hover {
    transform: translateY(-3px);
    border-color: #384060;
    box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}
.okr-link:focus-visible .okr-card {
    outline: 2px solid #4A9EFF;
    outline-offset: 3px;
}

/* Card head */
.c-head { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.c-title {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.c-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
    animation: dot-pulse 2.5s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%, 100% { box-shadow: 0 0 4px 1px currentColor; }
    50% { box-shadow: 0 0 12px 3px currentColor; }
}
.c-sub {
    color: #6B7B94;
    font-size: 0.76rem;
    margin-bottom: 14px;
    line-height: 1.35;
}

/* Card body */
.c-body {
    display: grid;
    grid-template-columns: 1fr; /* <<< removido o espaÃ§o do grÃ¡fico */
    gap: 12px;
    flex: 1;
    min-height: 0;
}
.okr-click {
    margin-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.06);
    padding-top: 8px;
    color: #6B7B94;
    font-size: 0.66rem;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}
.c-krs {
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding-right: 6px;
}
/* Scrollbar */
.c-krs::-webkit-scrollbar { width: 4px; }
.c-krs::-webkit-scrollbar-track { background: transparent; }
.c-krs::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.12);
    border-radius: 2px;
}
.c-krs::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

/* KR row */
.kr {
    padding: 9px 0 8px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.kr:first-child { border-top: none; padding-top: 0; }
.kr-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 5px;
}
.kr-nm { color: #8090A8; font-size: 0.76rem; font-weight: 500; }
.kr-vl { color: #FFF; font-size: 0.92rem; font-weight: 700; white-space: nowrap; }
.kr-bar-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 3px;
}
.kr-track {
    flex: 1;
    height: 3px;
    background: rgba(255,255,255,0.07);
    border-radius: 2px;
    overflow: hidden;
}
.kr-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}
.kr-pct {
    font-size: 0.68rem;
    font-weight: 600;
    min-width: 30px;
    text-align: right;
}
.kr-meta {
    color: #4A5670;
    font-size: 0.65rem;
    letter-spacing: 0.2px;
}

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
@media (max-width: 1100px) {
    .hdr { flex-direction: column; align-items: flex-start; gap: 0.8rem; }
}
@media (max-width: 768px) {
    .sum-row { flex-wrap: wrap; }
    .sum-card { min-width: 45%; }
    .hdr-title { font-size: 1.3rem; }
    .block-container { padding-top: 1.2rem; }
}
</style>""", unsafe_allow_html=True)


# â”€â”€â”€ Header â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if "selected_okr" not in st.session_state:
    st.session_state["selected_okr"] = None

selected_from_url = st.query_params.get("okr")
if selected_from_url is not None:
    if isinstance(selected_from_url, list):
        selected_from_url = selected_from_url[0]
    try:
        selected_idx = int(selected_from_url)
        if 0 <= selected_idx < len(OKRS):
            st.session_state["selected_okr"] = selected_idx
    except (TypeError, ValueError):
        pass
    st.query_params.clear()

st.markdown("""
<div class="hdr">
    <div>
        <div class="hdr-title">OKRs EstratÃ©gicos</div>
        <div class="hdr-sub">PagBrasil &middot; Indicadores de Performance</div>
    </div>
    <span class="hdr-badge">Atualizado em Fev / 2026</span>
</div>
""", unsafe_allow_html=True)


# â”€â”€â”€ Summary Metrics â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
total_krs = sum(len(o["krs"]) for o in OKRS)
# status por OKR agora Ã© calculado pelos KRs
okr_statuses = [okr_status_from_krs(o["krs"]) for o in OKRS]
on_track = sum(1 for s in okr_statuses if s == "green")
attention = sum(1 for s in okr_statuses if s == "yellow")
at_risk = sum(1 for s in okr_statuses if s == "red")
valid_pcts = [kr["pct"] for o in OKRS for kr in o["krs"] if kr.get("pct", 0) > 0]
avg_pct = round(sum(valid_pcts) / len(valid_pcts)) if valid_pcts else 0

st.markdown(f"""
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
        <div class="sum-lbl">AtenÃ§Ã£o</div>
    </div>
    <div class="sum-card">
        <div class="sum-val" style="color:#F87171">{at_risk}</div>
        <div class="sum-lbl">Em Risco</div>
    </div>
    <div class="sum-card">
        <div class="sum-val">{avg_pct}%</div>
        <div class="sum-lbl">Progresso MÃ©dio</div>
    </div>
</div>
""", unsafe_allow_html=True)


# â”€â”€â”€ Card Renderer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def render_card(okr: dict, idx: int) -> None:
    accent = okr["accent"]
    status = okr_status_from_krs(okr["krs"])
    sc = STATUS_COLORS[status]

    rows = ""
    for kr in okr["krs"]:
        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pct_text = f'{kr["pct"]}%' if kr["pct"] > 0 else "-"
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

    st.markdown(
        f'<a class="okr-link" href="?okr={idx}" aria-label="Abrir detalhes de {okr["title"]}">'
        f'  <div class="okr-card" style="border-left:4px solid {accent};">'
        f'    <div class="c-head">'
        f'      <span class="c-title" style="color:{accent}">{okr["title"]}</span>'
        f'      <span class="c-dot" style="background:{sc};color:{sc}"></span>'
        f'    </div>'
        f'    <div class="c-sub">{okr["subtitle"]}</div>'
        f'    <div class="c-body">'
        f'      <div class="c-krs">{rows}</div>'
        f'    </div>'
        f'    <div class="okr-click">Clique para visao executiva detalhada</div>'
        f'  </div>'
        f'</a>',
        unsafe_allow_html=True,
    )


@st.dialog("OKR Executivo")
def render_okr_dialog(okr: dict, idx: int) -> None:
    status = okr_status_from_krs(okr["krs"])
    krs = okr["krs"]
    valid_pcts = [kr["pct"] for kr in krs if kr.get("pct", 0) > 0]
    avg_progress = round(sum(valid_pcts) / len(valid_pcts)) if valid_pcts else 0
    on_track = sum(1 for kr in krs if kr.get("pct", 0) >= 95)
    in_attention = sum(1 for kr in krs if 70 <= kr.get("pct", 0) < 95)
    in_risk = sum(1 for kr in krs if 0 < kr.get("pct", 0) < 70)

    st.markdown(f"### {okr['title']}")
    st.caption(okr["subtitle"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Status", STATUS_LABELS[status])
    m2.metric("Progresso medio", f"{avg_progress}%")
    m3.metric("KRs on track", on_track)
    m4.metric("KRs em risco", in_risk)

    left, right = st.columns([1.7, 1])
    with left:
        st.markdown("**Tendencia dos ultimos 12 meses**")
        trend_df = pd.DataFrame(
            {
                "Mes": pd.date_range(end=pd.Timestamp.today(), periods=len(okr["chart"]), freq="M"),
                "Valor": okr["chart"],
            }
        )
        st.line_chart(trend_df, x="Mes", y="Valor", use_container_width=True, height=250)
    with right:
        st.markdown("**Leituras rapidas**")
        current = okr["chart"][-1]
        previous = okr["chart"][-2] if len(okr["chart"]) > 1 else None
        delta = current - previous if previous is not None else None
        delta_text = f"{delta:+.2f} vs anterior" if delta is not None else None
        period_avg = sum(okr["chart"]) / len(okr["chart"]) if okr["chart"] else 0
        st.metric("Indice atual", f"{current:.2f}", delta_text)
        st.metric("Media do periodo", f"{period_avg:.2f}")
        st.metric("KRs em atencao", in_attention)
        st.metric("Total de KRs", len(krs))

    st.markdown("**Detalhamento dos KRs**")
    kr_df = build_kr_dataframe(okr)
    st.dataframe(
        kr_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "KR": st.column_config.TextColumn("KR", width="large"),
            "Progresso (%)": st.column_config.ProgressColumn(
                "Progresso (%)", min_value=0, max_value=100, format="%d%%"
            ),
        },
    )

    alerts = [kr for kr in sorted(krs, key=lambda item: item.get("pct", 0)) if 0 < kr.get("pct", 0) < 95]
    if alerts:
        st.markdown("**Pontos de decisao imediata**")
        for kr in alerts[:3]:
            st.markdown(f"- `{kr['name']}`: {kr['pct']}% | Atual: {kr['val']} | Meta: {kr['meta']}")

    if st.button("Fechar visao executiva", use_container_width=True, key=f"close_okr_dialog_{idx}"):
        st.session_state["selected_okr"] = None
        st.rerun()


# â”€â”€â”€ Layout: Row 1 (3 cards) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
row1 = st.columns(3)
for i in range(3):
    with row1[i]:
        render_card(OKRS[i], i)

# âœ… EspaÃ§amento entre as linhas de cards
st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

# â”€â”€â”€ Layout: Row 2 (2 cards centered) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_, col_p, col_c, _ = st.columns([0.5, 1, 1, 0.5])
with col_p:
    render_card(OKRS[3], 3)
with col_c:
    render_card(OKRS[4], 4)

selected_okr = st.session_state.get("selected_okr")
if isinstance(selected_okr, int) and 0 <= selected_okr < len(OKRS):
    render_okr_dialog(OKRS[selected_okr], selected_okr)

# â”€â”€â”€ Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<div class="ftr">
    PagBrasil &nbsp;Â·&nbsp; Dashboard EstratÃ©gico de OKRs &nbsp;Â·&nbsp; People &amp; Development
</div>
""", unsafe_allow_html=True)
