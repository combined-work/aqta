import os
import sys
import subprocess

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def setup():
    print("AQTA First-Run Setup")

    # 1. Check requirements
    # run_command("pip install -r requirements.txt") # Assuming requirements.txt exists

    # 2. Setup env
    if not os.path.exists("config/broker_secrets.env"):
        run_command("cp config/broker_secrets.env.example config/broker_secrets.env")
        print("Created config/broker_secrets.env. Please fill in your API keys.")

    # 3. Initialize DB
    run_command("export PYTHONPATH=$PYTHONPATH:. && python3 engine/database/migrations.py")

    # 4. Fetch initial data (Mocked)
    print("Warming up historical data cache...")
    os.makedirs("data_cache/features", exist_ok=True)

    print("Setup complete. You can now start the engine and UI.")
    print("Run engine: python3 engine/api/engine_api.py")
    print("Run UI: python3 ui/ui_server.py")

if __name__ == "__main__":
    setup()
