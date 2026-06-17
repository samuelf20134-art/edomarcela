"""
SolvEDO — Equações de 2ª Ordem com Coeficientes Constantes
         ay'' + by' + cy = 0
Autora : Marcela
Engine : SymPy · Streamlit

CORREÇÃO CRÍTICA v2.2:
  dsolve() entra em RecursionError com coeficientes float.
  Solução: converter tudo para sp.Rational(str(v)) antes de montar a EDO.
"""

import streamlit as st
import sympy as sp
from sympy import Function, dsolve, Eq, symbols, latex

# ─────────────────────────────────────────────────────────────
# PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="SolvEDO · Marcela", page_icon="∂", layout="centered")

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --bg:#faf5f6;--card:#ffffff;--panel:#f7edf0;
  --rose:#c7979b;--rose-dk:#a97478;--rose-sf:#e8c4c7;
  --nude:#e2d0cc;--slate:#58535e;--slate-lt:#96909c;
  --text:#3a353f;--text-s:#7a7280;--border:#e4d4d8;
  --ok:#6fa882;--warn:#c8986a;--err:#c06870;
  --mono:'JetBrains Mono',monospace;
  --sans:'Inter',system-ui,sans-serif;
  --r:14px;--rsm:9px;
  --sh:0 4px 28px rgba(160,100,110,0.09);
}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;font-family:var(--sans)!important;color:var(--text)!important;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stToolbar"]{display:none!important;}
.block-container{max-width:660px!important;padding:0 0 60px!important;}

