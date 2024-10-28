from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from predict import class_names, predict_single_file, load_model
import os

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def filter_prediction(predicted_label, confidence):
    if predicted_label in ["드럼세탁기소리", "통돌이세탁기소리", "화장실물내리는소리"]:
        return "", 0
    elif confidence < 0.5:
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
    predicted_label, confidence = predict_single_file(file.filename, model, class_names, device)
    res, conf = filter_prediction(predicted_label, confidence)

    # 파일 삭제
    os.remove(file.filename)
    
    return {"prediction": res, "confidence": conf}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=24245)