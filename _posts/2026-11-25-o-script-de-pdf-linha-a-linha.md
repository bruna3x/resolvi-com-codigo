---
layout: post
title: "O script de PDF explicado linha a linha"
date: 2026-11-25 10:00:00 -0300
resumo: "O que significa cada linha e cada símbolo do programa que salva páginas em PDF, e como adaptá-lo sem quebrar nada."
ferramentas: [Python, Playwright, CSS]
sistema: Windows
nivel: "Quem já rodou a receita e quer entender"
---

Na receita [Como salvar qualquer página web em PDF]({{ '/receitas/salvar-pagina-web-em-pdf/' | relative_url }}) o programa é só copiado e colado. Aqui ele é desmontado: o que cada linha faz, o que cada símbolo significa e até onde dá para mexer.

## As três peças

1. **O navegador em modo de depuração.** Uma janela do navegador aberta com uma "porta" (a 9222) por onde um programa pode controlá-la. Você navega nela normalmente.
2. **O script `pagina_pdf.py`.** Um arquivo de texto com instruções em Python. Ele se conecta ao navegador pela porta, pergunta qual aba você quer e gera o PDF dela.
3. **O PowerShell.** O terminal onde você digita os comandos para abrir o navegador e rodar o script.

## O comando que abre o navegador

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\perfil-pdf"
```

| Parte | O que significa |
|---|---|
| `&` | No PowerShell, manda executar o programa cujo caminho vem a seguir entre aspas |
| `"C:\Program Files\...\chrome.exe"` | Caminho do navegador. Fica entre aspas porque tem espaço em "Program Files" |
| `--remote-debugging-port=9222` | Abre a porta 9222, por onde o script se conecta. Os dois traços indicam uma opção do programa |
| `--user-data-dir="..."` | Usa um perfil separado do seu navegador do dia a dia. É obrigatório: o navegador não libera a porta no perfil principal |
| `$env:USERPROFILE` | Atalho do PowerShell para a sua pasta de usuário (`C:\Users\seu-nome`) |

Logins feitos nessa janela ficam guardados no perfil separado, então da próxima vez você já entra logado.

## O script

```python
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
```

## Linha a linha

| Linha | O que faz |
|---|---|
| `from playwright.sync_api import sync_playwright` | Carrega a ferramenta Playwright para dentro do script |
| `with sync_playwright() as p:` | Liga o Playwright e dá a ele o apelido `p`. Tudo que está recuado abaixo acontece com ele ligado; ao final, ele desliga sozinho |
| `browser = p.chromium.connect_over_cdp("http://localhost:9222")` | Conecta ao navegador pela porta 9222. `localhost` significa "este computador" |
| `context = browser.contexts[0]` | Pega a janela do navegador. `[0]` significa "o primeiro item": em Python a contagem começa em 0 |
| `# Mostra as abas abertas` | Comentário. Tudo depois de `#` é ignorado pelo Python; serve de anotação |
| `for i, pg in enumerate(context.pages):` | Repete a linha de baixo para cada aba aberta. `i` é o número da aba e `pg` é a aba |
| `print(i, "-", pg.title(), "-", pg.url)` | Escreve na tela o número, o título e o endereço de cada aba |
| `numero = int(input("Número da aba: "))` | `input` mostra a pergunta e espera você digitar. `int` transforma o que foi digitado em número |
| `nome = input("Nome do PDF (sem .pdf): ")` | Pergunta o nome do arquivo e guarda em `nome` |
| `pagina = context.pages[numero]` | Seleciona a aba escolhida |
| `pagina.emulate_media(media="screen")` | Faz o PDF sair com a aparência da tela, e não com o layout de impressão do site |
| `pagina.add_style_tag(content="""...""")` | Injeta regras de CSS, a linguagem de aparência das páginas, só para este PDF. As três aspas permitem escrever um texto de várias linhas |
| `img, table { break-inside: avoid; }` | Não cortar imagens nem tabelas no meio entre duas páginas |
| `h1, h2, h3 { break-after: avoid; }` | Não deixar um título sozinho no fim da página |
| `pagina.pdf(...)` | Gera o PDF. O que está entre parênteses são as configurações, uma por linha |
| `path=nome + ".pdf"` | Nome do arquivo: o que foi digitado mais a extensão. `+` junta dois textos |
| `format="A4"` | Tamanho do papel |
| `margin={"top": "15mm", ...}` | Margens de cada lado. As chaves agrupam pares de nome e valor |
| `print_background=True` | Mantém cores e imagens de fundo |
| `scale=0.9` | Zoom do conteúdo: 0.9 é 90% do tamanho real |
| `print("Pronto:", nome + ".pdf")` | Avisa que terminou |

## Os símbolos

