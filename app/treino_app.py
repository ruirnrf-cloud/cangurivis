# -*- coding: utf-8 -*-
"""Cangurivis - app de treino pro Rui Neto e pro Rafael (v1, sem agendador por
habilidade ainda).

Local: streamlit run app/treino_app.py
Nuvem: hospedado no Streamlit Community Cloud, sempre disponivel, sem depender
do PC de casa ligado -- ver pipeline/STATUS.md secao "Fase 5".

v1 deliberadamente simples: cada perfil (Rui/Rafael) tem sua propria trilha de
provas (PERFIS) e junta as questoes aprovadas dessa trilha, sorteia sem
repetir as ja respondidas antes (uma questao usada e "queimada" -- ver
memoria cangurivis-srs-por-habilidade), mostra a escada de dicas so depois de
errar (nunca a resposta de cara). O log de respostas de cada perfil fica num
arquivo proprio dentro do mesmo Gist privado do GitHub (nao em arquivo local)
porque o Community Cloud pode recriar o container e apagar disco local a
qualquer redeploy -- precisa de storage externo pra nao perder o progresso.

Rafael tem 7 anos (2o ano) e vai treinar com a mesma interface do Rui --
sem narracao em audio nem quebra de enunciado em blocos: decisao consciente
do usuario, porque a prova de verdade nao tem esses apoios e ele precisa
aprender a ler o enunciado como ele vai aparecer no dia.

Nao tem ainda: agendador por tag/habilidade, Elo/dificuldade adaptativa. Fica
pra quando houver dado de uso real pra guiar o design disso.
"""
import glob
import json
import os
import random
from datetime import datetime

import requests
import streamlit as st

BASE = "saida"
LETRAS = ["A", "B", "C", "D", "E"]

GIST_ID = st.secrets.get("GIST_ID", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
ACCESS_PIN = st.secrets.get("PIN", "")

# Cada filho treina na propria trilha de provas (nivel de olimpiada
# diferente) e tem o progresso gravado num arquivo proprio dentro do mesmo
# Gist -- nunca mistura o banco nem o log dos dois.
PERFIS = {
    "rui": {"nome": "Rui", "trilhas": ["mirim_m2"], "gist_arquivo": "progresso_rui.json"},
    "rafael": {"nome": "Rafael", "trilhas": ["mirim_m1"], "gist_arquivo": "progresso_rafael.json"},
}

st.set_page_config(layout="centered", page_title="Cangurivis - Treino")


# ---------- dados ----------

def carregar_banco(trilhas):
    """Junta as questoes aprovadas das trilhas do perfil (ex.: mirim_m2 pro Rui) num pool so."""
    pool = []
    caminhos = []
    for trilha in trilhas:
        caminhos += glob.glob(f"{BASE}/{trilha}/*/rascunho.json")
    for rascunho_path in sorted(caminhos):
        prova_dir = os.path.dirname(rascunho_path).replace("\\", "/")
        rev_path = f"{prova_dir}/revisao.json"
        if not os.path.exists(rev_path):
            continue
        rascunho = json.load(open(rascunho_path, encoding="utf-8"))
        revisao = json.load(open(rev_path, encoding="utf-8"))
        for num_str, q_rev in revisao.items():
            if q_rev.get("status") not in ("aprovado", "aprovado_com_ressalva"):
                continue
            if not q_rev.get("dica_curta") or not q_rev.get("solucao_completa"):
                continue  # ainda nao passou pela escrita de solucao (Fase 4)
            q_raw = rascunho["questoes"].get(num_str)
            if not q_raw:
                continue
            pool.append({
                "id": q_raw["id"],
                "prova": prova_dir.split("/")[-1],
                "imagem_questao": q_raw["imagem_questao"],
                "gabarito": q_rev["gabarito"],
                "tags": q_rev.get("tags", []),
                "dica_curta": q_rev.get("dica_curta", ""),
                "primeiro_passo": q_rev.get("primeiro_passo", ""),
                "solucao_completa": q_rev.get("solucao_completa", ""),
            })
    return pool


def _gist_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def carregar_log(gist_arquivo):
    resp = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=_gist_headers(), timeout=10)
    resp.raise_for_status()
    arquivo = resp.json()["files"].get(gist_arquivo)
    if arquivo is None:
        return {"respostas": []}  # perfil novo, ainda sem arquivo gravado no gist
    return json.loads(arquivo["content"])


