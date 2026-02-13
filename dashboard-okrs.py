import streamlit as st
import pandas as pd
import altair as alt
import re
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

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
EXCEL_MONTH_COLUMNS = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

# Dashboard KR name (normalized) -> target strategic KR label (normalized/partial) from Excel
KR_NAME_LINKS = {
    "receita": "receita",
    "receita nacional nb": "receita nacional nb",
    "receita internacional xb": "receita internacional xb",
    "receita prod 24 meses": "receita de produtos com menos de 24 meses",
    "clientes c novos prod": "clientes enderecaveis que usam novos produtos",
    "clientes c novas func": "clientes enderecaveis que usam novas funcionalidades",
    "taxa de falhas criticas": "taxa de falhas criticas",
    "indice inovacao percebida": "indice de inovacao percebida pesquisa",
    "taxa de conversao": "taxa de conversao",
    "receita por pessoa": "receita por pessoa",
    "tempo onboarding nb": "tempo medio de ciclo de onboarding de merchants nb aceite da proposta ate a primeira transacao todas que foram a processing no mes",
    "tempo onboarding xb": "tempo medio de ciclo de onboarding de merchants xb digital aceite da proposta ate a primeira transacao todas que foram a processing no mes",
    "processos documentados": "processos documentados disponiveis de forma sistemica",
    "indice de engajamento": "indice de engajamento",
    "de certificacao interna": "de certificacao interna desempenho treinamento formal",
    "enps": "enps",
    "pontuacao gptw": "pontuacao gptw",
    "nps": "nps net promoter score",
    "contas nao ativadas": "de contas nao ativadas",
    "mrr churn rate": "mrr churn rate",
    "atendimentos no sla": "de atendimentos dentro do sla com clientes",
    "taxa de chargeback": "taxa de chargeback r",
    "csat": "csat customer satisfaction score",
    "indicador de branding": "indicador de branding",
    "n solic contas ativas": "no de solicitacoes ticket no zendesk por no de contas ativas organizacoes zendesk",
}

