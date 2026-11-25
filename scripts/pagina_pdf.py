"""Salva em PDF uma aba aberta em um navegador Chromium (Chrome, Edge, Brave).

Antes de rodar, abra o navegador com a porta de depuração 9222.
Passo a passo completo no site, na receita "Como salvar qualquer página web em PDF".
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

    # Mostra as abas abertas
    for i, pg in enumerate(context.pages):
        print(i, "-", pg.title(), "-", pg.url)

    numero = int(input("Número da aba: "))
    nome = input("Nome do PDF (sem .pdf): ")
    pagina = context.pages[numero]

    pagina.emulate_media(media="screen")
    pagina.add_style_tag(content="""
        img, table { break-inside: avoid; }
        h1, h2, h3 { break-after: avoid; }
    """)
    pagina.pdf(
        path=nome + ".pdf",
        format="A4",
        margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"},
        print_background=True,
        scale=0.9,
    )
    print("Pronto:", nome + ".pdf")
