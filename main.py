from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my E-commerce Backend!"}

@app.get("/categories")
def get_categories():
    response = supabase.table("categories").select("*").execute()
    return response.data

@app.get("/products")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data

# --- Naya POST Route jo File Upload handle karega ---
@app.post("/products")
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...) # Yeh hamari asli photo file lega
):
    # 1. Photo ko ek unique naam dena (taaki same naam ke 2 photo crash na karein)
    unique_filename = f"{int(time.time())}_{image.filename}"
    
    # 2. Photo ko read karna
    file_bytes = await image.read()
    
    # 3. Photo ko Supabase 'product-images' bucket mein upload karna
    supabase.storage.from_("product-images").upload(
        path=unique_filename, 
        file=file_bytes, 
        file_options={"content-type": image.content_type}
    )
    
    # 4. Upload kiye hue photo ka Public URL (Link) nikalna
    image_url = supabase.storage.from_("product-images").get_public_url(unique_filename)
    
    # 5. Ab finally product ki saari details database mein save karna
    new_product = {
        "name": name,
        "description": description,
        "price": price,
        "image_url": image_url, # Yeh link ab humne khud banaya hai!
        "category_id": category_id
    }
    
    response = supabase.table("products").insert(new_product).execute()
    return response.data