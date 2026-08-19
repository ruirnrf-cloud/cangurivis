import pymupdf, re, json, collections

RE = re.compile(r'QUEST[ÃA]O\s+(\d{1,2})\s*[–\-]\s*ALTERNATIVA\s+([A-E])')

doc = pymupdf.open("../acervo/mirim/2025_F1_SOL_M2.pdf")
full_text = "\n".join(page.get_text("text") for page in doc)
pairs = RE.findall(full_text)
gabarito = {int(n): letra for n, letra in pairs}

print("Encontrados:", len(gabarito))
nums = sorted(gabarito.keys())
print("Numeros:", nums)
print("1..15 sem lacuna/duplicata:", nums == list(range(1,16)))

dist = collections.Counter(gabarito.values())
print("Distribuicao de letras:", dict(dist))
print("Degenerada (>60% mesma letra)?", max(dist.values())/15 > 0.6)

with open("gabarito_2025_f1_m2.json","w",encoding="utf-8") as f:
    json.dump({str(k):v for k,v in sorted(gabarito.items())}, f, ensure_ascii=False, indent=2)
print()
for k in sorted(gabarito): print(f"  q{k:02d} = {gabarito[k]}")
