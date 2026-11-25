# Resolvi com código

Site com problemas reais resolvidos com código, explicados para quem não programa.
Feito com Jekyll e publicado pelo GitHub Pages.

## Estrutura

| Pasta ou arquivo | O que é |
|---|---|
| `_posts/` | As receitas, uma por arquivo Markdown |
| `scripts/` | Os scripts das receitas, prontos para baixar |
| `sobre.md` | Página Sobre |
| `index.html` | Página inicial (lista as receitas sozinha) |
| `_layouts/` | Moldes das páginas |
| `assets/css/style.css` | Aparência: cores e fontes ficam no topo do arquivo |
| `_config.yml` | Nome do site, autora e endereço |

## Publicar uma receita nova

1. Criar um arquivo em `_posts/` com o nome `AAAA-MM-DD-titulo-sem-acentos.md`.
2. Começar o arquivo com o cabeçalho:

   ```yaml
   ---
   layout: post
   title: "Título da receita"
   date: 2026-12-01 09:00:00 -0300
   resumo: "Uma frase dizendo que problema ela resolve."
   ferramentas: [Python]
   sistema: Windows
   nivel: "Quem nunca programou"
   ---
   ```

3. Escrever o texto em Markdown logo abaixo.
4. Enviar para o GitHub:

   ```powershell
   git add .
   git commit -m "Nova receita: titulo"
   git push
   ```

O site atualiza sozinho em um ou dois minutos.

## Etiquetas dos blocos de código

A etiqueta acima de cada bloco depende da linguagem indicada depois das três crases:

| Linguagem | Etiqueta |
|---|---|
| `powershell` | Digite no PowerShell |
| `python` | Conteúdo do arquivo .py |
| `css` | Regra de CSS |
| `plaintext` | O que aparece na tela |
