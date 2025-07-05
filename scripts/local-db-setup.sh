#!/bin/bash

# TutorAgent Local Database Access Script
# This script helps you connect your local Redis Insight and pgAdmin4 to AWS databases

echo "🔧 TutorAgent Local Database Access Setup"
echo "=========================================="

# Database connection details
BASTION_IP="3.27.36.22"
POSTGRES_HOST="tutor-agent-postgres.cutcydwvusa4.ap-southeast-2.rds.amazonaws.com"
REDIS_HOST="tutor-agent-redis.c4deqb.ng.0001.apse2.cache.amazonaws.com"
SSH_KEY="~/.ssh/tutor-agent-bastion"

# Database credentials
DB_USER="tutor_user"
DB_PASSWORD="tutor_password_123"
DB_NAME="tutor_agent_db"

echo ""
echo "📊 Connection Details:"
echo "Bastion Host: $BASTION_IP"
echo "PostgreSQL: $POSTGRES_HOST:5432"
echo "Redis: $REDIS_HOST:6379"
echo ""

# Function to start PostgreSQL tunnel
start_postgres_tunnel() {
    echo "🐘 Starting PostgreSQL tunnel..."
    echo "Command: ssh -i $SSH_KEY -L 5432:$POSTGRES_HOST:5432 ec2-user@$BASTION_IP -N"
    echo ""
    echo "📋 pgAdmin4 Connection Settings:"
    echo "Host: localhost"
    echo "Port: 5432"
    echo "Database: $DB_NAME"
    echo "Username: $DB_USER"
    echo "Password: $DB_PASSWORD"
    echo ""
    echo "Press Ctrl+C to stop the tunnel"
    ssh -i $SSH_KEY -L 5432:$POSTGRES_HOST:5432 ec2-user@$BASTION_IP -N
}

# Function to start Redis tunnel
start_redis_tunnel() {
    echo "🔴 Starting Redis tunnel..."
    echo "Command: ssh -i $SSH_KEY -L 6379:$REDIS_HOST:6379 ec2-user@$BASTION_IP -N"
    echo ""
    echo "📋 Redis Insight Connection Settings:"
    echo "Host: localhost"
    echo "Port: 6379"
    echo "Database Index: 0"
    echo "No password required"
    echo ""
    echo "Press Ctrl+C to stop the tunnel"
    ssh -i $SSH_KEY -L 6379:$REDIS_HOST:6379 ec2-user@$BASTION_IP -N
}

# Function to start both tunnels in background
start_both_tunnels() {
    echo "🚀 Starting both tunnels in background..."
    
    # Start PostgreSQL tunnel in background
    ssh -i $SSH_KEY -L 5432:$POSTGRES_HOST:5432 ec2-user@$BASTION_IP -N &
    POSTGRES_PID=$!
    echo "PostgreSQL tunnel started (PID: $POSTGRES_PID)"
    
    # Start Redis tunnel in background
    ssh -i $SSH_KEY -L 6379:$REDIS_HOST:6379 ec2-user@$BASTION_IP -N &
    REDIS_PID=$!
    echo "Redis tunnel started (PID: $REDIS_PID)"
    
    echo ""
    echo "✅ Both tunnels are running!"
    echo "PostgreSQL: localhost:5432 (PID: $POSTGRES_PID)"
    echo "Redis: localhost:6379 (PID: $REDIS_PID)"
    echo ""
    echo "To stop tunnels, run: kill $POSTGRES_PID $REDIS_PID"
    echo "PIDs saved to tunnel_pids.txt"
    echo "$POSTGRES_PID $REDIS_PID" > tunnel_pids.txt
}

# Function to stop tunnels
stop_tunnels() {
    if [ -f tunnel_pids.txt ]; then
        echo "🛑 Stopping tunnels..."
        PIDS=$(cat tunnel_pids.txt)
        kill $PIDS 2>/dev/null
        rm tunnel_pids.txt
        echo "✅ Tunnels stopped"
    else
        echo "❌ No running tunnels found"
    fi
}

# Main menu
echo "Choose an option:"
echo "1) Start PostgreSQL tunnel only"
echo "2) Start Redis tunnel only"  
echo "3) Start both tunnels in background"
echo "4) Stop all tunnels"
echo "5) Show connection info"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        start_postgres_tunnel
        ;;
    2)
        start_redis_tunnel
        ;;
    3)
        start_both_tunnels
        ;;
    4)
        stop_tunnels
        ;;
    5)
        echo ""
        echo "📋 Connection Information:"
        echo ""
        echo "🐘 PostgreSQL (for pgAdmin4):"
        echo "  Host: localhost"
        echo "  Port: 5432"
        echo "  Database: $DB_NAME"
        echo "  Username: $DB_USER"
        echo "  Password: $DB_PASSWORD"
        echo ""
        echo "🔴 Redis (for Redis Insight):"
        echo "  Host: localhost"
        echo "  Port: 6379"
        echo "  Database Index: 0"
        echo "  No authentication required"
        echo ""
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
