# TutorAgent MVP Design - Year 7 Maths Homework Tutor

## MVP Overview

**Target Use Case**: Year 7 students upload homework documents and receive personalized, step-by-step tutoring for each math question using the Socratic method.

**Core Value Proposition**: Transform homework from a struggle into a guided learning experience where students discover solutions through AI-powered questioning rather than being given direct answers.

---

## User Journey

### Primary Flow
1. **Upload**: Student uploads homework document (PDF/image) from Year 7 maths chapter
2. **Parse**: System extracts and identifies individual questions
3. **Queue**: Questions are presented one by one for tutoring
4. **Tutor**: For each question, AI provides guided assistance using Socratic method
5. **Progress**: Student works through all questions with personalized support
6. **Summary**: Brief recap of concepts learned and areas for improvement

### Example Session Flow
```
Student uploads "Chapter 5: Integers and Fractions - Homework.pdf"
↓
System identifies: Q1, Q2, Q3, Q4, Q5
↓
"Let's start with Question 1: Calculate -7 + 12 - 8"
↓
Tutor: "What do you notice about these numbers? Are they all positive?"
↓
Student: "No, some are negative"
↓
Tutor: "Great observation! When we see negative numbers, what's a good first step?"
... (guided problem solving continues)
```

---

## Technical Architecture

### Simplified 3-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                Document Upload Interface                    │
│                    (Web/Mobile App)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ Upload PDF/Image
┌─────────────────────▼───────────────────────────────────────┐
│               Session Manager                               │
│    • Question queue management                              │
│    • Student state tracking                                 │
│    • Session context maintenance                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Document   │ │ Assessment  │ │   Tutor     │
│  Parser     │ │   Agent     │ │   Agent     │
│   Agent     │ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Agent Specifications

#### 1. Document Parser Agent
**Responsibilities:**
- Extract text from uploaded PDF/image files
- Identify and separate individual questions
- Parse mathematical expressions and notation
- Classify question types (algebra, geometry, word problems, etc.)
- Estimate difficulty level per question

**Technology Stack:**
- OCR: PaddleOCR or Tesseract for text extraction
- Math parsing: SymPy for mathematical expression handling
- PDF processing: PyPDF2 or pdfplumber
- Image processing: OpenCV for image preprocessing

**Input/Output:**
- Input: PDF/Image file
- Output: Structured question list with metadata

#### 2. Assessment Agent
**Responsibilities:**
- Conduct initial skill assessment based on first question attempt
- Continuously adapt to student responses throughout session
- Identify knowledge gaps and misconceptions
- Adjust tutoring approach based on student performance

**Key Features:**
- Quick 2-3 question diagnostic for skill level
- Real-time confidence and understanding assessment
- Adaptive difficulty adjustment
- Learning style detection (visual, verbal, kinesthetic cues)

**Technology Stack:**
- NLP: spaCy or NLTK for response analysis
- ML: Simple classification models for skill assessment
- Pattern recognition: Custom rules for common misconceptions

#### 3. Tutor Agent
**Responsibilities:**
- Guide students through problem-solving using Socratic method
- Provide appropriate hints without giving direct answers
- Adapt communication style to Year 7 level (ages 12-13)
- Maintain encouraging and patient tone throughout

**Core Capabilities:**
- Generate probing questions that guide discovery
- Provide graduated hints when students are stuck
- Explain concepts using age-appropriate analogies
- Celebrate progress and reframe mistakes as learning opportunities

**Technology Stack:**
- LLM: OpenAI GPT-4 or Claude for natural conversation
- Prompt engineering: Specialized prompts for Socratic questioning
- Context management: Maintain conversation history and student state

---

## Year 7 Maths Curriculum Scope

### Primary Topics for MVP
1. **Integers and Directed Numbers**
   - Addition and subtraction with negative numbers
   - Multiplication and division of integers
   - Order of operations with integers

2. **Fractions and Decimals**
   - Adding and subtracting fractions with different denominators
   - Multiplying and dividing fractions
   - Converting between fractions, decimals, and percentages

3. **Basic Algebra**
   - Simple linear equations (one variable)
   - Substitution into formulas
   - Basic algebraic manipulation

4. **Geometry Basics**
   - Area and perimeter calculations
   - Angle properties (parallel lines, triangles)
   - Basic coordinate geometry

5. **Word Problems**
   - Multi-step problems involving above topics
   - Real-world applications

### Difficulty Progression
- **Beginner**: Single-step problems, clear patterns
- **Intermediate**: Two-step problems, some complexity
- **Advanced**: Multi-step problems, problem-solving strategies

---

## Student Assessment Framework

### Initial Assessment (2-3 questions)
**Purpose**: Quickly gauge student's current skill level and confidence

**Sample Diagnostic Questions:**
1. "Calculate: 15 - (-8) + 3"
2. "Solve for x: 2x + 5 = 13"
3. "A rectangle has length 8cm and width 5cm. What is its area?"

### Continuous Assessment Indicators

#### Skill Level Markers
**Beginner Indicators:**
- Struggles to identify problem type
- Makes basic computational errors
- Needs guidance on where to start
- Shows uncertainty with mathematical language

**Intermediate Indicators:**
- Recognizes problem patterns
- Can perform basic operations but struggles with multi-step problems
- Shows some mathematical reasoning
- Makes procedural errors but understands concepts

