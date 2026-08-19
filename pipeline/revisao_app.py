# -*- coding: utf-8 -*-
"""Tela de revisao do Cangurivis: um item por tela, atalhos de teclado,
fila por prova, aprovacao em lote pros itens ja revisados.

Roda com: streamlit run pipeline/revisao_app.py

Nota: usa uma coluna estreita no topo do layout em vez de st.sidebar --
essa instalacao do streamlit (1.61.1) nao renderiza nada dentro de
`with st.sidebar:` (confirmado com um teste isolado, sem excecao no log,
o container simplesmente nao aparece no DOM). Colunas normais nao tem
esse problema.
"""
import glob
import json
import os

import streamlit as st

BASE = "saida"
LETRAS = ["A", "B", "C", "D", "E"]

st.set_page_config(layout="wide", page_title="Cangurivis - Revisao")


# ---------- dados ----------

def listar_provas():
    dirs = sorted(os.path.dirname(p).replace("\\", "/") for p in glob.glob(f"{BASE}/*/*/rascunho.json"))
    return dirs


def carregar_prova(prova_dir):
    rascunho = json.load(open(f"{prova_dir}/rascunho.json", encoding="utf-8"))
    rev_path = f"{prova_dir}/revisao.json"
    revisao = json.load(open(rev_path, encoding="utf-8")) if os.path.exists(rev_path) else {}
    return rascunho, revisao


def salvar_revisao(prova_dir, revisao):
    with open(f"{prova_dir}/revisao.json", "w", encoding="utf-8") as f:
        json.dump(revisao, f, ensure_ascii=False, indent=2)


def questao_a_partir_do_rascunho(q_raw):
    # usa o rascunho automatico (extrair_texto.py) como ponto de partida --
    # sempre editavel, nunca aprovado sem passar pela revisao humana
    alt_rascunho = q_raw.get("alternativas_rascunho")
    alt_tipo = "texto" if alt_rascunho else "imagem"
    if alt_rascunho:
        alternativas = [{"letra": a["letra"], "texto": a["texto"]} for a in alt_rascunho]
    else:
        alternativas = [{"letra": l, "texto": ""} for l in LETRAS]
    return {
        "enunciado_md": q_raw.get("enunciado_rascunho", ""),
        "alternativa_tipo": alt_tipo,
        "alternativas": alternativas,
        "gabarito": q_raw["gabarito"] or "",
        "solucao_md": "",
        "figura_essencial": True,
        "problemas": "",
        "status": "pendente",
    }


# ---------- atalhos de teclado ----------
# o componente html do streamlit roda num iframe, mas e same-origin com a
# pagina principal, entao da pra escutar keydown no document pai e clicar
# nos botoes reais pelo texto visivel -- funciona sem pacote pip extra.

def atalhos_js():
    st.components.v1.html(
        """
        <script>
        const doc = window.parent.document;
        if (!doc.__cangurivis_shortcuts_bound) {
            doc.__cangurivis_shortcuts_bound = true;
            doc.addEventListener('keydown', function(e) {
                const tag = (e.target.tagName || '').toLowerCase();
                const editando = tag === 'textarea' || tag === 'input';
                function clicar(texto) {
                    const btns = Array.from(doc.querySelectorAll('button'));
                    const btn = btns.find(b => b.innerText.includes(texto));
                    if (btn) { btn.click(); return true; }
                    return false;
                }
                if (!editando && e.key === 'ArrowRight') { clicar('Proxima'); e.preventDefault(); }
                else if (!editando && e.key === 'ArrowLeft') { clicar('Anterior'); e.preventDefault(); }
                else if (!editando && e.key.toLowerCase() === 'd') { clicar('Duvida'); e.preventDefault(); }
                else if (e.ctrlKey && e.key === 'Enter') { clicar('Salvar'); e.preventDefault(); }
            });
        }
        </script>
        """,
        height=0,
    )


# ---------- app ----------

provas = listar_provas()
if not provas:
    st.error(f"Nenhuma prova encontrada em {BASE}/*/*/rascunho.json — rode o pipeline primeiro.")
    st.stop()

if "prova_dir" not in st.session_state:
    st.session_state.prova_dir = provas[0]
if "idx" not in st.session_state:
    st.session_state.idx = 0

st.markdown("## 🦘 Cangurivis — revisão")

col_nav, col_img, col_form = st.columns([0.85, 1.5, 1.6], gap="medium")

with col_nav, st.container(border=True):
    escolha = st.selectbox("Prova", provas, index=provas.index(st.session_state.prova_dir),
                            format_func=lambda p: p.split("/")[-1])
    if escolha != st.session_state.prova_dir:
        st.session_state.prova_dir = escolha
        st.session_state.idx = 0
        st.rerun()

    rascunho, revisao = carregar_prova(st.session_state.prova_dir)
    nums = sorted(int(n) for n in rascunho["questoes"].keys())

    n_revisadas = sum(1 for n in nums if str(n) in revisao and revisao[str(n)]["status"] != "pendente")
    st.progress(n_revisadas / len(nums) if nums else 0, text=f"{n_revisadas}/{len(nums)} revisadas")

    st.caption("FILA · clique pra pular direto")
    fila_box = st.container(height=280, border=False)
    with fila_box:
        for n in nums:
            r = revisao.get(str(n))
            if r is None:
                icone = "⚪"
            elif r["status"] == "aprovado":
                icone = "🟢"
            elif r["status"] == "aprovado_com_ressalva":
                icone = "🟡"
            elif r["status"] == "duvida":
                icone = "🔴"
            else:
                icone = "⚪"
            tipo = "primary" if n == nums[st.session_state.idx] else "secondary"
            if st.button(f"{icone} Questão {n:02d}", key=f"jump_{n}", width="stretch", type=tipo):
                st.session_state.idx = nums.index(n)
                st.rerun()

    limpos = [n for n in nums if str(n) in revisao and revisao[str(n)]["status"] == "aprovado_com_ressalva"]
    if limpos and st.button(f"✅ Aprovar em lote ({len(limpos)} com ressalva leve)", width="stretch"):
        for n in limpos:
            revisao[str(n)]["status"] = "aprovado"
        salvar_revisao(st.session_state.prova_dir, revisao)
        st.rerun()

