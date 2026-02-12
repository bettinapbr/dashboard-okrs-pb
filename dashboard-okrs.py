import streamlit as st
import pandas as pd
import altair as alt

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


# ─── Autenticação Gestor (segunda senha) ─────────────────────────────
def check_gestor_password():
    """Autentica gestor com segunda senha para acesso aos KRs Táticos."""

    def gestor_password_entered():
        if st.session_state.get("gestor_password_input") == st.secrets.get("gestor_password", ""):
            st.session_state["is_gestor"] = True
        else:
            st.session_state["is_gestor"] = False
            st.session_state["gestor_login_failed"] = True
        if "gestor_password_input" in st.session_state:
            del st.session_state["gestor_password_input"]

    if st.session_state.get("is_gestor", False):
        return

    if st.session_state.get("show_gestor_login", False):
        st.sidebar.markdown(
            '<div style="padding:20px 0 10px;">'
            '<h3 style="color:#34D399;margin:0;">🔐 Acesso Gestor</h3>'
            '<p style="color:#6B7B94;font-size:0.85rem;">Digite a senha de gestor para acessar KRs Táticos</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.sidebar.text_input(
            "Senha Gestor",
            type="password",
            on_change=gestor_password_entered,
            key="gestor_password_input",
        )
        if st.session_state.get("gestor_login_failed", False):
            st.sidebar.error("Senha de gestor incorreta.")
        if st.sidebar.button("Cancelar", key="cancel_gestor"):
            st.session_state["show_gestor_login"] = False
            st.session_state["gestor_login_failed"] = False
            st.rerun()


# ─── Session State Defaults ──────────────────────────────────────────
if "is_gestor" not in st.session_state:
    st.session_state["is_gestor"] = False
if "show_gestor_login" not in st.session_state:
    st.session_state["show_gestor_login"] = False
if "gestor_login_failed" not in st.session_state:
    st.session_state["gestor_login_failed"] = False
if "selected_okr" not in st.session_state:
    st.session_state["selected_okr"] = None
if "selected_kr_idx" not in st.session_state:
    st.session_state["selected_kr_idx"] = None
if "selected_tatico_okr" not in st.session_state:
    st.session_state["selected_tatico_okr"] = None
if "selected_tatico_kr" not in st.session_state:
    st.session_state["selected_tatico_kr"] = None

check_gestor_password()

# ─── Constants ───────────────────────────────────────────────────────
STATUS_COLORS = {"green": "#34D399", "yellow": "#FBBF24", "red": "#F87171"}
STATUS_LABELS = {"green": "On Track", "yellow": "Atenção", "red": "Em Risco"}

