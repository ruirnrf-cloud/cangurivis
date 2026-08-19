import pymupdf, json

doc = pymupdf.open("../acervo/mirim/2025_F1_PROVA_M2.pdf")
bands = json.load(open("bands_2025_f1_m2.json", encoding="utf-8"))

def merge_close(rects, gap=15):
    rects = [pymupdf.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        for i in range(len(rects)):
            for j in range(i+1, len(rects)):
                a, b = rects[i], rects[j]
                exp = pymupdf.Rect(a.x0-gap, a.y0-gap, a.x1+gap, a.y1+gap)
                if exp.intersects(b):
                    rects[i] = a | b
                    rects.pop(j)
                    changed = True
                    break
            if changed:
                break
    return rects

def trim_against_text(r, text_blocks, passes=4):
    # encolhe r para fora de blocos de texto que cobrem uma borda inteira,
    # em vez de descartar o cluster so por tocar texto (evita perder figura real)
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


results = {}
for num_s, m in bands.items():
    num = int(num_s)
    pi = m["pagina_pdf"] - 1
    page = doc[pi]
    band_rect = pymupdf.Rect(0, m["y_top"], page.rect.width, m["y_bottom"])

    def is_hairline(r):
        # linhas divisorias finas (regua entre questoes) nao devem virar ponte de merge
        w, h = r.width, r.height
        thin = min(w, h)
        long_ = max(w, h)
        return thin < 4 and long_ > 60

    # blocos de texto "de conteudo" (paragrafo/enunciado real), nao marcadores soltos
    text_blocks = []
    for b in page.get_text("blocks"):
        tbr = pymupdf.Rect(b[:4])
        if band_rect.intersects(tbr) and len(b[4].split()) >= 2:
            text_blocks.append(tbr & band_rect)

    clusters = page.cluster_drawings(clip=band_rect, x_tolerance=3, y_tolerance=3)
    clusters = [c for c in clusters if c.width > 12 and c.height > 12 and (c.width*c.height) > 300]
    clusters = [c for c in clusters if not is_hairline(c)]
    merged = merge_close(clusters, gap=15)
    # tambem inclui imagens rasterizadas embutidas na banda
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"])
        if r.width > 12 and r.height > 12 and band_rect.intersects(r) and not is_hairline(r):
            merged.append(r & band_rect)
    merged = merge_close(merged, gap=15)

    def text_overlap_ratio(r, text_blocks):
        area = r.width * r.height
        if area <= 0:
            return 0.0
        covered = sum((r & tbr).width * (r & tbr).height for tbr in text_blocks if r.intersects(tbr))
        return covered / area

    SMALL_AREA = 3000  # abaixo disso, e do tamanho de 1-2 linhas de texto, nao de uma figura de verdade
    trimmed = []
    for r in merged:
        if r.width*r.height < SMALL_AREA and text_overlap_ratio(r, text_blocks) > 0.3:
            continue  # fragmento de vetor dentro de bloco de texto (ex: marcador de lista) -> descarta
        trimmed.append(trim_against_text(r, text_blocks))
    merged = [r for r in trimmed if not r.is_empty and r.width*r.height > 400 and not is_hairline(r)]

    PAD = 6
    paths = []
    for k, r in enumerate(merged):
        rp = pymupdf.Rect(r.x0-PAD, r.y0-PAD, r.x1+PAD, r.y1+PAD) & band_rect
        r = rp
        pix = page.get_pixmap(clip=r, dpi=300)
        fn = f"figuras/q{num:02d}_fig{k}.png"
        pix.save(fn)
        paths.append({"path": fn, "bbox": [round(v,1) for v in r], "pagina": pi+1})
    results[num] = paths
    print(f"q{num:02d}: {len(merged)} cluster(s) -> {[p['path'] for p in paths]}")

with open("figuras_meta.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
