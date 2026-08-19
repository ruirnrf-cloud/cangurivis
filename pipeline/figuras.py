# -*- coding: utf-8 -*-
"""Isolamento de figura por banda: cluster_drawings + imagens rasterizadas,
recortado contra blocos de texto reais (nao so proximidade geometrica).
Validado no piloto apos o ajuste: 13/15 recortes limpos, 2 com ressalva leve
documentada (marcadores vetoriais sem contraparte textual -- ver RELATORIO.md).
"""
import pymupdf


def is_hairline(r):
    w, h = r.width, r.height
    thin = min(w, h)
    long_ = max(w, h)
    return thin < 4 and long_ > 60


def merge_close(rects, gap=15):
    rects = [pymupdf.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                exp = pymupdf.Rect(a.x0 - gap, a.y0 - gap, a.x1 + gap, a.y1 + gap)
                if exp.intersects(b):
                    rects[i] = a | b
                    rects.pop(j)
                    changed = True
                    break
            if changed:
                break
    return rects


def trim_against_text(r, text_blocks, passes=4):
    r = pymupdf.Rect(r)
    for _ in range(passes):
        changed = False
        for tbr in text_blocks:
            if not r.intersects(tbr):
                continue
            inter = r & tbr
            if inter.is_empty:
                continue
            if inter.width >= 0.6 * r.width:
                if abs(inter.y0 - r.y0) < 2 and inter.y1 < r.y1:
                    r.y0 = inter.y1
                    changed = True
                elif abs(inter.y1 - r.y1) < 2 and inter.y0 > r.y0:
                    r.y1 = inter.y0
                    changed = True
            if inter.height >= 0.6 * r.height:
                if abs(inter.x0 - r.x0) < 2 and inter.x1 < r.x1:
                    r.x0 = inter.x1
                    changed = True
                elif abs(inter.x1 - r.x1) < 2 and inter.x0 > r.x0:
                    r.x1 = inter.x0
                    changed = True
        if not changed:
            break
    return r


def text_overlap_ratio(r, text_blocks):
    area = r.width * r.height
    if area <= 0:
        return 0.0
    covered = sum((r & tbr).width * (r & tbr).height for tbr in text_blocks if r.intersects(tbr))
    return covered / area


def isolar_figuras(pdf_path, bands, out_dir, prefixo="q", pad=6, dpi=300):
    doc = pymupdf.open(pdf_path)
    results = {}
    for num, m in bands.items():
        page = doc[m["pagina_pdf"] - 1]
        band_rect = pymupdf.Rect(0, m["y_top"], page.rect.width, m["y_bottom"])

        text_blocks = []
        for b in page.get_text("blocks"):
            tbr = pymupdf.Rect(b[:4])
            if band_rect.intersects(tbr) and len(b[4].split()) >= 2:
                text_blocks.append(tbr & band_rect)

        clusters = page.cluster_drawings(clip=band_rect, x_tolerance=3, y_tolerance=3)
        clusters = [c for c in clusters if c.width > 12 and c.height > 12 and (c.width * c.height) > 300]
        clusters = [c for c in clusters if not is_hairline(c)]
        merged = merge_close(clusters, gap=15)
        for info in page.get_image_info():
            r = pymupdf.Rect(info["bbox"])
            if r.width > 12 and r.height > 12 and band_rect.intersects(r) and not is_hairline(r):
                merged.append(r & band_rect)
        merged = merge_close(merged, gap=15)

        # descarta por overlap com texto, independente do tamanho: peca de figura
        # de verdade fica em branco (overlap medido ~0-0.2 em todos os casos
        # confirmados a olho); fragmento de ruido (texto parcialmente vetorizado,
        # marcador de lista) fica sempre >=0.5. 0.4 fica no meio com folga.
        trimmed = []
        for r in merged:
            if text_overlap_ratio(r, text_blocks) > 0.4:
                continue
            trimmed.append(trim_against_text(r, text_blocks))
        merged = [r for r in trimmed if not r.is_empty and r.width * r.height > 400 and not is_hairline(r)]

        paths = []
        for k, r in enumerate(merged):
            rp = pymupdf.Rect(r.x0 - pad, r.y0 - pad, r.x1 + pad, r.y1 + pad) & band_rect
            pix = page.get_pixmap(clip=rp, dpi=dpi)
            fn = f"{out_dir}/{prefixo}{num:02d}_fig{k}.png"
            pix.save(fn)
            paths.append({"path": fn, "bbox": [round(v, 1) for v in rp], "pagina": m["pagina_pdf"]})
        results[num] = paths
    return results
