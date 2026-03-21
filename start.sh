# go to script directory (safe if launched from elsewhere)
cd /c/Users/markj/source/repos/Python_Camino_BE

# activate virtual environment (edit path if needed)
source venv/bin/activate

# start FastAPI
uvicorn src.app.main:app --reload