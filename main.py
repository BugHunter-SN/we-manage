from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import employee_routes
from database import engine, Base
from models import Employee
from pathlib import Path

load_dotenv()

app = FastAPI(title="Employee Management System", version="1.0.0")

# Create templates instance with correct path
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "employee_repo" / "templates"))

# Share templates with routes module
employee_routes.templates = templates

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "employee_repo" / "static")), name="static")
app.include_router(employee_routes.router)

# @app.on_event("startup")
# def startup_event():
#     print("Creating database tables if they do not exist...")
#     Base.metadata.create_all(bind=engine)
#     print("Tables are ready.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)