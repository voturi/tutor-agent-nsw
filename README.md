# TutorAgent - AI Mathematics Tutor

## Overview
An AI tutor agent designed to provide personalized, step-by-step guidance for Year 7 mathematics homework exercises. Students upload their homework documents, and the AI guides them through each question using the Socratic method, fostering critical thinking and building mathematical intuition.

## MVP Focus: Year 7 Maths Homework Helper

### Target Use Case
- **Primary**: Year 7 students (ages 12-13) working on mathematics homework
- **Secondary**: Parents seeking guided homework support for their children

### Core Value Proposition
Transform homework from a struggle into a guided learning experience where students discover solutions through AI-powered Socratic questioning rather than being given direct answers.

### Key Workflow
1. **Upload**: Student uploads homework document (PDF/image)
2. **Parse**: System extracts and identifies individual questions
3. **Tutor**: AI guides through each question step-by-step
4. **Learn**: Student discovers solutions through guided questioning
5. **Progress**: Track improvement across homework sessions

## MVP Features

### 1. Document Upload & Processing
- Support for PDF and image uploads of homework documents
- Automatic text extraction and mathematical notation parsing
- Question identification and separation
- Problem type classification (algebra, geometry, word problems)

### 2. Intelligent Tutoring System
- **Socratic Method**: Guides students to discover answers through questioning
- **Adaptive Assessment**: Quick skill level detection and continuous adaptation
- **Step-by-Step Guidance**: Breaks complex problems into manageable steps
- **Hint System**: Graduated hints without giving away answers

### 3. Year 7 Curriculum Support
- **Integers & Directed Numbers**: Addition, subtraction, multiplication, division
- **Fractions & Decimals**: Operations and conversions
- **Basic Algebra**: Simple equations and substitution
- **Geometry Basics**: Area, perimeter, angles
- **Word Problems**: Multi-step real-world applications

### 4. Student-Centered Learning
- **Age-Appropriate Communication**: Friendly, patient tone for 12-13 year olds
- **Mistake-Friendly Environment**: Errors treated as learning opportunities
- **Confidence Building**: Positive reinforcement and progress recognition
- **Individual Pacing**: Adapts to each student's learning speed

### 5. Session Management
- Question-by-question progression through homework
- Session state tracking and context maintenance
- Progress summary and learning insights
- Performance analytics across homework sessions

## MVP Technical Architecture

### Simplified 3-Agent System

The MVP uses a streamlined 3-agent architecture focused on core homework tutoring functionality:

```
┌─────────────────────────────────────────────────────────────┐
│                Document Upload Interface                    │
│                    (Web Application)                        │
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

### MVP Agent Specifications

#### 1. Document Parser Agent
**Primary Responsibilities:**
- Extract text from uploaded PDF/image files
- Identify and separate individual homework questions
- Parse mathematical expressions and notation
- Classify question types (algebra, geometry, word problems)
- Estimate difficulty level per question

**Technology Stack:**
- **OCR**: PaddleOCR or Tesseract for text extraction
- **Math Parsing**: SymPy for mathematical expression handling
- **Document Processing**: PyPDF2 or pdfplumber for PDFs
- **Image Processing**: OpenCV for image preprocessing

#### 2. Assessment Agent
**Primary Responsibilities:**
- Conduct quick skill assessment based on initial question attempts
- Continuously adapt to student responses throughout session
- Identify knowledge gaps and common misconceptions
- Adjust tutoring approach based on student performance

**Key Capabilities:**
- 2-3 question diagnostic for skill level detection
- Real-time confidence and understanding assessment
- Adaptive difficulty adjustment per question
- Response quality analysis (confident/hesitant, correct/incorrect)

**Technology Stack:**
- **NLP**: spaCy or NLTK for response analysis
- **Classification**: Simple ML models for skill assessment
- **Pattern Recognition**: Rule-based system for common errors

#### 3. Tutor Agent
**Primary Responsibilities:**
- Guide students through problem-solving using Socratic method
- Generate appropriate questions that lead to discovery
- Provide graduated hints without giving direct answers
- Maintain encouraging, age-appropriate communication style

**Core Capabilities:**
- Socratic questioning adapted to Year 7 level
- Step-by-step problem breakdown
- Contextual hint generation
- Mistake reframing as learning opportunities
- Progress celebration and confidence building

**Technology Stack:**
- **LLM**: OpenAI GPT-4 or Claude for natural conversation
- **Prompt Engineering**: Specialized prompts for Socratic tutoring
- **Context Management**: Session state and conversation history

### MVP System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Interface                            │
│              (React.js Frontend)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/WebSocket
┌─────────────────────▼───────────────────────────────────────┐
│                 API Gateway                                 │
│               (FastAPI Backend)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│               Session Manager                               │
│            (State Management + Redis)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌────▼────┐ ┌──────▼──────┐
│   Document   │ │Assessment│ │    Tutor    │
│   Parser     │ │  Agent   │ │   Agent     │
│   Agent      │ │          │ │             │
└──────────────┘ └─────────┘ └─────────────┘
        │             │             │
        ▼             ▼             ▼
┌──────────────┬──────────────┬──────────────┐
│ File Storage │ PostgreSQL   │ LLM API      │
│ (Documents)  │ (Sessions)   │ (GPT-4)      │
└──────────────┴──────────────┴──────────────┘
```

