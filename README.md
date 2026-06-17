# SolvEDO ∂ · v2.0

**Resolvedor de EDOs de 2ª Ordem — Coeficientes Constantes**  
`ay'' + by' + cy = 0`  
Autora: **Marcela**

---

## ✨ Funcionalidades

- Entrada por coeficientes `a`, `b`, `c` — sem digitar equações
- Preview em tempo real da equação montada
- Equação característica com discriminante (Δ) calculado
- Classificação automática das raízes: reais distintas, repetida ou complexas
- Solução geral renderizada em LaTeX
- Verificação analítica via `checkodesol`

## 🚀 Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📦 Deploy no Streamlit Cloud

1. Suba os arquivos `app.py` e `requirements.txt` na **raiz** do repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Selecione o repositório, arquivo: `app.py` → **Deploy** ✅

## 🧮 Exemplos

| a | b | c | Tipo de raiz |
|---|---|---|---|
| 1 | -5 | 6 | Reais distintas |
| 1 | 2 | 1 | Raiz repetida |
| 1 | 0 | 1 | Complexas (y'' + y = 0) |
| 1 | -3 | 2 | Reais distintas |

---

*Desenvolvido com 🌸 por Marcela*
