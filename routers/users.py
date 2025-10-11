from fastapi import APIRouter, UploadFile, HTTPException, status, Response, Cookie
from uuid import uuid4
from data.s3_client import S3Client


KB = 1024
MB = KB * 1024
GB = MB * 1024
ALLOWED_FILE_EXTENSION = ["mov", "mp4", "mkv"]

router = APIRouter(prefix="/users")
s3 = S3Client(secret_key='b257586363994a4592d8a305fa5880b3',
              access_key='23de8ea4cc42439d95d8c16fb649455e',
              bucket_name='cloud-storage',
              endpoint_url='https://s3.aestheticperforator.ru')



@router.post("/upload_file")
async def upload_file(response: Response, token: str | None = Cookie(default=None), file: UploadFile | None = None):

    if token == None:
        token = uuid4()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не найден")
    
    if not file.filename.split(".")[-1] in ALLOWED_FILE_EXTENSION:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Файл не правильного формата")

    file_name = file.filename
    file_data = await file.read(10 * MB)
    upload = await s3.upload_file(file_name, file_data, token)
    if upload:
        response.set_cookie("user_id", f"{token}")
        return {"status": "ok", "data": f"Файл {file_name} успешно загружен в облако"}
    else:
        return {"status": "failed", "data": f"Файл {file_name} неудалось загрузить в облако"}


@router.get("/get_files/metadata")
async def get_files(token: str | None = Cookie(default=None)):
    if token != None:
        objects = await s3.get_objects(token)
        files_data = []
        for obj in objects.get("Contents", []):
            key = obj["Key"]
            async with s3.get_client() as client:
                head = await client.head_object(Bucket=s3.bucket_name, Key=key)
                obj["Metadata"] = head.get("Metadata", {})
                files_data.append(obj)
        return {"response": {"data": files_data}}
    else:
        return {"У вас нет файлов"}

@router.get("/get_files/")
async def get_files(token: str | None = Cookie(default=None)):
    if token != None:
        objects = await s3.get_objects(token)
        return {"response": {"data": objects}}
    else:
        return {"У вас нет файлов"}