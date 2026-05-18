from fastapi.templating import Jinja2Templates

# Initialize templates here to avoid circular imports with main.py
templates = Jinja2Templates(directory="app/templates")
