import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';
import { UserProvider } from './context/UserContext';
import { ChatProvider } from './context/ChatContext';
import { WebSocketProvider } from './context/WebSocketContext';
import reportWebVitals from './reportWebVitals';

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <BrowserRouter>
    <UserProvider>
      <ChatProvider>
        <WebSocketProvider>
          <App />
        </WebSocketProvider>
      </ChatProvider>
    </UserProvider>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
