"""
SolvEDO — Equações de 2ª Ordem com Coeficientes Constantes
         ay'' + by' + cy = 0
Autora : Marcela
Engine : SymPy · Streamlit
"""

import streamlit as st
import sympy as sp
from sympy import Function, dsolve, Eq, symbols, exp, cos, sin, sqrt, latex

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SolvEDO · Coeficientes",
    page_icon="∂",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Tokens ── */
:root {
  --bg:          #faf5f6;
  --card:        #ffffff;
  --panel:       #f7edf0;
  --rose:        #c7979b;
  --rose-dark:   #a97478;
  --rose-glow:   rgba(199,151,155,0.18);
  --rose-soft:   #e8c4c7;
  --nude:        #e2d0cc;
  --slate:       #58535e;
  --slate-lt:    #96909c;
  --text:        #3a353f;
  --text-soft:   #7a7280;
  --border:      #e4d4d8;
  --success:     #6fa882;
  --warn:        #c8986a;
  --error:       #c06870;
  --mono:        'JetBrains Mono', monospace;
  --sans:        'Inter', system-ui, sans-serif;
  --r:           14px;
  --r-sm:        9px;
  --shadow-card: 0 4px 28px rgba(160,100,110,0.09);
  --shadow-btn:  0 4px 16px rgba(199,151,155,0.40);
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: var(--sans) !important;
  color: var(--text) !important;
}
[data-testid="stHeader"]        { background: transparent !important; }
[data-testid="stToolbar"]       { display: none !important; }
.block-container {
  max-width: 660px !important;
  padding: 0 0 60px !important;
}

