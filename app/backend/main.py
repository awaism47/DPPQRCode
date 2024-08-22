from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import pandas as pd
import qrcode
import os
import uuid
from fastapi.responses import JSONResponse
from typing import  Optional
from app.backend.services.data_processing_services import read_csv, get_column_headers, map_csv_to_model
from app.backend.schemas.dpp import DigitalProductPassport1

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
# Serve QR code images
app.mount("/qr-codes", StaticFiles(directory="app/backend/qr_codes"), name="qr-codes")
templates = Jinja2Templates(directory="app/frontend/templates")

# Temp directory for storing uploaded files
TEMP_DIR = "app/backend/temp"
Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

# Directory to store generated QR codes
QR_CODE_DIR = "app/backend/qr_codes"
Path(QR_CODE_DIR).mkdir(parents=True, exist_ok=True)

DPP_SCHEMA = DigitalProductPassport1

@app.get("/")
def upload_file(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/map-columns/")
async def map_columns(request: Request, file: UploadFile = File(...)):
    file_location = f"{TEMP_DIR}/{file.filename}"
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    
    df = read_csv(file_location)
    csv_columns = get_column_headers(df)
    model_fields = DigitalProductPassport1.model_fields.keys()
    
    return templates.TemplateResponse("map.html", {
        "request": request, 
        "csv_columns": csv_columns, 
        "model_fields": model_fields,
        "file_path": file_location
    })


@app.post("/generate-json/")
async def generate_json(
    request: Request,
    file_path: str = Form(...),
    metadata: Optional[str] = Form(None),
    characteristics: Optional[str] = Form(None),
    commercial: Optional[str] = Form(None),
    identification: Optional[str] = Form(None),
    sources: Optional[str] = Form(None),
    materials: Optional[str] = Form(None),
    handling: Optional[str] = Form(None),
    additionalData: Optional[str] = Form(None),
    operation: Optional[str] = Form(None),
    sustainability: Optional[str] = Form(None)
):
    # Print for debugging
    print("Metadata received:", metadata)
    print("Characteristics received:", characteristics)

    # Collect the mappings from the form
    mappings = {
        "metadata": metadata,
        "characteristics": characteristics,
        "commercial": commercial,
        "identification": identification,
        "sources": sources,
        "materials": materials,
        "handling": handling,
        "additionalData": additionalData,
        "operation": operation,
        "sustainability": sustainability,
    }

    # Clean up mappings to remove any fields that weren't mapped
    #mappings = {k: v for k, v in mappings.items() if v}

    # Read the CSV
    df = read_csv(file_path)

    # Map the CSV data to the DigitalProductPassport model using the provided mappings
    product_models = map_csv_to_model(df, mappings)

    products_json = []

    for product in product_models:
        product_json = product.model_dump_json()

        # Generate a unique ID for the product
        product_id = str(uuid.uuid4())

        # Save the JSON to a file (optional)
        json_file_path = os.path.join(QR_CODE_DIR, f"{product_id}.json")
        with open(json_file_path, "w") as json_file:
            json_file.write(product_json)

        # Generate a URL that points to the JSON data
        json_url = request.url_for("get_product_json", product_id=product_id)

        # Generate a QR code for the JSON URL
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(product_json)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code image
        qr_code_path = os.path.join(QR_CODE_DIR, f"{product_id}.png")
        img.save(qr_code_path)

        products_json.append({
            "json": product_json,
            "qr_code_path": qr_code_path
        })

    # Render the JSON and QR codes in the template
    return templates.TemplateResponse("displayjson.html", {
        "request": request,
        "products": products_json
    })

@app.get("/product/{product_id}/json")
async def get_product_json(product_id: str):
    json_file_path = os.path.join(QR_CODE_DIR, f"{product_id}.json")
    if not os.path.exists(json_file_path):
        return JSONResponse(status_code=404, content={"message": "Product not found"})
    
    with open(json_file_path, "r") as json_file:
        product_json = json_file.read()

    return JSONResponse(content=product_json)