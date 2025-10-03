from fastapi import APIRouter, UploadFile, HTTPException, status
from data.s3_client import S3Client


router = APIRouter(prefix="/users")
s3 = S3Client(secret_key='b257586363994a4592d8a305fa5880b3',
              access_key='23de8ea4cc42439d95d8c16fb649455e',
              bucket_name='cloud-storage',
              endpoint_url='https://s3.aestheticperforator.ru')

@router.get("/get_users")
async def get_users():
    return {"users": 'bam'}

@router.get("/get_user_files")
async def get_user_files():
    return {"user": "files..."}

@router.post("/upload_file")
async def upload_file(file: UploadFile | None = None):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не найден")

    file_name = file.filename
    file_data = await file.read(10 * 1024 * 1024)
    print(file_name)
    upload = await s3.upload_file(file_name, file_data)
    if upload:
        return {"status": "ok", "data": f"Файл {file_name} успешно загружен в облако"}
    else:
        return {"status": "failed", "data": f"Файл {file_name} неудалось загрузить в облако"}
    
@router.post("/upload_file_html")
async def upload_file(file: UploadFile | None = None):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не найден")

    file_name = file.filename
    file_data = await file.read(10 * 1024 * 1024)
    print(file_name)
    upload = await s3.upload_custom_file(file_name, file_data)
    if upload:
        return {"status": "ok", "data": f"Файл {file_name} успешно загружен в облако"}
    else:
        return {"status": "failed", "data": f"Файл {file_name} неудалось загрузить в облако"}