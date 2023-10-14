<!DOCTYPE html>
<html>
<head>
    <title>Text Messaging App</title>
</head>
<body>
    <div id="chat">
        <div id="message-list"></div>
        <input type="text" id="message-input" placeholder="Type a message">
        <button id="send-button">Send</button>
    </div>

    <script>
        const messageList = document.getElementById('message-list');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');

        // Replace with the appropriate API endpoint
        const apiEndpoint = 'http://your-api-endpoint.com';

        sendButton.addEventListener('click', () => {
            const message = messageInput.value;
            if (message) {
                sendMessage(message);
                messageInput.value = '';
            }
        });

        function sendMessage(message) {
            const sender = 'User1'; // Replace with the sender's username
            const recipient = 'User2'; // Replace with the recipient's username

            const data = {
                sender,
                recipient,
                message,
            };

            fetch(`${apiEndpoint}/send_message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                });
        }

        function getMessages(user) {
            fetch(`${apiEndpoint}/get_messages/${user}`)
                .then(response => response.json())
                .then(messages => {
                    messages.forEach(message => {
                        const messageItem = document.createElement('div');
                        messageItem.textContent = `${message.sender}: ${message.translated_message}`;
                        messageList.appendChild(messageItem);
                    });
                })
                .catch(error => {
                    console.error('Error fetching messages:', error);
                });
        }

        // Replace 'User2' with the recipient's username
        getMessages('User2');
    </script>
</body>
</html>
