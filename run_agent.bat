@echo off
echo [%date% %time%] CryptoDaily Agent Starting... >> C:\Users\jitum\Desktop\bitcoin-agent\logs\agent_log.txt

:: Activate virtual environment and run agent
cd C:\Users\jitum\Desktop\bitcoin-agent
call venv\Scripts\activate.bat
python agent.py >> C:\Users\jitum\Desktop\bitcoin-agent\logs\agent_log.txt 2>&1

echo [%date% %time%] Agent finished. >> C:\Users\jitum\Desktop\bitcoin-agent\logs\agent_log.txt