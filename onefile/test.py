import os
import re
from PIL import Image


def merge(param):
    print(param)

    location = param

    files = os.listdir(location)

    file_groups = {}

    pattern = re.compile(r'수집\[(\d+)\](\d+)')

    for file in files:
        match = pattern.match(file)
        if match:
            group_num = match.group(1)
            file_num = int(match.group(2))  # 숫자 부분을 정수로 변환하여 정렬 가능하도록 합니다.
            if group_num not in file_groups:
                file_groups[group_num] = []
            file_groups[group_num].append((file_num, file))  # 파일 번호와 파일명을 함께 저장

    for group, files in file_groups.items():
        # 파일 번호 기준으로 정렬
        files.sort(key=lambda x: x[0])

        images = []
        total_height = 0
        max_width = 0

        for _, file in files:
            file_path = os.path.join(location, file)
            try:
                img = Image.open(file_path).convert('RGB')  # 모든 이미지를 RGB로 변환
                images.append(img)
                total_height += img.height
                max_width = max(max_width, img.width)
            except Exception as e:
                print(f"Error opening {file_path}: {e}")

        concatenated_image = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for img in images:
            concatenated_image.paste(img, (0, y_offset))
            y_offset += img.height

        output_file_path = os.path.join(location, f'수집{group}.jpg')
        concatenated_image.save(output_file_path)

if __name__ == "__main__":
    c = "C:/Users/Rainbow Brain/Desktop/imgdir"
    merge(c)