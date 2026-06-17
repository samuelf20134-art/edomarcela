"""
SolvEDO — Equações de 2ª Ordem com Coeficientes Constantes
         ay'' + by' + cy = 0
Autora : Marcela
Engine : SymPy · Streamlit
"""

import streamlit as st
import sympy as sp
from sympy import Function, dsolve, Eq, symbols, latex

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SolvEDO · Marcela",
    page_icon="∂",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #faf5f6;
  --card:      #ffffff;
  --panel:     #f7edf0;
  --rose:      #c7979b;
  --rose-dark: #a97478;
  --rose-soft: #e8c4c7;
  --nude:      #e2d0cc;
  --slate:     #58535e;
  --slate-lt:  #96909c;
  --text:      #3a353f;
  --text-soft: #7a7280;
  --border:    #e4d4d8;
  --success:   #6fa882;
  --warn:      #c8986a;
  --error:     #c06870;
  --mono:      'JetBrains Mono', monospace;
  --sans:      'Inter', system-ui, sans-serif;
  --r:         14px;
  --r-sm:      9px;
  --shadow:    0 4px 28px rgba(160,100,110,0.09);
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: var(--sans) !important;
  color: var(--text) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { max-width: 660px !important; padding: 0 0 60px !important; }

/* HEADER */
.app-header {
  background: linear-gradient(135deg,#c7979b 0%,#b07478 55%,#956068 100%);
  border-radius: 0 0 22px 22px;
  padding: 28px 32px 24px;
  margin-bottom: 28px;
  display: flex; align-items: center; gap: 16px;
  box-shadow: 0 6px 32px rgba(160,100,110,0.22);
}
.hdr-badge {
  width:52px;height:52px;flex-shrink:0;
  background:rgba(255,255,255,0.20);border:1.5px solid rgba(255,255,255,0.30);
  border-radius:13px;display:flex;align-items:center;justify-content:center;
  font-size:24px;font-weight:700;color:#fff;
}
.hdr-text h1 {
  color:#fff!important;margin:0!important;padding:0!important;
  font-size:1.35rem!important;font-weight:700!important;
}
.hdr-text p { color:rgba(255,255,255,0.75)!important;font-size:0.78rem!important;margin:3px 0 0!important;font-weight:300; }
.hdr-author { margin-left:auto;text-align:right;color:rgba(255,255,255,0.80);font-size:0.73rem;line-height:1.5; }
.hdr-author strong { display:block;color:#fff;font-size:0.88rem; }

/* EQ PREVIEW */
.eq-preview {
  background:var(--panel);border:1.5px solid var(--border);
  border-radius:var(--r);padding:16px 22px 14px;
  margin-bottom:22px;text-align:center;
}
.eq-preview-label {
  font-size:0.66rem;font-weight:700;letter-spacing:0.13em;
  text-transform:uppercase;color:var(--slate-lt);margin-bottom:8px;
}
.eq-preview-eq { font-family:var(--mono);font-size:1.18rem;letter-spacing:0.03em; }
.ca { color:#a97478;font-weight:700; }
.cb { color:#7a82c0;font-weight:700; }
.cc { color:#6fa882;font-weight:700; }

/* MAIN CARD */
.main-card {
  background:var(--card);border:1px solid var(--border);
  border-radius:var(--r);padding:26px 28px 22px;
  box-shadow:var(--shadow);margin-bottom:18px;
}
.card-title {
  font-size:0.66rem;font-weight:700;letter-spacing:0.13em;
  text-transform:uppercase;color:var(--slate-lt);
  padding-bottom:10px;border-bottom:1px solid var(--border);margin-bottom:18px;
}

/* BADGES */
.coef-badge {
  width:32px;height:32px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-size:1rem;font-weight:700;
  margin:0 auto 6px;border:2px solid;
}
.ba { color:#a97478;background:#f7edf0;border-color:var(--rose-soft); }
.bb { color:#7a82c0;background:#eef0f8;border-color:#c8ccea; }
.bc { color:#6fa882;background:#edf5f0;border-color:#b8d8c4; }

/* INPUTS */
[data-testid="stNumberInput"] label {
  font-family:var(--sans)!important;font-size:0.78rem!important;
  font-weight:600!important;color:var(--slate)!important;
}
[data-testid="stNumberInput"] input {
  font-family:var(--mono)!important;font-size:1rem!important;
  font-weight:500!important;background:var(--bg)!important;
  border:1.5px solid var(--nude)!important;border-radius:var(--r-sm)!important;
  color:var(--text)!important;text-align:center!important;
  transition:border-color 0.2s,box-shadow 0.2s!important;
}
[data-testid="stNumberInput"] input:focus {
  border-color:var(--rose)!important;
  box-shadow:0 0 0 3px rgba(199,151,155,0.18)!important;outline:none!important;
}

/* BOTÃO */
[data-testid="stButton"]>button {
  font-family:var(--sans)!important;font-weight:600!important;
  font-size:0.95rem!important;letter-spacing:0.04em!important;
  background:linear-gradient(135deg,var(--rose) 0%,var(--rose-dark) 100%)!important;
  color:#fff!important;border:none!important;border-radius:var(--r-sm)!important;
  padding:13px 0!important;width:100%!important;margin-top:8px!important;
  box-shadow:0 4px 16px rgba(199,151,155,0.40)!important;
  transition:opacity 0.2s,transform 0.15s!important;
}
[data-testid="stButton"]>button:hover {
  opacity:0.87!important;transform:translateY(-2px)!important;
}

/* RESULT CARD */
.res-card {
  background:var(--card);border:1px solid var(--border);
  border-radius:var(--r);overflow:hidden;
  margin-bottom:14px;box-shadow:var(--shadow);
}
.res-head {
  background:linear-gradient(90deg,var(--panel),#fdf6f7);
  padding:10px 18px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:8px;
}
.res-head-title {
  font-size:0.67rem;font-weight:700;letter-spacing:0.12em;
  text-transform:uppercase;color:var(--slate);
}
.res-body { padding:16px 20px; }

/* DISCRIMINANTE */
.delta-row {
  display:flex;align-items:center;gap:10px;
  background:var(--bg);border-radius:var(--r-sm);
  padding:11px 15px;margin-bottom:12px;border:1px solid var(--border);
  font-family:var(--mono);
}
.delta-lbl { font-size:0.76rem;color:var(--slate-lt);min-width:100px; }
.delta-val { font-size:1rem;font-weight:700; }
.dpos { color:var(--success); }
.dzero{ color:var(--warn); }
.dneg { color:#8890cc; }

/* CASE BADGE */
.case-badge {
  display:inline-block;font-size:0.71rem;font-weight:600;
  padding:4px 13px;border-radius:20px;margin-bottom:14px;letter-spacing:0.05em;
}
.cb-real { background:#edf5f0;color:var(--success);border:1px solid #b8d8c4; }
.cb-rep  { background:#fdf3e8;color:var(--warn);   border:1px solid #e8ccaa; }
.cb-comp { background:#eef0f8;color:#7a82c0;       border:1px solid #c8ccea; }

/* RAÍZES GRID */
.roots-grid { display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px; }
.root-box {
  background:var(--bg);border:1px solid var(--border);
  border-radius:var(--r-sm);padding:12px 10px;text-align:center;
}
.root-lbl { font-size:0.67rem;color:var(--slate-lt);font-weight:600;
            letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px; }
.root-val { font-size:0.95rem;font-weight:600;color:var(--text); }

/* VERIFICAÇÃO */
.check-ok   { color:var(--success);font-weight:600;font-size:0.82rem; }
.check-warn { color:var(--warn);   font-weight:600;font-size:0.82rem; }

/* ERRO */
.err-box {
  background:#fdf0f1;border:1.5px solid #e8b8bb;
  border-left:4px solid var(--error);border-radius:var(--r-sm);
  padding:13px 16px;font-family:var(--mono);font-size:0.8rem;color:#8a3a3e;
}

/* EMPTY */
.empty-wrap {
  display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:50px 24px;gap:10px;
  color:var(--text-soft);text-align:center;
}
.es-icon { font-size:2.8rem;opacity:0.28;margin-bottom:4px; }
.es-text  { font-size:0.87rem;line-height:1.75; }

/* FOOTER */
.app-footer {
  margin-top:32px;padding:13px 0;border-top:1px solid var(--border);
  display:flex;justify-content:space-between;align-items:center;
}
.ft-l { font-size:0.7rem;color:var(--slate-lt); }
.ft-r { font-size:0.69rem;font-family:var(--mono);color:#fff;
        background:var(--rose-dark);padding:3px 11px;border-radius:20px; }

/* st.latex override */
[data-testid="stMarkdownContainer"] .katex { font-size: 1.15rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# LÓGICA MATEMÁTICA
# ─────────────────────────────────────────────────────────────
def resolver_edo(a, b, c):
    t = symbols('t', real=True)
    y = Function('y')

    edo = Eq(a * y(t).diff(t, 2) + b * y(t).diff(t) + c * y(t), 0)
    sol = dsolve(edo, y(t))

    r = symbols('r')
    carac    = a*r**2 + b*r + c
    delta_ex = sp.Rational(b**2) - 4*sp.Rational(a)*sp.Rational(c)
    raizes   = sp.solve(carac, r)

    df = float(b**2 - 4*a*c)
    if abs(df) < 1e-9:
        tipo = "repetida"
    elif df > 0:
        tipo = "reais"
    else:
        tipo = "complexas"

    # Verificação
    try:
        ok, _ = sp.checkodesol(edo, sol)
        verif_ok = ok
    except Exception:
        verif_ok = None

    return {
        "edo": edo, "sol": sol,
        "carac": carac, "delta": delta_ex, "delta_f": df,
        "raizes": raizes, "tipo": tipo, "verif_ok": verif_ok,
    }


def fmt(v):
    if v == int(v):
        return str(int(v))
    return f"{v:.2f}".rstrip('0').rstrip('.')


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="hdr-badge">∂</div>
  <div class="hdr-text">
    <h1>SolvEDO</h1>
    <p>Equações de 2ª Ordem · Coeficientes Constantes</p>
  </div>
  <div class="hdr-author"><strong>Marcela</strong>Matemática · SymPy</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in [("av", 1.0), ("bv", 0.0), ("cv", 0.0)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# PREVIEW DA EQUAÇÃO
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="eq-preview">
  <div class="eq-preview-label">Equação Configurada</div>
  <div class="eq-preview-eq">
    <span class="ca">{fmt(st.session_state.av)}</span>y'' +&nbsp;
    <span class="cb">{fmt(st.session_state.bv)}</span>y' +&nbsp;
    <span class="cc">{fmt(st.session_state.cv)}</span>y = 0
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CARD DE ENTRADA
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Coeficientes da EDO</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="coef-badge ba">a</div>', unsafe_allow_html=True)
    a = st.number_input("Coeficiente a (y'')", value=1.0, step=1.0, format="%.2f", key="av")
with c2:
    st.markdown('<div class="coef-badge bb">b</div>', unsafe_allow_html=True)
    b = st.number_input("Coeficiente b (y')",  value=0.0, step=1.0, format="%.2f", key="bv")
with c3:
    st.markdown('<div class="coef-badge bc">c</div>', unsafe_allow_html=True)
    c = st.number_input("Coeficiente c (y)",   value=0.0, step=1.0, format="%.2f", key="cv")

if a == 0:
    st.markdown(
        '<div class="err-box" style="margin-top:10px;">'
        '⚠ O coeficiente <b>a</b> não pode ser zero.</div>',
        unsafe_allow_html=True
    )

resolver_btn = st.button("Resolver EDO", use_container_width=True, disabled=(a == 0))
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# RESULTADO
# ─────────────────────────────────────────────────────────────
if not resolver_btn:
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
        except Exception as e:
            st.markdown(f'<div class="err-box">⚠ Erro: {e}</div>', unsafe_allow_html=True)
            st.stop()

    tipo  = res["tipo"]
    df    = res["delta_f"]
    delta = res["delta"]

    # ── CARD 1: EDO ──
    st.markdown("""
    <div class="res-card">
      <div class="res-head"><span>📝</span><span class="res-head-title">Equação Diferencial</span></div>
      <div class="res-body">
    """, unsafe_allow_html=True)
    st.latex(latex(res["edo"]))
    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── CARD 2: EQUAÇÃO CARACTERÍSTICA + RAÍZES ──
    st.markdown("""
    <div class="res-card">
      <div class="res-head"><span>🔢</span><span class="res-head-title">Análise da Equação Característica</span></div>
      <div class="res-body">
    """, unsafe_allow_html=True)

    # Equação característica
    st.latex(latex(Eq(res["carac"], 0)))

    # Discriminante
    if abs(df) < 1e-9:
        dcls, dsym = "dzero", f"\\Delta = 0"
    elif df > 0:
        dcls, dsym = "dpos",  f"\\Delta = {latex(delta)}"
    else:
        dcls, dsym = "dneg",  f"\\Delta = {latex(delta)}"

    st.markdown(f"""
    <div class="delta-row">
      <span class="delta-lbl">Discriminante</span>
      <span class="delta-val {dcls}">{dsym.replace('\\','\\\\')}</span>
    </div>
    """.replace('\\\\', '\\'), unsafe_allow_html=True)

    # Type badge
    if tipo == "reais":
        st.markdown('<span class="case-badge cb-real">📗 Raízes Reais e Distintas</span>', unsafe_allow_html=True)
    elif tipo == "repetida":
        st.markdown('<span class="case-badge cb-rep">📙 Raiz Real Repetida</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="case-badge cb-comp">📘 Raízes Complexas Conjugadas</span>', unsafe_allow_html=True)

    # Raízes — renderizadas com st.latex, lado a lado via colunas
    raizes = res["raizes"]
    if len(raizes) >= 2:
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown('<div class="root-box"><div class="root-lbl">Raiz r₁</div>', unsafe_allow_html=True)
            st.latex(latex(sp.simplify(raizes[0])))
            st.markdown('</div>', unsafe_allow_html=True)
        with rc2:
            st.markdown('<div class="root-box"><div class="root-lbl">Raiz r₂</div>', unsafe_allow_html=True)
            st.latex(latex(sp.simplify(raizes[1])))
            st.markdown('</div>', unsafe_allow_html=True)
    elif len(raizes) == 1:
        st.markdown('<div class="root-box"><div class="root-lbl">r₁ = r₂</div>', unsafe_allow_html=True)
        st.latex(latex(sp.simplify(raizes[0])))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── CARD 3: SOLUÇÃO GERAL ──
    st.markdown("""
    <div class="res-card">
      <div class="res-head"><span>✨</span><span class="res-head-title">Solução Geral</span></div>
      <div class="res-body">
    """, unsafe_allow_html=True)

    st.latex(latex(res["sol"]))

    if res["verif_ok"] is True:
        st.markdown('<p class="check-ok">✓ Solução verificada pelo SymPy</p>', unsafe_allow_html=True)
    elif res["verif_ok"] is False:
        st.markdown('<p class="check-warn">⚠ Verificação retornou negativo</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="check-warn">⚠ Verificação automática inconclusiva</p>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <span class="ft-l">Autora: <strong>Marcela</strong> · SymPy &amp; Streamlit</span>
  <span class="ft-r">SolvEDO v2.1</span>
</div>
""", unsafe_allow_html=True)
