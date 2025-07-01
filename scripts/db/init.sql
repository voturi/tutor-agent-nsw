-- TutorAgent MVP Database Initialization Script

-- Create database (this runs automatically in Docker)
-- CREATE DATABASE tutor_agent_db;

-- Connect to the database
\c tutor_agent_db;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables for MVP

-- Upload tracking table
CREATE TABLE IF NOT EXISTS uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_path TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'uploaded',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    questions_extracted INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session tracking table
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    upload_id UUID NOT NULL REFERENCES uploads(id),
    student_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    questions_total INTEGER DEFAULT 0,
    questions_completed INTEGER DEFAULT 0,
    current_question_index INTEGER DEFAULT 0,
    skill_level VARCHAR(50) DEFAULT 'unknown',
    confidence_level VARCHAR(50) DEFAULT 'neutral',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Questions table
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    upload_id UUID NOT NULL REFERENCES uploads(id),
    question_index INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(100),
    difficulty_level VARCHAR(50),
    topic VARCHAR(100),
    extracted_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interactions table for tracking tutor-student conversations
CREATE TABLE IF NOT EXISTS interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    question_id UUID REFERENCES questions(id),
    interaction_type VARCHAR(50) NOT NULL, -- question, response, hint, assessment
    student_input TEXT,
    tutor_response TEXT,
    confidence_level VARCHAR(50),
    skill_assessment JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session analytics table
CREATE TABLE IF NOT EXISTS session_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES sessions(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value TEXT NOT NULL,
    metric_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_uploads_status ON uploads(status);
CREATE INDEX IF NOT EXISTS idx_uploads_created_at ON uploads(created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_upload_id ON sessions(upload_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_questions_upload_id ON questions(upload_id);
CREATE INDEX IF NOT EXISTS idx_questions_question_index ON questions(question_index);
CREATE INDEX IF NOT EXISTS idx_interactions_session_id ON interactions(session_id);
CREATE INDEX IF NOT EXISTS idx_interactions_created_at ON interactions(created_at);
CREATE INDEX IF NOT EXISTS idx_session_analytics_session_id ON session_analytics(session_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_uploads_updated_at BEFORE UPDATE ON uploads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing (optional)
-- This will be useful for development and testing

COMMENT ON TABLE uploads IS 'Tracks uploaded homework documents and their processing status';
COMMENT ON TABLE sessions IS 'Tracks tutoring sessions for each uploaded homework';
COMMENT ON TABLE questions IS 'Stores extracted questions from uploaded documents';
COMMENT ON TABLE interactions IS 'Logs all interactions between tutor and student';
COMMENT ON TABLE session_analytics IS 'Stores analytics and metrics for each session';

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tutor_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tutor_user;

-- Database initialization complete
SELECT 'TutorAgent MVP database initialized successfully!' as status;