atalhos_js()

idx = max(0, min(st.session_state.idx, len(nums) - 1))
num = nums[idx]
q_raw = rascunho["questoes"][str(num)]
q_rev = revisao.get(str(num)) or questao_a_partir_do_rascunho(q_raw)

with col_img, st.container(border=True):
    st.markdown(f"**{st.session_state.prova_dir.split('/')[-1]}** · questão {idx+1}/{len(nums)} · "
                f"`{q_raw['id']}`")
    st.image(q_raw["imagem_questao"], width="stretch", caption="Imagem canônica (fallback)")
    st.divider()
    if q_raw["figuras"]:
        st.caption(f"{len(q_raw['figuras'])} FIGURA(S) ISOLADA(S)")
        fig_cols = st.columns(min(len(q_raw["figuras"]), 4))
        for i, fp in enumerate(q_raw["figuras"]):
            fig_cols[i % len(fig_cols)].image(fp, width="stretch")
    else:
        st.caption("SEM FIGURA ISOLADA")

with col_form, st.container(border=True):
    if str(num) not in revisao:
        conf = q_raw.get("confianca_texto", "vazio")
        rotulo = {"alta": "🟢 rascunho automático — confiança alta",
                  "baixa": "🟡 rascunho automático — confiança baixa, confira com atenção",
                  "vazio": "⚪ nada extraído automaticamente — preencha do zero"}[conf]
        st.caption(rotulo)
    with st.form(key=f"form_{num}", border=False):
        enunciado = st.text_area("Enunciado", value=q_rev["enunciado_md"], height=100)

        alt_tipo = st.radio("Tipo de alternativa", ["texto", "imagem", "numero_aberto"],
                             index=["texto", "imagem", "numero_aberto"].index(q_rev["alternativa_tipo"]),
                             horizontal=True)

        alternativas = []
        if alt_tipo == "texto":
            alt_cols = st.columns(5)
            for i, letra in enumerate(LETRAS):
                atual = next((a["texto"] for a in q_rev["alternativas"] if a["letra"] == letra), "")
                v = alt_cols[i].text_input(letra, value=atual, key=f"alt_{num}_{letra}")
                alternativas.append({"letra": letra, "texto": v})
        else:
            st.caption("Alternativas em imagem/numero aberto: conferir pelas figuras ao lado.")
            alternativas = q_rev["alternativas"]

        gabarito = st.selectbox("Gabarito (extraido automaticamente, confira)", LETRAS,
                                 index=LETRAS.index(q_rev["gabarito"]) if q_rev["gabarito"] in LETRAS else 0)
        if q_raw["gabarito"] and gabarito != q_raw["gabarito"]:
            st.warning(f"Diferente do extraido pelo pipeline ({q_raw['gabarito']}) — confirme antes de salvar.")

        solucao = st.text_area("Solucao (linguagem simples, para a crianca)", value=q_rev["solucao_md"], height=120)
        figura_essencial = st.checkbox("Figura e essencial pra resolver (nao so ilustrativa)",
                                        value=q_rev["figura_essencial"])
        problemas = st.text_input("Observacoes / ressalvas (deixe vazio se limpo)", value=q_rev["problemas"])

        col_a, col_b, col_c = st.columns(3)
        salvar_prox = col_a.form_submit_button("💾 Salvar e avancar (Ctrl+Enter)", width="stretch")
        duvida = col_b.form_submit_button("🔴 Duvida — pular", width="stretch")
        so_salvar = col_c.form_submit_button("Salvar sem avancar", width="stretch")

        if salvar_prox or so_salvar or duvida:
            novo = {
                "enunciado_md": enunciado,
                "alternativa_tipo": alt_tipo,
                "alternativas": alternativas,
                "gabarito": gabarito,
                "solucao_md": solucao,
                "figura_essencial": figura_essencial,
                "problemas": problemas,
                "status": "duvida" if duvida else ("aprovado" if not problemas.strip() else "aprovado_com_ressalva"),
            }
            revisao[str(num)] = novo
            salvar_revisao(st.session_state.prova_dir, revisao)
            if salvar_prox or duvida:
                st.session_state.idx = min(idx + 1, len(nums) - 1)
            st.rerun()

    nav_a, nav_b = st.columns(2)
    if nav_a.button("◀ Anterior", disabled=idx == 0, width="stretch"):
        st.session_state.idx = idx - 1
        st.rerun()
    if nav_b.button("Proxima ▶", disabled=idx == len(nums) - 1, width="stretch"):
        st.session_state.idx = idx + 1
        st.rerun()
