async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    document.getElementById("user-input").value = ""; // Clear the input

    // Add user message to the chat log (before sending)
    const chatLog = document.getElementById("chat-log");
    const userDiv = document.createElement("div");
    userDiv.classList.add("message", "user-message");
    userDiv.textContent = userInput;
    chatLog.appendChild(userDiv);
    chatLog.scrollTop = chatLog.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const botResponse = data.response;

        // Add bot message to the chat log
        const botDiv = document.createElement("div");
        botDiv.classList.add("message", "bot-message");
        botDiv.textContent = botResponse;
        chatLog.appendChild(botDiv);
        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to bottom

    } catch (error) {
        console.error("Error sending message:", error);
        // Display an error message in the chat log
        const errorDiv = document.createElement("div");
        errorDiv.classList.add("message", "error-message");
        errorDiv.textContent = "Error: Could not get a response.";
        chatLog.appendChild(errorDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
}

// Add event listener for Enter key
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent default form submission behavior
        sendMessage();
    }
});