'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Upload, RefreshCw, Bot, User, FileText, BookOpen, ToggleLeft, ToggleRight } from 'lucide-react';
import PDFViewer from '../../components/PDFViewer';
import SimplePDFViewer from '../../components/SimplePDFViewer';

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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'initial-greeting',
      role: 'assistant',
      content: 'Hi!',
      timestamp: new Date().toISOString(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedDoc, setUploadedDoc] = useState<UploadedDocument | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [useSimplePDFViewer, setUseSimplePDFViewer] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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

  // File validation
  const validateFile = (file: File): string | null => {
    if (file.type !== 'application/pdf') {
      return 'Please upload a PDF file only.';
    }
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      return 'File size must be less than 10MB.';
    }
    return null;
  };

  // Handle file upload
  const handleFileUpload = async (file: File) => {
    const error = validateFile(file);
    if (error) {
      alert(error);
      return;
    }

    setIsLoading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + 10;
      });
    }, 200);

    try {
      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', file);

      // Upload to backend API
      const response = await fetch('http://localhost:8000/api/v1/pdf-chat/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const uploadResult = await response.json();
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      // Process the upload result
      setTimeout(() => {
        const processedDoc: UploadedDocument = {
          id: uploadResult.document_id,
          name: uploadResult.filename,
          size: uploadResult.file_size,
          uploadedAt: new Date().toISOString(),
          questionsExtracted: uploadResult.questions_extracted,
          currentQuestion: 1
        };
        
        setUploadedDoc(processedDoc);
        setUploadedFile(file);
        setSessionId(uploadResult.session_id);
        
        // Replace initial greeting with welcome message from session history
        fetchSessionHistory(uploadResult.session_id);
        
        setIsLoading(false);
        setUploadProgress(0);
      }, 1000);

    } catch (error) {
      console.error('Upload failed:', error);
      clearInterval(progressInterval);
      setIsLoading(false);
      setUploadProgress(0);
      alert('Upload failed. Please try again.');
    }
  };

  // Drag and drop handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  // File input handler
  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  // Click to upload
  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  // Fetch session history
  const fetchSessionHistory = async (sessionId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/pdf-chat/session/${sessionId}/history`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      }
    } catch (error) {
      console.error('Failed to fetch session history:', error);
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim() || isLoading || !sessionId) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, newMessage]);
    setInputValue('');
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/pdf-chat/send', {
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

      const data = await response.json();
      
      const responseMessage: Message = {
        id: data.message.id,
        role: 'assistant',
        content: data.message.content,
        timestamp: data.message.timestamp,
        questionContext: data.message.question_context
      };
      
      setMessages(prev => [...prev, responseMessage]);
      setIsLoading(false);
      
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    }
  };

  const startNewSession = () => {
    setMessages([
      {
        id: 'initial-greeting',
        role: 'assistant',
        content: 'Hi!',
        timestamp: new Date().toISOString(),
      }
    ]);
    setUploadedDoc(null);
    setUploadedFile(null);
    setSessionId(null);
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <div className="w-96 bg-surface border-r border-custom flex flex-col">
        {/* Session Management Section */}
        <div className="border-b border-custom flex flex-col">
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

          <div className="px-4 pb-4">
            <div className="text-center text-muted">
              <p className="text-xs">
                {uploadedDoc ? 'Session active' : 'Upload homework to begin'}
              </p>
            </div>
          </div>
        </div>

        {/* PDF Display Section */}
        <div className="flex-1 border-b border-custom flex flex-col min-h-0">
          <div className="p-4 border-b border-custom">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Upload className="w-5 h-5 text-muted" />
                <span className="font-medium text-foreground">Document</span>
              </div>
              
              {uploadedDoc && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted">Simple</span>
                  <button
                    onClick={() => setUseSimplePDFViewer(!useSimplePDFViewer)}
                    className="p-1 rounded hover:bg-background"
                    title={`Switch to ${useSimplePDFViewer ? 'Advanced' : 'Simple'} PDF Viewer`}
                  >
                    {useSimplePDFViewer ? (
                      <ToggleRight className="w-5 h-5 text-primary" />
                    ) : (
                      <ToggleLeft className="w-5 h-5 text-muted" />
                    )}
                  </button>
                  <span className="text-xs text-muted">Advanced</span>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex-1 p-4 min-h-0">
            {!uploadedDoc ? (
              <div 
                className={`h-full border-2 border-dashed rounded-lg flex flex-col items-center justify-center transition-colors ${
                  dragActive 
                    ? 'border-primary bg-primary/5' 
                    : 'border-custom bg-surface-alt'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInputChange}
                  className="hidden"
                />
                
                {isLoading ? (
                  <div className="text-center">
                    <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-sm font-medium text-foreground mb-2">Processing your homework...</p>
                    {uploadProgress > 0 && (
                      <div className="w-48 mx-auto">
                        <div className="flex justify-between text-xs text-muted mb-1">
                          <span>Upload Progress</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <div className="w-full bg-background rounded-full h-2">
                          <div 
                            className="bg-primary h-2 rounded-full transition-all duration-300"
                            style={{ width: `${uploadProgress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <>
                    <Upload className={`w-12 h-12 mb-4 ${
                      dragActive ? 'text-primary' : 'text-muted'
                    }`} />
                    <p className="text-sm font-medium text-foreground mb-2">
                      {dragActive ? 'Drop your homework here!' : 'Upload your Year 7 maths homework'}
                    </p>
                    <p className="text-xs text-muted text-center mb-4">
                      I&apos;ll help you work through each question step by step
                    </p>
                    <button 
                      onClick={triggerFileInput}
                      className="bg-primary text-white px-4 py-2 rounded-lg text-sm hover:bg-primary-dark transition-colors"
                    >
                      Choose Homework File
                    </button>
                    <p className="text-xs text-muted mt-2">Drag & drop or click to browse • PDF files up to 10MB</p>
                    <div className="mt-4 text-xs text-muted text-center">
                      <p className="font-medium mb-1">I can help with:</p>
                      <p>• Integers & directed numbers</p>
                      <p>• Fractions & decimals</p>
                      <p>• Basic algebra</p>
                      <p>• Geometry & word problems</p>
                    </div>
                  </>
                )}
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
                
                {/* PDF Viewer */}
                <div className="flex-1">
                  {useSimplePDFViewer ? (
                    <SimplePDFViewer 
                      key={`simple-${uploadedFile?.name}-${uploadedFile?.size}`} 
                      file={uploadedFile} 
                      className="w-full h-full" 
                    />
                  ) : (
                    <PDFViewer 
                      key={`advanced-${uploadedFile?.name}-${uploadedFile?.size}`} 
                      file={uploadedFile} 
                      className="w-full h-full" 
                    />
                  )}
                </div>
              </div>
            )}
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
              <p className="text-sm">Upload your Year 7 maths homework and I&apos;ll guide you through each question using the Socratic method.</p>
              <p className="text-xs mt-2">I&apos;ll help you discover the answers yourself by asking the right questions!</p>
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
