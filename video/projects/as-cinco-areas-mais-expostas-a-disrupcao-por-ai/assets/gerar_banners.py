"""Gera os cartões, os quadros de cada take e a folha de sequência (1080 x 1920).

Saídas:
- assets/card-01..05.png: cartões brancos com tinta preta, em 2x.
- plano/take-01..07.png: quadros de cada take, como entram na composição.
- plano/sequencia.png: folha com os sete quadros lado a lado.

Rodar a partir da raiz do repositório:
    .venv/Scripts/python.exe video/projects/as-cinco-areas-mais-expostas-a-disrupcao-por-ai/assets/gerar_banners.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

from figuras import FIGURAS

ASSETS = Path(__file__).resolve().parent
PLANO = ASSETS.parent / "plano"
HTML = ASSETS / "html"

ITENS = [
    (1, "Corretagem de seguros", "Comparar propostas e preencher formulários sem crescer a equipe na mesma proporção."),
    (2, "Contabilidade e auditoria", "Automatizar rotinas para atender mais clientes com a equipe que você já tem."),
    (3, "Ciclo de receita em saúde", "Transformar notas clínicas em códigos de faturamento com menos trabalho manual."),
    (4, "Regulação de sinistros", "Agilizar a análise de apólices e danos, mantendo especialistas nas exceções."),
    (5, "Consultoria tributária", "Processar regras de várias jurisdições e liberar especialistas para decisões complexas."),
]

GANCHO = "As 5 áreas com mais oportunidade de disrupção com AI"
SUBGANCHO = "(segundo a Sequoia Capital)"
PALAVRA = "operação"
FRASE = "Eu envio o material no direct para quem quiser saber mais."

SEQUENCIA = [
    ("01 · Gancho", "00:00.0 a 00:05.0"),
    ("02 · Corretagem", "00:05.0 a 00:08.5"),
    ("03 · Contabilidade", "00:08.5 a 00:12.0"),
    ("04 · Saúde", "00:12.0 a 00:15.5"),
    ("05 · Sinistros", "00:15.5 a 00:19.0"),
    ("06 · Tributária", "00:19.0 a 00:22.5"),
    ("07 · CTA", "00:22.5 a 00:27.5"),
]

DEFS = """
<filter id="rough" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="3" seed="11" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="rough2" x="-25%" y="-25%" width="150%" height="150%">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<pattern id="ht-dark" width="11" height="11" patternUnits="userSpaceOnUse">
  <circle cx="5.5" cy="5.5" r="2.1" fill="#0A0A0A"/>
</pattern>
<marker id="seta" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="40" markerHeight="40" markerUnits="userSpaceOnUse" orient="auto">
  <path d="M0 0 L10 5 L0 10 Z" fill="#0A0A0A"/>
</marker>
"""

CSS_BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#555}
.grao::after{content:"";position:absolute;inset:0;z-index:9;pointer-events:none;background-image:radial-gradient(currentColor .5px,transparent .6px);background-size:4px 4px;opacity:.05}
"""

CSS_CARTAO = """
.cartao{position:relative;width:960px;height:1090px;overflow:hidden;background:#FFFFFF;color:#0A0A0A;font-family:"Inter",system-ui,sans-serif;box-shadow:inset 0 0 0 4px #0A0A0A}
.cartao::after{content:"";position:absolute;inset:0;z-index:9;pointer-events:none;background-image:radial-gradient(currentColor .5px,transparent .6px);background-size:4px 4px;opacity:.05}
.grosso{position:absolute;left:28px;top:40px;width:904px;height:9px;background:#0A0A0A}
.fino{position:absolute;left:28px;top:66px;width:904px;height:3px;background:#0A0A0A}
.chapeu{position:absolute;left:28px;top:94px;font-weight:500;font-size:24px;line-height:1;letter-spacing:.18em;text-transform:uppercase}
.titulo{position:absolute;left:28px;top:140px;width:904px;font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:800;font-size:80px;line-height:.94;letter-spacing:-.025em;text-wrap:balance}
.figura{position:absolute;left:28px;top:330px;width:904px;height:700px}
.figura svg{display:block;width:904px;height:700px;overflow:visible}
"""

CSS_QUADRO = """
.quadro{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0A0A0A;color:#FFFFFF;font-family:"Inter",system-ui,sans-serif}
.quadro .foto{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block}
.quadro .cartao-img{position:absolute;left:60px;top:240px;width:960px;height:1090px;display:block}
.quadro .legenda{position:absolute;left:88px;top:1400px;width:904px;font-weight:400;font-size:46px;line-height:1.32;border-top:3px solid #FFFFFF;padding-top:22px}
.quadro .legenda b{font-weight:700}
.impacto{position:absolute;left:88px;top:640px;width:904px;padding:36px 40px 32px;background:#0A0A0A;color:#FFFFFF;font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:800;font-size:92px;line-height:.98;letter-spacing:-.025em;text-wrap:balance}
.impacto small{display:block;margin-top:22px;font-family:"Inter",system-ui,sans-serif;font-weight:500;font-size:34px;line-height:1.2;letter-spacing:0}
.cta{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:88px}
.comenta{font-weight:500;font-size:60px;line-height:1}
.palavra{font-family:"Bricolage Grotesque",system-ui,sans-serif;font-weight:800;font-size:190px;line-height:.94;letter-spacing:-.025em;margin:44px 0 52px}
.frase{font-weight:400;font-size:50px;line-height:1.32;max-width:760px}
"""

