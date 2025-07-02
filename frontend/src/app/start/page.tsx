'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function StartPage() {
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

  const curriculumTopics = [
    { name: "Integers & Directed Numbers", icon: "🔢", exercises: 12 },
    { name: "Fractions & Decimals", icon: "➗", exercises: 15 },
    { name: "Basic Algebra", icon: "📐", exercises: 18 },
    { name: "Geometry Basics", icon: "📏", exercises: 14 },
    { name: "Word Problems", icon: "📝", exercises: 20 }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-surface shadow-lg border-b border-custom">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold text-primary">🤖 TutorAgent</Link>
            </div>
            <nav className="hidden md:flex space-x-8">
              <Link href="/" className="text-muted hover:text-primary transition-colors">Home</Link>
              <Link href="/tutoring" className="text-muted hover:text-primary transition-colors">Demo</Link>
              <a href="#about" className="text-muted hover:text-primary transition-colors">About</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-6 font-['Roboto_Condensed']">
            Choose Your Learning Path
          </h1>
          <p className="text-xl text-muted max-w-2xl mx-auto">
            Ready to tackle mathematics? Pick the option that works best for you right now.
          </p>
        </div>

        {/* Choice Cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Upload Homework Card */}
          <div className="bg-surface rounded-2xl p-8 shadow-lg border border-custom hover:shadow-xl transition-all duration-300 hover:scale-105">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">📄</div>
              <h2 className="text-2xl font-bold text-foreground mb-4 font-['Roboto_Condensed']">
                Upload Homework
              </h2>
              <p className="text-muted leading-relaxed mb-6">
                Got homework that needs help? Upload your document and get guided step-by-step assistance 
                through each problem using our AI tutor&apos;s thoughtful questioning approach.
              </p>
            </div>

            {/* Upload Area */}
            <div 
              className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 mb-6 ${ 
                dragActive 
                  ? 'border-primary bg-surface-alt' 
                  : 'border-custom hover:border-primary bg-surface-alt hover:bg-surface-hover'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="text-3xl mb-3">📤</div>
              <p className="text-sm text-muted mb-3">
                Drag & drop your homework here
              </p>
              <p className="text-xs text-muted-light">
                Supports PDF, PNG, JPG • Max 10MB
              </p>
            </div>

            <button className="w-full bg-primary hover:bg-primary-dark text-white py-3 px-6 rounded-lg font-medium transition-colors shadow-lg">
              Upload Document
            </button>

            <div className="mt-4 text-center">
              <p className="text-xs text-muted">
                ✨ Perfect for: Specific homework questions, assignments, practice sheets
              </p>
            </div>
          </div>

          {/* Practice Topics Card */}
          <div className="bg-surface rounded-2xl p-8 shadow-lg border border-custom hover:shadow-xl transition-all duration-300 hover:scale-105">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">📚</div>
              <h2 className="text-2xl font-bold text-foreground mb-4 font-['Roboto_Condensed']">
                Practice Topics
              </h2>
              <p className="text-muted leading-relaxed mb-6">
                Want to practice specific topics? Choose from our Year 7 curriculum-aligned exercises 
                and build your mathematical confidence step by step.
              </p>
            </div>

            {/* Topics List */}
            <div className="space-y-3 mb-6">
              {curriculumTopics.map((topic, index) => (
                <div 
                  key={index}
                  className="flex items-center justify-between p-3 bg-surface-alt rounded-lg border border-custom hover:bg-surface-hover transition-colors cursor-pointer"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{topic.icon}</span>
                    <span className="text-sm font-medium text-foreground">{topic.name}</span>
                  </div>
                  <span className="text-xs text-muted bg-surface px-2 py-1 rounded">
                    {topic.exercises} exercises
                  </span>
                </div>
              ))}
            </div>

            <button className="w-full bg-secondary hover:bg-secondary/90 text-white py-3 px-6 rounded-lg font-medium transition-colors shadow-lg">
              Browse All Topics
            </button>

            <div className="mt-4 text-center">
              <p className="text-xs text-muted">
                ✨ Perfect for: Skill building, exam prep, concept reinforcement
              </p>
            </div>
          </div>
        </div>

        {/* Additional Information */}
        <div className="mt-16 text-center">
          <div className="bg-surface-alt rounded-xl p-6 max-w-3xl mx-auto border border-custom">
            <h3 className="text-lg font-semibold text-foreground mb-3 font-['Roboto_Condensed']">
              🎯 How Our AI Tutor Helps
            </h3>
            <div className="grid md:grid-cols-3 gap-4 text-sm text-muted">
              <div>
                <span className="font-medium text-primary">Socratic Method:</span>
                <br />Guides you to discover answers through thoughtful questions
              </div>
              <div>
                <span className="font-medium text-secondary">Adaptive Learning:</span>
                <br />Adjusts difficulty based on your understanding level
              </div>
              <div>
                <span className="font-medium text-accent">Confidence Building:</span>
                <br />Celebrates progress and turns mistakes into learning opportunities
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Hint */}
        <div className="mt-8 text-center">
          <p className="text-sm text-muted">
            Not sure which option to choose? 
            <Link href="/tutoring" className="text-primary hover:text-primary-light transition-colors ml-1 underline">
              Preview the tutoring experience →
            </Link>
          </p>
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