def salvar_no_log(gist_arquivo, registro):
    log = carregar_log(gist_arquivo)
    log["respostas"].append(registro)
    conteudo = json.dumps(log, ensure_ascii=False, indent=2)
    resp = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers=_gist_headers(),
        json={"files": {gist_arquivo: {"content": conteudo}}},
        timeout=10,
    )
    resp.raise_for_status()


# ---------- PIN de acesso ----------
# A URL do app hospedado e publica (qualquer um com o link abre) -- esse PIN
# nao e seguranca de verdade, so evita que alguem tropece no link por acaso
# e veja questoes de prova oficial. Combine o numero com o Rui e a mae dele.

if ACCESS_PIN and not st.session_state.get("autenticado"):
    st.markdown("## 🦘 Cangurivis")
    pin_digitado = st.text_input("PIN", type="password")
    if st.button("Entrar", type="primary"):
        if pin_digitado == ACCESS_PIN:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("PIN errado.")
    st.stop()

# ---------- perfil (Rui ou Rafael) ----------
# a URL pode fixar o perfil (?quem=rafael), util pra cada um abrir sempre
# direto no proprio tablet sem precisar escolher.

if "perfil" not in st.session_state:
    perfil_url = st.query_params.get("quem")
    if perfil_url in PERFIS:
        st.session_state.perfil = perfil_url

if "perfil" not in st.session_state:
    st.markdown("## 🦘 Cangurivis")
    st.markdown("### Quem vai treinar?")
    cols = st.columns(len(PERFIS))
    for col, (chave, p) in zip(cols, PERFIS.items()):
        if col.button(p["nome"], width="stretch", type="primary"):
            st.session_state.perfil = chave
            st.query_params["quem"] = chave
            st.rerun()
    st.stop()

perfil = st.session_state.perfil
config_perfil = PERFIS[perfil]

# ---------- estado da sessao ----------

if "fila" not in st.session_state:
    log = carregar_log(config_perfil["gist_arquivo"])
    ja_feitas = {r["id"] for r in log["respostas"]}
    banco = carregar_banco(config_perfil["trilhas"])
    pendentes = [q for q in banco if q["id"] not in ja_feitas]
    random.shuffle(pendentes)
    st.session_state.fila = pendentes
    st.session_state.total_banco = len(banco)
    st.session_state.ja_feitas_antes = len(ja_feitas)
    st.session_state.pos = 0
    st.session_state.tentativas = 0
    st.session_state.revelado = 0  # 0=nada, 1=dica_curta, 2=primeiro_passo, 3=solucao_completa
    st.session_state.travado = False  # trava os botoes depois que a solucao aparece
    st.session_state.sessao_registros = []  # so as desta sessao, pra tela final


def proxima_questao():
    st.session_state.pos += 1
    st.session_state.tentativas = 0
    st.session_state.revelado = 0
    st.session_state.travado = False


def responder(letra, q):
    if letra == q["gabarito"]:
        salvar_no_log(config_perfil["gist_arquivo"], {
            "id": q["id"], "prova": q["prova"], "tags": q["tags"],
            "acertou_de_primeira": st.session_state.tentativas == 0,
            "tentativas": st.session_state.tentativas + 1,
            "dicas_usadas": st.session_state.revelado,
            "quando": datetime.now().isoformat(timespec="seconds"),
        })
        st.session_state.sessao_registros.append({
            "prova": q["prova"], "acertou_de_primeira": st.session_state.tentativas == 0,
            "dicas_usadas": st.session_state.revelado, "tags": q["tags"],
        })
        st.session_state.acabou_de_acertar = True
    else:
        st.session_state.tentativas += 1
        st.session_state.revelado = min(3, st.session_state.tentativas)
        if st.session_state.tentativas == 3:
            st.session_state.travado = True
            salvar_no_log(config_perfil["gist_arquivo"], {
                "id": q["id"], "prova": q["prova"], "tags": q["tags"],
                "acertou_de_primeira": False, "tentativas": st.session_state.tentativas,
                "dicas_usadas": 3, "quando": datetime.now().isoformat(timespec="seconds"),
            })
            st.session_state.sessao_registros.append({
                "prova": q["prova"], "acertou_de_primeira": False,
                "dicas_usadas": 3, "tags": q["tags"],
            })


