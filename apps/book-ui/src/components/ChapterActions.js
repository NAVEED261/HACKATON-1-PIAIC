import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000';

function ChapterActions({ chapterContent, onPersonalize }) {
  const {siteConfig} = useDocusaurusContext();

  const handlePersonalize = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Please sign in to personalize content.');
      return;
    }

    if (!chapterContent) {
      alert('No chapter content to personalize.');
      return;
    }

    try {
      // This is a simplified fetch. In a real app, you'd show loading states and handle errors more robustly.
      const response = await fetch(`${API_BASE_URL}/chapter/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ chapter_content: chapterContent }),
      });

      if (response.ok) {
        const data = await response.json();
        onPersonalize(data.personalized_content); // Callback to update parent component's content
        alert('Chapter personalized successfully!');
      } else {
        const errorData = await response.json();
        alert(`Personalization failed: ${errorData.detail || response.statusText}`);
      }
    } catch (error) {
      console.error('Error during personalization:', error);
      alert('An error occurred during personalization.');
    }
  };

  const handleTranslateToUrdu = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Please sign in to translate content.');
      return;
    }

    if (!chapterContent) {
      alert('No chapter content to translate.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/chapter/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ chapter_content: chapterContent }),
      });

      if (response.ok) {
        const data = await response.json();
        onPersonalize(data.translated_content); // Using onPersonalize to update chapter content
        alert('Chapter translated successfully!');
      } else {
        const errorData = await response.json();
        alert(`Translation failed: ${errorData.detail || response.statusText}`);
      }
    } catch (error) {
      console.error('Error during translation:', error);
      alert('An error occurred during translation.');
    }
  };

  return (
    <div style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
      <button onClick={handlePersonalize} style={{
        backgroundColor: '#28a745',
        color: 'white',
        padding: '10px 15px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        marginRight: '10px'
      }}>
        Personalize for Me
      </button>
      <button onClick={handleTranslateToUrdu} style={{
        backgroundColor: '#007bff',
        color: 'white',
        padding: '10px 15px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        marginRight: '10px'
      }}>
        Translate to Urdu
      </button>
    </div>
  );
}

export default ChapterActions;
