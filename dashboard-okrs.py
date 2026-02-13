import streamlit as st
import pandas as pd
import altair as alt
import re
import unicodedata
from pathlib import Path

# ─── Page Config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="OKRs PagBrasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Autenticação ────────────────────────────────────────────────────
def check_password():
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
STATUS_COLORS = {
    "green": "#34D399",
    "yellow": "#FBBF24",
    "red": "#F87171",
    "no_data": "#6B7B94",
}
STATUS_LABELS = {
    "green": "On Track",
    "yellow": "Atenção",
    "red": "Em Risco",
    "no_data": "Sem dados",
}
EXCEL_PATH = Path(r"C:\Users\joao.schramm\Downloads\Draft Dashboard OKRs.xlsx")
EXCEL_BASE_SHEET = "Base de dados"
MONTHS = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# ─── Mapeamento DIRETO: nome do KR no dashboard → trecho que aparece na planilha
MATCH_MAP = {
    "Receita": "receita",
    "Receita Nacional (NB)": "receita nacional nb",
    "Receita Internacional (XB)": "receita internacional xb",
    "Receita prod. < 24 meses": "produtos com menos de 24",
    "% clientes c/ novos prod.": "novos produtos",
    "% clientes c/ novas func.": "novas funcionalidades",
    "Taxa de Falhas Críticas": "falhas criticas",
    "Índice inovação percebida": "inovacao percebida",
    "Taxa de conversão": "taxa de conversao",
    "Receita por pessoa": "receita por pessoa",
    "Tempo onboarding NB": "onboarding de merchants nb",
    "Tempo onboarding XB": "onboarding de merchants xb",
    "% processos documentados": "processos documentados",
    "Índice de engajamento": "indice de engajamento",
    "% de certificação interna": "certificacao interna",
    "eNPS": "enps",
    "Pontuação GPTW": "gptw",
    "NPS": "nps net promoter",
    "% Contas Não Ativadas": "contas nao ativadas",
    "MRR Churn Rate": "mrr churn",
    "% atendimentos no SLA": "atendimentos dentro do sla",
    "Taxa de chargeback": "taxa de chargeback",
    "CSAT": "csat",
    "Indicador de branding": "indicador de branding",
    "Nº solic./contas ativas": "solicitacoes",
}

# ─── Estrutura do Dashboard (ZERO dados hardcoded — tudo vem do Excel) ─
OKRS = [
    {
        "title": "CRESCIMENTO",
        "subtitle": "Impulsionar o crescimento sustentável e rentável",
        "accent": "#54CA30",
        "krs": [
            {"name": "Receita"},
            {"name": "Receita Nacional (NB)"},
            {"name": "Receita Internacional (XB)"},
        ],
    },
    {
        "title": "INOVAÇÃO / PRODUTO",
        "subtitle": "Consolidar liderança em inovação e diferenciação",
        "accent": "#54CA30",
        "krs": [
            {"name": "Receita prod. < 24 meses"},
            {"name": "% clientes c/ novos prod."},
            {"name": "% clientes c/ novas func."},
            {"name": "Taxa de Falhas Críticas"},
            {"name": "Índice inovação percebida"},
            {"name": "Taxa de conversão"},
        ],
    },
    {
        "title": "EXCELÊNCIA OPERACIONAL",
        "subtitle": "Elevar a excelência operacional e eficiência",
        "accent": "#54CA30",
        "krs": [
            {"name": "Receita por pessoa"},
            {"name": "Tempo onboarding NB"},
            {"name": "Tempo onboarding XB"},
            {"name": "% processos documentados"},
        ],
    },
    {
        "title": "PESSOAS",
        "subtitle": "Desenvolver pessoas e lideranças para o próximo ciclo",
        "accent": "#0058B5",
        "krs": [
            {"name": "Índice de engajamento"},
            {"name": "% de certificação interna"},
            {"name": "eNPS"},
            {"name": "Pontuação GPTW"},
        ],
    },
    {
        "title": "CLIENTES",
        "subtitle": "Garantir experiências fluidas que impulsionem satisfação",
        "accent": "#0058B5",
        "krs": [
            {"name": "NPS"},
            {"name": "% Contas Não Ativadas"},
            {"name": "MRR Churn Rate"},
            {"name": "% atendimentos no SLA"},
            {"name": "Taxa de chargeback"},
            {"name": "CSAT"},
            {"name": "Indicador de branding"},
            {"name": "Nº solic./contas ativas"},
        ],
    },
]


