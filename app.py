from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from predict import class_names, predict_single_file, load_model
from sqlmodel import Session
from database import create_db_and_tables, engine
from contextlib import asynccontextmanager
import os, time, datetime
from models import Itech_Sensings_2424, Itech_Sensings_2424Receive

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
    print("Yield done")

app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def decide_noise_level(db_value):
    
    # db_value로 노이즈 레벨을 결정
    if db_value < 34:
        noise_level = "보통"
    elif db_value < 45:
        noise_level = "주의"
    else:
        noise_level = "경고"
    
    return noise_level

def filter_prediction(predicted_label, confidence, db_max):
    # if predicted_label in ["드럼세탁기소리", "통돌이세탁기소리", "화장실물내리는소리"]:
    #     return "", 0
    # elif confidence < 0.6:
    if (confidence < 0.6) or (db_max < 20):
        return "", 0
    else:
        return predicted_label, confidence

# 모델 로드
model, device = load_model()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 파일 저장
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)
    # 예측 수행
    predicted_label, confidence, db_max = predict_single_file(file.filename, model, class_names, device)
    noise_type, conf = filter_prediction(predicted_label, confidence, db_max)
    # 파일 삭제
    os.remove(file.filename)
    return {"noise_type": noise_type, "confidence": conf, "noise_level": decide_noise_level(db_max)}

@app.post("/upload-data/{device_id}")
async def upload_data(device_id: str, data: Itech_Sensings_2424Receive):
    rec = data.dict()
    rec['device_id'] = device_id
    rec['utime'] = int(time.time())
    rec['insert_datetime'] = datetime.datetime.now()
    data = Itech_Sensings_2424(**rec)
    with Session(engine) as session:
        session.add(data)
        session.commit()
    return "ok"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=24245, reload=True, log_config="log_conf.json")