### MVP Data Flow

**Document Processing Flow:**
```
Homework Upload → OCR Processing → Question Extraction → Question Queue
                                                            ↓
Student Ready → Present Next Question → Begin Tutoring Session
```

**Tutoring Session Flow:**
```
Current Question → Assessment Agent → Skill Level Detection
                      ↓
Tutor Agent → Socratic Questions → Student Response
                      ↓
Response Analysis → Adaptive Feedback → Next Question or Hint
                      ↓
Question Complete → Progress Update → Next Question Selection
```

**Session Management:**
```
Session Start → Question Queue → Individual Tutoring → Session Summary
                      ↓                ↓                    ↓
                Track Progress → Adapt Difficulty → Learning Insights
```

### MVP Technology Stack

#### Core Framework
- **Backend**: Python with FastAPI for API services
- **Frontend**: React.js for web interface
- **State Management**: Redis for session state and caching
- **LLM Integration**: OpenAI API (GPT-4) or Claude

#### Document Processing
- **OCR**: PaddleOCR or Tesseract for text extraction
- **Math Parsing**: SymPy for mathematical expressions
- **PDF Processing**: PyPDF2 or pdfplumber
- **Image Processing**: OpenCV for preprocessing

#### Data Storage
- **PostgreSQL**: User sessions and progress data
- **File Storage**: Local/cloud storage for uploaded documents
- **Redis**: Session state and real-time data

#### Infrastructure
- **Development**: Docker for containerization
- **Deployment**: Cloud platform (AWS/GCP) for production
- **Monitoring**: Basic logging and performance metrics

### ML Model Pipeline

#### Training Pipeline
```
Data Collection → Feature Engineering → Model Training → A/B Testing → Deployment
       ↓                  ↓                ↓              ↓            ↓
Student         Response          Fine-tune      Compare        Update
Interactions    Analysis          Models        Performance    Production
                                                              Models
```

#### Real-time Inference
```
Input → Preprocessing → Agent Routing → Model Inference → Response Generation
   ↓         ↓              ↓              ↓                ↓
Raw Data  Cleaned       Agent          AI Model         Personalized
         Structured    Selection       Prediction        Response
```

### Assessment & Personalization

#### Multi-Layered Assessment Approach
```
Layer 1: Problem Analysis (Automatic)
├── Topic identification from uploaded exercise
├── Difficulty level estimation
└── Required prerequisite skills mapping

Layer 2: Diagnostic Questions (Interactive)
├── 2-3 targeted questions based on the problem
├── Open-ended to reveal thinking process
└── Skill level indicators from responses

Layer 3: Real-time Adjustment (Adaptive)
├── Continuous assessment during problem solving
├── Response quality analysis
└── Confidence level detection
```

#### Skill Level Framework

**Beginner Indicators:**
- Struggles to identify what the problem is asking
- Doesn't recognize problem type or patterns
- Needs step-by-step guidance for basic operations
- Limited mathematical vocabulary
- Shows anxiety or avoidance behaviors

**Intermediate Indicators:**
- Recognizes problem type but unsure of approach
- Can perform basic operations but struggles with multi-step problems
- Has some mathematical vocabulary
- Shows willingness to try different approaches
- Makes logical errors but shows reasoning

**Advanced Indicators:**
- Quickly identifies problem type and approach
- Shows mathematical reasoning and pattern recognition
- Uses appropriate mathematical language
- Can attempt multiple solution methods
- Asks deeper "what if" questions

#### Dynamic Personalization Strategies

**Response Pattern Analysis:**
- Confident & Correct → Increase difficulty, ask extension questions
- Confident & Incorrect → Gentle questioning to reveal misconception
- Hesitant & Correct → Build confidence, explain why they're right
- Hesitant & Incorrect → Break down further, provide more support
- No Response → Simplify question, provide example, check understanding

**Learning Style Adaptation:**
- **Visual Learners:** "Picture this triangle in your mind...", "Let's draw a number line..."
- **Auditory/Verbal Learners:** "Let's talk through this step by step...", "Explain your thinking out loud..."
- **Kinesthetic Learners:** "Let's work with concrete numbers first...", "Try plugging in some values..."