# ─── Funções utilitárias ─────────────────────────────────────────────
def _norm(text) -> str:
    s = str(text or "").strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _is_blank(v) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and pd.isna(v):
        return True
    return str(v).strip() in {"", "nan", "None"}


def _parse_num(v):
    if _is_blank(v):
        return None
    if isinstance(v, (int, float)) and not pd.isna(v):
        return float(v)
    raw = str(v).replace("R$", "").replace(" ", "").strip()
    m = re.search(r"-?\d+(?:[.,]\d+)?", raw)
    if not m:
        return None
    t = m.group(0)
    if "." in t and "," in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def _display_val(v) -> str:
    if _is_blank(v):
        return "—"
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return f"{v:.4f}".rstrip("0").rstrip(".")
    return str(v).strip()


def _display_meta(v) -> str:
    """Mostra a meta TAL QUAL está no Excel. Sem inventar formato."""
    if _is_blank(v):
        return "—"
    # String → mostra direto
    if isinstance(v, str):
        return v.strip() if v.strip() else "—"
    # Inteiro
    if isinstance(v, int):
        return str(v)
    # Float
    if isinstance(v, float):
        if pd.isna(v):
            return "—"
        if v == int(v):
            return str(int(v))
        # Preserva decimais como o Excel mostra
        return f"{v:g}"
    return str(v).strip()


# ─── Leitura do Excel ────────────────────────────────────────────────
def load_excel(path: Path) -> list[dict]:
    """
    Lê TODAS as linhas da planilha e retorna lista de dicts com:
      name_norm, meta_raw, months (lista de valores brutos por mês)
    """
    if not path.exists():
        return []

    df = pd.read_excel(path, sheet_name=EXCEL_BASE_SHEET)
    cols = list(df.columns)

    # Encontrar coluna de nomes (index 2) e meta
    name_col = cols[2] if len(cols) > 2 else None
    meta_col = None
    for c in cols:
        if "meta" in str(c).strip().lower():
            meta_col = c
            break
    if meta_col is None and len(cols) > 3:
        meta_col = cols[3]

    # Encontrar colunas de meses
    month_cols = []
    for month_name in MONTHS:
        for c in cols:
            if _norm(c) == _norm(month_name):
                month_cols.append(c)
                break

    rows = []
    for _, row in df.iterrows():
        kr_name = row.get(name_col) if name_col else None
        if _is_blank(kr_name):
            continue

        rows.append({
            "name": str(kr_name).strip(),
            "name_norm": _norm(kr_name),
            "meta_raw": row.get(meta_col) if meta_col else None,
            "months": [row.get(mc) for mc in month_cols],
        })
    return rows


def find_match(dashboard_name: str, excel_rows: list[dict]) -> dict | None:
    """
    Match simples:
    1. Pega o trecho de busca do MATCH_MAP
    2. Procura esse trecho dentro do nome normalizado de cada linha do Excel
    3. Se "Receita" (genérico), pega match exato — não parcial
    """
    search = MATCH_MAP.get(dashboard_name)
    if not search:
        search = _norm(dashboard_name)

    # Para "receita" genérico, precisa ser match exato para não pegar "receita nacional"
    exact_only = (search == "receita" or search == "nps net promoter")

    candidates = []
    for row in excel_rows:
        if exact_only:
            # Match exato: o nome normalizado do Excel deve SER exatamente o search
            # OU começar com search + espaço seguido de algo que não seja "nacional/internacional/prod/por"
            if row["name_norm"] == search:
                return row
        else:
            if search in row["name_norm"]:
                candidates.append(row)

    if exact_only:
        # Fallback: talvez o nome seja um pouco diferente
        for row in excel_rows:
            if search in row["name_norm"]:
                # Pegar o mais curto (mais específico / mais próximo do exato)
                candidates.append(row)
        if candidates:
            candidates.sort(key=lambda r: len(r["name_norm"]))
            return candidates[0]
        return None

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        candidates.sort(key=lambda r: len(r["name_norm"]))
        return candidates[0]
    return None


