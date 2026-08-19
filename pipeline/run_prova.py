# -*- coding: utf-8 -*-
"""Orquestra segmentacao + gabarito + figuras + rascunho de texto para uma
prova, e grava um rascunho estruturado por questao (id canonico, banda,
gabarito, figuras, imagem da questao inteira, enunciado/alternativas em
texto). O rascunho de enunciado/alternativas e best-effort (ver
extrair_texto.py) -- a tela de revisao sempre deixa editar antes de aprovar.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from segmentar import segmentar, renderizar_bands
from gabarito import extrair_gabarito, validar_basico
from figuras import isolar_figuras
from extrair_texto import extrair_prova as extrair_texto_prova


def rodar(prova_pdf, sol_pdf, out_dir, meta_fonte):
    os.makedirs(f"{out_dir}/paginas", exist_ok=True)
    os.makedirs(f"{out_dir}/figuras", exist_ok=True)

    bands, aviso_segmentacao = segmentar(prova_pdf)
    gabarito = extrair_gabarito(sol_pdf)
    problemas = validar_basico(bands, gabarito)
    if aviso_segmentacao:
        problemas.insert(0, aviso_segmentacao)

    resultado = {
        "fonte": meta_fonte,
        "pdf_prova": prova_pdf,
        "pdf_solucao": sol_pdf,
        "n_questoes_segmentadas": len(bands),
        "n_gabaritos_extraidos": len(gabarito),
        "problemas_bloqueantes": problemas,
        "questoes": {},
    }

    if problemas:
        # nao vale a pena renderizar/isolar figura de uma prova cuja segmentacao
        # ja veio quebrada -- fica so o diagnostico, para decidir o proximo passo
        with open(f"{out_dir}/diagnostico.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        return resultado

    imagens = renderizar_bands(prova_pdf, bands, f"{out_dir}/paginas")
    figs = isolar_figuras(prova_pdf, bands, f"{out_dir}/figuras")
    textos = extrair_texto_prova(prova_pdf, bands)

    nivel_slug = meta_fonte["nivel_slug"]
    for num in sorted(bands):
        cid = f"{meta_fonte['olimpiada_slug']}-{meta_fonte['ano']}-f{meta_fonte['fase']}-{nivel_slug}-q{num:02d}"
        texto = textos.get(num, {})
        resultado["questoes"][num] = {
            "numero": num,
            "id": cid,
            "gabarito": gabarito.get(num),
            "banda": bands[num],
            "imagem_questao": imagens[num],
            "figuras": [p["path"] for p in figs.get(num, [])],
            "n_figuras": len(figs.get(num, [])),
            "enunciado_rascunho": texto.get("enunciado_md", ""),
            "alternativas_rascunho": texto.get("alternativas"),
            "confianca_texto": texto.get("confianca", "vazio"),
        }

    with open(f"{out_dir}/rascunho.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    return resultado


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("prova_pdf")
    ap.add_argument("sol_pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--olimpiada-slug", default="mirim")
    ap.add_argument("--nivel-slug", required=True)
    ap.add_argument("--ano", type=int, required=True)
    ap.add_argument("--fase", type=int, required=True)
    args = ap.parse_args()
    meta = {
        "olimpiada_slug": args.olimpiada_slug, "nivel_slug": args.nivel_slug,
        "ano": args.ano, "fase": args.fase,
    }
    r = rodar(args.prova_pdf, args.sol_pdf, args.out_dir, meta)
    print(json.dumps({k: v for k, v in r.items() if k != "questoes"}, ensure_ascii=False, indent=2))