#### Progress Tracking & Memory
- Skill level progression tracking
- Topic mastery indicators
- Common error patterns identification
- Preferred learning approaches
- Confidence level changes
- Engagement patterns analysis

#### Emotional Intelligence & Support

**Frustration Detection Signals:**
- Short, abrupt responses
- "I don't know" repeatedly
- Requests to skip or move on
- Negative self-talk ("I'm bad at math")

**Confidence Building Strategies:**
- **Micro-celebrations:** "That's exactly right!" for small wins
- **Process praise:** "I love how you thought through that step"
- **Mistake reframing:** "Great attempt! That shows you understand the first part"
- **Progress highlighting:** "Remember yesterday when this was tricky? Look how you got it now!"

### Year 7 Curriculum Scope
- **Target Age**: 12-13 years (Year 7/Grade 7)
- **Mathematics Topics**:
  - **Integers & Directed Numbers**: Addition, subtraction, multiplication, division with negatives
  - **Fractions & Decimals**: Operations, conversions, percentages
  - **Basic Algebra**: Simple linear equations, substitution, basic manipulation
  - **Geometry Basics**: Area, perimeter, angle properties, coordinate geometry
  - **Word Problems**: Multi-step problems applying above concepts

### Engagement Features
- Session length optimization
- Progress tracking and achievements
- Emotional support for frustrated students
- Motivation through positive reinforcement

## MVP Success Metrics

### Primary Metrics
- **Document Processing**: 90%+ accuracy in question extraction from homework
- **Student Engagement**: 70%+ homework session completion rate
- **Learning Progress**: Measurable improvement from first to last question in session
- **Student Satisfaction**: 80%+ positive feedback on tutoring helpfulness

### Secondary Metrics
- **Response Time**: System processing speed for documents and AI responses
- **Question Quality**: Accuracy of question parsing and classification
- **Adaptation Effectiveness**: How well system adjusts to individual student needs
- **Technical Performance**: System reliability and uptime

## MVP Development Phases

### Phase 1: Core Functionality (Weeks 1-4)
- [ ] Basic document upload and text extraction
- [ ] Simple question parsing and separation
- [ ] Basic tutor agent with Socratic questioning
- [ ] Minimal web interface for testing
- [ ] Support for basic Year 7 math problems

### Phase 2: Assessment Integration (Weeks 5-6)
- [ ] Initial skill assessment implementation
- [ ] Adaptive response system based on student performance
- [ ] Improved question classification and difficulty estimation
- [ ] Enhanced mathematical notation handling

### Phase 3: Polish and Testing (Weeks 7-8)
- [ ] Improved user interface and experience
- [ ] Testing with real Year 7 students and homework
- [ ] Performance optimization and bug fixes
- [ ] Session management and progress tracking

### Future Enhancements (Post-MVP)
- Advanced personalization features
- Multi-session learning paths
- Parent/teacher dashboards
- Expansion to additional grade levels and subjects

## Key Implementation Considerations

### Technical Challenges
1. **Mathematical Notation**: Accurate OCR processing of complex mathematical expressions
2. **Question Boundaries**: Reliably identifying where questions start and end in homework documents
3. **Context Maintenance**: Keeping track of student progress and conversation state
4. **Response Quality**: Ensuring Socratic questions are helpful and age-appropriate

### Educational Considerations
1. **Academic Integrity**: Providing guidance without doing homework for students
2. **Individual Learning**: Adapting to different learning styles and paces
3. **Curriculum Alignment**: Ensuring content matches Year 7 standards
4. **Progress Tracking**: Meaningful metrics for student improvement

### User Experience
1. **Simplicity**: Easy document upload and intuitive interface
2. **Engagement**: Maintaining student interest throughout homework session
3. **Feedback**: Clear progress indicators and learning insights
4. **Accessibility**: Support for different devices and learning needs

## Next Steps
1. **✅ MVP Design Complete** - Documented in `MVP Design.md`
2. **🔄 Technical Setup** - Development environment and basic architecture
3. **📋 Sample Data Collection** - Gather Year 7 homework examples for testing
4. **🔧 Proof of Concept** - Basic document parsing and question extraction
5. **🎨 UI/UX Design** - User interface mockups and interaction flows
6. **🧪 Initial Testing** - Validate core functionality with sample problems

---

## Related Documents
- **[MVP Design.md](./MVP%20Design.md)** - Detailed MVP specifications and implementation plan
- **Future**: Technical architecture deep-dive, API documentation, user testing results

---

**Status**: MVP Design Phase - Ready for Development  
**Last Updated**: July 1, 2025  
**Focus**: Year 7 Maths Homework Tutoring MVP