# ─── Data ────────────────────────────────────────────────────────────
OKRS = [
    {
        "title": "CRESCIMENTO",
        "subtitle": "Impulsionar o crescimento sustentável e rentável",
        "accent": "#54CA30",
        "status": "green",
        "chart": [8.1, 8.5, 9.2, 9.0, 9.8, 10.2, 10.5, 11.0, 11.3, 11.8, 12.0, 12.4],
        "krs": [
            {
                "name": "Receita",
                "val": "R$ 12.4M",
                "ant": "R$ 11.8M",
                "meta": "R$ 12.0M",
                "pct": 100,
                "taticos": [
                    {
                        "name": "Aumentar ticket médio em 15%",
                        "val": "12.8%",
                        "ant": "10.2%",
                        "meta": "15%",
                        "pct": 85,
                        "chart": [6.0, 7.1, 7.5, 8.0, 8.8, 9.5, 10.0, 10.2, 10.8, 11.5, 12.0, 12.8],
                    },
                    {
                        "name": "Conquistar 20 novos clientes tier 1",
                        "val": "13",
                        "ant": "8",
                        "meta": "20",
                        "pct": 65,
                        "chart": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13],
                    },
                ],
            },
            {
                "name": "Receita Nacional (NB)",
                "val": "R$ 8.7M",
                "ant": "R$ 8.2M",
                "meta": "R$ 8.5M",
                "pct": 100,
                "taticos": [
                    {
                        "name": "Expandir para 3 novas verticais",
                        "val": "3",
                        "ant": "1",
                        "meta": "3",
                        "pct": 100,
                        "chart": [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3],
                    },
                ],
            },
            {
                "name": "Receita Internacional (XB)",
                "val": "R$ 3.7M",
                "ant": "R$ 3.5M",
                "meta": "R$ 4.0M",
                "pct": 93,
                "taticos": [
                    {
                        "name": "Fechar parceria LATAM",
                        "val": "70%",
                        "ant": "40%",
                        "meta": "100%",
                        "pct": 70,
                        "chart": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 65, 70],
                    },
                    {
                        "name": "Ativar 10 merchants no México",
                        "val": "4",
                        "ant": "2",
                        "meta": "10",
                        "pct": 40,
                        "chart": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4],
                    },
                ],
            },
        ],
    },
    {
        "title": "INOVAÇÃO / PRODUTO",
        "subtitle": "Consolidar liderança em inovação e diferenciação",
        "accent": "#54CA30",
        "status": "green",
        "chart": [1.2, 1.4, 1.6, 1.8, 2.0, 2.1, 2.3, 2.5, 2.7, 2.8, 2.9, 3.1],
        "krs": [
            {
                "name": "Receita prod. < 24 meses",
                "val": "R$ 3.1M",
                "ant": "R$ 2.9M",
                "meta": "R$ 3.0M",
                "pct": 100,
                "taticos": [
                    {
                        "name": "Lançar 2 produtos novos no semestre",
                        "val": "2",
                        "ant": "1",
                        "meta": "2",
                        "pct": 100,
                        "chart": [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2],
                    },
                ],
            },
            {
                "name": "% clientes c/ novos prod.",
                "val": "34%",
                "ant": "31%",
                "meta": "35%",
                "pct": 97,
                "taticos": [
                    {
                        "name": "Campanha de adoção Q3/Q4",
                        "val": "88%",
                        "ant": "60%",
                        "meta": "90%",
                        "pct": 98,
                        "chart": [20, 30, 40, 45, 50, 55, 60, 65, 72, 78, 84, 88],
                    },
                ],
            },
            {
                "name": "% clientes c/ novas func.",
                "val": "28%",
                "ant": "25%",
                "meta": "30",
                "pct": 93,
                "taticos": [],
            },
            {
                "name": "Taxa de Falhas Críticas",
                "val": "0.12%",
                "ant": "0.15%",
                "meta": "≤ 0.10%",
                "pct": 83,
                "taticos": [
                    {
                        "name": "Cobertura de testes > 85%",
                        "val": "82%",
                        "ant": "75%",
                        "meta": "85%",
                        "pct": 96,
                        "chart": [60, 63, 65, 68, 70, 72, 74, 75, 77, 79, 81, 82],
                    },
                    {
                        "name": "Reduzir MTTR para < 2h",
                        "val": "2.3h",
                        "ant": "3.1h",
                        "meta": "≤ 2h",
                        "pct": 87,
                        "chart": [4.0, 3.8, 3.5, 3.3, 3.1, 3.0, 2.9, 2.7, 2.6, 2.5, 2.4, 2.3],
                    },
                ],
            },
            {
                "name": "Índice inovação percebida",
                "val": "8.1",
                "ant": "7.8",
                "meta": "8.0",
                "pct": 100,
                "taticos": [],
            },
            {
                "name": "Taxa de conversão",
                "val": "72.5%",
                "ant": "70.1%",
                "meta": "72.0%",
                "pct": 100,
                "taticos": [],
            },
        ],
    },
    {
        "title": "EXCELÊNCIA OPERACIONAL",
        "subtitle": "Elevar a excelência operacional e eficiência",
        "accent": "#54CA30",
        "status": "yellow",
        "chart": [310, 305, 298, 295, 290, 288, 285, 283, 280, 282, 284, 285],
        "krs": [
            {
                "name": "Receita por pessoa",
                "val": "R$ 285K",
                "ant": "R$ 290K",
                "meta": "R$ 300K",
                "pct": 95,
                "taticos": [
                    {
                        "name": "Automatizar 5 processos manuais",
                        "val": "4",
                        "ant": "2",
                        "meta": "5",
                        "pct": 80,
                        "chart": [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4],
                    },
                ],
            },
            {
                "name": "Tempo onboarding NB",
                "val": "12 dias",
                "ant": "14 dias",
                "meta": "≤ 10 dias",
                "pct": 83,
                "taticos": [
                    {
                        "name": "Implementar checklist digital",
                        "val": "90%",
                        "ant": "60%",
                        "meta": "100%",
                        "pct": 90,
                        "chart": [20, 30, 35, 40, 50, 55, 60, 65, 72, 80, 85, 90],
                    },
                    {
                        "name": "Treinar 100% do time comercial",
                        "val": "85%",
                        "ant": "60%",
                        "meta": "100%",
                        "pct": 85,
                        "chart": [20, 25, 30, 40, 45, 50, 55, 60, 65, 72, 80, 85],
                    },
                ],
            },
            {
                "name": "Tempo onboarding XB",
                "val": "18 dias",
                "ant": "20 dias",
                "meta": "≤ 15 dias",
                "pct": 83,
                "taticos": [],
            },
            {
                "name": "% processos documentados",
                "val": "67%",
                "ant": "62%",
                "meta": "75%",
                "pct": 89,
                "taticos": [
                    {
                        "name": "Mapear todos os processos críticos",
                        "val": "18/22",
                        "ant": "12/22",
                        "meta": "22/22",
                        "pct": 82,
                        "chart": [5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18],
                    },
                ],
            },
        ],
    },
    {
        "title": "PESSOAS",
        "subtitle": "Desenvolver pessoas e lideranças para o próximo ciclo",
        "accent": "#0058B5",
        "status": "green",
        "chart": [58, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72],
        "krs": [
            {
                "name": "Índice de engajamento",
                "val": "81%",
                "ant": "78%",
                "meta": "80%",
                "pct": 100,
                "taticos": [
                    {
                        "name": "Realizar 4 pulses no ano",
                        "val": "4",
                        "ant": "3",
                        "meta": "4",
                        "pct": 100,
                        "chart": [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4],
                    },
                    {
                        "name": "Plano de ação por área (100%)",
                        "val": "92%",
                        "ant": "70%",
                        "meta": "100%",
                        "pct": 92,
                        "chart": [30, 40, 45, 50, 55, 60, 65, 70, 75, 82, 88, 92],
                    },
                ],
            },
            {
                "name": "% de certificação interna",
                "val": "63%",
                "ant": "58%",
                "meta": "70%",
                "pct": 90,
                "taticos": [
                    {
                        "name": "Lançar plataforma de e-learning",
                        "val": "100%",
                        "ant": "50%",
                        "meta": "100%",
                        "pct": 100,
                        "chart": [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100, 100],
                    },
                ],
            },
            {
                "name": "eNPS",
                "val": "72",
                "ant": "68",
                "meta": "70",
                "pct": 100,
                "taticos": [],
            },
            {
                "name": "Pontuação GPTW",
                "val": "84",
                "ant": "81",
                "meta": "85",
                "pct": 99,
                "taticos": [
                    {
                        "name": "Implementar programa de mentoria",
                        "val": "85%",
                        "ant": "40%",
                        "meta": "100%",
                        "pct": 85,
                        "chart": [10, 15, 20, 30, 35, 40, 50, 55, 62, 70, 78, 85],
                    },
                ],
            },
        ],
    },
    {
        "title": "CLIENTES",
        "subtitle": "Garantir experiências fluidas que impulsionem satisfação",
        "accent": "#0058B5",
        "status": "red",
        "chart": [72, 71, 70, 69, 70, 69, 68, 69, 68, 67, 68, 68],
        "krs": [
            {
                "name": "NPS",
                "val": "+68",
                "ant": "+71",
                "meta": "+75",
                "pct": 91,
                "taticos": [
                    {
                        "name": "Programa de follow-up pós-venda",
                        "val": "78%",
                        "ant": "50%",
                        "meta": "95%",
                        "pct": 82,
                        "chart": [20, 28, 35, 40, 45, 50, 55, 60, 65, 70, 75, 78],
                    },
                    {
                        "name": "Reduzir tempo resposta < 4h",
                        "val": "5.2h",
                        "ant": "7h",
                        "meta": "≤ 4h",
                        "pct": 77,
                        "chart": [8.0, 7.5, 7.2, 7.0, 6.8, 6.5, 6.2, 6.0, 5.8, 5.5, 5.3, 5.2],
                    },
                ],
            },
            {
                "name": "% Contas Não Ativadas",
                "val": "15%",
                "ant": "17%",
                "meta": "≤ 10%",
                "pct": 67,
                "taticos": [
                    {
                        "name": "Fluxo de onboarding automatizado",
                        "val": "70%",
                        "ant": "30%",
                        "meta": "100%",
                        "pct": 70,
                        "chart": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 65, 70],
                    },
                ],
            },
            {
                "name": "MRR Churn Rate",
                "val": "1.8%",
                "ant": "2.1%",
                "meta": "≤ 1.5%",
                "pct": 83,
                "taticos": [
                    {
                        "name": "Health score para top 50 contas",
                        "val": "42/50",
                        "ant": "28/50",
                        "meta": "50/50",
                        "pct": 84,
                        "chart": [10, 14, 18, 20, 22, 25, 28, 30, 33, 36, 40, 42],
                    },
                ],
            },
            {
                "name": "% atendimentos no SLA",
                "val": "94%",
                "ant": "92%",
                "meta": "97%",
                "pct": 97,
                "taticos": [],
            },
            {
                "name": "Taxa de chargeback",
                "val": "R$ 142K",
                "ant": "R$ 155K",
                "meta": "≤ R$ 120K",
                "pct": 85,
                "taticos": [
                    {
                        "name": "Sistema anti-fraude v2",
                        "val": "88%",
                        "ant": "60%",
                        "meta": "100%",
                        "pct": 88,
                        "chart": [25, 30, 35, 40, 48, 55, 60, 65, 70, 78, 84, 88],
                    },
                ],
            },
            {
                "name": "CSAT",
                "val": "4.3/5",
                "ant": "4.2/5",
                "meta": "4.5/5",
                "pct": 96,
                "taticos": [],
            },
            {
                "name": "Indicador de branding",
                "val": "—",
                "ant": "—",
                "meta": "A definir",
                "pct": 0,
                "taticos": [],
            },
            {
                "name": "Nº solic./contas ativas",
                "val": "0.32",
                "ant": "0.35",
                "meta": "≤ 0.25",
                "pct": 78,
                "taticos": [],
            },
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


def resolve_kr_series(okr: dict, kr: dict, kr_idx: int) -> tuple[list[float], str]:
    kr_series = kr.get("chart")
    if isinstance(kr_series, list) and len(kr_series) > 0:
        return kr_series, "kr"

    okr_series = okr.get("chart", [])
    if not okr_series:
        return [], "none"

    amplitude = max(abs(v) for v in okr_series) or 1
    center = (len(okr.get("krs", [])) - 1) / 2
    offset = (kr_idx - center) * (amplitude * 0.015)
    slope = ((kr.get("pct", 0) - 85) / 100) * (amplitude * 0.02)
    midpoint = (len(okr_series) - 1) / 2
    derived = [round(v + offset + ((i - midpoint) * slope), 2) for i, v in enumerate(okr_series)]
    return derived, "derived"


def infer_y_axis_config(kr: dict) -> tuple[str, str]:
    probe = " ".join([str(kr.get("name", "")), str(kr.get("val", "")), str(kr.get("ant", "")), str(kr.get("meta", ""))]).lower()
    if "r$" in probe:
        return "Valor (R$)", ",.2f"
    if "%" in probe:
        return "Percentual (%)", ".1f"
    if "dia" in probe:
        return "Dias", ".0f"
    if "/5" in probe:
        return "Pontuação (0-5)", ".2f"
    if "nps" in probe or "enps" in probe:
        return "Pontos (NPS)", ".0f"
    if "pontuação" in probe or "indice" in probe or "índice" in probe:
        return "Índice", ".2f"
    if "hora" in probe or "h" in probe:
        return "Horas", ".1f"
    return "Valor", ",.2f"


def open_okr(idx: int):
    st.session_state["selected_okr"] = idx
    st.session_state["selected_kr_idx"] = 0


def close_okr():
    st.session_state["selected_okr"] = None
    st.session_state["selected_kr_idx"] = None


def open_tatico(idx: int):
    st.session_state["selected_tatico_okr"] = idx
    st.session_state["selected_tatico_kr"] = None


def close_tatico():
    st.session_state["selected_tatico_okr"] = None
    st.session_state["selected_tatico_kr"] = None


# ─── Dialog: KRs Estratégicos (Veja mais) ───────────────────────────
@st.dialog("Detalhes do OKR", width="large")
def okr_dialog_kr(okr: dict, idx: int):
    accent = okr["accent"]
    status = okr_status_from_krs(okr["krs"])
    sc = STATUS_COLORS[status]
    selected_kr_idx = st.session_state.get("selected_kr_idx", 0)
    if selected_kr_idx is None or not (0 <= selected_kr_idx < len(okr["krs"])):
        selected_kr_idx = 0
        st.session_state["selected_kr_idx"] = selected_kr_idx

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

    st.subheader("Key Results (clique para selecionar)")
    for kr_idx, kr in enumerate(okr["krs"]):
        is_selected = kr_idx == selected_kr_idx
        if st.button(
            f'{"Selecionado - " if is_selected else ""}{kr["name"]} | {kr["val"]}',
            key=f"select_kr_{idx}_{kr_idx}",
            use_container_width=True,
        ):
            st.session_state["selected_kr_idx"] = kr_idx
            st.rerun()

        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pct_text = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"
        row_border = f"1px solid {accent}" if is_selected else "1px solid rgba(255,255,255,0.04)"
        row_bg = "rgba(255,255,255,0.03)" if is_selected else "transparent"
        st.markdown(
            f"""
            <div style="padding:10px 10px;border:{row_border};border-radius:10px;background:{row_bg};margin:6px 0;">
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

    selected_kr = okr["krs"][selected_kr_idx]
    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    series, series_source = resolve_kr_series(okr, selected_kr, selected_kr_idx)
    df = pd.DataFrame({"Mês": months[: len(series)], "Valor": series})

    st.subheader(f'Evolução (últimos 12 meses) - {selected_kr["name"]}')
    if series_source == "derived":
        st.caption("Série derivada automaticamente para este KR. Para série oficial, preencha `chart` no KR.")
    elif series_source == "none":
        st.caption("Sem dados de série para este KR/OKR.")
    if len(series) > 0:
        y_min = min(series)
        y_max = max(series)
        y_pad = (y_max - y_min) * 0.12 if y_max != y_min else max(abs(y_max) * 0.12, 1)
        y_domain = [y_min - y_pad, y_max + y_pad]
        y_title, y_format = infer_y_axis_config(selected_kr)

        chart = (
            alt.Chart(df)
            .mark_line(point=True, strokeWidth=2.5)
            .encode(
                x=alt.X(
                    "Mês:N",
                    sort=months,
                    axis=alt.Axis(title="Mês", labelAngle=0),
                ),
                y=alt.Y(
                    "Valor:Q",
                    scale=alt.Scale(domain=y_domain, nice=True, zero=False),
                    axis=alt.Axis(title=y_title, format=y_format),
                ),
                tooltip=[alt.Tooltip("Mês:N", title="Mês"), alt.Tooltip("Valor:Q", title=y_title, format=y_format)],
            )
            .properties(height=320)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sem dados de evolução para este KR.")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    if st.button("Fechar", use_container_width=True, key=f"close_kr_{idx}"):
        close_okr()
        st.rerun()


# ─── Dialog: KRs Táticos ────────────────────────────────────────────
@st.dialog("KRs Táticos", width="large")
def tatico_dialog(okr: dict, idx: int):
    accent = okr["accent"]
    status = okr_status_from_krs(okr["krs"])
    sc = STATUS_COLORS[status]

    # ── Header do pilar ──
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(160deg, #181D2C 0%, #141822 100%);
            border: 1px solid #2B3350;
            border-left: 6px solid {accent};
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 16px;
        ">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
            <div>
              <div style="color:{accent};font-weight:800;letter-spacing:1.3px;font-size:0.85rem;">
                🎯 {okr["title"]} — KRs Táticos
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

    # ── Identificador do KR tático selecionado: "kr_idx:tatico_idx" ──
    selected_key = st.session_state.get("selected_tatico_kr", None)

    # ── Iterar por cada KR estratégico como agrupador ──
    has_any_tatico = False
    for kr_idx, kr in enumerate(okr["krs"]):
        taticos = kr.get("taticos", [])
        if not taticos:
            continue

        has_any_tatico = True

        # Header do KR estratégico (agrupador)
        kr_pc = pct_color(kr["pct"])
        kr_w = min(kr["pct"], 100)
        kr_pct_text = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"

        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.025);
                border: 1px solid #232940;
                border-left: 3px solid {accent};
                border-radius: 12px;
                padding: 14px 16px;
                margin-top: 8px;
                margin-bottom: 4px;
            ">
              <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <span style="color:#C8D6E5;font-size:0.88rem;font-weight:700;">{kr["name"]}</span>
                <span style="color:#FFF;font-size:0.95rem;font-weight:800;">{kr["val"]}</span>
              </div>
              <div style="display:flex;align-items:center;gap:10px;margin-top:6px;margin-bottom:3px;">
                <div style="flex:1;height:3px;background:rgba(255,255,255,0.07);border-radius:2px;overflow:hidden;">
                  <div style="width:{kr_w}%;height:100%;background:{kr_pc};"></div>
                </div>
                <span style="min-width:30px;text-align:right;color:{kr_pc};font-weight:700;font-size:0.72rem;">{kr_pct_text}</span>
              </div>
              <div style="color:#4A5670;font-size:0.68rem;">Ant: {kr["ant"]} · Meta: {kr["meta"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # KRs táticos abaixo desse agrupador
        for t_idx, tatico in enumerate(taticos):
            t_key = f"{kr_idx}:{t_idx}"
            is_selected = selected_key == t_key

            # Botão de seleção
            if st.button(
                f'{"▸ " if is_selected else "  "}{tatico["name"]} | {tatico["val"]}',
                key=f"sel_tat_{idx}_{kr_idx}_{t_idx}",
                use_container_width=True,
            ):
                st.session_state["selected_tatico_kr"] = t_key
                st.rerun()

            # Card visual do tático
            t_pc = pct_color(tatico["pct"])
            t_w = min(tatico["pct"], 100)
            t_pct_text = f'{tatico["pct"]}%' if tatico["pct"] > 0 else "—"
            t_border = f"1px solid {accent}" if is_selected else "1px solid rgba(255,255,255,0.04)"
            t_bg = "rgba(255,255,255,0.035)" if is_selected else "rgba(255,255,255,0.015)"

            st.markdown(
                f"""
                <div style="padding:10px 14px;border:{t_border};border-radius:10px;background:{t_bg};margin:4px 0 6px 20px;">
                  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;">
                    <span style="color:#8090A8;font-size:0.8rem;font-weight:600;">↳ {tatico["name"]}</span>
                    <span style="color:#FFF;font-size:0.88rem;font-weight:700;white-space:nowrap;">{tatico["val"]}</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:3px;">
                    <div style="flex:1;height:3px;background:rgba(255,255,255,0.07);border-radius:2px;overflow:hidden;">
                      <div style="width:{t_w}%;height:100%;background:{t_pc};"></div>
                    </div>
                    <span style="min-width:30px;text-align:right;color:{t_pc};font-weight:700;font-size:0.7rem;">{t_pct_text}</span>
                  </div>
                  <div style="color:#4A5670;font-size:0.68rem;">Ant: {tatico["ant"]} · Meta: {tatico["meta"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if not has_any_tatico:
        st.info("Nenhum KR tático cadastrado para este pilar.")

    # ── Gráfico de evolução do KR tático selecionado ──
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    if selected_key is not None:
        try:
            sel_kr_idx, sel_t_idx = selected_key.split(":")
            sel_kr_idx, sel_t_idx = int(sel_kr_idx), int(sel_t_idx)
            selected_tatico = okr["krs"][sel_kr_idx]["taticos"][sel_t_idx]
            parent_kr_name = okr["krs"][sel_kr_idx]["name"]
        except (ValueError, IndexError, KeyError):
            selected_tatico = None
            parent_kr_name = ""

        if selected_tatico:
            months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            series = selected_tatico.get("chart", [])

            st.subheader(f'Evolução — {selected_tatico["name"]}')
            st.caption(f'KR Estratégico: {parent_kr_name}')

            if series:
                df = pd.DataFrame({"Mês": months[: len(series)], "Valor": series})
                y_min = min(series)
                y_max = max(series)
                y_pad = (y_max - y_min) * 0.12 if y_max != y_min else max(abs(y_max) * 0.12, 1)
                y_domain = [y_min - y_pad, y_max + y_pad]
                y_title, y_format = infer_y_axis_config(selected_tatico)

                chart = (
                    alt.Chart(df)
                    .mark_line(point=True, strokeWidth=2.5, color="#A78BFA")
                    .encode(
                        x=alt.X(
                            "Mês:N",
                            sort=months,
                            axis=alt.Axis(title="Mês", labelAngle=0),
                        ),
                        y=alt.Y(
                            "Valor:Q",
                            scale=alt.Scale(domain=y_domain, nice=True, zero=False),
                            axis=alt.Axis(title=y_title, format=y_format),
                        ),
                        tooltip=[
                            alt.Tooltip("Mês:N", title="Mês"),
                            alt.Tooltip("Valor:Q", title=y_title, format=y_format),
                        ],
                    )
                    .properties(height=300)
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Sem dados de evolução para este KR tático.")
    else:
        st.markdown(
            '<div style="text-align:center;color:#4A5670;padding:20px 0;font-size:0.85rem;">'
            "👆 Selecione um KR tático acima para ver a evolução"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    if st.button("Fechar", use_container_width=True, key=f"close_tat_{idx}"):
        close_tatico()
        st.rerun()


# ─── Trigger dialogs from session state ──────────────────────────────
if st.session_state["selected_okr"] is not None:
    i = int(st.session_state["selected_okr"])
    if 0 <= i < len(OKRS):
        okr_dialog_kr(OKRS[i], i)

if st.session_state["selected_tatico_okr"] is not None:
    i = int(st.session_state["selected_tatico_okr"])
    if 0 <= i < len(OKRS):
        tatico_dialog(OKRS[i], i)

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

.c-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 4px; }
.c-head-left { display:flex; align-items:center; gap:10px; min-width:0; }
.c-title { font-family: 'Montserrat', 'Segoe UI', system-ui, sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
.c-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; flex-shrink: 0; animation: dot-pulse 2.5s ease-in-out infinite; }
@keyframes dot-pulse {
    0%, 100% { box-shadow: 0 0 4px 1px currentColor; }
    50% { box-shadow: 0 0 12px 3px currentColor; }
}
.c-sub { color: #6B7B94; font-size: 0.76rem; margin-bottom: 14px; line-height: 1.35; }

/* ============================================================
   BOTÕES "VEJA MAIS" + "KRs TÁTICOS"
   ============================================================ */
[data-testid="stColumn"] > div > div > div:has([data-testid="stButton"]) {
    display: flex !important;
    justify-content: flex-end !important;
    gap: 6px !important;
    margin-bottom: -44px !important;
    padding-right: 20px !important;
    padding-top: 18px !important;
    position: relative !important;
    z-index: 10 !important;
    pointer-events: none !important;
}

[data-testid="stColumn"] > div > div > div:has([data-testid="stButton"]) * {
    pointer-events: all !important;
}

/* Estilo pill do botão */
[data-testid="stColumn"] [data-testid="stButton"] button {
    border-radius: 999px !important;
    padding: 5px 14px !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    color: rgba(246,246,246,0.88) !important;
    line-height: 1.2 !important;
    min-height: unset !important;
    height: auto !important;
    white-space: nowrap !important;
    transition: background 180ms ease, border-color 180ms ease;
}
[data-testid="stColumn"] [data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.30) !important;
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

/* === GESTOR LOGIN BUTTON (sidebar trigger) === */
.gestor-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999;
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

# Conta KRs táticos total
total_taticos = sum(len(kr.get("taticos", [])) for o in OKRS for kr in o["krs"])

summary_gestor_card = ""
if st.session_state.get("is_gestor", False):
    summary_gestor_card = f"""
    <div class="sum-card">
        <div class="sum-val" style="color:#A78BFA">{total_taticos}</div>
        <div class="sum-lbl">KRs Táticos</div>
    </div>
    """

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
    {summary_gestor_card}
</div>
""",
    unsafe_allow_html=True,
)

# ─── Gestor access button (bottom of sidebar) ───────────────────────
if not st.session_state.get("is_gestor", False):
    with st.sidebar:
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        if st.button("🔐 Acesso Gestor", key="trigger_gestor_login", use_container_width=True):
            st.session_state["show_gestor_login"] = True
            st.rerun()
else:
    with st.sidebar:
        st.markdown(
            '<div style="padding:16px 0;">'
            '<p style="color:#A78BFA;font-weight:700;font-size:0.9rem;">🔓 Modo Gestor Ativo</p>'
            '<p style="color:#6B7B94;font-size:0.78rem;">Você tem acesso aos KRs Táticos</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Sair do modo gestor", key="logout_gestor", use_container_width=True):
            st.session_state["is_gestor"] = False
            st.session_state["show_gestor_login"] = False
            st.session_state["selected_tatico_okr"] = None
            st.session_state["selected_tatico_kr"] = None
            st.rerun()


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

    # ① Botões PRIMEIRO — CSS reposiciona dentro do card header
    btn_cols = st.columns([1, 1] if st.session_state.get("is_gestor", False) else [1])

    with btn_cols[0]:
        if st.button("Veja mais", key=f"open_{idx}"):
            open_okr(idx)
            st.rerun()

    if st.session_state.get("is_gestor", False):
        with btn_cols[-1]:
            # Verifica se tem táticos neste pilar
            has_taticos = any(kr.get("taticos") for kr in okr["krs"])
            if has_taticos:
                if st.button("🎯 Táticos", key=f"open_tat_{idx}"):
                    open_tatico(idx)
                    st.rerun()

    # ② Card HTML DEPOIS
    st.markdown(
        f"""
        <div class="okr-card" style="border-left:4px solid {accent};">
          <div class="c-head">
            <div class="c-head-left">
              <span class="c-title" style="color:{accent}">{okr["title"]}</span>
              <span class="c-dot" style="background:{sc};color:{sc}"></span>
            </div>
          </div>
          <div class="c-sub">{okr["subtitle"]}</div>
          <div class="c-body">
            <div class="c-krs">{rows}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