CSS_FOLHA = """
.folha{width:2160px;padding:27px;display:grid;grid-template-columns:repeat(7,270px);gap:36px;background:#D9D9D9}
.folha figure{margin:0}
.folha img{display:block;width:270px;height:480px;outline:1px solid #0A0A0A}
.folha figcaption{margin-top:14px;font-family:"Inter",system-ui,sans-serif;font-weight:500;font-size:22px;line-height:1.3;letter-spacing:.04em;text-transform:uppercase;color:#0A0A0A}
"""


def pagina(corpo, css, prefixo_fontes):
    fontes = (
        '@font-face{font-family:"Bricolage Grotesque";src:url("' + prefixo_fontes
        + 'bricolage-grotesque-latin-wght-normal.woff2") format("woff2");font-weight:200 800;font-style:normal}'
        '@font-face{font-family:"Inter";src:url("' + prefixo_fontes
        + 'inter-latin-wght-normal.woff2") format("woff2");font-weight:100 900;font-style:normal}'
    )
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>'
        + fontes + CSS_BASE + css
        + '</style></head><body>'
        + '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + DEFS + '</defs></svg>'
        + corpo + '</body></html>'
    )


def escrever(nome, corpo, css):
    arquivo = HTML / nome
    arquivo.write_text(pagina(corpo, css, "../fonts/"), encoding="utf-8")
    return arquivo


def captura(navegador, html, saida, dsf, largura, altura):
    pagina_web = navegador.new_page(viewport={"width": largura, "height": altura}, device_scale_factor=dsf)
    pagina_web.goto(html.as_uri())
    pagina_web.evaluate("document.fonts.ready")
    pagina_web.locator("#alvo").first.screenshot(path=str(saida))
    pagina_web.close()
    print("ok", saida.relative_to(ASSETS.parent).as_posix())


def cartao(numero, titulo):
    return (
        '<section class="cartao" id="alvo"><div class="grosso"></div><div class="fino"></div>'
        f'<div class="chapeu">Fig. {numero:02d}</div><h1 class="titulo">{titulo}</h1>'
        f'<div class="figura"><svg viewBox="0 0 904 700" fill="none" aria-hidden="true">{FIGURAS[numero]}</svg></div>'
        '</section>'
    )


def quadro(conteudo, extra=""):
    return '<section class="quadro grao ' + extra + '" id="alvo">' + conteudo + '</section>'


def main():
    HTML.mkdir(exist_ok=True)
    PLANO.mkdir(exist_ok=True)
    with sync_playwright() as p:
        navegador = p.chromium.launch()

        for numero, titulo, _ in ITENS:
            html = escrever(f"cartao-{numero:02d}.html", cartao(numero, titulo), CSS_CARTAO)
            captura(navegador, html, ASSETS / f"card-{numero:02d}.png", 2, 1080, 1920)

        conteudo = f'<img class="foto" src="../../plano/gancho-frame.png" alt=""><div class="impacto">{GANCHO}<small>{SUBGANCHO}</small></div>'
        html = escrever("take-01.html", quadro(conteudo), CSS_QUADRO)
        captura(navegador, html, PLANO / "take-01.png", 1, 1080, 1920)

        for numero, _, legenda in ITENS:
            conteudo = f'<img class="cartao-img" src="../card-{numero:02d}.png" alt=""><p class="legenda"><b>Fig. {numero:02d}.</b> {legenda}</p>'
            html = escrever(f"take-{numero + 1:02d}.html", quadro(conteudo), CSS_QUADRO)
            captura(navegador, html, PLANO / f"take-{numero + 1:02d}.png", 1, 1080, 1920)

        conteudo = f'<p class="comenta">comenta:</p><p class="palavra">“{PALAVRA}”</p><p class="frase">{FRASE}</p>'
        html = escrever("take-07.html", quadro(conteudo, "cta"), CSS_QUADRO)
        captura(navegador, html, PLANO / "take-07.png", 1, 1080, 1920)

        figuras = "".join(
            f'<figure><img src="../../plano/take-{n:02d}.png" alt=""><figcaption>{rotulo}<br>{tempo}</figcaption></figure>'
            for n, (rotulo, tempo) in enumerate(SEQUENCIA, start=1)
        )
        html = escrever("sequencia.html", '<main class="folha" id="alvo">' + figuras + '</main>', CSS_FOLHA)
        captura(navegador, html, PLANO / "sequencia.png", 1, 2160, 1000)

        navegador.close()


if __name__ == "__main__":
    main()
