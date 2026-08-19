import pymupdf, re, json

ANCHOR_RE = re.compile(r'^(\d{1,2})\.\s')

doc = pymupdf.open("../acervo/mirim/2025_F1_PROVA_M2.pdf")
anchors = []  # (num, page_index, y0)
for pi, page in enumerate(doc):
    full_text = page.get_text("text")
    if "QUADRO DE RESPOSTAS" in full_text:
        continue
    for b in page.get_text("blocks"):
        x0,y0,x1,y1,text,bno,btype = b
        m = ANCHOR_RE.match(text.strip())
        if m and x0 < 400:
            anchors.append((int(m.group(1)), pi, y0))

anchors.sort(key=lambda a: a[0])
assert [a[0] for a in anchors] == list(range(1,16)), "sequencia quebrada"

# bands: para cada questao, y0 ate o proximo anchor NA MESMA PAGINA, ou fim da pagina
by_page = {}
for num, pi, y0 in anchors:
    by_page.setdefault(pi, []).append((num, y0))
for pi in by_page:
    by_page[pi].sort(key=lambda t: t[1])

bands = {}  # num -> (page_index, y_top, y_bottom)
for pi, items in by_page.items():
    page_h = doc[pi].rect.height
    for idx, (num, y0) in enumerate(items):
        y_top = max(0, y0 - 4)
        if idx + 1 < len(items):
            y_bottom = items[idx+1][1] - 2
        else:
            y_bottom = page_h - 4  # deixa fora o rodape, que fica bem colado na borda
        bands[num] = (pi, y_top, y_bottom)

meta = {}
for num in range(1,16):
    pi, yt, yb = bands[num]
    page = doc[pi]
    rect = pymupdf.Rect(0, yt, page.rect.width, yb)
    pix = page.get_pixmap(clip=rect, dpi=200)
    fn = f"paginas/q{num:02d}_full.png"
    pix.save(fn)
    meta[num] = {"pagina_pdf": pi+1, "y_top": round(yt,1), "y_bottom": round(yb,1),
                 "width_px": pix.width, "height_px": pix.height}
    print(f"q{num:02d}: pagina {pi+1}, y=({yt:.0f},{yb:.0f}), {pix.width}x{pix.height}px -> {fn}")

with open("bands_2025_f1_m2.json","w",encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
