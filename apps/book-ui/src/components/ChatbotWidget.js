import React, { useState } from 'react';

function ChatbotWidget() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('Ask me anything about Physical AI & Humanoid Robotics!');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer('Thinking...');

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (response.ok) {
        setAnswer(data.answer);
      } else {
        setAnswer(data.detail || 'Error: Could not get an answer.');
      }
    } catch (error) {
      console.error('Error fetching chatbot response:', error);
      setAnswer('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      border: '1px solid #ccc',
      padding: '15px',
      borderRadius: '8px',
      marginTop: '20px',
      maxWidth: '600px',
      margin: '20px auto',
      backgroundColor: '#f9f9f9'
    }}>
      <h3>Textbook Chatbot</h3>
      <p><strong>Answer:</strong> {answer}</p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          style={{
            width: '100%',
            padding: '8px',
            marginRight: '10px',
            boxSizing: 'border-box'
          }}
        />
        <button type="submit" disabled={loading} style={{
          marginTop: '10px',
          padding: '8px 15px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}>
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </form>
    </div>
  );
}

export default ChatbotWidget;