**Advanced Indicators:**
- Quickly identifies solution approach
- Shows mathematical reasoning and pattern recognition
- Can explain their thinking clearly
- Attempts alternative solution methods

#### Response Quality Analysis
**Confident & Correct**: Increase difficulty, ask extension questions
**Confident & Incorrect**: Gentle questioning to reveal misconception
**Hesitant & Correct**: Build confidence, explain why they're right
**Hesitant & Incorrect**: Break down further, provide more support
**No Response**: Simplify question, provide example, check understanding

---

## Socratic Teaching Method Implementation

### Core Principles
1. **Guide, Don't Tell**: Ask questions that lead students to discover answers
2. **Build on Prior Knowledge**: Connect new concepts to what students already know
3. **Embrace Mistakes**: Use errors as learning opportunities
4. **Encourage Reasoning**: Ask "why" and "how" questions

### Question Types and Examples

#### Diagnostic Questions
- "What do you notice about this problem?"
- "What information are we given?"
- "What are we trying to find?"

#### Guiding Questions
- "What would happen if we...?"
- "Can you think of a similar problem we've solved?"
- "What's the first step we should take?"

#### Probing Questions
- "Why do you think that's the answer?"
- "How did you arrive at that solution?"
- "Is there another way to approach this?"

#### Confidence Building Questions
- "What part of this problem feels familiar?"
- "What strategies have worked for you before?"
- "What makes you think that's correct?"

### Adaptive Responses

#### When Student is Stuck
1. **Simplify**: Break the problem into smaller parts
2. **Relate**: Connect to familiar concepts or examples
3. **Hint**: Provide gentle nudges without giving away the answer
4. **Encourage**: Maintain positive, supportive tone

#### When Student Makes Errors
1. **Acknowledge**: Recognize the effort and thinking process
2. **Explore**: Ask questions to understand the misconception
3. **Guide**: Lead them to discover the error themselves
4. **Practice**: Provide similar problems to reinforce correct understanding

---

## Success Metrics for MVP

### Primary Metrics
1. **Engagement**: Average session duration and completion rate
2. **Learning Progress**: Improvement in accuracy from first to last question
3. **Student Satisfaction**: Post-session feedback on helpfulness and confidence
4. **Question Quality**: Ability to successfully parse and present homework questions

### Secondary Metrics
1. **Response Time**: System speed in processing documents and generating responses
2. **Error Rate**: Accuracy of OCR and question parsing
3. **Adaptation Effectiveness**: How well the system adjusts to student skill level
4. **Retention**: Students returning to use the system again

### Validation Criteria
- ✅ System can accurately extract 90%+ of questions from typical Year 7 homework
- ✅ Students show measurable improvement within a single session
- ✅ 80%+ of students find the tutoring helpful and encouraging
- ✅ Average session completion rate above 70%

---

## Implementation Phases

### Phase 1: Core Functionality (Weeks 1-4)
- [ ] Basic document upload and text extraction
- [ ] Simple question parsing and separation
- [ ] Basic tutor agent with Socratic questioning
- [ ] Minimal web interface for testing

### Phase 2: Assessment Integration (Weeks 5-6)
- [ ] Initial skill assessment implementation
- [ ] Adaptive response system based on student performance
- [ ] Improved question classification and difficulty estimation

### Phase 3: Polish and Testing (Weeks 7-8)
- [ ] Enhanced OCR for mathematical notation
- [ ] Improved user interface and experience
- [ ] Testing with real Year 7 students and homework
- [ ] Performance optimization and bug fixes

---

## Technical Considerations

### Data Flow
```
Document Upload → OCR Processing → Question Extraction → Question Queue
                                                            ↓
Student Response ← Tutor Agent ← Assessment Agent ← Current Question
        ↓                                              ↓
Progress Update → Session State → Next Question Selection
```

### Key Challenges
1. **Mathematical Notation**: Handling complex mathematical expressions in OCR
2. **Question Boundaries**: Accurately identifying where one question ends and another begins
3. **Context Maintenance**: Keeping track of student progress and adapting appropriately
4. **Response Quality**: Ensuring Socratic questions are helpful and age-appropriate

### Technology Stack Summary
- **Frontend**: React.js or Vue.js for web interface
- **Backend**: Python with FastAPI for API services
- **OCR**: PaddleOCR or Tesseract for text extraction
- **LLM**: OpenAI GPT-4 or Claude for conversational AI
- **Database**: PostgreSQL for session data, Redis for caching
- **Deployment**: Docker containers on cloud platform (AWS/GCP)

---

## Next Steps

### Immediate Actions
1. **Gather Sample Data**: Collect typical Year 7 homework documents for testing
2. **Define API Contracts**: Specify interfaces between agents
3. **Set Up Development Environment**: Configure tools and frameworks
4. **Create Proof of Concept**: Build minimal working version of document parsing

### Research Needs
1. **Year 7 Curriculum Standards**: Detailed analysis of typical homework formats
2. **Socratic Method Examples**: Collect examples of effective math tutoring dialogues
3. **Technical Evaluation**: Compare OCR solutions for mathematical content
4. **User Experience**: Design intuitive interface for homework upload and tutoring

### Success Validation
- [ ] Technical proof of concept working end-to-end
- [ ] Positive feedback from initial user testing
- [ ] Measurable learning outcomes in pilot sessions
- [ ] Scalable architecture foundation for future enhancements

---

**Document Status**: Initial MVP Design  
**Last Updated**: July 1, 2025  
**Next Review**: Weekly during development phases
