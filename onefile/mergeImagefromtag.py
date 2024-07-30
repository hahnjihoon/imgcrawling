import os
import re
from PIL import Image

def merge(param):
    location = param[0]

    files = os.listdir(location)

    file_groups = {}

    pattern = re.compile(r'수집\[(\d+)\]\d+')

    for file in files:
        match = pattern.match(file)
        if match:
            group_num = match.group(1)
            if group_num not in file_groups:
                file_groups[group_num] = []
            file_groups[group_num].append(file)

    for group, files in file_groups.items():
        images = []
        for file in files:
            file_path = os.path.join(location, file)
            img = Image.open(file_path)
            images.append(img)

        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)

        concatenated_image = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for img in images:
            concatenated_image.paste(img, (0, y_offset))
            y_offset += img.height

        output_file_path = os.path.join(location, f'수집{group}.jpg')
        concatenated_image.save(output_file_path)


if __name__ == "__main__":

    c = "D:/RPA/GS_Home/03.Output/20240729/1.수집이미지/고메통등심돈카츠 450g 3봉"

    param = [c]

    merge(param)
