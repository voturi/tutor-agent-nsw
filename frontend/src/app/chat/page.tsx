'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Upload, RefreshCw, Bot, User } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

interface ChatResponse {
  message: Message;
  session_id: string;
  assessment?: Record<string, unknown>;
  suggestions?: string[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Create new session on component mount
    createNewSession();
  }, []);

  const createNewSession = async () => {
    try {
      const response = await fetch('/api/v1/chat/session/new', {
        method: 'POST',
      });
      const data = await response.json();
      setSessionId(data.session_id);
      
      // Add welcome message
      const welcomeMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.message,
        timestamp: new Date().toISOString(),
      };
      setMessages([welcomeMessage]);
      
      // Set initial suggestions
      setSuggestions([
        "I need help with fractions",
        "Can you help me with algebra?",
        "I'm stuck on a geometry problem"
      ]);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          context: {
            timestamp: new Date().toISOString(),
          },
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data: ChatResponse = await response.json();
      setMessages(prev => [...prev, data.message]);
      setSessionId(data.session_id);
      setSuggestions(data.suggestions || []);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  const startNewSession = () => {
    setMessages([]);
    setSuggestions([]);
    setSessionId(null);
    createNewSession();
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <div className="w-80 bg-surface border-r border-custom flex flex-col">
        {/* Sidebar Header */}
        <div className="p-4 border-b border-custom">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-semibold text-foreground font-['Roboto_Condensed']">TutorAgent</h1>
              <p className="text-sm text-muted">Math Homework Helper</p>
            </div>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="p-4">
          <button
            onClick={startNewSession}
            className="w-full bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-dark transition-colors flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            New Chat
          </button>
        </div>

        {/* Session Info */}
        <div className="px-4 pb-4">
          <div className="text-xs text-muted">
            {sessionId ? `Session: ${sessionId.slice(0, 8)}...` : 'No active session'}
          </div>
        </div>

        {/* Conversation Summary (placeholder) */}
        <div className="flex-1 px-4">
          <div className="text-center text-muted py-8">
            <p className="text-sm">No conversations yet</p>
            <p className="text-xs mt-2">
              Ask about Year 7 math topics to start your learning journey
            </p>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-surface border-b border-custom p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-surface-alt rounded-full flex items-center justify-center border border-custom">
                <Bot className="w-6 h-6 text-muted" />
              </div>
              <div>
                <h2 className="font-semibold text-foreground font-['Roboto_Condensed']">
                  Math Tutor
                </h2>
                <p className="text-sm text-muted">Ready to help with Year 7 mathematics</p>
              </div>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 bg-surface-alt rounded-full flex items-center justify-center border border-custom flex-shrink-0">
                  <Bot className="w-5 h-5 text-muted" />
                </div>
              )}
              
              <div
                className={`max-w-2xl rounded-xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-primary text-white'
                    : 'bg-surface border border-custom text-foreground'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                {message.role === 'assistant' && (
                  <div className="text-xs text-muted mt-2">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                )}
              </div>

              {message.role === 'user' && (
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 bg-surface-alt rounded-full flex items-center justify-center border border-custom">
                <Bot className="w-5 h-5 text-muted" />
              </div>
              <div className="bg-surface border border-custom rounded-xl px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="px-4 pb-2">
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="text-sm bg-surface-alt hover:bg-surface-hover border border-custom rounded-lg px-3 py-2 text-muted hover:text-foreground transition-colors"
                  disabled={isLoading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t border-custom p-4">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask about your math homework..."
                className="w-full px-4 py-3 pr-12 bg-surface border border-custom rounded-xl text-foreground placeholder-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                disabled={isLoading}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted hover:text-foreground transition-colors"
              >
                <Upload className="w-5 h-5" />
              </button>
            </div>
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="bg-primary text-white px-4 py-3 rounded-xl hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <p className="text-xs text-muted mt-2 text-center">
            TutorAgent uses AI to help with Year 7 mathematics. Always verify important calculations.
          </p>
        </div>
      </div>
    </div>
  );
}
