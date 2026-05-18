from fastapi.templating import Jinja2Templates
import os

# Use absolute path so it works on Render regardless of working directory
_templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=_templates_dir)
