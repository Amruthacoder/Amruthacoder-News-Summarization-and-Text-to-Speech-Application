import subprocess

def run_fastapi():
    subprocess.Popen(["uvicorn", "api:app", "--reload"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    run_fastapi()
    run_streamlit()