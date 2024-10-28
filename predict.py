import librosa, numpy as np
from model.mobilenet_mfcc import mobilenet_v2_mfcc
import torch, time, os

# wav 파일을 MFCC로 변환하는 함수
def wav_to_mfcc(file_path, n_mfcc=40, max_len=100):
    y, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    # MFCC의 길이를 max_len으로 맞추기
    if mfcc.shape[1] < max_len:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_len - mfcc.shape[1])), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]
    
    return mfcc

def predict_single_file(file_path, model, class_names, device='cuda'):
    """단일 WAV 파일에 대한 예측을 수행합니다."""
    # 오디오 파일 로드 및 MFCC 변환
    mfcc = wav_to_mfcc(file_path)
    
    # MFCC를 모델 입력 형식으로 변환
    mfcc = np.expand_dims(mfcc, axis=(0, 1))  # (1, 1, n_mfcc, max_len) 형태로 변환
    mfcc_tensor = torch.FloatTensor(mfcc).to(device)
    
    # 예측 수행
    model.eval()
    with torch.no_grad():
        outputs = model(mfcc_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
    
    # 결과 반환
    predicted_label = class_names[predicted_class]
    confidence = probabilities[0][predicted_class].item()
    
    return predicted_label, confidence


# 모델 로딩
def load_model(num_classes = 17):   
    model = mobilenet_v2_mfcc(num_classes=num_classes)
    model.load_state_dict(torch.load('model/best_mobilenet_mfcc_model.pth'))
    # GPU 사용 가능 시 GPU로 모델 이동
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    return model, device

class_names = ['가구끄는소리',
 '강아지짓는소리',
 '고양이우는소리',
 '골프퍼팅(골굴리는소리)',
 '드럼세탁기소리',
 '런닝머신에서뛰는소리',
 '망치질소리',
 '문여닫는소리',
 '바이올린연주소리',
 '샤워할때물소리',
 '식기세척기소리',
 '아이들발걸음소리',
 '어른발걸음소리',
 '진공청소기소리',
 '통돌이세탁기소리',
 '피아노연주소리',
 '화장실물내리는소리']

# 예측
if __name__ == "__main__":  
    model, device = load_model()
    wavpath = './ai_hub_data/Validation/04.balanced_cropped음원/강아지짓는소리/N-10_221015_A_5_a_17064_1.wav'
    stime = time.time()
    count = 0
    target_dir = './not_home_noise_sound/normal'
    for file in os.listdir(target_dir):
        if file.endswith('wav'):
            wavpath = os.path.join(target_dir, file)
            count += 1
            predicted_label, confidence = predict_single_file(wavpath, model, class_names, device)
            if confidence < 0.6:
                # print(time.time()-stime)
                print(file)
                print(f"Predicted class: {predicted_label}")
                print(f"Confidence: {confidence:.2f}")
            if count == 50:
                break
