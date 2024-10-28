import os
from pydub import AudioSegment
from tqdm import tqdm

def convert_wav_files(input_dir, output_dir):
    # 출력 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 입력 디렉토리의 모든 WAV 파일 처리
    for root, dirs, files in os.walk(input_dir):
        for file in tqdm(files):
            if file.endswith('.wav') and 'A' in file:
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)

                # 출력 파일의 디렉토리가 없으면 생성
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    # WAV 파일 로드
                    audio = AudioSegment.from_wav(input_path)

                    # 16비트, 모노, 16kHz로 변환
                    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

                    # 변환된 파일 저장
                    audio.export(output_path, format='wav')
                except Exception as e:
                    print(f"오류 발생: {input_path} - {str(e)}")

# 사용 예
input_directory = 'ai_hub_data/Training/01.원천데이터'
output_directory = 'ai_hub_data/Training/011.wav변환'
convert_wav_files(input_directory, output_directory)