def populate_okrs(okrs: list[dict], path: Path) -> list[dict]:
    excel_rows = load_excel(path)
    debug = []

    for okr in okrs:
        for kr in okr["krs"]:
            kr["val"] = "—"
            kr["ant"] = "—"
            kr["meta"] = "—"
            kr["pct"] = 0
            kr["chart"] = []

            match = find_match(kr["name"], excel_rows)
            if match is None:
                debug.append({"KR": kr["name"], "Excel": "❌ NÃO ENCONTRADO", "Meta": "—"})
                continue

            # META: direto do Excel, sem reformatar
            kr["meta"] = _display_meta(match["meta_raw"])

            # Meses
            non_blank = [(i, v) for i, v in enumerate(match["months"]) if not _is_blank(v)]
            if non_blank:
                kr["val"] = _display_val(non_blank[-1][1])
                if len(non_blank) >= 2:
                    kr["ant"] = _display_val(non_blank[-2][1])
                kr["chart"] = [v for v in (_parse_num(v) for _, v in non_blank) if v is not None]

                # Progresso
                cur = _parse_num(non_blank[-1][1])
                tgt = _parse_num(match["meta_raw"])
                if cur is not None and tgt is not None and tgt != 0:
                    n = _norm(kr["name"])
                    lower_better = any(t in n for t in ("falha", "tempo", "churn", "nao ativadas", "chargeback", "solicitacoes"))
                    ratio = (tgt / cur) if lower_better and cur != 0 else (cur / tgt)
                    kr["pct"] = int(round(max(0.0, min(1.0, ratio)) * 100))

            debug.append({"KR": kr["name"], "Excel": match["name"], "Meta": kr["meta"]})

    st.session_state["_debug"] = debug
    st.session_state["_excel_found"] = path.exists()
    st.session_state["_excel_count"] = len(excel_rows)
    return okrs


# ─── Carregar ────────────────────────────────────────────────────────
OKRS = populate_okrs(OKRS, EXCEL_PATH)


# ─── Helpers UI ──────────────────────────────────────────────────────
def pct_color(pct: int) -> str:
    if pct <= 0: return "#6B7B94"
    if pct >= 95: return "#34D399"
    if pct >= 70: return "#FBBF24"
    return "#F87171"


def okr_status(krs):
    pcts = [kr.get("pct", 0) for kr in krs if kr.get("pct", 0) > 0]
    if not pcts: return "no_data"
    if any(p < 70 for p in pcts): return "red"
    if any(p < 95 for p in pcts): return "yellow"
    return "green"


def infer_y(kr):
    probe = " ".join([str(kr.get(k, "")) for k in ("name", "val", "ant", "meta")]).lower()
    if "r$" in probe: return "Valor (R$)", ",.2f"
    if "%" in probe: return "Percentual (%)", ".1f"
    if "dia" in probe: return "Dias", ".0f"
    if "/5" in probe: return "Pontuação (0-5)", ".2f"
    if "nps" in probe or "enps" in probe: return "Pontos (NPS)", ".0f"
    if "indice" in probe or "índice" in probe: return "Índice", ".2f"
    return "Valor", ",.2f"


def open_okr(idx):
    st.session_state["selected_okr"] = idx
    st.session_state["selected_kr_idx"] = 0


def close_okr():
    st.session_state["selected_okr"] = None
    st.session_state["selected_kr_idx"] = None


