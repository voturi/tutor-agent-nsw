# 🗄️ Local Database Access Guide

Connect your local Redis Insight and pgAdmin4 to AWS databases.

## 🎯 Quick Start

### 1. Start Database Tunnels
```bash
# Navigate to project directory
cd /Users/praveen.voturi/Documents/Projects/TutorAgent

# Run the setup script
./scripts/local-db-setup.sh

# Choose option 3 to start both tunnels in background
```

### 2. Manual Tunnel Commands (Alternative)
```bash
# PostgreSQL tunnel (Terminal 1)
ssh -i ~/.ssh/tutor-agent-bastion -L 5432:tutor-agent-postgres.cutcydwvusa4.ap-southeast-2.rds.amazonaws.com:5432 ec2-user@3.27.36.22 -N

# Redis tunnel (Terminal 2) 
ssh -i ~/.ssh/tutor-agent-bastion -L 6379:tutor-agent-redis.c4deqb.ng.0001.apse2.cache.amazonaws.com:6379 ec2-user@3.27.36.22 -N
```

## 🐘 pgAdmin4 Setup

### Connection Details:
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `tutor_agent_db`
- **Username**: `tutor_user`
- **Password**: `tutor_password_123`

### Steps:
1. Start PostgreSQL tunnel (see above)
2. Open pgAdmin4
3. Right-click "Servers" → "Create" → "Server"
4. **General Tab**:
   - Name: `TutorAgent Production`
5. **Connection Tab**:
   - Host: `localhost`
   - Port: `5432`
   - Database: `tutor_agent_db`
   - Username: `tutor_user`
   - Password: `tutor_password_123`
6. Click "Save"

## 🔴 Redis Insight Setup

### Connection Details:
- **Host**: `localhost`
- **Port**: `6379`
- **Database Index**: `0`
- **Authentication**: None required

### Steps:
1. Start Redis tunnel (see above)
2. Open Redis Insight
3. Click "Add Database"
4. Choose "Add Database Manually"
5. **Connection Details**:
   - Host: `localhost`
   - Port: `6379`
   - Database Alias: `TutorAgent Production`
6. Click "Add Database"

## 🧪 Test Connections

### PostgreSQL Test:
```bash
# Command line test
psql -h localhost -p 5432 -U tutor_user -d tutor_agent_db -c "SELECT version();"

# Should return PostgreSQL version information
```

### Redis Test:
```bash
# Install redis-cli if needed
brew install redis

# Test connection
redis-cli -h localhost -p 6379 ping

# Should return "PONG"
```

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "Connection refused" errors
- **Cause**: Tunnel not running
- **Solution**: Check tunnel status and restart
```bash
ps aux | grep ssh
./scripts/local-db-setup.sh
```

#### 2. "Permission denied" SSH errors
- **Cause**: SSH key permissions
- **Solution**: Fix permissions
```bash
chmod 400 ~/.ssh/tutor-agent-bastion
```

#### 3. "Port already in use" errors
- **Cause**: Another service using port 5432/6379
- **Solution**: Stop local databases or use different ports
```bash
# Stop local PostgreSQL/Redis if running
brew services stop postgresql
brew services stop redis

# Or use different local ports
ssh -i ~/.ssh/tutor-agent-bastion -L 15432:tutor-agent-postgres...:5432 ec2-user@3.27.36.22 -N
```

#### 4. Bastion host connection issues
- **Cause**: Security group or key issues
- **Solution**: Check bastion host status
```bash
# Check if bastion is running
aws ec2 describe-instances --instance-ids i-0955948c700c42027 --region ap-southeast-2
```

## 🚀 Advanced Usage

### Background Tunnels
```bash
# Start tunnels in background
./scripts/local-db-setup.sh
# Choose option 3

# Check running tunnels
cat tunnel_pids.txt

# Stop tunnels
./scripts/local-db-setup.sh
# Choose option 4
```

### Custom Port Mapping
```bash
# Use custom local ports to avoid conflicts
ssh -i ~/.ssh/tutor-agent-bastion -L 15432:tutor-agent-postgres.cutcydwvusa4.ap-southeast-2.rds.amazonaws.com:5432 ec2-user@3.27.36.22 -N &
ssh -i ~/.ssh/tutor-agent-bastion -L 16379:tutor-agent-redis.c4deqb.ng.0001.apse2.cache.amazonaws.com:6379 ec2-user@3.27.36.22 -N &

# Then use localhost:15432 and localhost:16379 in your tools
```

## 📊 Database Schema

### PostgreSQL Tables
Once connected, you can explore:
- Application tables (when created by your app)
- User sessions
- Document metadata
- Chat history

### Redis Keys
Common key patterns:
- `session:*` - User sessions
- `cache:*` - Application cache
- `rate_limit:*` - Rate limiting data

## 🔒 Security Notes

- ✅ All connections are encrypted via SSH tunnel
- ✅ No direct internet access to databases
- ✅ Bastion host provides secure gateway
- ⚠️ Keep SSH key secure (`~/.ssh/tutor-agent-bastion`)
- ⚠️ Stop tunnels when not needed to save costs

## 💡 Pro Tips

1. **Persistent Connections**: Use screen/tmux for long-running tunnels
2. **Multiple Environments**: Create separate bastion hosts for staging/prod
3. **Connection Pooling**: pgAdmin4 can maintain multiple connections
4. **Monitoring**: Use Redis Insight for real-time Redis monitoring
5. **Backups**: Use pgAdmin4 to create local database backups

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify bastion host is running in AWS console
3. Test SSH connection to bastion host directly
4. Check security group rules allow your connections

**Infrastructure Status**: All tunnels route through bastion host `3.27.36.22`
