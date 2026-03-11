from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from ord_api import create_erid
from vk_api import publish_post, upload_photo

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/publish")
async def publish(
    text: str = Form(...),
    link: str = Form(...),
    kktu: str = Form(...),
    ord_key: str = Form(...),
    vk_token: str = Form(...),
    owner_id: str = Form(...),
    image: UploadFile = File(None)
):

    erid_data = create_erid(ord_key, text, link, kktu)

    if "error" in erid_data:
        return {"error": erid_data["error"]}

    erid = erid_data["erid"]

    final_text = f"Реклама. ERID: {erid}\n\n{text}\n{link}"

    attachment = None

    if image:
        image_bytes = await image.read()
        attachment = upload_photo(
            vk_token,
            owner_id,
            ("image.jpg", image_bytes)
        )

    vk_result = publish_post(
        vk_token,
        owner_id,
        final_text,
        attachment
    )

    return {
        "erid": erid,
        "vk_result": vk_result
    }
