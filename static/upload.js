document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById('uploadForm');
    form.onsubmit = function(event) {
        event.preventDefault();
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);

        xhr.onload = function() {
            if (this.status == 200) {
                var resposta = JSON.parse(this.response);
                var mensagemSucesso = document.getElementById('mensagemSucesso');
                mensagemSucesso.textContent = resposta.mensagem;
                mensagemSucesso.style.display = 'block';
            } else {
                console.error('Erro no upload:', this.response);
            }
        };
        xhr.send(formData);
    };
});