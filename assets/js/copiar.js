// Acrescenta um botão "Copiar" em cada bloco de código.
document.querySelectorAll("div.highlighter-rouge").forEach(function (bloco) {
  var codigo = bloco.querySelector("code");
  if (!codigo || !navigator.clipboard) return;

  var botao = document.createElement("button");
  botao.type = "button";
  botao.className = "copiar";
  botao.textContent = "Copiar";
  botao.addEventListener("click", function () {
    navigator.clipboard.writeText(codigo.innerText.trimEnd()).then(function () {
      botao.textContent = "Copiado";
      setTimeout(function () { botao.textContent = "Copiar"; }, 1800);
    });
  });
  bloco.appendChild(botao);
});