# ─── Data ────────────────────────────────────────────────────────────
OKRS = [
    {
        "title": "CRESCIMENTO",
        "subtitle": "Impulsionar o crescimento sustentável e rentável",
        "accent": "#54CA30",
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
        "accent": "#54CA30",
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
        "accent": "#54CA30",
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
        "accent": "#0058B5",
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
        "accent": "#0058B5",
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


def _is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    return str(value).strip() in {"", "nan", "None"}


def _normalize_text(value: str) -> str:
    value = str(value or "").strip().lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _parse_numeric(value):
    if _is_blank(value):
        return None
    if isinstance(value, (int, float)) and not pd.isna(value):
        return float(value)

    raw = str(value).strip().replace("R$", "").replace(" ", "")
    match = re.search(r"-?\d+(?:[.,]\d+)?", raw)
    if not match:
        return None

    token = match.group(0)
    if "." in token and "," in token:
        token = token.replace(".", "").replace(",", ".")
    elif "," in token and "." not in token:
        token = token.replace(",", ".")

    try:
        return float(token)
    except ValueError:
        return None


def _to_display(value) -> str:
    if _is_blank(value):
        return "—"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value).strip()


def _format_excel_meta(value, kr_name: str = "") -> str:
    """Formata o valor da meta preservando o formato original do Excel.

    Lida com os casos comuns:
    - Percentuais armazenados como decimal (0.85 -> 85%)
    - Valores monetários
    - Números inteiros
    - Strings já formatadas (passam direto)
    """
    if _is_blank(value):
        return ""

    # Se já é string com formatação (R$, %, ≤, etc.), preservar como está
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            return stripped
        return ""

    # Se é número, precisamos inferir o formato correto
    if isinstance(value, (int, float)) and not pd.isna(value):
        num = float(value)
        name_lower = _normalize_text(kr_name)

        # Detectar se é percentual pelo nome do KR ou pelo valor (0 < x < 1 tipicamente %)
        pct_terms = (
            "taxa", "percentual", "clientes", "conversao", "engajamento",
            "certificacao", "processos", "documentados", "contas", "ativadas",
            "churn", "atendimentos", "sla", "falhas",
        )
        is_likely_pct = any(term in name_lower for term in pct_terms)

        # Se o valor está entre 0 e 1 (exclusive) e o KR sugere percentual,
        # o Excel provavelmente armazenou como decimal
        if is_likely_pct and 0 < abs(num) < 1:
            pct_val = num * 100
            if pct_val == int(pct_val):
                return f"{int(pct_val)}%"
            # Mostrar com até 2 casas decimais
            return f"{pct_val:.2f}%".rstrip("0").rstrip(".").replace(".", ",") + "%"

        # Se o valor é >= 1 e parece percentual, mostrar como está com %
        if is_likely_pct and num >= 1:
            if num == int(num):
                return f"{int(num)}%"
            return f"{num:.2f}".rstrip("0").rstrip(".").replace(".", ",") + "%"

        # Detectar se é valor monetário
        money_terms = ("receita", "r$", "valor", "chargeback")
        is_likely_money = any(term in name_lower for term in money_terms)
        if is_likely_money:
            if num >= 1_000_000:
                millions = num / 1_000_000
                if millions == int(millions):
                    return f"R$ {int(millions)}M"
                return f"R$ {millions:.1f}M".replace(".", ",")
            elif num >= 1_000:
                thousands = num / 1_000
                if thousands == int(thousands):
                    return f"R$ {int(thousands)}K"
                return f"R$ {thousands:.1f}K".replace(".", ",")
            else:
                if num == int(num):
                    return f"R$ {int(num)}"
                return f"R$ {num:.2f}".replace(".", ",")

        # Detectar dias
        if "tempo" in name_lower or "onboarding" in name_lower or "dia" in name_lower:
            if num == int(num):
                return f"{int(num)} dias"
            return f"{num:.1f} dias".replace(".", ",")

        # Número genérico
        if num == int(num):
            return str(int(num))
        return f"{num:.4f}".rstrip("0").rstrip(".").replace(".", ",")

    return str(value).strip()


def _compute_progress_pct(kr_name: str, current_value, target_value):
    current_num = _parse_numeric(current_value)
    target_num = _parse_numeric(target_value)
    if current_num is None or target_num is None or target_num == 0:
        return None

    normalized = _normalize_text(kr_name)
    lower_is_better_terms = (
        "falha",
        "tempo",
        "churn",
        "nao ativadas",
        "chargeback",
        "solicitacoes",
    )
    lower_is_better = any(term in normalized for term in lower_is_better_terms)
    ratio = (target_num / current_num) if lower_is_better and current_num != 0 else (current_num / target_num)
    return int(round(max(0.0, min(1.0, ratio)) * 100))


def _find_col(columns, preferred_names: list[str], fallback_index: int):
    for name in preferred_names:
        if name in columns:
            return name
    return columns[fallback_index]


def load_excel_strategic_rows(excel_path: str) -> list[dict]:
    df = pd.read_excel(excel_path, sheet_name=EXCEL_BASE_SHEET)

    code_col = _find_col(list(df.columns), ["KRs ESTRATÉGICOS PAGBRASIL 2026"], 1)
    name_col = _find_col(list(df.columns), ["Unnamed: 2"], 2)
    meta_col = _find_col(list(df.columns), ["Meta"], 3)

    month_cols = [m for m in EXCEL_MONTH_COLUMNS if m in df.columns]
    strategic = df[df[code_col].notna() & (df[code_col].astype(str).str.strip() != "")].copy()

    records = []
    for _, row in strategic.iterrows():
        kr_name = row.get(name_col, "")
        if _is_blank(kr_name):
            continue

        month_raw = [row.get(col) for col in month_cols]
        month_num = [_parse_numeric(v) for v in month_raw]
        chart_values = [v for v in month_num if v is not None]
        has_month_data = len(chart_values) > 0
        non_blank_month = [v for v in month_raw if not _is_blank(v)]
        current_raw = non_blank_month[-1] if non_blank_month else None
        previous_raw = non_blank_month[-2] if len(non_blank_month) >= 2 else None

        target_raw = row.get(meta_col, None)
        pct = _compute_progress_pct(str(kr_name), current_raw, target_raw) if has_month_data else None

        records.append(
            {
                "name": str(kr_name).strip(),
                "name_norm": _normalize_text(kr_name),
                "current_raw": current_raw,
                "previous_raw": previous_raw,
                "target_raw": target_raw,
                "chart": chart_values,
                "pct": pct,
                "has_month_data": has_month_data,
            }
        )
    return records


def load_excel_meta_rows(excel_path: str) -> list[dict]:
    df = pd.read_excel(excel_path, sheet_name=EXCEL_BASE_SHEET)
    name_col = _find_col(list(df.columns), ["Unnamed: 2"], 2)
    meta_col = _find_col(list(df.columns), ["Meta"], 3)

    records = []
    for _, row in df.iterrows():
        kr_name = row.get(name_col, "")
        target_raw = row.get(meta_col, None)
        if _is_blank(kr_name) or _is_blank(target_raw):
            continue

        records.append(
            {
                "name": str(kr_name).strip(),
                "name_norm": _normalize_text(kr_name),
                "target_raw": target_raw,
            }
        )
    return records


def _find_excel_record_for_kr(kr_name: str, strategic_records: list[dict]):
    source_norm = _normalize_text(kr_name)
    target_norm = KR_NAME_LINKS.get(source_norm, source_norm)

    for rec in strategic_records:
        if rec["name_norm"] == target_norm:
            return rec

    candidates = []
    for rec in strategic_records:
        name_norm = rec["name_norm"]
        if target_norm in name_norm:
            candidates.append(rec)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        candidates.sort(key=lambda item: abs(len(item["name_norm"]) - len(target_norm)))
        return candidates[0]

    target_tokens = set(target_norm.split())
    scored = []
    for rec in strategic_records:
        name_tokens = set(rec["name_norm"].split())
        common = target_tokens & name_tokens
        if not common:
            continue
        score = len(common) / max(1, len(target_tokens))
        similarity = SequenceMatcher(None, target_norm, rec["name_norm"]).ratio()
        scored.append((score, len(common), similarity, -abs(len(rec["name_norm"]) - len(target_norm)), rec))

    if not scored:
        return None

    scored.sort(key=lambda item: (item[0], item[1], item[2], item[3]), reverse=True)
    best = scored[0]
    return best[4] if (best[0] >= 0.34 or best[2] >= 0.55) else None


def apply_excel_strategic_data(okrs: list[dict], excel_path: Path) -> list[dict]:
    strategic_records = []
    meta_records = []
    try:
        if excel_path.exists():
            strategic_records = load_excel_strategic_rows(str(excel_path))
            meta_records = load_excel_meta_rows(str(excel_path))
    except Exception:
        strategic_records = []
        meta_records = []

    # Fast exact-lookup for metas from Excel, keyed by normalized KR name.
    # Armazena tanto o valor bruto quanto o nome do KR para formatação contextual.
    meta_lookup = {}
    for rec in meta_records:
        meta_lookup[rec["name_norm"]] = {
            "target_raw": rec["target_raw"],
            "name": rec["name"],
        }

    updated_okrs = []
    for okr in okrs:
        okr_copy = dict(okr)
        new_krs = []
        for kr in okr.get("krs", []):
            kr_copy = dict(kr)
            # Dashboard always starts blank and is only filled by monthly Excel data.
            kr_copy["val"] = "—"
            kr_copy["ant"] = "—"
            kr_copy["meta"] = kr.get("meta", "") if not _is_blank(kr.get("meta", None)) else ""
            kr_copy["pct"] = 0
            kr_copy["chart"] = []

            rec = _find_excel_record_for_kr(kr_copy.get("name", ""), strategic_records)
            source_norm = _normalize_text(kr_copy.get("name", ""))
            target_norm = KR_NAME_LINKS.get(source_norm, source_norm)

            # ── META: priorizar valor direto do Excel ──
            meta_resolved = False

            # 1) Lookup exato por nome normalizado
            meta_entry = meta_lookup.get(target_norm, None)
            if meta_entry is not None and not _is_blank(meta_entry["target_raw"]):
                kr_copy["meta"] = _format_excel_meta(
                    meta_entry["target_raw"],
                    kr_name=meta_entry["name"],
                )
                meta_resolved = True

            # 2) Fallback: buscar no record estratégico encontrado
            if not meta_resolved and rec is not None and not _is_blank(rec.get("target_raw", None)):
                kr_copy["meta"] = _format_excel_meta(
                    rec["target_raw"],
                    kr_name=rec["name"],
                )
                meta_resolved = True

            # 3) Fallback: fuzzy match nos meta_records
            if not meta_resolved:
                meta_rec = _find_excel_record_for_kr(kr_copy.get("name", ""), meta_records)
                if meta_rec is not None and not _is_blank(meta_rec.get("target_raw", None)):
                    kr_copy["meta"] = _format_excel_meta(
                        meta_rec["target_raw"],
                        kr_name=meta_rec["name"],
                    )
                    meta_resolved = True

            # 4) Se nenhum Excel match, mantém o hardcoded do OKRS dict (já setado acima)

            # ── VALORES MENSAIS ──
            if rec is not None:
                if rec.get("has_month_data", False):
                    if not _is_blank(rec["current_raw"]):
                        kr_copy["val"] = _to_display(rec["current_raw"])
                    if not _is_blank(rec["previous_raw"]):
                        kr_copy["ant"] = _to_display(rec["previous_raw"])
                    if rec["chart"]:
                        kr_copy["chart"] = rec["chart"]
                    if rec["pct"] is not None:
                        kr_copy["pct"] = rec["pct"]
            new_krs.append(kr_copy)
        okr_copy["krs"] = new_krs
        updated_okrs.append(okr_copy)

    return updated_okrs


OKRS = apply_excel_strategic_data(OKRS, EXCEL_PATH)

# ─── Helpers ─────────────────────────────────────────────────────────
def pct_color(pct: int) -> str:
    if pct <= 0:
        return "#6B7B94"
    if pct >= 95:
        return "#34D399"
    if pct >= 70:
        return "#FBBF24"
    return "#F87171"


def okr_status_from_krs(krs: list[dict]) -> str:
    pcts = [kr.get("pct", 0) for kr in krs if kr.get("pct", 0) > 0]
    if not pcts:
        return "no_data"
    if any(p < 70 for p in pcts):
        return "red"
    if any(p < 95 for p in pcts):
        return "yellow"
    return "green"

def resolve_kr_series(okr: dict, kr: dict, kr_idx: int) -> tuple[list[float], str]:
    """Resolve the chart series for a KR.

    Uses only explicit KR series from Excel.
    """
    kr_series = kr.get("chart")
    if isinstance(kr_series, list) and len(kr_series) > 0:
        return kr_series, "kr"

    return [], "none"


def infer_y_axis_config(kr: dict) -> tuple[str, str]:
    """Infer Y-axis title and numeric format from KR metadata."""
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
    return "Valor", ",.2f"


def open_okr(idx: int):
    st.session_state["selected_okr"] = idx
    st.session_state["selected_kr_idx"] = 0


def close_okr():
    st.session_state["selected_okr"] = None
    st.session_state["selected_kr_idx"] = None


# ─── Dialog ──────────────────────────────────────────────────────────
def okr_dialog_legacy_unused(okr: dict, idx: int):
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


# ─── Session State ────────────────────────────────────────────────────
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
    if series_source == "none":
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
                    sort=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
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


if "selected_okr" not in st.session_state:
    st.session_state["selected_okr"] = None
if "selected_kr_idx" not in st.session_state:
    st.session_state["selected_kr_idx"] = None

if st.session_state["selected_okr"] is not None:
    i = int(st.session_state["selected_okr"])
    if 0 <= i < len(OKRS):
        okr_dialog_kr(OKRS[i], i)

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
   AÇÕES DO CARD ("Veja mais" e "Squads")
   Escopo pelo key do container para evitar conflito global.
   ============================================================ */
div[class*="st-key-okr_actions_"] {
    margin-bottom: 12px;
    padding-right: 0;
    padding-top: 0;
    overflow: visible;
}
div[class*="st-key-okr_actions_"] [data-testid="stHorizontalBlock"] {
    display: flex;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: center;
    gap: 0.6rem;
}
div[class*="st-key-okr_actions_"] [data-testid="stHorizontalBlock"] > div {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 112px;
}
div[class*="st-key-okr_actions_"] [data-testid="stButton"] {
    flex: 0 0 auto;
    width: auto !important;
}

/* Estilo pill dos botões do card */
div[class*="st-key-okr_actions_"] [data-testid="stButton"] button {
    display: inline-flex !important;
    justify-content: center !important;
    width: 100% !important;
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
div[class*="st-key-okr_actions_"] [data-testid="stButton"] button:hover {
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

    # ① Botões PRIMEIRO — mesma posição do header com escopo estável
    with st.container(
        key=f"okr_actions_{idx}",
        horizontal=True,
        horizontal_alignment="left",
        gap="small",
    ):
        open_clicked = st.button("Veja mais", key=f"open_{idx}")
        squads_clicked = st.button("Squads", key=f"squads_{idx}")

    if open_clicked or squads_clicked:
        open_okr(idx)
        st.rerun()

    # ② Card HTML DEPOIS — botões ficam acima com espaçamento fixo
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
