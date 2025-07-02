'use client';

import { useState } from 'react';
import Link from 'next/link';

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
            Year 7 Maths Through 
            <span className="text-primary">Discovery</span>
          </h1>
          <p className="text-xl text-muted mb-8 max-w-3xl mx-auto">
            An AI tutor that guides your child to discover solutions through thoughtful questions, 
            building confidence and mathematical thinking skills.
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
              Start Your Learning Journey
            </h3>
            <p className="text-muted mb-6">
              Upload homework and let our AI tutor guide your child through thoughtful questioning
            </p>
            <button className="bg-primary text-white px-8 py-3 rounded-lg font-medium hover:bg-primary-dark transition-colors shadow-lg">
              Choose File
            </button>
            <div className="mt-4 space-y-2">
              <div>
                <Link href="/start" className="text-primary hover:text-primary-light transition-colors text-sm underline font-medium">
                  → Start Learning Journey
                </Link>
              </div>
              <div>
                <Link href="/tutoring" className="text-muted hover:text-primary transition-colors text-xs underline">
                  Preview Tutoring Interface
                </Link>
              </div>
            </div>
            <p className="text-sm text-muted-light mt-4">
              Supports PDF, PNG, JPG • Max 10MB
            </p>
          </div>
        </div>

        {/* Features Grid */}
        <div id="features" className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">🧮</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Guided Discovery Learning</h3>
            <p className="text-muted">
              Through thoughtful questions, students discover solutions themselves, building deeper understanding.
            </p>
          </div>
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">📚</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Socratic Method Tutoring</h3>
            <p className="text-muted">
              Like a patient teacher, asks the right questions to help students think through problems.
            </p>
          </div>
          <div className="bg-surface p-6 rounded-xl shadow-lg border border-custom hover:bg-surface-hover transition-colors">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="text-lg font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Builds Confidence</h3>
            <p className="text-muted">
              Mistakes become learning opportunities. Every small discovery builds mathematical confidence.
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
              <p className="text-muted text-sm">Share your homework - the starting point for discovery</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">2️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Assess</h4>
              <p className="text-muted text-sm">AI understands the problem and your child&apos;s learning level</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">3️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Guide</h4>
              <p className="text-muted text-sm">Asks thoughtful questions that lead to &ldquo;aha!&rdquo; moments</p>
            </div>
            <div className="text-center">
              <div className="bg-surface-alt w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-custom">
                <span className="text-2xl">4️⃣</span>
              </div>
              <h4 className="font-semibold mb-2 text-foreground font-['Roboto_Condensed']">Discover</h4>
              <p className="text-muted text-sm">Students find solutions themselves, building lasting understanding</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-primary text-white rounded-2xl p-12 shadow-xl">
          <h2 className="text-3xl font-bold mb-4 font-['Roboto_Condensed']">Ready to Transform Homework Time?</h2>
          <p className="text-purple-100 mb-8 text-lg">
            Join parents who&apos;ve seen their children grow from frustrated to confident learners
          </p>
          <button className="bg-white text-primary px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors shadow-lg">
            Start Guided Learning
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
