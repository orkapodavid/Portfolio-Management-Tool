# Memurai on Windows: Setup & Development Guide

## Overview

Memurai is the official Windows-native Redis port, developed in partnership with Redis. It provides native performance without virtualization, WSL, or Docker overhead, making it ideal for Windows development environments.

### Key Benefits
- Native Windows executable (no WSL, Docker, or virtual machines)
- Full Redis 7.2.6 compatibility
- Enterprise-ready with active support
- Windows Service integration
- Windows Event Log support
- High performance with minimal resource footprint

---

## System Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows 10 or Windows Server 2012+ |
| **Architecture** | 64-bit only |
| **Redis Compatibility** | Redis 7.2.6 |
| **Disk Space** | ~50MB for installation |
| **RAM** | Configurable (default: unlimited, recommended: set via maxmemory) |

---

## Installation

### Option 1: GUI Installation (Recommended for Beginners)

1. **Download Memurai**
   - Visit [memurai.com/get-memurai](https://www.memurai.com/get-memurai)
   - Choose the Developer Edition (free) or Enterprise Edition
   - Download the `.msi` installer

2. **Run the Installer**
   - Execute the `.msi` file
   - Accept the license agreement
   - Choose installation folder (default: `C:\Program Files\Memurai`)

3. **Configuration Options**
   - **Install as Windows Service**: Recommended for development (checked by default)
   - **Port**: Default is 6379. Change if you need multiple instances
   - **Firewall Rule**: Creates Windows Firewall rule for the selected port

4. **Completion**
   - Memurai service starts automatically after installation
   - Accessible immediately via `memurai-cli` in any terminal

### Option 2: Command Line Installation

Install silently with default settings:

```cmd
msiexec /quiet /i Memurai.msi
```

Install with custom parameters:

```cmd
msiexec /quiet /i Memurai.msi INSTALLFOLDER="C:\MyRedis" PORT=8000 ADD_FIREWALL_RULE=1
```

**Available Parameters:**

| Parameter | Default | Example |
|---|---|---|
| `INSTALLFOLDER` | `C:\Program Files\Memurai` | `INSTALLFOLDER="C:\MyRedis"` |
| `ADD_INSTALLFOLDER_TO_PATH` | 1 (yes) | `ADD_INSTALLFOLDER_TO_PATH=0` |
| `INSTALL_SERVICE` | 1 (yes) | `INSTALL_SERVICE=0` (no service) |
| `PORT` | 6379 | `PORT=8000` |
| `ADD_FIREWALL_RULE` | 1 (yes) | `ADD_FIREWALL_RULE=0` |

### Option 3: Package Manager Installation

**Using Chocolatey:**
```powershell
choco install memurai-developer
```

**Using Winget:**
```powershell
winget install -e --id Memurai.MemuraiDeveloper
```

### Verify Installation

Open PowerShell or Command Prompt and test:

```cmd
memurai-cli ping
```

Expected output: `PONG`

If Memurai is running as a service, this command confirms connectivity.

---

## Configuration

### Configuration File Basics

Memurai uses a plain text configuration file (`memurai.conf`) compatible with Redis and Valkey 7 syntax.

**File Location:**
- Default: `C:\Program Files\Memurai\memurai.conf`
- Custom: Any location where you have read-write access

**Format:**
```
keyword arg1 arg2 ... argN
```

Arguments with spaces must be quoted:
```
logfile "C:\logs\memurai log.txt"
```

Paths can use either backslash or forward slash:
```
logfile "C:/logs/memurai-log.txt"
```

### Running Memurai with Custom Configuration

**Standalone (not as service):**
```cmd
cd C:\Users\YourUsername\myconfig
memurai.exe memurai.conf
```

**As Windows Service:**
```cmd
memurai.exe --service-install --service-name "memurai-dev" C:\path\to\memurai.conf
```

**Override Config via Command Line:**
```cmd
memurai.exe memurai.conf --port 8000 --loglevel debug
```

### Essential Configuration for Development

Create a `memurai-dev.conf` file with these settings:

```ini
# Port
port 6379

# Logging
loglevel debug
logfile "C:/dev/memurai/memurai.log"

# Memory management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence - RDB snapshots
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir "C:/dev/memurai/data"

# Persistence - AOF (optional for development)
appendonly no

# Database count
databases 16

# Instance name (helpful for logs)
instance-name "memurai-dev"

# Windows Event Log verbosity
winlog-level debug

# TCP settings
timeout 0
tcp-backlog 511
tcp-keepalive 300
```

### Common Configuration Flags

| Flag | Purpose | Example |
|---|---|---|
| `port` | Server port | `port 6379` |
| `loglevel` | Log verbosity (debug, verbose, notice, warning) | `loglevel notice` |
| `logfile` | Log file path | `logfile "C:/logs/memurai.log"` |
| `maxmemory` | Memory limit | `maxmemory 256mb` |
| `maxmemory-policy` | Eviction policy when memory full | `maxmemory-policy allkeys-lru` |
| `save` | RDB snapshot timing | `save 900 1` (save after 900s if 1 key changed) |
| `appendonly` | Enable AOF persistence | `appendonly yes` |
| `appendfsync` | AOF sync frequency (always, everysec, no) | `appendfsync everysec` |
| `databases` | Number of databases (0-15) | `databases 16` |
| `dir` | Data directory | `dir "C:/dev/memurai/data"` |
| `instance-name` | Instance identifier for logs | `instance-name "my-instance"` |
| `winlog-level` | Windows Event Log level | `winlog-level notice` |

### Unsupported Flags (Ignored by Memurai)

These Redis flags are ignored on Windows:
```
always-show-logo, activedefrag, daemonize, supervised, 
syslog-*, unixsocket*
```

---

## Windows Service Management

### Service Installation (Manual)

Install Memurai as a Windows Service with a custom configuration:

```cmd
memurai.exe --service-install --service-name "memurai-dev" "C:\dev\memurai.conf"
```

For Sentinel mode:
```cmd
memurai.exe --service-install --service-name "memurai-sentinel" --sentinel "C:\dev\memurai-sentinel.conf"
```

### Service Commands

**Start Service:**
```cmd
memurai.exe --service-start
memurai.exe --service-start --service-name "memurai-dev"
net start memurai
net start memurai-dev
```

**Stop Service:**
```cmd
memurai.exe --service-stop
memurai.exe --service-stop --service-name "memurai-dev"
net stop memurai
net stop memurai-dev
```

**Uninstall Service:**
```cmd
memurai.exe --service-uninstall
memurai.exe --service-uninstall --service-name "memurai-dev"
```

**View Service Status:**
- Open Services app: `services.msc`
- Search for "Memurai" or your custom service name
- Right-click → Properties to view details

### Configuration Changes

When you modify a configuration file used by a service, restart the service for changes to take effect:

```cmd
memurai.exe --service-stop --service-name "memurai-dev"
memurai.exe --service-start --service-name "memurai-dev"
```

Alternatively, use `CONFIG SET` in memurai-cli for runtime changes (some settings only):
```
config set maxmemory 512mb
config set loglevel debug
```

---

## Command Line Interface (memurai-cli)

### Connecting to Memurai

```cmd
memurai-cli
```

Default connection: `127.0.0.1:6379`

Connect to specific host and port:
```cmd
memurai-cli -h 192.168.1.100 -p 8000
```

### Basic Commands

```cmd
# Check connection
PING
> PONG

# Set a key-value pair
SET mykey "Hello Memurai"
> OK

# Get a value
GET mykey
> "Hello Memurai"

# Delete a key
DEL mykey
> (integer) 1

# List all keys
KEYS *
> 1) "key1"
> 2) "key2"

# Check server info
INFO
> # Server
> redis_version:7.2.6
> ...

# Flush all databases (warning: destructive)
FLUSHALL
> OK

# Exit CLI
QUIT
```

### Running Commands Directly

```cmd
memurai-cli SET message "Hello from PowerShell"
memurai-cli GET message
memurai-cli PING
```

### Monitoring Commands in Real-Time

```cmd
# Monitor all commands executed
memurai-cli MONITOR

# Watch key access
memurai-cli WATCH mykey

# Check slow queries
memurai-cli SLOWLOG GET 10
```

---

## Development Setup

### Node.js Development

**Install Dependencies:**
```bash
npm install ioredis
# or
npm install redis
```

**Example: Using ioredis**

```javascript
const Redis = require('ioredis');

// Connect to Memurai
const redis = new Redis({
  host: '127.0.0.1',
  port: 6379,
  db: 0
});

// Set a value
redis.set('user:123', JSON.stringify({ name: 'John', age: 30 }));

// Get a value
redis.get('user:123').then(result => {
  console.log('Retrieved:', JSON.parse(result));
});

// Use async/await
async function example() {
  await redis.set('greeting', 'Hello Memurai');
  const value = await redis.get('greeting');
  console.log(value); // "Hello Memurai"
  
  await redis.quit();
}

example();
```

**Example: Using redis client**

```javascript
const { createClient } = require('redis');

const client = createClient({
  socket: {
    host: '127.0.0.1',
    port: 6379
  }
});

await client.connect();

await client.set('key', 'value');
const value = await client.get('key');
console.log(value); // 'value'

await client.disconnect();
```

### Python Development

**Install Dependencies:**
```bash
pip install redis
```

**Example:**
```python
import redis
import json

# Connect to Memurai
r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

# Set a value
r.set('user:123', json.dumps({'name': 'John', 'age': 30}))

# Get a value
user = json.loads(r.get('user:123'))
print(user)  # {'name': 'John', 'age': 30}

# Use as cache
def get_user(user_id):
    cache_key = f'user:{user_id}'
    cached = r.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # Simulate database fetch
    user = {'id': user_id, 'name': 'User'}
    r.setex(cache_key, 3600, json.dumps(user))  # Cache for 1 hour
    return user

print(get_user(123))
```

### Testing with Multiple Instances

For testing Memurai cluster or failover scenarios:

```cmd
# Terminal 1: Primary instance on default port
memurai-cli -p 6379

# Terminal 2: Replica instance on port 6380
memurai.exe --port 6380

# Terminal 3: Connect replica to primary
memurai-cli -p 6380
> SLAVEOF 127.0.0.1 6379
```

---

## Persistence & Data Management

### RDB (Snapshot) Persistence

RDB creates point-in-time snapshots of your entire dataset.

**Configuration:**
```ini
# Save snapshots at these intervals
save 900 1       # After 900s if 1 key changed
save 300 10      # After 300s if 10 keys changed
save 60 10000    # After 60s if 10000 keys changed

rdbcompression yes      # Compress RDB file
rdbchecksum yes        # Add checksum to RDB file
dbfilename dump.rdb    # RDB filename
dir "C:/data/redis"    # Data directory
```

**Manual Snapshot:**
```cmd
memurai-cli BGSAVE
# or for blocking save
memurai-cli SAVE
```

### AOF (Append-Only File) Persistence

AOF logs every write operation for durability.

**Configuration:**
```ini
appendonly yes                    # Enable AOF
appendfilename "appendonly.aof"   # AOF filename
appendfsync everysec              # Sync every second (balanced)
# appendfsync always              # Sync after each command (slower but safest)
# appendfsync no                  # OS decides when to sync (fastest but risky)
```

**AOF Rewrite (Compact the log):**
```cmd
memurai-cli BGREWRITEAOF
```

### Hybrid Persistence (RDB + AOF)

Best of both worlds: fast recovery with high durability.

**Configuration:**
```ini
save 900 1                  # RDB snapshot
appendonly yes              # Enable AOF
aof-use-rdb-preamble yes   # Use RDB format for AOF base
```

### Data Recovery

**From RDB (automatic on startup):**
```cmd
# Memurai automatically loads dump.rdb on startup
memurai-cli
> INFO keyspace
```

**From AOF (automatic on startup):**
```cmd
# Memurai replays appendonly.aof on startup
memurai-cli
> INFO keyspace
```

---

## Performance Tuning

### Memory Management

```ini
# Set maximum memory usage
maxmemory 512mb

# Eviction policy when max memory reached
maxmemory-policy allkeys-lru    # LRU: evict oldest
# maxmemory-policy volatile-lru  # LRU: evict expiring keys only
# maxmemory-policy noeviction    # No eviction (return error when full)
```

### Connection Optimization

```ini
tcp-backlog 511         # TCP connection queue
timeout 0               # Client timeout (0 = no timeout)
tcp-keepalive 300       # Keep-alive probe interval (seconds)
maxclients 10000        # Maximum concurrent clients
```

### Slow Query Logging

Identify slow operations:

```cmd
# Enable slow query log (log queries slower than 10000 microseconds)
memurai-cli CONFIG SET slowlog-log-slower-than 10000

# View slowlog
memurai-cli SLOWLOG GET 10

# Clear slowlog
memurai-cli SLOWLOG RESET

# Get slowlog length
memurai-cli SLOWLOG LEN
```

### Monitor Performance

```cmd
# Real-time command monitoring
memurai-cli MONITOR

# Server statistics
memurai-cli INFO

# Memory usage
memurai-cli INFO memory

# CPU usage
memurai-cli INFO cpu

# Keyspace stats
memurai-cli INFO keyspace
```

---

## Troubleshooting

### Common Issues & Solutions

**Issue: "Address already in use" or "Port already bound"**
```cmd
# Check if service is running
net start memurai
# or change port
memurai.exe --port 8000

# Check what's using the port (PowerShell)
netstat -ano | findstr :6379
```

**Issue: "Cannot write to log file" or data directory**
```cmd
# Ensure Memurai has write permissions
# Right-click folder → Properties → Security → Edit permissions
# Add full control for "NT AUTHORITY\NetworkService"

# Or run from user's working directory with write access
cd C:\Users\YourUsername\memurai-data
memurai.exe memurai.conf
```

**Issue: Service won't start**
```cmd
# Check Windows Event Log for errors
eventvwr.msc
# Search for source "Memurai"

# Try installing with verbose logging
msiexec /i Memurai.msi /l*v install.log

# Check log file
type install.log
```

**Issue: "memurai-cli: command not found"**
```cmd
# Add Memurai to PATH (if not already)
set PATH=%PATH%;C:\Program Files\Memurai

# Or specify full path
C:\Program Files\Memurai\memurai-cli.exe
```

**Issue: Cannot connect to Memurai**
```cmd
# Check if service is running
memurai-cli PING

# Check port
netstat -ano | findstr :6379

# Check if firewall is blocking
# Windows Firewall → Allow an app → check Memurai
```

---

## Best Practices for Development

1. **Use Configuration Files**: Avoid command-line parameters for consistency
2. **Enable Logging**: Set `loglevel debug` during development
3. **Monitor Memory**: Set `maxmemory` to prevent unbounded growth
4. **Backup Data**: Regularly backup `dump.rdb` and `appendonly.aof`
5. **Test Persistence**: Verify data recovery after restart
6. **Use Separate Instances**: Create separate service instances for different projects
7. **Connection Pooling**: Use client library connection pools in production code
8. **Error Handling**: Implement retry logic and connection timeouts
9. **Watch Slow Queries**: Use `SLOWLOG` to identify bottlenecks
10. **Document Configuration**: Comment your config file for future reference

---

## Multiple Instances Example

Development scenario with multiple Memurai instances:

**Primary Configuration** (`memurai-main.conf`):
```ini
port 6379
instance-name "memurai-main"
logfile "C:/memurai-logs/main.log"
dir "C:/memurai-data/main"
```

**Cache Instance** (`memurai-cache.conf`):
```ini
port 6380
instance-name "memurai-cache"
logfile "C:/memurai-logs/cache.log"
maxmemory 256mb
maxmemory-policy allkeys-lru
appendonly no
```

**Install Both Services:**
```cmd
memurai.exe --service-install --service-name "memurai-main" "C:\memurai-main.conf"
memurai.exe --service-install --service-name "memurai-cache" "C:\memurai-cache.conf"

# Start both
memurai.exe --service-start --service-name "memurai-main"
memurai.exe --service-start --service-name "memurai-cache"

# Connect to cache instance
memurai-cli -p 6380
```

---

## Additional Resources

- **Official Memurai Docs**: [docs.memurai.com](https://docs.memurai.com)
- **Redis Command Reference**: [redis.io/commands](https://redis.io/commands)
- **Memurai Website**: [memurai.com](https://memurai.com)
- **Node.js Redis Clients**:
  - [ioredis](https://github.com/luin/ioredis)
  - [node_redis](https://github.com/redis/node-redis)
- **Python Redis Client**: [redis-py](https://github.com/redis/redis-py)

---

**Version**: Memurai 4.x (Redis 7.2 compatible)  
**Last Updated**: January 2026
