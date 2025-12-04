import React from 'react';
import ChatbotWidget from '../components/ChatbotWidget';

// Docusaurus Root component wrapper
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
}