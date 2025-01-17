document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput) {
        fetch('/send_input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addFeedback(userInput);
                document.getElementById('user-input').value = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

function addFeedback(input) {
    const feedbackList = document.getElementById('feedback-list');
    const feedbackItem = document.createElement('li');
    feedbackItem.textContent = `You typed: "${input}"`;
    feedbackList.appendChild(feedbackItem);
}