/* HEADER */
.hdr{background:linear-gradient(135deg,#c7979b 0%,#b07478 55%,#956068 100%);border-radius:0 0 22px 22px;padding:28px 32px 24px;margin-bottom:28px;display:flex;align-items:center;gap:16px;box-shadow:0 6px 32px rgba(160,100,110,.22);}
.hdr-icon{width:52px;height:52px;flex-shrink:0;background:rgba(255,255,255,.20);border:1.5px solid rgba(255,255,255,.30);border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;color:#fff;}
.hdr-text h1{color:#fff!important;margin:0!important;padding:0!important;font-size:1.35rem!important;font-weight:700!important;}
.hdr-text p{color:rgba(255,255,255,.75)!important;font-size:.78rem!important;margin:3px 0 0!important;font-weight:300;}
.hdr-auth{margin-left:auto;text-align:right;color:rgba(255,255,255,.80);font-size:.73rem;line-height:1.5;}
.hdr-auth strong{display:block;color:#fff;font-size:.88rem;}

/* PREVIEW */
.eq-prev{background:var(--panel);border:1.5px solid var(--border);border-radius:var(--r);padding:16px 22px 14px;margin-bottom:22px;text-align:center;}
.eq-lbl{font-size:.66rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--slate-lt);margin-bottom:8px;}
.eq-eq{font-family:var(--mono);font-size:1.18rem;letter-spacing:.03em;}
.ca{color:#a97478;font-weight:700;}.cb{color:#7a82c0;font-weight:700;}.cc{color:#6fa882;font-weight:700;}

/* MAIN CARD */
.mcard{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:26px 28px 22px;box-shadow:var(--sh);margin-bottom:18px;}
.mtitle{font-size:.66rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--slate-lt);padding-bottom:10px;border-bottom:1px solid var(--border);margin-bottom:18px;}

/* BADGES */
.cbadge{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:1rem;font-weight:700;margin:0 auto 6px;border:2px solid;}
.ba{color:#a97478;background:#f7edf0;border-color:var(--rose-sf);}
.bb{color:#7a82c0;background:#eef0f8;border-color:#c8ccea;}
.bc{color:#6fa882;background:#edf5f0;border-color:#b8d8c4;}

/* INPUTS */
[data-testid="stNumberInput"] label{font-family:var(--sans)!important;font-size:.78rem!important;font-weight:600!important;color:var(--slate)!important;}
[data-testid="stNumberInput"] input{font-family:var(--mono)!important;font-size:1rem!important;font-weight:500!important;background:var(--bg)!important;border:1.5px solid var(--nude)!important;border-radius:var(--rsm)!important;color:var(--text)!important;text-align:center!important;transition:border-color .2s,box-shadow .2s!important;}
[data-testid="stNumberInput"] input:focus{border-color:var(--rose)!important;box-shadow:0 0 0 3px rgba(199,151,155,.18)!important;outline:none!important;}

/* BOTÃO */
[data-testid="stButton"]>button{font-family:var(--sans)!important;font-weight:600!important;font-size:.95rem!important;letter-spacing:.04em!important;background:linear-gradient(135deg,var(--rose) 0%,var(--rose-dk) 100%)!important;color:#fff!important;border:none!important;border-radius:var(--rsm)!important;padding:13px 0!important;width:100%!important;margin-top:8px!important;box-shadow:0 4px 16px rgba(199,151,155,.40)!important;transition:opacity .2s,transform .15s!important;}
[data-testid="stButton"]>button:hover{opacity:.87!important;transform:translateY(-2px)!important;}

/* RESULT CARDS */
.rcard{background:var(--card);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;margin-bottom:14px;box-shadow:var(--sh);}
.rhead{background:linear-gradient(90deg,var(--panel),#fdf6f7);padding:10px 18px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;}
.rhead-t{font-size:.67rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--slate);}
.rbody{padding:16px 20px;}

/* DISCRIMINANTE */
.drow{display:flex;align-items:center;gap:10px;background:var(--bg);border-radius:var(--rsm);padding:11px 15px;margin-bottom:12px;border:1px solid var(--border);font-family:var(--mono);}
.dlbl{font-size:.76rem;color:var(--slate-lt);min-width:100px;}
.dval{font-size:1rem;font-weight:700;}
.dp{color:var(--ok);}.dz{color:var(--warn);}.dn{color:#8890cc;}

/* CASE BADGE */
.csbadge{display:inline-block;font-size:.71rem;font-weight:600;padding:4px 13px;border-radius:20px;margin-bottom:14px;letter-spacing:.05em;}
.cb-r{background:#edf5f0;color:var(--ok);border:1px solid #b8d8c4;}
.cb-rep{background:#fdf3e8;color:var(--warn);border:1px solid #e8ccaa;}
.cb-c{background:#eef0f8;color:#7a82c0;border:1px solid #c8ccea;}

/* CHECK */
.chk-ok{color:var(--ok);font-weight:600;font-size:.82rem;}
.chk-warn{color:var(--warn);font-weight:600;font-size:.82rem;}

/* ERRO */
.errbox{background:#fdf0f1;border:1.5px solid #e8b8bb;border-left:4px solid var(--err);border-radius:var(--rsm);padding:13px 16px;font-family:var(--mono);font-size:.8rem;color:#8a3a3e;}

/* EMPTY */
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 24px;gap:10px;color:var(--text-s);text-align:center;}
.es-i{font-size:2.8rem;opacity:.28;margin-bottom:4px;}
.es-t{font-size:.87rem;line-height:1.75;}

/* FOOTER */
.ft{margin-top:32px;padding:13px 0;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;}
.ftl{font-size:.7rem;color:var(--slate-lt);}
.ftr{font-size:.69rem;font-family:var(--mono);color:#fff;background:var(--rose-dk);padding:3px 11px;border-radius:20px;}

/* KaTeX */
[data-testid="stMarkdownContainer"] .katex{font-size:1.1rem!important;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# LÓGICA MATEMÁTICA — CORREÇÃO CRÍTICA
# ─────────────────────────────────────────────────────────────
def to_rat(v: float) -> sp.Rational:
    """
    Converte float → sp.Rational via string.
    Isso evita o RecursionError que o SymPy lança com coeficientes float
    em dsolve() para EDOs de 2ª ordem.
    Exemplo: 1.5 → Rational('1.5') → 3/2
    """
    return sp.Rational(str(v))


def resolver_edo(a_f: float, b_f: float, c_f: float) -> dict:
    """
    Resolve  a·y'' + b·y' + c·y = 0  com coeficientes racionais exatos.
    Retorna dicionário com todos os dados para exibição.
    """
    # ── Conversão para Rational (fix do RecursionError) ──
    a = to_rat(a_f)
    b = to_rat(b_f)
    c = to_rat(c_f)

    t = symbols('t', real=True)
    y = Function('y')

    # EDO simbólica
    edo = Eq(a * y(t).diff(t, 2) + b * y(t).diff(t) + c * y(t), 0)

    # Solução geral
    sol = dsolve(edo, y(t))

    # Equação característica:  a·r² + b·r + c = 0
    r = symbols('r')
    carac = a * r**2 + b * r + c
    delta = b**2 - 4 * a * c      # exato, pois a,b,c são Rational
    raizes = sp.solve(carac, r)

    # Classificação pelo discriminante
    delta_f = float(delta)
    if abs(delta_f) < 1e-12:
        tipo = "repetida"
    elif delta_f > 0:
        tipo = "reais"
    else:
        tipo = "complexas"

    # Verificação analítica
    try:
        ok, _ = sp.checkodesol(edo, sol)
        verif_ok = bool(ok)
    except Exception:
        verif_ok = None

    return {
        "edo": edo, "sol": sol,
        "carac": carac, "delta": delta, "delta_f": delta_f,
        "raizes": raizes, "tipo": tipo, "verif_ok": verif_ok,
    }


def fmt(v: float) -> str:
    """Formata coeficiente para exibição limpa no preview."""
    if float(v) == int(float(v)):
        return str(int(float(v)))
    return f"{float(v):.4g}"


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <div class="hdr-icon">∂</div>
  <div class="hdr-text">
    <h1>SolvEDO</h1>
    <p>Equações de 2ª Ordem · Coeficientes Constantes</p>
  </div>
  <div class="hdr-auth"><strong>Marcela</strong>Matemática · SymPy</div>
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
<div class="eq-prev">
  <div class="eq-lbl">Equação Configurada</div>
  <div class="eq-eq">
    <span class="ca">{fmt(st.session_state.av)}</span>y'' +&nbsp;
    <span class="cb">{fmt(st.session_state.bv)}</span>y' +&nbsp;
    <span class="cc">{fmt(st.session_state.cv)}</span>y = 0
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ENTRADAS
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="mcard">', unsafe_allow_html=True)
st.markdown('<div class="mtitle">Coeficientes da EDO</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="cbadge ba">a</div>', unsafe_allow_html=True)
    a_in = st.number_input("Coeficiente a (y'')", value=1.0, step=1.0, format="%.4g", key="av")
with c2:
    st.markdown('<div class="cbadge bb">b</div>', unsafe_allow_html=True)
    b_in = st.number_input("Coeficiente b (y')",  value=0.0, step=1.0, format="%.4g", key="bv")
with c3:
    st.markdown('<div class="cbadge bc">c</div>', unsafe_allow_html=True)
    c_in = st.number_input("Coeficiente c (y)",   value=0.0, step=1.0, format="%.4g", key="cv")

if a_in == 0:
    st.markdown(
        '<div class="errbox" style="margin-top:10px;">⚠ O coeficiente <b>a</b> não pode ser zero — a equação deixa de ser de 2ª ordem.</div>',
        unsafe_allow_html=True,
    )

btn = st.button("Resolver EDO", use_container_width=True, disabled=(a_in == 0))
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# RESULTADO
# ─────────────────────────────────────────────────────────────
if not btn:
    st.markdown("""
    <div class="empty">
      <div class="es-i">∫</div>
      <div class="es-t">Defina os coeficientes <strong>a</strong>, <strong>b</strong> e <strong>c</strong><br>e clique em <strong>Resolver EDO</strong>.</div>
    </div>""", unsafe_allow_html=True)
else:
    with st.spinner("Calculando..."):
        try:
            res = resolver_edo(a_in, b_in, c_in)
        except Exception as e:
            st.markdown(f'<div class="errbox">⚠ Erro ao processar: {e}</div>', unsafe_allow_html=True)
            st.stop()

    tipo = res["tipo"]
    df   = res["delta_f"]
    delta_sym = res["delta"]

    # ── Card 1: EDO ──
    st.markdown('<div class="rcard"><div class="rhead"><span>📝</span><span class="rhead-t">Equação Diferencial</span></div><div class="rbody">', unsafe_allow_html=True)
    st.latex(latex(res["edo"]))
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Card 2: Equação Característica + Discriminante + Raízes ──
    st.markdown('<div class="rcard"><div class="rhead"><span>🔢</span><span class="rhead-t">Análise da Equação Característica</span></div><div class="rbody">', unsafe_allow_html=True)

    st.latex(latex(Eq(res["carac"], 0)))

    # Discriminante
    if abs(df) < 1e-12:
        dcls, dsym = "dz", f"\\Delta = 0"
    elif df > 0:
        dcls, dsym = "dp", f"\\Delta = {latex(delta_sym)}"
    else:
        dcls, dsym = "dn", f"\\Delta = {latex(delta_sym)}"

    st.markdown(f'<div class="drow"><span class="dlbl">Discriminante</span><span class="dval {dcls}">\\({dsym}\\)</span></div>', unsafe_allow_html=True)

    # Badge de tipo
    if tipo == "reais":
        st.markdown('<span class="csbadge cb-r">📗 Raízes Reais e Distintas</span>', unsafe_allow_html=True)
    elif tipo == "repetida":
        st.markdown('<span class="csbadge cb-rep">📙 Raiz Real Repetida</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="csbadge cb-c">📘 Raízes Complexas Conjugadas</span>', unsafe_allow_html=True)

    # Raízes com st.latex (sem HTML cru)
    raizes = res["raizes"]
    if len(raizes) >= 2:
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown('<div style="text-align:center;font-size:.7rem;color:#96909c;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;">Raiz r₁</div>', unsafe_allow_html=True)
            st.latex(latex(sp.simplify(raizes[0])))
        with rc2:
            st.markdown('<div style="text-align:center;font-size:.7rem;color:#96909c;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;">Raiz r₂</div>', unsafe_allow_html=True)
            st.latex(latex(sp.simplify(raizes[1])))
    elif len(raizes) == 1:
        st.markdown('<div style="text-align:center;font-size:.7rem;color:#96909c;font-weight:600;margin-bottom:4px;">r₁ = r₂</div>', unsafe_allow_html=True)
        st.latex(latex(sp.simplify(raizes[0])))

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Card 3: Solução Geral ──
    st.markdown('<div class="rcard"><div class="rhead"><span>✨</span><span class="rhead-t">Solução Geral</span></div><div class="rbody">', unsafe_allow_html=True)
    st.latex(latex(res["sol"]))

    if res["verif_ok"] is True:
        st.markdown('<p class="chk-ok">✓ Solução verificada pelo SymPy</p>', unsafe_allow_html=True)
    elif res["verif_ok"] is False:
        st.markdown('<p class="chk-warn">⚠ Verificação retornou negativo</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="chk-warn">⚠ Verificação automática inconclusiva</p>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="ft">
  <span class="ftl">Autora: <strong>Marcela</strong> · SymPy &amp; Streamlit · Python</span>
  <span class="ftr">SolvEDO v2.2</span>
</div>
""", unsafe_allow_html=True)