- **Recuo de 4 espaços.** Em Python, o recuo indica o que está "dentro" de quê. Não pode ser apagado nem desalinhado.
- **`=`** guarda um valor em um nome, como em `nome = ...`. Dentro de parênteses, define uma configuração, como em `scale=0.9`.
- **`.`** significa "use esta função deste objeto": `pagina.pdf()` é "gerar o PDF da página".
- **Aspas** delimitam texto. Sem aspas, o Python entende como nome de variável ou número.
- **`:`** no fim de uma linha (`with`, `for`) abre um bloco, e as linhas seguintes vêm recuadas.
- **`#`** começa um comentário.

## Onde o PDF é salvo

O PDF é salvo na **pasta em que o PowerShell está** quando o script roda. O PowerShell mostra essa pasta no começo de cada linha: `PS C:\Users\seu-nome>` significa que você está em `C:\Users\seu-nome`.

| Quero | Comando |
|---|---|
| Ver em que pasta estou | `pwd` |
| Listar os PDFs da pasta | `ls *.pdf` |
| Abrir um PDF | `start nome.pdf` |
| Abrir a pasta no Explorador de Arquivos | `explorer .` |
| Ir para outra pasta | `cd Documents` |
| Voltar uma pasta | `cd ..` |
| Voltar para a pasta do usuário | `cd ~` |

Se já existir um PDF com o mesmo nome, ele é **sobrescrito** sem aviso.

## Esconder um elemento da página

Menu, banner de cookies e barras fixas costumam poluir o PDF. Para tirar:

1. No navegador, clique com o botão direito no elemento indesejado e escolha **Inspecionar**.
2. No painel que abre, veja o `id` ou a `class` do elemento. Exemplo: `<div id="menu-topo" class="barra">`.
3. Acrescente uma linha no CSS do script, dentro das três aspas:

```css
#menu-topo { display: none !important; }
.barra { display: none !important; }
```

`#` seleciona por `id` e `.` seleciona por `class`. `display: none` esconde, e `!important` garante que a regra vença as do site.

Para forçar uma quebra de página antes de um elemento, a regra é `seletor { break-before: page; }`.

## O que não mexer

- A porta `9222`, a não ser que você mude também no comando do navegador.
- O recuo das linhas.
- A primeira linha do script.

Se depois de editar aparecer `IndentationError`, o recuo de alguma linha ficou desalinhado.

## Por que não usar o navegador do próprio Playwright

O Playwright consegue abrir um navegador sozinho, sem você fazer nada. O problema é que sites com reCAPTCHA detectam esse navegador automatizado e entregam um captcha quebrado, com imagens pela metade. Conectando ao seu navegador de verdade, quem resolve o captcha é você, numa janela normal, e o script só entra depois.

## Exemplo real: Currículo Lattes

A página pública do Lattes pede um captcha antes de mostrar o currículo, e o Ctrl+P dela sai mal formatado. Com esta receita:

1. Abra o navegador em modo de depuração.
2. Abra o link do currículo, resolva o captcha e espere o currículo aparecer.
3. Confira a data de "Última atualização" no topo: a versão pública demora a refletir alterações recentes.
4. Em outro PowerShell, rode `py pagina_pdf.py`.
5. Escolha a aba do currículo, não a do captcha, e dê um nome ao arquivo.
6. Abra com `start nome.pdf`.

## Para ir além

<aside class="indicacao">
  <p class="indicacao-aviso">Indicação com link de afiliado: se você comprar por ele, eu recebo uma comissão, sem custo extra para você.</p>
  <p><strong><a href="https://www.amazon.com.br/dp/B0FLF3FPYR?linkCode=ll2&amp;tag=livros3x-20&amp;linkId=0246f8bda3bc86abbafd4a866fe79ac7&amp;ref_=as_li_ss_tl" rel="sponsored nofollow noopener" target="_blank">Automatize Tarefas Maçantes com Python</a></strong>, de Al Sweigart. Ensina Python a quem não é programador, por meio de pequenos projetos de automação: renomear arquivos em lote, preencher planilhas, extrair dados de páginas. É a mesma lógica das receitas deste site, em formato de livro.</p>
</aside>

## Conceitos desta receita

- **Script:** arquivo de texto com instruções que o Python executa de cima para baixo.
- **Biblioteca:** código pronto feito por outras pessoas, instalado com `pip`. Playwright é uma biblioteca.
- **CDP (porta de depuração):** canal que permite a um script controlar um navegador já aberto.
- **CSS:** linguagem que define a aparência das páginas web. Dá para injetar regras próprias antes de gerar o PDF.
- **Caminho relativo e completo:** `nome.pdf` é relativo à pasta em que você está; `C:\Users\seu-nome\nome.pdf` funciona de qualquer lugar.
- **`py` e `python`:** no Windows, o comando `py` garante o Python oficial quando há mais de um instalado.
