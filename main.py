from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import employee_routes

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Employee Management System", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="./employee_repo/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="./employee_repo/templates")

# Include routers
app.include_router(employee_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