# ---------- tela ----------

col_titulo, col_trocar = st.columns([6, 1])
col_titulo.markdown(f"## 🦘 Cangurivis — hora de treinar, {config_perfil['nome']}!")
if col_trocar.button("↩", help="Trocar quem vai treinar"):
    for chave in ("perfil", "fila", "pos", "tentativas", "revelado", "travado",
                  "sessao_registros", "total_banco", "ja_feitas_antes", "acabou_de_acertar"):
        st.session_state.pop(chave, None)
    st.query_params.clear()
    st.rerun()

fila = st.session_state.fila

if st.session_state.pos >= len(fila):
    feitas_agora = len(st.session_state.sessao_registros)
    if feitas_agora == 0:
        st.success("Você já respondeu todas as questões disponíveis até agora! 🎉")
        st.caption("Assim que eu adicionar mais provas ao banco, aparecem questões novas aqui.")
    else:
        acertos_de_primeira = sum(1 for r in st.session_state.sessao_registros if r["acertou_de_primeira"])
        precisou_dica = [r for r in st.session_state.sessao_registros if r["dicas_usadas"] > 0]
        plural = "questões" if feitas_agora != 1 else "questão"
        st.success(f"Sessão terminada! {feitas_agora} {plural}, {acertos_de_primeira} acertada(s) de primeira. 🎉")
        if precisou_dica:
            st.markdown(f"**Questões que deram mais trabalho (pra revisar com {config_perfil['nome']}):**")
            for r in precisou_dica:
                tags = ", ".join(r["tags"]) if r["tags"] else "sem tag"
                st.markdown(f"- {r['prova']} — {tags} ({r['dicas_usadas']} dica(s) usada(s))")
    st.caption(f"Progresso total: {st.session_state.ja_feitas_antes + feitas_agora}/{st.session_state.total_banco} "
               f"questões do banco já respondidas.")
    st.stop()

q = fila[st.session_state.pos]

st.caption(f"Questão {st.session_state.pos + 1} de {len(fila)} nesta sessão · {q['prova']}")
st.image(q["imagem_questao"], width="stretch")

if st.session_state.get("acabou_de_acertar"):
    st.success("🎉 Isso aí! Resposta certa.")
    with st.expander("Ver a explicação completa", expanded=False):
        st.markdown(q["solucao_completa"])
    if st.button("Próxima questão ▶", type="primary", width="stretch"):
        st.session_state.acabou_de_acertar = False
        proxima_questao()
        st.rerun()
    st.stop()

cols = st.columns(5)
for i, letra in enumerate(LETRAS):
    if cols[i].button(letra, key=f"resp_{st.session_state.pos}_{letra}",
                       width="stretch", disabled=st.session_state.travado):
        responder(letra, q)
        st.rerun()

if st.session_state.tentativas > 0 and not st.session_state.travado:
    st.warning("Essa não foi... tenta de novo! 💪")

if st.session_state.revelado >= 1:
    st.info(f"**Dica:** {q['dica_curta']}")
if st.session_state.revelado >= 2:
    st.info(f"**Primeiro passo:** {q['primeiro_passo']}")
if st.session_state.revelado >= 3:
    st.error(f"**A resposta certa era {q['gabarito']}.** Olha como resolve:")
    st.markdown(q["solucao_completa"])
    if st.button("Próxima questão ▶", type="primary", width="stretch", key="prox_apos_solucao"):
        proxima_questao()
        st.rerun()
