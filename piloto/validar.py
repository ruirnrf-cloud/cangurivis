import json, collections

d = json.load(open("saida/mirim_2025_f1_m2.json", encoding="utf-8"))
qs = d["questoes"]

erros = []

# 1. contagem
if len(qs) != 15:
    erros.append(f"contagem: esperado 15, achado {len(qs)}")

# 2. numeracao sem lacuna/duplicata
nums = sorted(q["numero"] for q in qs)
if nums != list(range(1,16)):
    erros.append(f"numeracao com lacuna/duplicata: {nums}")

# 3. toda letra do gabarito existe entre as alternativas da questao
for q in qs:
    letras = [a["letra"] for a in q["alternativas"]]
    if len(letras) != 5:
        erros.append(f"q{q['numero']:02d}: {len(letras)} alternativas, esperado 5")
    if q["gabarito"] not in letras:
        erros.append(f"q{q['numero']:02d}: gabarito {q['gabarito']} nao esta entre as alternativas {letras}")

# 4. distribuicao de letras nao degenerada
dist = collections.Counter(q["gabarito"] for q in qs)
mx = max(dist.values())
if mx/len(qs) > 0.6:
    erros.append(f"distribuicao degenerada: {dict(dist)}")

# 5. ids canonicos unicos
ids = [q["id"] for q in qs]
if len(set(ids)) != len(ids):
    erros.append("ids canonicos duplicados")

# 6. todo arquivo de figura/imagem referenciado existe de fato no disco
import os
faltando = []
for q in qs:
    for p in [q["imagem_questao"]] + q["figuras"]:
        if not os.path.exists(p):
            faltando.append(p)
if faltando:
    erros.append(f"arquivos referenciados mas ausentes no disco: {faltando}")

print(f"Gabarito completo: {dict(sorted((q['numero'], q['gabarito']) for q in qs))}")
print(f"Distribuicao de letras: {dict(sorted(dist.items()))}")
print()
if erros:
    print(f"FALHOU: {len(erros)} problema(s)")
    for e in erros:
        print(" -", e)
else:
    print("TODAS AS VALIDACOES PASSARAM (contagem, numeracao, gabarito-em-alternativas, distribuicao, ids unicos, arquivos existem)")
