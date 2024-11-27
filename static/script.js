// Função para adicionar mensagens ao chat
function addMessage(sender, text) {
    const chatMessages = document.getElementById("chatMessages");
    
    const message = document.createElement("div");
    message.classList.add("message", sender);
    
    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    messageContent.textContent = text;
    
    message.appendChild(messageContent);
    chatMessages.appendChild(message);
    
    // Rolagem automática para a última mensagem
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Função para recarregar os documentos no backend
function reloadDocuments() {
    fetch("/reload-documents", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Documentos recarregados com sucesso!");
        console.log("Recarregamento:", data);
    })
    .catch(error => {
        console.error("Erro ao recarregar documentos:", error);
        alert("Erro ao recarregar documentos.");
    });
}

// Permitir enviar mensagem ao pressionar Enter
const messageInput = document.getElementById("messageInput");
messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Adicionar indicador de digitação
function showTypingIndicator() {
    const chatMessages = document.getElementById("chatMessages");
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("message", "bot");
    typingIndicator.id = "typingIndicator";
    typingIndicator.innerHTML = `<div class="message-content">Digitando...</div>`;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remover indicador de digitação
function removeTypingIndicator() {
    const typingIndicator = document.getElementById("typingIndicator");
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Atualizar envio de mensagens
function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const messageText = messageInput.value.trim();

    if (messageText) {
        addMessage("user", messageText);
        messageInput.value = "";

        showTypingIndicator(); // Mostrar indicador de digitação

        fetch("/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: messageText })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator(); // Remover indicador ao receber a resposta
            addMessage("bot", data.answer || "Desculpe, não entendi.");
        })
        .catch(error => {
            removeTypingIndicator();
            console.error("Erro ao enviar a mensagem:", error);
            addMessage("bot", "Ocorreu um erro. Tente novamente mais tarde.");
        });
    }
}
