'use client';

import { useState } from 'react';

export default function TutoringPage() {
  const [sessionTime, setSessionTime] = useState(0);
  const [currentProgress, setCurrentProgress] = useState(3); // Current question number
  const [totalQuestions] = useState(8); // Total questions in homework

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="bg-surface border-b border-custom p-4 flex-shrink-0">
        <div className="max-w-full mx-auto flex items-center justify-between">
          {/* Progress Section */}
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-3">
              <span className="text-sm text-muted font-medium">Progress:</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 h-2 bg-surface-alt rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary transition-all duration-300"
                    style={{ width: `${(currentProgress / totalQuestions) * 100}%` }}
                  />
                </div>
                <span className="text-sm text-foreground font-medium">
                  {currentProgress}/{totalQuestions}
                </span>
              </div>
            </div>
            
            {/* Session Timer */}
            <div className="flex items-center space-x-2">
              <span className="text-sm text-muted">Time:</span>
              <span className="text-sm text-foreground font-mono">
                {Math.floor(sessionTime / 60)}:{(sessionTime % 60).toString().padStart(2, '0')}
              </span>
            </div>
          </div>

          {/* Exit Button */}
          <button className="bg-surface-alt hover:bg-surface-hover text-muted hover:text-foreground px-4 py-2 rounded-lg border border-custom transition-colors">
            Exit Session
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 flex overflow-hidden">
        {/* Left Panel - Problem Area (40%) */}
        <div className="w-2/5 bg-surface border-r border-custom flex flex-col">
          {/* Current Problem Section */}
          <div className="flex-1 p-6 overflow-auto">
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-foreground mb-4 font-['Roboto_Condensed']">
                Question {currentProgress}
              </h2>
              
              {/* Problem Content */}
              <div className="bg-surface-alt p-4 rounded-lg border border-custom mb-4">
                <p className="text-foreground leading-relaxed">
                  A rectangle has a length that is 3 cm more than twice its width. 
                  If the perimeter of the rectangle is 42 cm, find the length and width of the rectangle.
                </p>
                
                {/* Visual Elements Placeholder */}
                <div className="mt-4 p-3 bg-surface-hover rounded border border-custom">
                  <div className="text-sm text-muted text-center">
                    📐 Visual diagram will appear here
                  </div>
                </div>
              </div>

              {/* Highlight Areas */}
              <div className="space-y-2">
                <div className="text-sm text-muted">Key Information:</div>
                <div className="space-y-1">
                  <div className="text-sm bg-primary/20 text-primary px-2 py-1 rounded inline-block">
                    Length = 2 × width + 3
                  </div>
                  <div className="text-sm bg-secondary/20 text-secondary px-2 py-1 rounded inline-block ml-2">
                    Perimeter = 42 cm
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Tools Section */}
          <div className="p-4 border-t border-custom bg-surface-alt">
            <h3 className="text-sm font-semibold text-foreground mb-3 font-['Roboto_Condensed']">
              Tools
            </h3>
            <div className="grid grid-cols-3 gap-2">
              <button className="p-3 bg-surface hover:bg-surface-hover border border-custom rounded-lg text-center transition-colors">
                <div className="text-lg mb-1">📝</div>
                <div className="text-xs text-muted">Scratchpad</div>
              </button>
              <button className="p-3 bg-surface hover:bg-surface-hover border border-custom rounded-lg text-center transition-colors">
                <div className="text-lg mb-1">🧮</div>
                <div className="text-xs text-muted">Calculator</div>
              </button>
              <button className="p-3 bg-surface hover:bg-surface-hover border border-custom rounded-lg text-center transition-colors">
                <div className="text-lg mb-1">✏️</div>
                <div className="text-xs text-muted">Draw</div>
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel - Chat & Hints (60%) */}
        <div className="w-3/5 flex flex-col">
          {/* Chat Interface */}
          <div className="flex-1 flex flex-col">
            {/* Chat Messages */}
            <div className="flex-1 p-4 overflow-auto bg-background">
              <div className="space-y-4 max-w-none">
                {/* AI Message */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-white text-sm">🤖</span>
                  </div>
                  <div className="flex-1">
                    <div className="bg-surface p-3 rounded-lg border border-custom">
                      <p className="text-foreground text-sm">
                        Great! Let's work through this step by step. What do you think is the first thing we need to do when we see a word problem like this?
                      </p>
                    </div>
                    <div className="text-xs text-muted mt-1">2 minutes ago</div>
                  </div>
                </div>

                {/* Student Message */}
                <div className="flex items-start space-x-3 justify-end">
                  <div className="flex-1 text-right">
                    <div className="bg-primary p-3 rounded-lg inline-block max-w-xs">
                      <p className="text-white text-sm">
                        Maybe identify what we're looking for?
                      </p>
                    </div>
                    <div className="text-xs text-muted mt-1">1 minute ago</div>
                  </div>
                  <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-white text-sm">👤</span>
                  </div>
                </div>

                {/* AI Response */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                    <span className="text-white text-sm">🤖</span>
                  </div>
                  <div className="flex-1">
                    <div className="bg-surface p-3 rounded-lg border border-custom">
                      <p className="text-foreground text-sm">
                        Excellent thinking! 🎯 Yes, identifying what we're looking for is always a great first step. What exactly are we trying to find in this problem?
                      </p>
                    </div>
                    <div className="text-xs text-muted mt-1">Just now</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Chat Input */}
            <div className="p-4 border-t border-custom bg-surface">
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Type your response..."
                  className="flex-1 p-3 bg-background border border-custom rounded-lg text-foreground placeholder-muted focus:outline-none focus:border-primary"
                />
                <button className="bg-primary hover:bg-primary-dark text-white px-4 py-3 rounded-lg transition-colors">
                  Send
                </button>
              </div>
              
              {/* Quick Actions */}
              <div className="flex space-x-2 mt-3">
                <button className="text-xs bg-surface-alt hover:bg-surface-hover text-muted hover:text-foreground px-3 py-1 rounded border border-custom transition-colors">
                  I need help
                </button>
                <button className="text-xs bg-surface-alt hover:bg-surface-hover text-muted hover:text-foreground px-3 py-1 rounded border border-custom transition-colors">
                  I understand
                </button>
                <button className="text-xs bg-surface-alt hover:bg-surface-hover text-muted hover:text-foreground px-3 py-1 rounded border border-custom transition-colors">
                  Can you repeat?
                </button>
              </div>
            </div>
          </div>

          {/* Adaptive Hints Panel */}
          <div className="p-4 bg-surface-alt border-t border-custom">
            <h3 className="text-sm font-semibold text-foreground mb-3 font-['Roboto_Condensed']">
              💡 Helpful Tips
            </h3>
            <div className="space-y-2">
              <div className="text-xs bg-surface p-2 rounded border border-custom">
                <span className="text-primary font-medium">Remember:</span>
                <span className="text-muted ml-1">Perimeter = 2(length + width)</span>
              </div>
              <div className="text-xs bg-surface p-2 rounded border border-custom">
                <span className="text-secondary font-medium">Progress:</span>
                <span className="text-muted ml-1">You're doing great! Take your time to think it through.</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Bottom Bar */}
      <footer className="bg-surface border-t border-custom p-4 flex-shrink-0">
        <div className="max-w-full mx-auto flex items-center justify-between">
          <button className="bg-secondary hover:bg-secondary/80 text-white px-4 py-2 rounded-lg transition-colors">
            💡 Get Hint
          </button>
          
          <div className="flex space-x-3">
            <button className="bg-surface-alt hover:bg-surface-hover text-muted hover:text-foreground px-4 py-2 rounded-lg border border-custom transition-colors">
              ⏸️ Take Break
            </button>
            <button className="bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg transition-colors">
              Next Question →
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
