import os, json
from pydub import AudioSegment

def crop_sound_with_json(wav_file_path, json_file_path, output_dir):
    # 오디오 파일 로드
    audio = AudioSegment.from_wav(wav_file_path)

    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)['annotation']

    # 오디오 파일 자르기
    count = 0
    for item in data:
        start_time = item['startTime'] * 1000 # 초를 밀리초로 변환
        end_time = item['endTime'] * 1000 # 초를 밀리초로 변환
        duration = end_time - start_time
        if duration < 400:
            start_time = max(0, start_time - 500)
            end_time = max(1000, end_time + 500)
        elif duration < 800:
            start_time = max(0, start_time - 300)
            end_time = max(1000, end_time + 300)
        cropped_audio = audio[start_time:end_time]
        os.makedirs(os.path.join(output_dir, item['labelText']), exist_ok=True)
        output_path = os.path.join(output_dir, item['labelText'], f"{os.path.basename(wav_file_path).split('.')[0]}_{count}.wav")
        cropped_audio.export(output_path, format='wav')
        count += 1

    print(f"{os.path.basename(wav_file_path)} 처리 완료")
        
if __name__ == "__main__":
    data_types = ['Validation', 'Training']
    for data_type in data_types:
        wav_file_dir = f'/ai_hub_data/{data_type}/011.wav변환'
        json_file_dir = f'/ai_hub_data/{data_type}/02.라벨링데이터'
        output_dir = f'/ai_hub_data/{data_type}/03.cropped음원'
        os.makedirs(output_dir, exist_ok=True)
        for dir in os.listdir(wav_file_dir):
            for file in os.listdir(os.path.join(wav_file_dir, dir)):
                if file.endswith('.wav'):
                    wav_file_path = os.path.join(wav_file_dir, dir, file)
                    json_file_path = os.path.join(json_file_dir, f"{dir}_label".replace('S', 'L'), file.replace('.wav', '.json'))
                    crop_sound_with_json(wav_file_path, json_file_path, output_dir)