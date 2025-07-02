# TutorAgent Chat Interface Setup

A simple chat interface similar to GitHub Copilot for Year 7 mathematics tutoring using Gemini 2.5 Pro.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+ for backend
- Node.js 18+ for frontend  
- Redis (optional but recommended)
- Gemini API key

### 2. Environment Setup

Copy the environment file and add your API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Start Redis (Optional)
```bash
# Using Docker (recommended)
docker run --name redis -p 6379:6379 -d redis

# Or install locally and start
redis-server
```

### 4. Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend will start on http://localhost:8000

### 5. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend will start on http://localhost:3000

### 6. Test the Chat Interface

Visit http://localhost:3000/chat to use the tutoring interface!

## 🏗️ Architecture

### Backend
- **FastAPI** web framework
- **Gemini 2.5 Pro** for AI tutoring and assessment
- **Redis** for session management
- **Pydantic** for data validation

### Frontend  
- **Next.js 15** with TypeScript
- **Tailwind CSS** for styling
- **Lucide React** for icons
- Responsive design matching existing app theme

### Key Features
- **Socratic Method**: AI guides students through discovery
- **Skill Assessment**: Adapts to student's level in real-time
- **Session Management**: Maintains conversation context
- **Suggestions**: Helpful prompts based on student progress
- **Dark/Light Theme**: Consistent with existing app styling

## 📁 File Structure

```
TutorAgent/
├── backend/
│   ├── agents/assessment/
│   │   └── gemini_agent.py         # Gemini-powered assessment
│   ├── api/routes/
│   │   └── chat.py                 # Chat API endpoints
│   └── services/
│       └── redis.py                # Session storage
├── frontend/
│   └── src/app/chat/
│       └── page.tsx                # Chat interface
└── test_chat.py                    # Setup test script
```

## 🔧 Testing

Run the test script to verify setup:
```bash
python test_chat.py
```

## 🎨 UI Design

The chat interface follows the GitHub Copilot design pattern:
- **Sidebar**: Session management and conversation history
- **Main Area**: Message thread with user/assistant bubbles  
- **Input Area**: Message input with suggestions
- **Consistent Styling**: Matches existing TutorAgent theme

## 🤖 AI Behavior

### Assessment Agent
- Analyzes student responses for skill level
- Detects emotional state (confident/frustrated)  
- Identifies knowledge gaps
- Adapts tutoring approach

### Tutoring Response
- Uses Socratic method questioning
- Never gives direct answers
- Celebrates progress and discoveries
- Age-appropriate language for 12-13 year olds

## 🔧 Customization

### Adding New Models
To use different AI models, create new agents in `backend/agents/`:
```python
# Example: OpenAI agent
class OpenAIAssessmentAgent:
    # Implement same interface as GeminiAssessmentAgent
```

### Styling Changes
Update `frontend/src/app/globals.css` for theme modifications.

### New Features
- Add routes in `backend/api/routes/chat.py`
- Update frontend components in `frontend/src/app/chat/`

## 📚 Next Steps

1. **Document Upload**: Add file upload to chat interface
2. **Question Parsing**: Integrate document parser agent
3. **Session History**: Show previous conversations in sidebar  
4. **Assessment Dashboard**: Visual progress tracking
5. **Multi-User Support**: User accounts and auth

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**
- Check Python dependencies: `pip install -r backend/requirements.txt`
- Verify environment variables in `.env`

**Frontend connection errors**  
- Ensure backend is running on port 8000
- Check proxy configuration in `frontend/next.config.ts`

**Redis connection issues**
- Start Redis: `docker run --name redis -p 6379:6379 -d redis`
- Sessions will fall back to memory if Redis unavailable

**Gemini API errors**
- Add valid `GEMINI_API_KEY` to `.env`
- Check API quota and billing

### Debug Mode
Set `DEBUG=true` in `.env` for detailed logging.

## 📄 License

Part of the TutorAgent MVP - Year 7 Mathematics Homework Helper