/* ─── HEADER ─── */
.app-header {
  background: linear-gradient(135deg, #c7979b 0%, #b07478 55%, #956068 100%);
  border-radius: 0 0 22px 22px;
  padding: 30px 36px 26px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 18px;
  box-shadow: 0 6px 32px rgba(160,100,110,0.22);
}
.header-badge {
  width: 56px; height: 56px; flex-shrink: 0;
  background: rgba(255,255,255,0.20);
  border: 1.5px solid rgba(255,255,255,0.32);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; font-weight: 700; color: #fff;
}
.header-text h1 {
  color: #fff !important; margin: 0 !important; padding: 0 !important;
  font-size: 1.4rem !important; font-weight: 700 !important;
  letter-spacing: 0.01em;
}
.header-text p {
  color: rgba(255,255,255,0.78) !important;
  font-size: 0.8rem !important; margin: 4px 0 0 !important;
  font-weight: 300; letter-spacing: 0.03em;
}
.header-author {
  margin-left: auto; text-align: right; flex-shrink: 0;
  color: rgba(255,255,255,0.80); font-size: 0.74rem; line-height: 1.5;
}
.header-author strong { display: block; color: #fff; font-size: 0.9rem; }

/* ─── SEÇÃO DE EQUAÇÃO ─── */
.eq-preview-wrap {
  background: var(--panel);
  border: 1.5px solid var(--border);
  border-radius: var(--r);
  padding: 18px 24px 14px;
  margin-bottom: 24px;
  text-align: center;
}
.eq-label {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.13em; text-transform: uppercase;
  color: var(--slate-lt); margin-bottom: 10px;
}
.eq-display {
  font-size: 1.25rem;
  color: var(--text);
  font-family: var(--mono);
  letter-spacing: 0.04em;
}
.eq-display .coef-a { color: var(--rose-dark); font-weight: 600; }
.eq-display .coef-b { color: #7a82c0;          font-weight: 600; }
.eq-display .coef-c { color: var(--success);   font-weight: 600; }

/* ─── CARD PRINCIPAL ─── */
.main-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 28px 30px 24px;
  box-shadow: var(--shadow-card);
  margin-bottom: 20px;
}
.card-section-title {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.13em; text-transform: uppercase;
  color: var(--slate-lt);
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}

/* ─── INPUTS NUMÉRICOS ─── */
[data-testid="stNumberInput"] {
  background: transparent !important;
}
[data-testid="stNumberInput"] label {
  font-family: var(--sans) !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
  color: var(--slate) !important;
  letter-spacing: 0.02em;
}
[data-testid="stNumberInput"] input {
  font-family: var(--mono) !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  background: var(--bg) !important;
  border: 1.5px solid var(--nude) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
  text-align: center !important;
  padding: 10px 0 !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color: var(--rose) !important;
  box-shadow: 0 0 0 3px var(--rose-glow) !important;
  outline: none !important;
}

/* Colorir borda do input por posição (a=rosa, b=roxo, c=verde) */
div[data-testid="column"]:nth-child(1) [data-testid="stNumberInput"] input:focus {
  border-color: var(--rose-dark) !important;
  box-shadow: 0 0 0 3px rgba(199,151,155,0.20) !important;
}
div[data-testid="column"]:nth-child(2) [data-testid="stNumberInput"] input:focus {
  border-color: #8890cc !important;
  box-shadow: 0 0 0 3px rgba(136,144,204,0.18) !important;
}
div[data-testid="column"]:nth-child(3) [data-testid="stNumberInput"] input:focus {
  border-color: var(--success) !important;
  box-shadow: 0 0 0 3px rgba(111,168,130,0.18) !important;
}

/* setas do number input */
[data-testid="stNumberInput"] button {
  border-radius: 6px !important;
  border-color: var(--nude) !important;
  color: var(--slate) !important;
}

/* ─── COEF BADGE ─── */
.coef-badge {
  display: flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 8px;
  font-family: var(--mono); font-size: 1rem; font-weight: 700;
  margin: 0 auto 6px; border: 2px solid;
}
.badge-a { color: var(--rose-dark); background: #f7edf0; border-color: var(--rose-soft); }
.badge-b { color: #7a82c0;          background: #eef0f8; border-color: #c8ccea; }
.badge-c { color: var(--success);   background: #edf5f0; border-color: #b8d8c4; }

/* ─── BOTÃO ─── */
[data-testid="stButton"] > button {
  font-family: var(--sans) !important;
  font-weight: 600 !important; font-size: 0.95rem !important;
  background: linear-gradient(135deg, var(--rose) 0%, var(--rose-dark) 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  padding: 13px 0 !important;
  width: 100% !important;
  letter-spacing: 0.04em !important;
  box-shadow: var(--shadow-btn) !important;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
  margin-top: 8px !important;
}
[data-testid="stButton"] > button:hover {
  opacity: 0.88 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 7px 22px rgba(199,151,155,0.48) !important;
}
[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
}

/* ─── CARDS DE RESULTADO ─── */
.res-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  overflow: hidden;
  margin-bottom: 14px;
  box-shadow: var(--shadow-card);
}
.res-card-head {
  background: linear-gradient(90deg, var(--panel), #fdf6f7);
  padding: 11px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px;
}
.rch-icon { font-size: 0.95rem; }
.rch-title {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--slate);
}
.res-card-body { padding: 18px 22px; }

/* ─── DISCRIMINANTE + RAÍZES ─── */
.delta-box {
  display: flex; align-items: center; gap: 10px;
  background: var(--bg); border-radius: var(--r-sm);
  padding: 12px 16px; margin-bottom: 12px;
  border: 1px solid var(--border);
}
.delta-label {
  font-family: var(--mono); font-size: 0.78rem;
  color: var(--slate-lt); min-width: 80px;
}
.delta-value { font-family: var(--mono); font-size: 1rem; font-weight: 600; }
.delta-pos  { color: var(--success); }
.delta-zero { color: var(--warn); }
.delta-neg  { color: #8890cc; }

.case-badge {
  display: inline-block; font-size: 0.72rem; font-weight: 600;
  padding: 4px 12px; border-radius: 20px; margin-bottom: 12px;
  letter-spacing: 0.05em;
}
.case-real  { background: #edf5f0; color: var(--success); border: 1px solid #b8d8c4; }
.case-rep   { background: #fdf3e8; color: var(--warn);    border: 1px solid #e8ccaa; }
.case-comp  { background: #eef0f8; color: #7a82c0;        border: 1px solid #c8ccea; }

/* ─── EQUAÇÃO DESTACADA ─── */
.eq-box {
  background: linear-gradient(135deg, #fdf4f6, #fef8f0);
  border: 1.5px solid var(--rose-soft);
  border-radius: var(--r-sm);
  padding: 20px 24px;
  text-align: center;
  margin: 10px 0;
  font-size: 1.05rem;
}

/* ─── RAÍZES ─── */
.roots-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 10px; margin-top: 8px;
}
.root-item {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--r-sm); padding: 10px 14px; text-align: center;
}
.root-label { font-size: 0.68rem; color: var(--slate-lt); font-weight: 600;
              letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }
.root-value { font-family: var(--mono); font-size: 0.95rem; color: var(--text); font-weight: 500; }

/* ─── STATUS CHECK ─── */
.check-ok   { color: var(--success); font-weight: 600; font-size: 0.82rem; }
.check-warn { color: var(--warn);    font-weight: 600; font-size: 0.82rem; }

/* ─── ERRO ─── */
.err-box {
  background: #fdf0f1; border: 1.5px solid #e8b8bb;
  border-left: 4px solid var(--error); border-radius: var(--r-sm);
  padding: 14px 18px; font-family: var(--mono);
  font-size: 0.8rem; color: #8a3a3e;
}

/* ─── EMPTY STATE ─── */
.empty-wrap {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 50px 24px; gap: 10px;
  color: var(--text-soft); text-align: center;
}
.es-icon { font-size: 2.8rem; opacity: 0.30; margin-bottom: 4px; }
.es-text  { font-size: 0.87rem; line-height: 1.75; }

/* ─── FOOTER ─── */
.app-footer {
  margin-top: 36px;
  padding: 14px 0;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}
.ft-left  { font-size: 0.71rem; color: var(--slate-lt); }
.ft-right {
  font-size: 0.7rem; font-family: var(--mono);
  color: #fff; background: var(--rose-dark);
  padding: 3px 11px; border-radius: 20px;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--nude); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# LÓGICA MATEMÁTICA
# ─────────────────────────────────────────────────────────────

def resolver_edo(a: float, b: float, c: float):
    """
    Resolve  ay'' + by' + cy = 0  com coeficientes reais.
    Retorna dict com discriminante, raízes, tipo, solução geral e HTML.
    """
    t = symbols('t', real=True)
    y = Function('y')

    # Monta e resolve
    edo = Eq(a * y(t).diff(t, 2) + b * y(t).diff(t) + c * y(t), 0)
    sol = dsolve(edo, y(t))

    # Equação característica: ar² + br + c = 0
    r = symbols('r')
    carac = a * r**2 + b * r + c
    delta = sp.Rational(b**2) - 4 * sp.Rational(a) * sp.Rational(c)

    raizes = sp.solve(carac, r)

    # Tipo de raiz
    delta_float = float(b**2 - 4*a*c)
    if abs(delta_float) < 1e-10:
        tipo = "repetida"
    elif delta_float > 0:
        tipo = "reais_distintas"
    else:
        tipo = "complexas"

    return {
        "edo":    edo,
        "sol":    sol,
        "delta":  delta,
        "delta_f": delta_float,
        "raizes": raizes,
        "tipo":   tipo,
        "carac":  carac,
    }


def build_result_html(res: dict, a, b, c) -> str:
    """Monta o HTML dos cards de resultado."""

    # ── Discriminante ──
    df = res["delta_f"]
    if abs(df) < 1e-10:
        dcls = "delta-zero"; dsymbol = "Δ = 0"
    elif df > 0:
        dcls = "delta-pos";  dsymbol = f"Δ = {sp.latex(res['delta'])}"
    else:
        dcls = "delta-neg";  dsymbol = f"Δ = {sp.latex(res['delta'])}"

    # ── Tipo ──
    tipo = res["tipo"]
    if tipo == "reais_distintas":
        case_lbl  = "Raízes Reais e Distintas"
        case_cls  = "case-real"
        case_icon = "📗"
    elif tipo == "repetida":
        case_lbl  = "Raiz Real Repetida"
        case_cls  = "case-rep"
        case_icon = "📙"
    else:
        case_lbl  = "Raízes Complexas Conjugadas"
        case_cls  = "case-comp"
        case_icon = "📘"

    # ── Raízes HTML ──
    raizes = res["raizes"]
    if len(raizes) == 2:
        r1_tex = sp.latex(sp.simplify(raizes[0]))
        r2_tex = sp.latex(sp.simplify(raizes[1]))
        roots_html = f"""
        <div class="roots-grid">
          <div class="root-item">
            <div class="root-label">r₁</div>
            <div class="root-value">\\({r1_tex}\\)</div>
          </div>
          <div class="root-item">
            <div class="root-label">r₂</div>
            <div class="root-value">\\({r2_tex}\\)</div>
          </div>
        </div>"""
    elif len(raizes) == 1:
        r1_tex = sp.latex(sp.simplify(raizes[0]))
        roots_html = f"""
        <div class="roots-grid">
          <div class="root-item">
            <div class="root-label">r₁ = r₂</div>
            <div class="root-value">\\({r1_tex}\\)</div>
          </div>
        </div>"""
    else:
        roots_html = "<p style='color:var(--text-soft);font-size:0.82rem;'>Raízes não determinadas.</p>"

    # Verificação
    try:
        ok, _ = sp.checkodesol(res["edo"], res["sol"])
        verif = (
            '<span class="check-ok">✓ Solução verificada pelo SymPy</span>'
            if ok else
            '<span class="check-warn">⚠ Verificação automática inconclusiva</span>'
        )
    except Exception:
        verif = '<span class="check-warn">⚠ Verificação não disponível</span>'

    # LaTeX
    edo_tex = sp.latex(res["edo"])
    sol_tex = sp.latex(res["sol"])
    car_tex = sp.latex(sp.Eq(res["carac"], 0))

    html = f"""
    <!-- EDO montada -->
    <div class="res-card">
      <div class="res-card-head">
        <span class="rch-icon">📝</span>
        <span class="rch-title">Equação Diferencial</span>
      </div>
      <div class="res-card-body">
        <div class="eq-box">\\[ {edo_tex} \\]</div>
      </div>
    </div>

    <!-- Equação característica -->
    <div class="res-card">
      <div class="res-card-head">
        <span class="rch-icon">🔢</span>
        <span class="rch-title">Equação Característica</span>
      </div>
      <div class="res-card-body">
        <div class="eq-box" style="font-size:1rem;">\\[ {car_tex} \\]</div>
        <div class="delta-box" style="margin-top:14px;">
          <span class="delta-label">Discriminante</span>
          <span class="delta-value {dcls}">\\({dsymbol}\\)</span>
        </div>
        <span class="case-badge {case_cls}">{case_icon} {case_lbl}</span>
        {roots_html}
      </div>
    </div>

    <!-- Solução geral -->
    <div class="res-card">
      <div class="res-card-head">
        <span class="rch-icon">✨</span>
        <span class="rch-title">Solução Geral</span>
      </div>
      <div class="res-card-body">
        <div class="eq-box">\\[ {sol_tex} \\]</div>
        <div style="margin-top:12px;">{verif}</div>
      </div>
    </div>
    """
    return html


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="header-badge">∂</div>
  <div class="header-text">
    <h1>SolvEDO</h1>
    <p>Equações de 2ª Ordem · Coeficientes Constantes</p>
  </div>
  <div class="header-author">
    <strong>Marcela</strong>
    Matemática · SymPy
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PREVIEW DA EQUAÇÃO (dinâmico via session_state)
# ─────────────────────────────────────────────────────────────
if "a_val" not in st.session_state:
    st.session_state.a_val = 1.0
if "b_val" not in st.session_state:
    st.session_state.b_val = 0.0
if "c_val" not in st.session_state:
    st.session_state.c_val = 0.0

def fmt(v):
    """Formata coeficiente para exibição limpa."""
    if v == int(v):
        return str(int(v))
    return f"{v:.2f}".rstrip('0').rstrip('.')

a_prev = st.session_state.a_val
b_prev = st.session_state.b_val
c_prev = st.session_state.c_val

st.markdown(f"""
<div class="eq-preview-wrap">
  <div class="eq-label">Equação configurada</div>
  <div class="eq-display">
    <span class="coef-a">{fmt(a_prev)}</span>y'' +&nbsp;
    <span class="coef-b">{fmt(b_prev)}</span>y' +&nbsp;
    <span class="coef-c">{fmt(c_prev)}</span>y = 0
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CARD DE ENTRADA — COEFICIENTES
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="card-section-title">Coeficientes da EDO</div>', unsafe_allow_html=True)

# Badges coloridos acima de cada coluna
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.markdown('<div class="coef-badge badge-a">a</div>', unsafe_allow_html=True)
with col_b2:
    st.markdown('<div class="coef-badge badge-b">b</div>', unsafe_allow_html=True)
with col_b3:
    st.markdown('<div class="coef-badge badge-c">c</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    a = st.number_input(
        "Coeficiente  a  (y'')",
        value=1.0, step=1.0,
        format="%.2f",
        key="a_val",
    )
with col2:
    b = st.number_input(
        "Coeficiente  b  (y')",
        value=0.0, step=1.0,
        format="%.2f",
        key="b_val",
    )
with col3:
    c = st.number_input(
        "Coeficiente  c  (y)",
        value=0.0, step=1.0,
        format="%.2f",
        key="c_val",
    )

st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

# Aviso se a = 0
if a == 0:
    st.markdown(
        '<div class="err-box" style="margin-bottom:12px;">'
        '⚠ O coeficiente <b>a</b> não pode ser zero — a equação deixa de ser de 2ª ordem.'
        '</div>',
        unsafe_allow_html=True
    )

resolver = st.button("Resolver EDO", use_container_width=True, disabled=(a == 0))
st.markdown('</div>', unsafe_allow_html=True)  # fecha main-card


# ─────────────────────────────────────────────────────────────
# ÁREA DE RESULTADO
# ─────────────────────────────────────────────────────────────
if not resolver:
    st.markdown("""
    <div class="empty-wrap">
      <div class="es-icon">∫</div>
      <div class="es-text">
        Defina os coeficientes <strong>a</strong>, <strong>b</strong> e <strong>c</strong><br>
        e clique em <strong>Resolver EDO</strong>.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    with st.spinner("Calculando..."):
        try:
            res = resolver_edo(float(a), float(b), float(c))
            html_result = build_result_html(res, a, b, c)
            st.markdown(html_result, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(
                f'<div class="err-box">⚠ Erro ao processar: {e}</div>',
                unsafe_allow_html=True
            )


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <span class="ft-left">Autora: <strong>Marcela</strong> · SymPy &amp; Streamlit · Python</span>
  <span class="ft-right">SolvEDO v2.0</span>
</div>
""", unsafe_allow_html=True)
