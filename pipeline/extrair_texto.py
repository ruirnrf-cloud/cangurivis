# -*- coding: utf-8 -*-
"""Rascunho automatico de enunciado + alternativas em texto, reconstruindo
ordem de leitura a partir dos blocos de texto do PDF. E DELIBERADAMENTE um
rascunho, nao fonte de verdade -- a tela de revisao sempre deixa o campo
editavel, e quem revisa confere contra a imagem antes de aprovar.

Duas dificuldades reais que moldam a heuristica:
1. Os marcadores (A)(B)(C)(D)(E) costumam ser circulo vetorial, nao texto --
   entao nao da pra usar "onde esta o marcador" pra achar as alternativas.
   Na pratica, quando a alternativa e um valor curto (numero/palavra), as 5
   costumam vir como UM bloco so, uma por linha, na ordem A-E de cima pra
   baixo -- isso e o sinal mais confiavel que achei (ver STATUS.md).
2. O enunciado as vezes vem fragmentado em mais de um bloco quando tem uma
   figura no meio do texto (frase, figura, mais uma frase). Um filtro de x0
   (< X_COL_MAX) separa isso de rotulos de grafico/tabela que ficam mais pra
   direita, sem depender de posicao "antes/depois" da banda.
"""
import re

X_COL_MAX = 150  # blocos mais a direita costumam ser rotulo de figura/tabela, nao enunciado
ALT_LINHA_MAX_CHARS = 30
ALT_BLOCO_MAX_CHARS = 160

ANCHOR_STRIP_RE = re.compile(r'^\d{1,2}\.\s*')
TEM_PALAVRA_RE = re.compile(r'[A-Za-zÀ-ÿ]{3,}')  # distingue frase de rotulo de celula/numero solto
SENTENCA_RE = re.compile(r'([.!?:;]\s*[•●\-]?\s*|^)([a-zà-ÿ])')  # tb pula marcador de lista (• ● -) antes da palavra


def _juntar_linhas(texto):
    # junta as linhas de um bloco multi-linha com espaco, EXCETO quando a
    # linha quebrou bem no meio de uma palavra hifenizada (ex.: "QUEBRA-\nCABECA")
    # -- nesse caso o hifen ja e a pontuacao certa, nao precisa de espaco extra
    linhas = texto.split("\n")
    out = linhas[0]
    for linha in linhas[1:]:
        if out.endswith("-"):
            out += linha.lstrip()
        elif linha.strip():
            out += " " + linha
    return out


def _para_case_normal(texto):
    # a prova inteira vem em caixa alta; deixar em minusculo com maiuscula de
    # frase e bem mais legivel pra uma crianca. Nomes proprios no meio da
    # frase (ex.: "JUSSARA" so no inicio, mas as vezes citado de novo depois)
    # ficam errados por essa transformacao -- e por isso que o campo continua
    # editavel na tela de revisao, isso aqui e so um ponto de partida melhor
    # que caixa alta crua.
    if not texto or texto.upper() != texto:
        return texto  # ja nao esta so em maiuscula, nao mexe
    minusculo = texto.lower()
    return SENTENCA_RE.sub(lambda m: m.group(1) + m.group(2).upper(), minusculo)


def _blocos_de_texto(page, band_rect):
    blocos = []
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text, bno, btype = b
        if btype != 0:
            continue
        import pymupdf
        r = pymupdf.Rect(x0, y0, x1, y1)
        if not band_rect.intersects(r):
            continue
        text = text.strip()
        if not text:
            continue
        blocos.append({"x0": x0, "y0": y0, "text": text})
    blocos.sort(key=lambda b: b["y0"])
    return blocos


def _achar_bloco_alternativas(blocos):
    for i, b in enumerate(blocos):
        linhas = [l.strip() for l in b["text"].split("\n") if l.strip()]
        if len(linhas) != 5:
            continue
        if len(b["text"]) > ALT_BLOCO_MAX_CHARS:
            continue
        if any(len(l) > ALT_LINHA_MAX_CHARS for l in linhas):
            continue
        return i, linhas
    return None, None


def extrair_questao(page, band_rect):
    import pymupdf
    band_rect = pymupdf.Rect(band_rect)
    blocos = _blocos_de_texto(page, band_rect)
    if not blocos:
        return {"enunciado_md": "", "alternativas": None, "confianca": "vazio"}

    blocos[0]["text"] = ANCHOR_STRIP_RE.sub("", blocos[0]["text"])

    alt_idx, alt_linhas = _achar_bloco_alternativas(blocos)

    enunciado_partes = []
    for i, b in enumerate(blocos):
        if i == alt_idx:
            continue
        if b["x0"] > X_COL_MAX:
            continue  # provavel rotulo de grafico/tabela, nao enunciado
        if i > 0 and not TEM_PALAVRA_RE.search(b["text"]):
            continue  # rotulo de celula/numero solto (ex.: alternativa em imagem), nao frase
        enunciado_partes.append(_juntar_linhas(b["text"]).strip())
    enunciado = re.sub(r"\s+", " ", " ".join(enunciado_partes)).strip()
    enunciado = _para_case_normal(enunciado)

    if alt_linhas:
        # NAO normaliza case aqui: alternativa costuma ser lista com virgula
        # ("DUDA, ANA, CLEO..."), nao frase com ponto -- recapitalizar so
        # separaria certo por virgula por acidente e erraria os outros nomes
        # de forma dificil de notar. Caixa alta crua e mais seguro que isso.
        alt_linhas = [re.sub(r"\s+", " ", l).strip() for l in alt_linhas]
        alternativas = [{"letra": l, "texto": t} for l, t in zip("ABCDE", alt_linhas)]
        confianca = "alta"
    else:
        alternativas = None
        confianca = "baixa"  # provavel alternativa em imagem, ou padrao nao reconhecido

    return {"enunciado_md": enunciado, "alternativas": alternativas, "confianca": confianca}


def extrair_prova(pdf_path, bands):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    resultado = {}
    for num, m in bands.items():
        page = doc[m["pagina_pdf"] - 1]
        band_rect = pymupdf.Rect(0, m["y_top"], page.rect.width, m["y_bottom"])
        resultado[num] = extrair_questao(page, band_rect)
    return resultado
