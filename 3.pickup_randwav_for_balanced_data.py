import os, random, shutil

def random_sample(lst, n):
    """
    주어진 리스트에서 n개의 요소를 무작위로 선택하여 새로운 리스트를 반환합니다.
    
    Args:
        lst (list): 원본 리스트
        n (int): 선택할 요소의 개수
        
    Returns:
        list: 무작위로 선택된 n개의 요소로 구성된 새로운 리스트
    """
    if n > len(lst):
        raise ValueError("선택할 요소의 개수가 원본 리스트의 길이보다 큽니다.")
    
    result = random.sample(lst, n)
    return result
        
        
# if __name__ == "__main__":
#     data_types = ['Validation', 'Training']
#     for data_type in data_types:
#         input_dir = f'/ai_hub_data/{data_type}/03.cropped음원'
#         output_dir = f'/ai_hub_data/{data_type}/04.balanced_cropped음원'
#         os.makedirs(output_dir, exist_ok=True)
#         for cls in os.listdir(input_dir):
#             files = os.listdir(os.path.join(input_dir, cls))
#             if data_type == 'Training':
#                 target_samples = 900
#             else:
#                 target_samples = 100
#             if len(files) < target_samples:
#                 continue
#             selected_files = random_sample(files, target_samples)
#             for file in selected_files:
#                 os.makedirs(os.path.join(output_dir, cls), exist_ok=True)
#                 src = os.path.join(input_dir, cls, file)
#                 dst = os.path.join(output_dir, cls, file)
#                 shutil.copy(src, dst)
                
if __name__ == "__main__":
    input_dir = './not_home_noise_sound/normal'
    output_dir = './test_data/noise_or_not/not_noise'
    files = os.listdir(os.path.join(input_dir))
    target_samples = 50
    selected_files = random_sample(files, target_samples)
    for file in selected_files:
        src = os.path.join(input_dir, file)
        dst = os.path.join(output_dir, file)
        shutil.copy(src, dst)