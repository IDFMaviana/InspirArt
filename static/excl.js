document.getElementById("excl").addEventListener("submit", function(event) {
    event.preventDefault(); // Impede o envio do formulário

    // Envia uma solicitação para a rota Flask usando fetch
    fetch("/exclui_pasta", {
        method: "POST"
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Erro ao limpar pasta');
    })
    .then(data => {
        // Atualiza a página após 1 segundo
        setTimeout(() => {
            location.reload();
        }, 1000);
    })
    .catch(error => {
        console.error('Erro:', error); // Exibe o erro no console
    });
});