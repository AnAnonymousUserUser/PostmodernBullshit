<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScholarGPT Interface</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }
        .chat-container {
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .message {
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }
        .message .user {
            font-weight: bold;
            margin-bottom: 2px;
        }
        .message .content {
            padding: 8px 12px;
            border-radius: 10px;
            display: inline-block;
        }
        .message.user-message .content {
            background-color: #1e88e5;
            color: #fff;
        }
        .message.ai-message .content {
            background-color: #f1f1f1;
            white-space: pre-wrap; /* Preserves line breaks and spaces in the text */
            /* Add other styling properties as needed */
        }
        .input-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            max-width: 600px;
            margin: auto;
        }
        .input-container input[type="text"] {
            flex-grow: 1;
            padding: 8px 12px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .input-container button {
            margin-left: 10px;
            padding: 8px 12px;
            background-color: #1e88e5;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .input-container button:hover {
            background-color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="message ai-message"></div>
        <!-- Add more messages here -->
    </div>
    <div class="input-container">
        <input type="text" id="userInput" class="form-control" placeholder="Type your message here...">
        <button class="btn btn-success" onclick="sendMessage()">Send</button>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/markdown-it/dist/markdown-it.min.js"></script>
    <script>
        let conversationHistory = "";
        const url = new URL(window.location.href);
        const engine = url.searchParams.get('engine');
        const md = new markdownit();
        
        async function sendMessage() {
            const userInput = document.getElementById("userInput");
            const message = userInput.value.trim();

            if (message === "") {
                return;
            }

            // Add user message to the chat
            addMessage("User", message, "user-message");

            // Clear input field
            userInput.value = "";

            // Call the Flask backend to get the AI response
            let AIResponse = await fetchAIResponse(message);
            
            console.log(AIResponse)
            // Add AI response to the chat
            // addMessage(`${engine}`, AIResponse, "ai-message");
            addMessage('AI', AIResponse, "ai-message");
        }
        
        async function fetchAIResponse(message) {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({message: message})
            });

            if (!response.ok) {
                return "An error occurred. Please try again.";
            }

            const jsonResponse = await response.json();
            return String(jsonResponse.response);
        }
        
        function addMessage(user, content, messageType) {
            conversationHistory += `${content}\n\n`;
            //conversationHistory += `${content}\n`;
            
            const chatContainer = document.querySelector(".chat-container");
            const message = document.createElement("div");
            message.classList.add("message");
            message.classList.add(messageType);

            const userElement = document.createElement("span");
            userElement.classList.add("user");
            userElement.textContent = `${user}:`;
            message.appendChild(userElement);

            const contentElement = document.createElement("span");
            //const content = md.render(content);
            contentElement.classList.add("content");
            contentElement.textContent = content;
            //contentElement.textContent = content;
            message.appendChild(contentElement);

            chatContainer.appendChild(message);
        }

        // Add event listener to trigger sendMessage when pressing Enter
        document.getElementById("userInput").addEventListener("keyup", function(event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
        
        addMessage('AI', '欢迎来到后现代答辩生成器，今天想来点答辩吗？', "ai-message");
    </script>
</body>
</html>
