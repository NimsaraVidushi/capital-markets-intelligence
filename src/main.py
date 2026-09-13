import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

def run_script(script_name):
    script_path = BASE_DIR / "src" / script_name
    print(f"\n{'='*50}\nRunning {script_name}...\n{'='*50}")
    
    result = subprocess.run([sys.executable, str(script_path)])
    
    if result.returncode != 0:
        print(f"\nError executing {script_name}. Pipeline stopped.")
        sys.exit(1)
    
    print(f"\nSuccessfully completed {script_name}.")

def main():
    print("Starting Capital Markets Intelligence Pipeline")
    
    scripts = [
        "download_data.py",
        "clean_data.py",
        "feature_engineering.py",
        "load_data.py"
    ]
    
    # Optional: "load_data.py" will be added once database type is finalized.
    
    for script in scripts:
        run_script(script)
        
    print("\nPipeline execution finished successfully.")

if __name__ == "__main__":
    main()
