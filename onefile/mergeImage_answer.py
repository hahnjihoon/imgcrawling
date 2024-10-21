from PIL import Image
import os
from collections import defaultdict

def merge_answer(param):
    print('start', param)

    # 파일이 저장된 경로에서 파일 목록 불러오기
    file_names = sorted([f for f in os.listdir(param) if f.endswith('.png')])

    print('-------------', file_names)

    # 파일명을 그룹화 (_ 기준으로 앞부분이 동일한 파일끼리)
    grouped_files = defaultdict(list)
    for file in file_names:
        group_key = file.split('_')[0]  # _ 앞부분을 기준으로 그룹화
        grouped_files[group_key].append(file)

    # 각 그룹에 대해 이미지 병합 수행
    for group_key, files in grouped_files.items():
        # 파일을 열고 이미지 리스트에 담음
        images = [Image.open(os.path.join(param, f)) for f in files]

        # 이미지 크기 계산 (세로 병합이므로 넓이는 가장 넓은 이미지, 높이는 모든 이미지의 높이 합)
        total_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)

        # 병합할 새 이미지 생성
        merged_image = Image.new('RGB', (total_width, total_height))

        # 이미지를 세로로 병합
        y_offset = 0
        for img in images:
            merged_image.paste(img, (0, y_offset))
            y_offset += img.height

        # 병합된 이미지 저장 (각 그룹별로)
        output_path = os.path.join(param, f'{group_key}_merge_answer.png')
        merged_image.save(output_path)

        print(f'Merged image for group {group_key} saved as {output_path}')

if __name__ == "__main__":
    c = "C:/Users/Rainbow Brain/Desktop/merge_test_2"
    merge_answer(c)

