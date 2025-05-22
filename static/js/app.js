const toggleBtn = document.getElementById('theme-toggle');
const icon = toggleBtn.querySelector('i');

toggleBtn.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark-theme');

    // Toggle icon
    if (document.documentElement.classList.contains('dark-theme')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("message-form");
    const input = document.getElementById("user-input");
    const messagesArea = document.getElementById("messages-area");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const userMessage = input.value.trim();
        if (!userMessage) return;

        appendMessage("user", userMessage);
        input.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage("bot", data.reply || "Xin lỗi, không có phản hồi.");
        } catch (error) {
            appendMessage("bot", "Lỗi máy chủ. Vui lòng thử lại.");
        }
    });

    function appendMessage(sender, message) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender === "bot" ? "bot-message" : "user-message");

        msgDiv.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
                <span class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
        `;
        messagesArea.appendChild(msgDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
});