# ─── Dialog ──────────────────────────────────────────────────────────
@st.dialog("Detalhes do OKR", width="large")
def okr_dialog(okr, idx):
    accent = okr["accent"]
    status = okr_status(okr["krs"])
    sc = STATUS_COLORS[status]
    sel = st.session_state.get("selected_kr_idx", 0) or 0
    if not (0 <= sel < len(okr["krs"])):
        sel = 0

    st.markdown(
        f'<div style="background:linear-gradient(160deg,#181D2C,#141822);border:1px solid #2B3350;'
        f'border-left:6px solid {accent};border-radius:18px;padding:18px;margin-bottom:12px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<div><div style="color:{accent};font-weight:800;letter-spacing:1.3px;font-size:0.85rem;">{okr["title"]}</div>'
        f'<div style="color:#6B7B94;margin-top:6px;">{okr["subtitle"]}</div></div>'
        f'<div style="display:flex;align-items:center;gap:10px;">'
        f'<span style="width:10px;height:10px;border-radius:50%;background:{sc};display:inline-block;"></span>'
        f'<span style="color:#9DB2CC;font-size:0.85rem;">{STATUS_LABELS[status]}</span></div></div></div>',
        unsafe_allow_html=True,
    )

    st.subheader("Key Results")
    for ki, kr in enumerate(okr["krs"]):
        is_sel = ki == sel
        if st.button(f'{"▶ " if is_sel else ""}{kr["name"]} | {kr["val"]}', key=f"sel_{idx}_{ki}", use_container_width=True):
            st.session_state["selected_kr_idx"] = ki
            st.rerun()

        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pt = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"
        brd = f"1px solid {accent}" if is_sel else "1px solid rgba(255,255,255,0.04)"
        bg = "rgba(255,255,255,0.03)" if is_sel else "transparent"
        st.markdown(
            f'<div style="padding:10px;border:{brd};border-radius:10px;background:{bg};margin:6px 0;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:6px;">'
            f'<span style="color:#8090A8;font-size:0.85rem;font-weight:600;">{kr["name"]}</span>'
            f'<span style="color:#FFF;font-size:0.95rem;font-weight:800;">{kr["val"]}</span></div>'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">'
            f'<div style="flex:1;height:4px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden;">'
            f'<div style="width:{w}%;height:100%;background:{pc};"></div></div>'
            f'<span style="min-width:36px;text-align:right;color:{pc};font-weight:800;font-size:0.8rem;">{pt}</span></div>'
            f'<div style="color:#4A5670;font-size:0.75rem;">Ant: {kr["ant"]} · Meta: {kr["meta"]}</div></div>',
            unsafe_allow_html=True,
        )

    skr = okr["krs"][sel]
    series = skr.get("chart", [])
    mlabels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    st.subheader(f'Evolução — {skr["name"]}')
    if series:
        df = pd.DataFrame({"Mês": mlabels[:len(series)], "Valor": series})
        ymin, ymax = min(series), max(series)
        ypad = (ymax - ymin) * 0.12 if ymax != ymin else max(abs(ymax) * 0.12, 1)
        yt, yf = infer_y(skr)
        ch = (alt.Chart(df).mark_line(point=True, strokeWidth=2.5)
              .encode(x=alt.X("Mês:N", sort=mlabels, axis=alt.Axis(title="Mês", labelAngle=0)),
                      y=alt.Y("Valor:Q", scale=alt.Scale(domain=[ymin - ypad, ymax + ypad], nice=True, zero=False),
                               axis=alt.Axis(title=yt, format=yf)),
                      tooltip=[alt.Tooltip("Mês:N"), alt.Tooltip("Valor:Q", format=yf)])
              .properties(height=320))
        st.altair_chart(ch, use_container_width=True)
    else:
        st.info("Sem dados de evolução para este KR.")

    if st.button("Fechar", use_container_width=True, key=f"close_{idx}"):
        close_okr()
        st.rerun()


# ─── Session State ───────────────────────────────────────────────────
if "selected_okr" not in st.session_state:
    st.session_state["selected_okr"] = None
if "selected_kr_idx" not in st.session_state:
    st.session_state["selected_kr_idx"] = None

if st.session_state["selected_okr"] is not None:
    i = int(st.session_state["selected_okr"])
    if 0 <= i < len(OKRS):
        okr_dialog(OKRS[i], i)

