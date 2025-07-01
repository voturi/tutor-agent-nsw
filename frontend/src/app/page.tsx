'use client';

import { useState } from 'react';

export default function Home() {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    // TODO: Handle file upload
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-surface shadow-lg border-b border-custom">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-primary">🤖 TutorAgent</div>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#features" className="text-muted hover:text-primary transition-colors">Features</a>
              <a href="#how-it-works" className="text-muted hover:text-primary transition-colors">How it Works</a>
              <a href="#about" className="text-muted hover:text-primary transition-colors">About</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 font-['Roboto_Condensed']">
            Year 7 Maths Made 
            <span className="text-primary">Simple</span>
          </h1>
          <p className="text-xl text-muted mb-8 max-w-3xl mx-auto">
            Upload your homework, get instant AI-powered help with step-by-step explanations 
            aligned to the NSW Mathematics curriculum.
          </p>
        </div>

        {/* Upload Section */}
        <div className="max-w-2xl mx-auto mb-16">
          <div 
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 ${
              dragActive 
                ? 'border-primary bg-surface-alt' 
                : 'border-custom hover:border-primary bg-surface hover:bg-surface-alt'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="text-6xl mb-4">📄</div>
            <h3 className="text-lg font-semibold text-foreground mb-2 font-['Roboto_Condensed']">
              Upload Your Homework
            </h3>
            <p className="text-muted mb-6">
              Drag and drop your homework image or PDF, or click to browse
            </p>
            <button className="bg-primary text-white px-8 py-3 rounded-lg font-medium hover:bg-primary-dark transition-colors shadow-lg">
              Choose File
            </button>
            <p className="text-sm text-muted-light mt-4">
              Supports PDF, PNG, JPG • Max 10MB
            </p>
          </div>
        </div>

        {/* Features Grid */}
        <div id="features" className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">🧮</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Step-by-Step Solutions</h3>
            <p className="text-muted">
              Get detailed explanations for algebra, geometry, statistics, and more.
            </p>
          </div>
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">📚</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">NSW Curriculum Aligned</h3>
            <p className="text-muted">
              Content specifically designed for Year 7 NSW Mathematics syllabus.
            </p>
          </div>
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Instant Feedback</h3>
            <p className="text-muted">
              Get immediate help anytime, with explanations tailored to your level.
            </p>
          </div>
        </div>

        {/* How it Works */}
        <div id="how-it-works" className="bg-surface rounded-2xl p-8 mb-16 shadow-lg border border-custom">
          <h2 className="text-3xl font-bold text-center mb-12 text-secondary font-['Roboto_Condensed']">How TutorAgent Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">1️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Upload</h4>
              <p className="text-muted text-sm">Take a photo or upload your homework</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">2️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Analyze</h4>
              <p className="text-muted text-sm">AI reads and understands your questions</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">3️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Explain</h4>
              <p className="text-muted text-sm">Get step-by-step solutions and explanations</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">4️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Learn</h4>
              <p className="text-muted text-sm">Understand concepts and improve your skills</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-primary text-white rounded-2xl p-12 shadow-xl">
          <h2 className="text-3xl font-bold mb-4 font-['Roboto_Condensed']">Ready to Boost Your Maths Skills?</h2>
          <p className="text-purple-100 mb-8 text-lg">
            Join thousands of Year 7 students getting better grades with TutorAgent
          </p>
          <button className="bg-white text-primary px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors shadow-lg">
            Start Your First Question
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-surface-alt border-t border-custom mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-muted">
              © 2025 TutorAgent. Designed for NSW Year 7 Mathematics students.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
