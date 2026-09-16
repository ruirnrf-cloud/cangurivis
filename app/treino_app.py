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

Modos de treino (escolhidos depois do perfil): "treino" (todas as provas, com
escada de dicas), "f2" (so questoes de 2a fase, com dicas) e "simulado" (15
questoes de 2a fase, uma resposta por questao, sem dica nem feedback, com
tempo -- do jeito que a prova de verdade e). Os dois ultimos existem porque
o Rui Neto e o Rafael passaram pra 2a fase da OBMEP Mirim 2026 (10/11/2026).
No simulado, se faltam questoes de 2a fase ineditas, ele completa com
questoes ja respondidas (simulado serve pra treinar ritmo, nao so conteudo).

Nao tem ainda: agendador por tag/habilidade, Elo/dificuldade adaptativa. Fica
pra quando houver dado de uso real pra guiar o design disso.
"""
import glob
import json
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st

BASE = "saida"
LETRAS = ["A", "B", "C", "D", "E"]
# pontos por resposta certa, conforme quantas dicas precisou (0 = sem ajuda nenhuma)
PONTOS_POR_DICAS = {0: 10, 1: 6, 2: 3, 3: 1}

GIST_ID = st.secrets.get("GIST_ID", "")
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
ACCESS_PIN = st.secrets.get("PIN", "")
# Se definido, o log de progresso vai pra arquivos nessa pasta em vez do Gist --
# so pra testar o app localmente sem sujar o progresso real das criancas.
LOG_LOCAL_DIR = os.environ.get("CANGURIVIS_LOG_DIR", "")

MODOS = {
    "treino": {"rotulo": "🎲 Treino normal",
               "desc": "Todas as provas, com a escada de dicas quando errar."},
    "f2": {"rotulo": "🎯 Só 2ª fase",
           "desc": "Só questões de 2ª fase, com dicas. Pra afiar pro dia da prova."},
    "simulado": {"rotulo": "⏱️ Simulado 2ª fase",
                 "desc": "15 questões de 2ª fase, uma resposta por questão, sem dica, com o tempo marcando. "
                         "Igual à prova de verdade: o resultado só aparece no final."},
}
SIMULADO_N = 15

# Cada filho treina na propria trilha de provas (nivel de olimpiada
# diferente) e tem o progresso gravado num arquivo proprio dentro do mesmo
# Gist -- nunca mistura o banco nem o log dos dois.
PERFIS = {
    "rui": {"nome": "Rui", "trilhas": ["mirim_m2", "pmc"], "gist_arquivo": "progresso_rui.json"},
    "rafael": {"nome": "Rafael", "trilhas": ["mirim_m1"], "gist_arquivo": "progresso_rafael.json"},
    "bebel": {"nome": "Bebel", "trilhas": ["mirim_m2"], "gist_arquivo": "progresso_bebel.json"},
    "rui_filho": {"nome": "Rui Filho", "trilhas": ["mirim_m2"], "gist_arquivo": "progresso_rui_filho.json"},
}

st.set_page_config(layout="centered", page_title="Cangurivis - Treino")
if LOG_LOCAL_DIR:
    st.caption("⚠️ Modo de teste: progresso em arquivo local, não no Gist.")


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
            prova = prova_dir.split("/")[-1]  # ex.: 2025_f2 (OBMEP) ou 2022_uk (PMC, sem fase)
            pool.append({
                "id": q_raw["id"],
                "prova": prova,
                "fase": 2 if prova.endswith("_f2") else 1 if prova.endswith("_f1") else None,
                "modo": q_raw.get("modo", "imagem"),
                "imagem_questao": q_raw.get("imagem_questao"),
                "enunciado_md": q_raw.get("enunciado_md"),
                "alternativas": q_raw.get("alternativas"),
                "figura": q_raw.get("figura"),
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
    if LOG_LOCAL_DIR:
        caminho = os.path.join(LOG_LOCAL_DIR, gist_arquivo)
        if not os.path.exists(caminho):
            return {"respostas": []}
        return json.load(open(caminho, encoding="utf-8"))
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
    if LOG_LOCAL_DIR:
        os.makedirs(LOG_LOCAL_DIR, exist_ok=True)
        with open(os.path.join(LOG_LOCAL_DIR, gist_arquivo), "w", encoding="utf-8") as f:
            f.write(conteudo)
        return
    resp = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}",
        headers=_gist_headers(),
        json={"files": {gist_arquivo: {"content": conteudo}}},
        timeout=10,
    )
    resp.raise_for_status()


def calcular_stats(respostas):
    """Pontos, nivel, sequencia de dias e acerto por habilidade a partir do log completo
    (todas as sessoes ja gravadas, nao so a de agora)."""
    # no simulado nao tem dica: errou (dicas_usadas 3) vale 0 ponto, nao o 1 ponto de
    # "viu a solucao" do treino normal.
    pontos_totais = sum(
        0 if r.get("modo") == "simulado" and r["dicas_usadas"] == 3 else PONTOS_POR_DICAS[r["dicas_usadas"]]
        for r in respostas
    )

    # so entram no calculo de "acertou" as respostas onde a criança escolheu a letra certa
    # de verdade (dicas_usadas 0-2); quando travado em 3 tentativas a solucao foi revelada
    # sem ela acertar, entao isso mede dificuldade, nao acerto. No simulado nao tem esse
    # caso: errou (3) e uma resposta de verdade, entra no denominador.
    respondidas_certo = [r for r in respostas if r["dicas_usadas"] < 3 or r.get("modo") == "simulado"]
    taxa_de_primeira = (
        sum(1 for r in respondidas_certo if r["dicas_usadas"] == 0) / len(respondidas_certo) * 100
        if respondidas_certo else 0
    )

    por_tag = {}
    for r in respondidas_certo:
        for tag in r["tags"]:
            s = por_tag.setdefault(tag, {"de_primeira": 0, "total": 0})
            s["total"] += 1
            if r["dicas_usadas"] == 0:
                s["de_primeira"] += 1
    acerto_por_tag = {
        tag: round(s["de_primeira"] / s["total"] * 100)
        for tag, s in por_tag.items()
        if s["total"] >= 3  # amostra pequena demais vira grafico ruidoso
    }

    dias_com_treino = {r["quando"][:10] for r in respostas}
    dias_seguidos = 0
    if dias_com_treino:
        hoje = datetime.now().date()
        cursor = hoje if hoje.isoformat() in dias_com_treino else hoje - timedelta(days=1)
        while cursor.isoformat() in dias_com_treino:
            dias_seguidos += 1
            cursor -= timedelta(days=1)

    return {
        "pontos_totais": pontos_totais,
        "nivel": pontos_totais // 100 + 1,
        "pontos_no_nivel": pontos_totais % 100,
        "taxa_de_primeira": taxa_de_primeira,
        "acerto_por_tag": acerto_por_tag,
        "dias_seguidos": dias_seguidos,
    }


# ---------- PIN de acesso ----------
# A URL do app hospedado e publica (qualquer um com o link abre) -- esse PIN
# nao e seguranca de verdade, so evita que alguem tropece no link por acaso
# e veja questoes de prova oficial. Combine o numero com o Rui e a mae dele.

if ACCESS_PIN and not LOG_LOCAL_DIR and not st.session_state.get("autenticado"):  # PIN so protege a URL publica
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

# ---------- modo de treino ----------

if "modo" not in st.session_state:
    st.markdown(f"## 🦘 Cangurivis — {config_perfil['nome']}, como vai treinar hoje?")
    for chave, m in MODOS.items():
        if st.button(m["rotulo"], width="stretch", type="primary" if chave == "treino" else "secondary",
                     key=f"modo_{chave}"):
            st.session_state.modo = chave
            st.rerun()
        st.caption(m["desc"])
    if st.button("↩ Trocar quem vai treinar", key="trocar_na_tela_de_modo"):
        st.session_state.pop("perfil", None)
        st.query_params.clear()
        st.rerun()
    st.stop()

modo = st.session_state.modo
simulado = modo == "simulado"

# ---------- estado da sessao ----------

if "fila" not in st.session_state:
    log = carregar_log(config_perfil["gist_arquivo"])
    ja_feitas = {r["id"] for r in log["respostas"]}
    banco_total = carregar_banco(config_perfil["trilhas"])
    banco = [q for q in banco_total if q["fase"] == 2] if modo in ("f2", "simulado") else banco_total
    pendentes = [q for q in banco if q["id"] not in ja_feitas]
    random.shuffle(pendentes)
    if simulado:
        # simulado e pra treinar ritmo e formato: se nao sobram 15 ineditas de 2a fase,
        # completa com questoes que a crianca ja viu (marcadas na tela final).
        if len(pendentes) < SIMULADO_N:
            repetidas = [q for q in banco if q["id"] in ja_feitas]
            random.shuffle(repetidas)
            pendentes += repetidas[:SIMULADO_N - len(pendentes)]
        pendentes = pendentes[:SIMULADO_N]
        st.session_state.simulado_inicio = datetime.now()
        st.session_state.simulado_repetidas = {q["id"] for q in pendentes if q["id"] in ja_feitas}
    st.session_state.fila = pendentes
    st.session_state.ids_banco = {q["id"] for q in banco_total}  # progresso e sempre sobre o banco inteiro
    st.session_state.pos = 0
    st.session_state.escolha = None  # letra marcada no simulado, antes de confirmar
    st.session_state.tentativas = 0
    st.session_state.revelado = 0  # 0=nada, 1=dica_curta, 2=primeiro_passo, 3=solucao_completa
    st.session_state.travado = False  # trava os botoes depois que a solucao aparece
    st.session_state.sessao_registros = []  # so as desta sessao, pra tela final
    st.session_state.log_completo = log  # cache em memoria pra stats sem bater no Gist de novo
    st.session_state.combo = 0  # respostas certas seguidas sem pedir dica, nesta sessao
    st.session_state.mostrar_progresso = False


def progresso_banco():
    """(respondidas, total) sobre o banco inteiro do perfil, contando ids distintos do log
    (uma questao repetida no simulado nao conta duas vezes)."""
    ids = st.session_state.ids_banco
    feitas = {r["id"] for r in st.session_state.log_completo["respostas"]} & ids
    return len(feitas), len(ids)


def proxima_questao():
    st.session_state.pos += 1
    st.session_state.tentativas = 0
    st.session_state.revelado = 0
    st.session_state.travado = False
    st.session_state.escolha = None


def responder_simulado(letra, q):
    """Uma resposta so, sem dica: grava no log (errou = dicas_usadas 3, que o
    calcular_stats ja trata como 'nao acertou') e guarda a questao inteira pra
    tela final mostrar o que errou, com a solucao."""
    acertou = letra == q["gabarito"]
    registro = {
        "id": q["id"], "prova": q["prova"], "tags": q["tags"],
        "acertou_de_primeira": acertou, "tentativas": 1,
        "dicas_usadas": 0 if acertou else 3, "modo": "simulado",
        "quando": datetime.now().isoformat(timespec="seconds"),
    }
    salvar_no_log(config_perfil["gist_arquivo"], registro)
    st.session_state.log_completo["respostas"].append(registro)
    st.session_state.combo = st.session_state.combo + 1 if acertou else 0
    st.session_state.sessao_registros.append({
        "prova": q["prova"], "acertou_de_primeira": acertou,
        "dicas_usadas": 0 if acertou else 3, "tags": q["tags"],
        "resposta": letra, "questao": q,
    })
    proxima_questao()


def responder(letra, q):
    if letra == q["gabarito"]:
        registro = {
            "id": q["id"], "prova": q["prova"], "tags": q["tags"],
            "acertou_de_primeira": st.session_state.tentativas == 0,
            "tentativas": st.session_state.tentativas + 1,
            "dicas_usadas": st.session_state.revelado,
            "quando": datetime.now().isoformat(timespec="seconds"),
        }
        salvar_no_log(config_perfil["gist_arquivo"], registro)
        st.session_state.log_completo["respostas"].append(registro)
        st.session_state.combo = st.session_state.combo + 1 if st.session_state.revelado == 0 else 0
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
            st.session_state.combo = 0
            registro = {
                "id": q["id"], "prova": q["prova"], "tags": q["tags"],
                "acertou_de_primeira": False, "tentativas": st.session_state.tentativas,
                "dicas_usadas": 3, "quando": datetime.now().isoformat(timespec="seconds"),
            }
            salvar_no_log(config_perfil["gist_arquivo"], registro)
            st.session_state.log_completo["respostas"].append(registro)
            st.session_state.sessao_registros.append({
                "prova": q["prova"], "acertou_de_primeira": False,
                "dicas_usadas": 3, "tags": q["tags"],
            })


# ---------- tela ----------

col_titulo, col_progresso, col_trocar = st.columns([5, 1, 1])
col_titulo.markdown(f"## 🦘 Cangurivis — hora de treinar, {config_perfil['nome']}!")
if col_progresso.button("📊", help="Ver meu progresso"):
    st.session_state.mostrar_progresso = not st.session_state.mostrar_progresso
    st.rerun()
CHAVES_SESSAO = ("fila", "pos", "tentativas", "revelado", "travado", "sessao_registros",
                 "ids_banco", "acabou_de_acertar", "log_completo", "combo",
                 "mostrar_progresso", "modo", "escolha", "simulado_inicio", "simulado_repetidas")


def limpar_sessao(trocar_perfil):
    for chave in CHAVES_SESSAO:
        st.session_state.pop(chave, None)
    if trocar_perfil:
        st.session_state.pop("perfil", None)
        st.query_params.clear()
    st.rerun()


if col_trocar.button("↩", help="Trocar quem vai treinar"):
    limpar_sessao(trocar_perfil=True)

stats = calcular_stats(st.session_state.log_completo["respostas"])

if st.session_state.mostrar_progresso:
    feitas, total = progresso_banco()
    st.progress(min(1.0, feitas / total) if total else 0.0)
    st.caption(f"{feitas}/{total} questões do banco já respondidas")

    col1, col2, col3 = st.columns(3)
    col1.metric("⭐ Pontos", stats["pontos_totais"])
    col2.metric("🏆 Nível", stats["nivel"])
    col3.metric("🔥 Dias seguidos", stats["dias_seguidos"])
    st.caption(f"Faltam {100 - stats['pontos_no_nivel']} pontos pro nível {stats['nivel'] + 1}.")

    if stats["taxa_de_primeira"]:
        st.markdown(f"**{stats['taxa_de_primeira']:.0f}%** das questões você acerta de primeira, sem pedir dica.")

    if stats["acerto_por_tag"]:
        st.markdown("**Acerto por habilidade** (sem usar dica):")
        df_tags = pd.DataFrame({"acerto (%)": stats["acerto_por_tag"]}).sort_values("acerto (%)")
        st.bar_chart(df_tags)
    else:
        st.caption("Continua praticando pra desbloquear o gráfico por habilidade!")

    if st.button("◀ Voltar a treinar", type="primary", width="stretch"):
        st.session_state.mostrar_progresso = False
        st.rerun()
    st.stop()

fila = st.session_state.fila

if st.session_state.pos >= len(fila):
    feitas_agora = len(st.session_state.sessao_registros)
    if simulado and feitas_agora:
        acertos = sum(1 for r in st.session_state.sessao_registros if r["acertou_de_primeira"])
        minutos = int((datetime.now() - st.session_state.simulado_inicio).total_seconds() // 60)
        st.success(f"Simulado terminado! **{acertos} de {feitas_agora}** certas em {minutos} min. 🎉")
        erradas = [r for r in st.session_state.sessao_registros if not r["acertou_de_primeira"]]
        if erradas:
            st.markdown(f"**Pra revisar com {config_perfil['nome']}** (o que errou, com a solução):")
            for r in erradas:
                qe = r["questao"]
                with st.expander(f"{qe['prova']} — marcou {r['resposta']}, certa era {qe['gabarito']}"):
                    if qe.get("modo") == "texto":
                        st.markdown(qe["enunciado_md"])
                        if qe.get("figura"):
                            st.image(qe["figura"], width="stretch")
                    else:
                        st.image(qe["imagem_questao"], width="stretch")
                    st.markdown(qe["solucao_completa"])
        else:
            st.markdown("Gabaritou! 🏆")
        if st.session_state.simulado_repetidas:
            st.caption(f"{len(st.session_state.simulado_repetidas)} dessas questões você já tinha visto antes "
                       "(não sobravam 15 inéditas de 2ª fase).")
    elif feitas_agora == 0 and modo == "f2":
        st.success("Você já respondeu todas as questões de 2ª fase disponíveis! 🎉")
        st.caption("Dá pra treinar o ritmo no modo Simulado, que repete questões já vistas quando precisa.")
    elif feitas_agora == 0:
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
    feitas, total = progresso_banco()
    st.caption(f"Progresso total: {feitas}/{total} questões do banco já respondidas.")
    if feitas_agora:
        st.markdown(f"⭐ **{stats['pontos_totais']} pontos** · 🏆 **nível {stats['nivel']}** · "
                     f"🔥 **{stats['dias_seguidos']} dia(s) seguido(s)** treinando")
    if st.button("🎲 Escolher outro modo de treino", type="primary", width="stretch"):
        limpar_sessao(trocar_perfil=False)
    if st.button("📊 Ver meu progresso completo", width="stretch"):
        st.session_state.mostrar_progresso = True
        st.rerun()
    st.stop()

q = fila[st.session_state.pos]

if simulado:
    minutos = int((datetime.now() - st.session_state.simulado_inicio).total_seconds() // 60)
    st.caption(f"⏱️ Simulado 2ª fase · Questão {st.session_state.pos + 1} de {len(fila)} · {minutos} min")
else:
    col_pts, col_nivel, col_combo = st.columns(3)
    col_pts.metric("⭐ Pontos", stats["pontos_totais"])
    col_nivel.metric("🏆 Nível", stats["nivel"])
    col_combo.metric("🔥 Combo", st.session_state.combo)
    rotulo_modo = "Só 2ª fase · " if modo == "f2" else ""
    st.caption(f"{rotulo_modo}Questão {st.session_state.pos + 1} de {len(fila)} nesta sessão · {q['prova']}")

if q.get("modo") == "texto":
    st.markdown(q["enunciado_md"])
    if q.get("figura"):
        st.image(q["figura"], width="stretch")
    st.markdown("  \n".join(f"**{a['letra']})** {a['texto']}" for a in q["alternativas"]))
else:
    st.image(q["imagem_questao"], width="stretch")

if simulado:
    # marca a letra (pode trocar) e so grava ao confirmar -- evita perder questao por
    # toque errado no tablet, mas continua sem dica e sem dizer se acertou.
    cols = st.columns(5)
    for i, letra in enumerate(LETRAS):
        if cols[i].button(letra, key=f"sim_{st.session_state.pos}_{letra}", width="stretch",
                          type="primary" if st.session_state.escolha == letra else "secondary"):
            st.session_state.escolha = letra
            st.rerun()
    if st.session_state.escolha:
        st.caption(f"Você marcou **{st.session_state.escolha}**. Pode trocar antes de confirmar.")
    if st.button("Confirmar e ir pra próxima ▶", type="primary", width="stretch",
                 disabled=st.session_state.escolha is None):
        responder_simulado(st.session_state.escolha, q)
        st.rerun()
    st.stop()

if st.session_state.get("acabou_de_acertar"):
    st.balloons()
    if st.session_state.combo >= 3:
        st.success(f"🎉 Isso aí! Resposta certa. Combo de {st.session_state.combo}! 🔥")
    else:
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
