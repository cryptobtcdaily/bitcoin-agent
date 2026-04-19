# CryptoDaily Daily Agent Runner
$logFile = "C:\Users\jitum\Desktop\bitcoin-agent\logs\agent_log.txt"
$agentDir = "C:\Users\jitum\Desktop\bitcoin-agent"

# Create logs folder if it doesn't exist
New-Item -ItemType Directory -Force -Path "$agentDir\logs" | Out-Null

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"
chcp 65001 | Out-Null

# Log start
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $logFile "[$timestamp] Agent Starting..."

# Change to agent directory
Set-Location $agentDir

# Activate venv and run agent
& "$agentDir\venv\Scripts\Activate.ps1"
python -X utf8 agent.py 2>&1 | Tee-Object -FilePath $logFile -Append

# Log finish
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content $logFile "[$timestamp] Agent Finished."