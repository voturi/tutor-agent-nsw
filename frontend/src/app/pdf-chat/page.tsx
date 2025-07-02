'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Upload, RefreshCw, Bot, User, FileText, BookOpen } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  questionContext?: string;
}

interface UploadedDocument {
  id: string;
  name: string;
  size: number;
  uploadedAt: string;
  questionsExtracted: number;
  currentQuestion: number;
}

export default function PDFChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedDoc, setUploadedDoc] = useState<UploadedDocument | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  const simulateFileUpload = () => {
    setIsLoading(true);
    
    setTimeout(() => {
      const mockDoc: UploadedDocument = {
        id: Date.now().toString(),
        name: 'Year7_Maths_Homework_Week3.pdf',
        size: 245760,
        uploadedAt: new Date().toISOString(),
        questionsExtracted: 8,
        currentQuestion: 1
      };
      
      setUploadedDoc(mockDoc);
      
      const welcomeMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `Great! I've processed your homework and found ${mockDoc.questionsExtracted} questions. I can see you have problems covering integers, fractions, and some basic algebra.\n\nI'm here to guide you through each question step by step. I won't give you the answers directly - instead, I'll ask you questions to help you discover the solutions yourself. This way, you'll truly understand the concepts!\n\nReady to start with Question 1? What type of problem do you think it is when you look at it?`,
        timestamp: new Date().toISOString(),
        questionContext: 'Document uploaded - starting session'
      };
      
      setMessages([welcomeMessage]);
      setIsLoading(false);
    }, 2000);
  };

  const sendMessage = (message: string) => {
    if (!message.trim() || isLoading) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, newMessage]);
    setInputValue('');
    setIsLoading(true);
    
    setTimeout(() => {
      const responses = [
        "That's a good start! What do you think the first step should be?",
        "I can see you're thinking about this. Can you tell me what information the problem gives you?",
        "Interesting approach! What happens when you try that method?",
        "Great question! Let's break this down - what operation do you think we need here?",
        "You're on the right track! Can you explain your reasoning to me?"
      ];
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      const responseMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: randomResponse,
        timestamp: new Date().toISOString(),
        questionContext: uploadedDoc ? `Question ${uploadedDoc.currentQuestion}` : undefined
      };
      setMessages(prev => [...prev, responseMessage]);
      setIsLoading(false);
    }, 1000);
  };

  const startNewSession = () => {
    setMessages([]);
    setUploadedDoc(null);
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <div className="w-96 bg-surface border-r border-custom flex flex-col">
        {/* PDF Display Section */}
        <div className="flex-1 border-b border-custom">
          <div className="p-4 border-b border-custom">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Upload className="w-5 h-5 text-muted" />
                <span className="font-medium text-foreground">Document</span>
              </div>
              <div className="text-xs text-muted">PDF Viewer</div>
            </div>
          </div>
          
          <div className="h-80 p-4">
            {!uploadedDoc ? (
              <div className="h-full border-2 border-dashed border-custom rounded-lg flex flex-col items-center justify-center bg-surface-alt">
                <Upload className="w-12 h-12 text-muted mb-4" />
                <p className="text-sm font-medium text-foreground mb-2">Upload your Year 7 maths homework</p>
                <p className="text-xs text-muted text-center mb-4">
                  I'll help you work through each question step by step
                </p>
                <button 
                  onClick={simulateFileUpload}
                  disabled={isLoading}
                  className="bg-primary text-white px-4 py-2 rounded-lg text-sm hover:bg-primary-dark transition-colors disabled:opacity-50"
                >
                  {isLoading ? 'Processing...' : 'Choose Homework File'}
                </button>
                <p className="text-xs text-muted mt-2">Supports PDF files up to 10MB</p>
                <div className="mt-4 text-xs text-muted text-center">
                  <p className="font-medium mb-1">I can help with:</p>
                  <p>• Integers & directed numbers</p>
                  <p>• Fractions & decimals</p>
                  <p>• Basic algebra</p>
                  <p>• Geometry & word problems</p>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col">
                {/* Document Info */}
                <div className="bg-surface border border-custom rounded-lg p-3 mb-3">
                  <div className="flex items-start gap-3">
                    <FileText className="w-5 h-5 text-primary mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground truncate">{uploadedDoc.name}</p>
                      <p className="text-xs text-muted">
                        {Math.round(uploadedDoc.size / 1024)}KB • {uploadedDoc.questionsExtracted} questions found
                      </p>
                    </div>
                  </div>
                </div>
                
                {/* Progress Indicator */}
                <div className="bg-surface-alt border border-custom rounded-lg p-3 mb-3">
                  <div className="flex items-center gap-2 mb-2">
                    <BookOpen className="w-4 h-4 text-primary" />
                    <span className="text-sm font-medium text-foreground">Progress</span>
                  </div>
                  <div className="text-xs text-muted mb-2">
                    Question {uploadedDoc.currentQuestion} of {uploadedDoc.questionsExtracted}
                  </div>
                  <div className="w-full bg-background rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full transition-all duration-300"
                      style={{ width: `${(uploadedDoc.currentQuestion / uploadedDoc.questionsExtracted) * 100}%` }}
                    ></div>
                  </div>
                </div>
                
                {/* PDF Viewer Placeholder */}
                <div className="flex-1 bg-background border border-custom rounded-lg p-4 flex items-center justify-center">
                  <div className="text-center text-muted">
                    <FileText className="w-8 h-8 mx-auto mb-2" />
                    <p className="text-sm">PDF Viewer</p>
                    <p className="text-xs">Question highlighting coming soon</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Session Management Section */}
        <div className="h-64 flex flex-col">
          <div className="p-4 border-b border-custom">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="font-semibold text-foreground">TutorAgent</h1>
                <p className="text-sm text-muted">Math Homework Helper</p>
              </div>
            </div>
          </div>

          <div className="p-4">
            <button
              onClick={startNewSession}
              className="w-full bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-primary-dark transition-colors flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              New Session
            </button>
          </div>

          <div className="flex-1 px-4 pb-4">
            <div className="text-center text-muted">
              <p className="text-xs">
                {uploadedDoc ? 'Session active' : 'Upload homework to begin'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="bg-surface border-b border-custom p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-surface-alt rounded-full flex items-center justify-center border border-custom">
                <Bot className="w-6 h-6 text-muted" />
              </div>
              <div>
                <h2 className="font-semibold text-foreground">Year 7 Math Tutor</h2>
                <p className="text-sm text-muted">Ready to guide you through your homework</p>
              </div>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && !uploadedDoc && (
            <div className="text-center text-muted py-8">
              <Bot className="w-16 h-16 mx-auto mb-4 text-muted" />
              <h3 className="text-lg font-medium text-foreground mb-2">Welcome to TutorAgent!</h3>
              <p className="text-sm">Upload your Year 7 maths homework and I'll guide you through each question using the Socratic method.</p>
              <p className="text-xs mt-2">I'll help you discover the answers yourself by asking the right questions!</p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 bg-surface-alt rounded-full flex items-center justify-center border border-custom">
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
                    {message.questionContext && ` • ${message.questionContext}`}
                  </div>
                )}
              </div>

              {message.role === 'user' && (
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
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
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="border-t border-custom p-4">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={uploadedDoc ? "Tell me what you think about this problem..." : "Upload your homework first..."}
                className="w-full px-4 py-3 pr-12 bg-surface border border-custom rounded-xl text-foreground placeholder-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                disabled={isLoading || !uploadedDoc}
              />
            </div>
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading || !uploadedDoc}
              className="bg-primary text-white px-4 py-3 rounded-xl hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <p className="text-xs text-muted mt-2 text-center">
            TutorAgent guides you through problems using questions - no direct answers given!
          </p>
        </div>
      </div>
    </div>
  );
}
