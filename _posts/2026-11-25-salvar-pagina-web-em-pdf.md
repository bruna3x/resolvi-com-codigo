---
layout: post
title: "Como salvar qualquer página web em PDF"
date: 2026-11-25 09:00:00 -0300
resumo: "Um jeito de gerar PDF com controle de margem, tamanho e número de páginas, que funciona até em sites com login ou captcha."
ferramentas: [Python, Playwright]
sistema: Windows
nivel: "Quem nunca programou"
---

Quem já tentou salvar uma página com Ctrl+P conhece o resultado: tabela cortada no meio, menu ocupando metade da folha, cores que somem. Existe um jeito melhor, usado por programadores, que dá controle sobre margem, tamanho e número de páginas. E não precisa saber programar: é copiar, colar e mudar meia dúzia de valores.

Funciona em qualquer navegador da família Chromium: **Chrome, Edge, Brave, Opera e Vivaldi**.

## A ideia em uma frase

Você abre a página normalmente no seu navegador, e um pequeno programa se conecta a ele só para gerar o PDF. Como é você quem navega, funciona até em páginas com login ou captcha.

## O que você precisa

- Um navegador Chromium instalado
- O Python, baixado de [python.org](https://www.python.org/downloads/)
- Cinco minutos para a configuração inicial

## Configuração (só na primeira vez)

### 1. Instale a ferramenta

Abra o PowerShell (procure por "PowerShell" no menu Iniciar) e cole, uma linha por vez:

```powershell
py -m pip install playwright
py -m playwright install chromium
```

Isso instala o Playwright, a ferramenta que conversa com o navegador.

### 2. Crie o programa

Ainda no PowerShell:

```powershell
notepad pagina_pdf.py
```

O Bloco de Notas pergunta se você quer criar o arquivo. Responda **Sim**, cole o código abaixo, salve com Ctrl+S e feche.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

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

Esse arquivo serve para sempre e para qualquer página.

## Salvando uma página

### 1. Abra o navegador em modo especial

No PowerShell, cole o comando do seu navegador.

**Chrome**

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\perfil-pdf"
```

**Edge**

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\perfil-pdf"
```

**Brave**

```powershell
& "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\perfil-pdf"
```

Abre uma janela limpa do navegador, sem seus favoritos e logins. É normal: ela usa um perfil separado, criado só para isso.

### 2. Abra a página

Nessa janela, entre na página que quer salvar. Faça login ou resolva o captcha, se houver. Se a página for longa, role até o fim para carregar todas as imagens.

### 3. Rode o programa

Abra **outra** janela do PowerShell, sem fechar o navegador, e digite:

```powershell
py pagina_pdf.py
```

Vai aparecer a lista de abas abertas, cada uma com um número:

```plaintext
0 - Nova guia - chrome://newtab/
1 - Título da página - https://site.com/pagina
Número da aba:
```

Digite o número da aba que quer salvar e aperte Enter. Depois digite um nome para o arquivo e aperte Enter de novo.

### 4. Abra o PDF

```powershell
start nome-que-voce-deu.pdf
```

O arquivo fica na sua pasta de usuário (`C:\Users\seu-nome`). Para vê-la no Explorador de Arquivos, digite `explorer .`

## O que você pode mudar

Para editar o programa, digite `notepad pagina_pdf.py`, altere o valor, salve e rode de novo. Tudo que vale a pena mexer está dentro do bloco `pagina.pdf(...)`:

| Linha | O que controla | Opções |
|---|---|---|
| `format="A4"` | Tamanho do papel | `"A3"`, `"A5"`, `"Letter"`, `"Legal"` |
| `scale=0.9` | Zoom do conteúdo | De `0.1` a `2`. Menor = cabe mais por página. `1.0` = tamanho real |
| `margin={...}` | Margem de cada lado | Qualquer valor em `mm`, `cm` ou `in`. Use `"0"` para sem margem |
| `print_background=True` | Cores e imagens de fundo | `False` para economizar tinta |

E três linhas que você pode **acrescentar** dentro do mesmo bloco:

| Linha nova | Efeito |
|---|---|
| `landscape=True,` | Página deitada (paisagem) |
| `page_ranges="1-3",` | Salva só as páginas 1 a 3 |
| `page_ranges="1, 4-6",` | Salva a página 1 e as de 4 a 6 |

Fora desse bloco, duas mudanças úteis:

- **A página saiu diferente do esperado?** Apague a linha `pagina.emulate_media(media="screen")`. Sem ela, o PDF usa o layout de impressão que o próprio site preparou, que às vezes é mais limpo.
- **Quer salvar em outra pasta?** Na hora de digitar o nome, inclua a pasta: `Documents\relatorio` salva dentro de Documentos.

> Dois cuidados ao editar: não apague as vírgulas no fim das linhas e não mexa nos espaços do início de cada linha. O Python usa esses espaços para entender a estrutura do programa.

## Se algo der errado

| O que aconteceu | Como resolver |
|---|---|
| Erro de conexão ao rodar o programa | O navegador especial não está aberto. Volte ao passo 1 |
| O comando do navegador não é encontrado | O navegador está instalado em outra pasta. Clique com o botão direito no atalho dele, vá em Propriedades e copie o caminho do campo "Destino" |
| `No module named 'playwright'` | Você rodou com `python` em vez de `py`, ou pulou a instalação. Refaça o passo 1 da configuração |
| `can't open file` | O PowerShell está em outra pasta. Digite `cd ~` e tente de novo |
| Erro ao gravar o PDF | Já existe um PDF aberto com esse nome. Feche-o ou escolha outro nome |
| Imagens em branco | Role a página até o fim antes de rodar o programa |

## Resumo

**Uma vez só:**

```powershell
py -m pip install playwright
py -m playwright install chromium
notepad pagina_pdf.py
```

Cole o código do programa, salve e feche.

**Toda vez que quiser salvar uma página:**

1. Abra o navegador em modo especial (exemplo com o Chrome):

   ```powershell
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\perfil-pdf"
   ```

2. Abra a página nessa janela.
3. Em outro PowerShell, rode o programa:

   ```powershell
   py pagina_pdf.py
   ```

4. Digite o número da aba e o nome do arquivo.
5. Abra o resultado:

   ```powershell
   start nome.pdf
   ```

Quer entender o que cada linha do programa faz? Veja [o script explicado linha a linha]({{ '/receitas/o-script-de-pdf-linha-a-linha/' | relative_url }}).