# ─── CSS ─────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');
.stApp { background: radial-gradient(ellipse at 12% 8%, #141B2D 0%, #0F1117 50%, #0B0E14 100%); font-family: 'Nunito', system-ui, sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1500px; }
[data-testid="stHorizontalBlock"] { gap: 1.1rem; align-items: stretch; }
[data-testid="stColumn"] > div, [data-testid="stColumn"] > div > div { height: 100%; }
[data-testid="stElementToolbar"], [data-testid="stToolbar"] { display: none !important; }

.hdr { display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; margin-bottom: 1.2rem; border-bottom: 1px solid #1C2132; }
.hdr-title { font-family: 'Montserrat', sans-serif; font-size: 1.7rem; font-weight: 800; color: #FFF; margin: 0; }
.hdr-sub { font-size: 1.7rem; font-weight: 800; line-height: 1.05; color: rgba(246,246,246,0.92); font-family: 'Montserrat', sans-serif; }
.hdr-logo-right { height: 48px; width: auto; opacity: 0.95; }

.sum-row { display: flex; gap: 0.8rem; margin-bottom: 1.4rem; }
.sum-card { flex: 1; background: rgba(255,255,255,0.035); border: 1px solid #1C2132; border-radius: 12px; padding: 14px 0; text-align: center; }
.sum-card:hover { background: rgba(255,255,255,0.06); }
.sum-val { font-size: 1.5rem; font-weight: 800; color: #FFF; }
.sum-lbl { font-size: 0.68rem; color: #5E6E85; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 2px; }

.okr-card { background: linear-gradient(160deg, #181D2C 0%, #141822 100%); border: 1px solid #232940; border-radius: 16px; padding: 20px 20px 16px; height: 420px; display: flex; flex-direction: column; overflow: hidden; transition: transform 180ms ease, box-shadow 180ms ease; }
.okr-card:hover { transform: translateY(-3px); border-color: #384060; box-shadow: 0 16px 48px rgba(0,0,0,0.4); }
.c-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 4px; }
.c-head-left { display: flex; align-items: center; gap: 10px; }
.c-title { font-family: 'Montserrat', sans-serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
.c-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; animation: dot-pulse 2.5s ease-in-out infinite; }
@keyframes dot-pulse { 0%, 100% { box-shadow: 0 0 4px 1px currentColor; } 50% { box-shadow: 0 0 12px 3px currentColor; } }
.c-sub { color: #6B7B94; font-size: 0.76rem; margin-bottom: 14px; line-height: 1.35; }

div[class*="st-key-okr_actions_"] { margin-bottom: 12px; }
div[class*="st-key-okr_actions_"] [data-testid="stHorizontalBlock"] { display: flex; flex-wrap: nowrap; gap: 0.6rem; }
div[class*="st-key-okr_actions_"] [data-testid="stHorizontalBlock"] > div { flex: 0 0 auto !important; width: auto !important; min-width: 112px; }
div[class*="st-key-okr_actions_"] [data-testid="stButton"] button {
    border-radius: 999px !important; padding: 5px 14px !important; font-size: 0.72rem !important; font-weight: 700 !important;
    background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.16) !important;
    color: rgba(246,246,246,0.88) !important; white-space: nowrap !important; min-height: unset !important; height: auto !important;
}
div[class*="st-key-okr_actions_"] [data-testid="stButton"] button:hover { background: rgba(255,255,255,0.12) !important; }

.c-body { flex: 1; min-height: 0; }
.c-krs { display: flex; flex-direction: column; overflow-y: auto; padding-right: 6px; }
.c-krs::-webkit-scrollbar { width: 4px; }
.c-krs::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 2px; }
.kr { padding: 9px 0 8px; border-top: 1px solid rgba(255,255,255,0.05); }
.kr:first-child { border-top: none; padding-top: 0; }
.kr-top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
.kr-nm { color: #8090A8; font-size: 0.76rem; font-weight: 500; }
.kr-vl { color: #FFF; font-size: 0.92rem; font-weight: 700; white-space: nowrap; }
.kr-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
.kr-track { flex: 1; height: 3px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; }
.kr-fill { height: 100%; border-radius: 2px; transition: width 0.8s cubic-bezier(0.4,0,0.2,1); }
.kr-pct { font-size: 0.68rem; font-weight: 600; min-width: 30px; text-align: right; }
.kr-meta { color: #4A5670; font-size: 0.65rem; }

.ftr { text-align: center; color: #3D4A60; font-size: 0.72rem; padding-top: 1.2rem; margin-top: 1.8rem; border-top: 1px solid #1C2132; }
@media (max-width: 768px) { .sum-row { flex-wrap: wrap; } .sum-card { min-width: 45%; } }
</style>""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
    <div><div class="hdr-title">OKRs Estratégicos</div>
    <div class="hdr-sub">PagBrasil &middot; Indicadores de Performance</div></div>
    <img class="hdr-logo-right" src="https://i.imgur.com/CYyv2PD.png" alt="PagBrasil" />
</div>""", unsafe_allow_html=True)

# ─── Debug (REMOVER depois de validar) ───────────────────────────────
with st.expander("🔍 Debug — Verificar matching Excel ↔ Dashboard", expanded=False):
    st.write(f"**Excel:** `{EXCEL_PATH}` → {'✅ Encontrado' if st.session_state.get('_excel_found') else '❌ Não encontrado'}")
    st.write(f"**Linhas lidas:** {st.session_state.get('_excel_count', 0)}")
    dbg = st.session_state.get("_debug", [])
    if dbg:
        st.dataframe(pd.DataFrame(dbg), use_container_width=True, hide_index=True)

# ─── Summary ─────────────────────────────────────────────────────────
total_krs = sum(len(o["krs"]) for o in OKRS)
statuses = [okr_status(o["krs"]) for o in OKRS]
on_track = sum(1 for s in statuses if s == "green")
attention = sum(1 for s in statuses if s == "yellow")
at_risk = sum(1 for s in statuses if s == "red")
valid_pcts = [kr["pct"] for o in OKRS for kr in o["krs"] if kr.get("pct", 0) > 0]
avg_pct = round(sum(valid_pcts) / len(valid_pcts)) if valid_pcts else 0

st.markdown(f"""
<div class="sum-row">
    <div class="sum-card"><div class="sum-val">{total_krs}</div><div class="sum-lbl">Key Results</div></div>
    <div class="sum-card"><div class="sum-val" style="color:#34D399">{on_track}</div><div class="sum-lbl">On Track</div></div>
    <div class="sum-card"><div class="sum-val" style="color:#FBBF24">{attention}</div><div class="sum-lbl">Atenção</div></div>
    <div class="sum-card"><div class="sum-val" style="color:#F87171">{at_risk}</div><div class="sum-lbl">Em Risco</div></div>
    <div class="sum-card"><div class="sum-val">{avg_pct}%</div><div class="sum-lbl">Progresso Médio</div></div>
</div>""", unsafe_allow_html=True)


# ─── Card Renderer ───────────────────────────────────────────────────
def render_card(okr, idx):
    accent = okr["accent"]
    status = okr_status(okr["krs"])
    sc = STATUS_COLORS[status]

    rows = ""
    for kr in okr["krs"]:
        pc = pct_color(kr["pct"])
        w = min(kr["pct"], 100)
        pt = f'{kr["pct"]}%' if kr["pct"] > 0 else "—"
        rows += (
            f'<div class="kr"><div class="kr-top"><span class="kr-nm">{kr["name"]}</span>'
            f'<span class="kr-vl">{kr["val"]}</span></div>'
            f'<div class="kr-bar-row"><div class="kr-track"><div class="kr-fill" style="width:{w}%;background:{pc}"></div></div>'
            f'<span class="kr-pct" style="color:{pc}">{pt}</span></div>'
            f'<div class="kr-meta">Ant: {kr["ant"]}  ·  Meta: {kr["meta"]}</div></div>'
        )

    with st.container(key=f"okr_actions_{idx}", horizontal=True, horizontal_alignment="left", gap="small"):
        oc = st.button("Veja mais", key=f"open_{idx}")
        sc2 = st.button("Squads", key=f"squads_{idx}")
    if oc or sc2:
        open_okr(idx)
        st.rerun()

    st.markdown(
        f'<div class="okr-card" style="border-left:4px solid {accent};">'
        f'<div class="c-head"><div class="c-head-left">'
        f'<span class="c-title" style="color:{accent}">{okr["title"]}</span>'
        f'<span class="c-dot" style="background:{sc};color:{sc}"></span></div></div>'
        f'<div class="c-sub">{okr["subtitle"]}</div>'
        f'<div class="c-body"><div class="c-krs">{rows}</div></div></div>',
        unsafe_allow_html=True,
    )


# ─── Layout ──────────────────────────────────────────────────────────
row1 = st.columns(3)
for i in range(3):
    with row1[i]:
        render_card(OKRS[i], i)

st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

_, col_p, col_c, _ = st.columns([0.5, 1, 1, 0.5])
with col_p:
    render_card(OKRS[3], 3)
with col_c:
    render_card(OKRS[4], 4)

st.markdown('<div class="ftr">PagBrasil &nbsp;·&nbsp; Dashboard Estratégico de OKRs &nbsp;·&nbsp; People &amp; Development</div>', unsafe_allow_html=True)
