# -*- coding: utf-8 -*-
"""Segmentacao de questoes por ancora de texto + banda por posicao.
Validado no piloto (mirim 2025 F1 M2, 15/15 sem erro). Generalizado aqui para
qualquer prova com o padrao 'N. ENUNCIADO' numerado sequencialmente.
"""
import re
import pymupdf

ANCHOR_RE = re.compile(r'^(\d{1,2})\.(\s|$)')
# alguns layouts (ex.: mirim 2022) colocam o numero da questao num bloco
# separado, so "N.    \n", sem o enunciado junto -- depois do strip() nao
# sobra nenhum whitespace pra casar com \s, entao aceitamos fim-de-string tambem


def segmentar(pdf_path, x_max_ancora=400):
    """Retorna (bands, aviso). bands: {num: {pagina_pdf, y_top, y_bottom}}.
    aviso e None se a sequencia 1..N bateu certinho, ou uma string explicando
    o problema (numeracao quebrada) caso contrario -- pipeline nao deve parar
    sozinho, quem decide o que fazer com o aviso e quem chama.
    """
    doc = pymupdf.open(pdf_path)
    anchors = []  # (num, page_index, y0)
    for pi, page in enumerate(doc):
        full_text = page.get_text("text")
        if "QUADRO DE RESPOSTAS" in full_text:
            continue  # capa/gabarito, nao e pagina de questoes
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, text, bno, btype = b
            m = ANCHOR_RE.match(text.strip())
            if m and x0 < x_max_ancora:
                anchors.append((int(m.group(1)), pi, y0))

    anchors.sort(key=lambda a: a[0])
    nums = [a[0] for a in anchors]
    aviso = None
    if not nums:
        aviso = "nenhuma ancora encontrada (texto pode estar vetorizado -- ver chars/pagina)"
    elif nums != list(range(nums[0], nums[0] + len(nums))) or len(set(nums)) != len(nums):
        aviso = f"sequencia de numeros quebrada ou duplicada: {nums}"

    by_page = {}
    for num, pi, y0 in anchors:
        by_page.setdefault(pi, []).append((num, y0))
    for pi in by_page:
        by_page[pi].sort(key=lambda t: t[1])

    bands = {}
    for pi, items in by_page.items():
        page_h = doc[pi].rect.height
        for idx, (num, y0) in enumerate(items):
            y_top = max(0, y0 - 4)
            if idx + 1 < len(items):
                y_bottom = items[idx + 1][1] - 2
            else:
                y_bottom = page_h - 4
            bands[num] = {"pagina_pdf": pi + 1, "y_top": round(y_top, 1), "y_bottom": round(y_bottom, 1)}

    return bands, aviso


def renderizar_bands(pdf_path, bands, out_dir, dpi=200, prefixo="q"):
    doc = pymupdf.open(pdf_path)
    paths = {}
    for num, m in bands.items():
        page = doc[m["pagina_pdf"] - 1]
        rect = pymupdf.Rect(0, m["y_top"], page.rect.width, m["y_bottom"])
        pix = page.get_pixmap(clip=rect, dpi=dpi)
        fn = f"{out_dir}/{prefixo}{num:02d}_full.png"
        pix.save(fn)
        paths[num] = fn
    return paths
