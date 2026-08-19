# -*- coding: utf-8 -*-
"""Extracao do gabarito oficial (regex QUESTAO N - ALTERNATIVA X) + as 4
validacoes bloqueantes definidas no plano. Validado no piloto: 15/15 corretos,
conferido de duas formas independentes.
"""
import re

GAB_RE = re.compile(r'QUEST[AÃ]O\s+(\d{1,2})\s*[–\-]\s*ALTERNATIVA\s+([A-E])', re.IGNORECASE)


def extrair_gabarito(sol_pdf_path):
    import pymupdf
    doc = pymupdf.open(sol_pdf_path)
    full_text = "\n".join(p.get_text("text") for p in doc)
    gabarito = {}
    for m in GAB_RE.finditer(full_text.upper()):
        gabarito[int(m.group(1))] = m.group(2)
    return gabarito


def validar_basico(bands, gabarito):
    """As checagens que nao dependem de alternativas transcritas: contagem,
    numeracao sem lacuna, gabarito com letra valida, distribuicao nao degenerada.
    Retorna lista de problemas (vazia = passou).
    """
    problemas = []
    nums_bands = sorted(bands.keys())
    nums_gab = sorted(gabarito.keys())

    if nums_bands != nums_gab:
        problemas.append(f"questoes segmentadas ({nums_bands}) != questoes com gabarito ({nums_gab})")

    if nums_bands and nums_bands != list(range(nums_bands[0], nums_bands[0] + len(nums_bands))):
        problemas.append(f"numeracao das questoes tem lacuna ou duplicata: {nums_bands}")

    letras_invalidas = {n: l for n, l in gabarito.items() if l not in "ABCDE"}
    if letras_invalidas:
        problemas.append(f"letras de gabarito fora de A-E: {letras_invalidas}")

    if gabarito:
        from collections import Counter
        dist = Counter(gabarito.values())
        total = len(gabarito)
        if total >= 8 and max(dist.values()) / total > 0.6:
            problemas.append(f"distribuicao de letras degenerada (uma letra domina >60%): {dict(dist)}")

    return problemas
