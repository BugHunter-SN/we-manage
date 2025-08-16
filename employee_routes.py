from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from database import supabase, SUPABASE_BUCKET, SUPABASE_URL
from models import EmployeeCreate, EmployeeUpdate
from forms import as_form
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="./employee_repo/templates")

@router.get("/", response_class=HTMLResponse)
async def read_employees(request: Request):
    response = supabase.table('employees').select('*').eq('is_active', True).execute()
    employees = response.data
    return templates.TemplateResponse('index.html', {"request": request, "employees": employees})

@router.get("/add", response_class=HTMLResponse)
async def add_employee_form(request: Request):
    return templates.TemplateResponse('add_employee.html', {"request": request})

@router.post("/add")
async def add_employee(
    request: Request,
    employee: EmployeeCreate = Depends(EmployeeCreate.as_form),
    image: UploadFile = File(None)
):
    image_url = None
    if image and image.filename != "":
        image_filename = f"{employee.first_name}_{employee.last_name}_{image.filename}"
        file_content = await image.read()
        
        try:
            # Upload file to Supabase storage
            response = supabase.storage.from_(SUPABASE_BUCKET).upload(image_filename, file_content)
            
            # Check if upload was successful
            # Supabase storage upload returns different response structure
            if not hasattr(response, 'error') or response.error is None:
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{image_filename}"
            else:
                # Handle upload error - you can choose to continue without image or raise an exception
                print(f"Image upload failed: {response.error}")
                # Optionally raise an exception if image is required
                # raise HTTPException(status_code=400, detail=f"Image upload failed: {response.error}")
        except Exception as e:
            print(f"Storage error: {str(e)}")
            # Optionally handle storage errors
            # raise HTTPException(status_code=400, detail=f"Storage error: {str(e)}")
    
    # Insert employee data
    try:
        result = supabase.table("employees").insert({
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'salary': employee.salary,
            'image_url': image_url
        }).execute()
        
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create employee")
            
    except Exception as e:
        # If database insert fails and we uploaded an image, you might want to clean it up
        if image_url:
            try:
                supabase.storage.from_(SUPABASE_BUCKET).remove([image_filename])
            except:
                pass  # Ignore cleanup errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return RedirectResponse("/", status_code=303)

@router.get("/edit/{employee_id}", response_class=HTMLResponse)
async def edit_employee_form(request: Request, employee_id: int):
    response = supabase.table('employees').select('*').eq('id', employee_id).single().execute()
    employee = response.data
    return templates.TemplateResponse('edit_employee.html', {"request": request, "employee": employee})

@router.post("/edit/{employee_id}")
async def edit_employee(
    request: Request,
    employee_id: int,
    employee: EmployeeUpdate = Depends(EmployeeUpdate.as_form),
    image: UploadFile = File(None)
):
    update_data = {}
    
    # Only update fields that are provided
    if employee.first_name:
        update_data['first_name'] = employee.first_name
    if employee.last_name:
        update_data['last_name'] = employee.last_name
    if employee.email:
        update_data['email'] = employee.email
    if employee.salary:
        update_data['salary'] = employee.salary
    
    # Handle image upload if provided
    if image and image.filename != "":
        image_filename = f"{employee.first_name or 'employee'}_{employee.last_name or 'update'}_{image.filename}"
        file_content = await image.read()
        
        try:
            # Upload file to Supabase storage
            response = supabase.storage.from_(SUPABASE_BUCKET).upload(image_filename, file_content)
            
            # Check if upload was successful
            if not hasattr(response, 'error') or response.error is None:
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{image_filename}"
                update_data['image_url'] = image_url
            else:
                # Handle upload error
                print(f"Image upload failed: {response.error}")
                # Optionally raise an exception if image update is critical
                # raise HTTPException(status_code=400, detail=f"Image upload failed: {response.error}")
        except Exception as e:
            print(f"Storage error: {str(e)}")
            # Optionally handle storage errors
            # raise HTTPException(status_code=400, detail=f"Storage error: {str(e)}")
    
    # Update employee
    try:
        result = supabase.table("employees").update(update_data).eq('id', employee_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Employee not found or update failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return RedirectResponse("/", status_code=303)

@router.post("/deactivate/{employee_id}")
async def deactivate_employee(employee_id: int):
    try:
        result = supabase.table("employees").update({'is_active': False}).eq('id', employee_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Employee not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return RedirectResponse("/", status_code=303)