from PIL import Image
import os

def merge_answer(param):
    path = param[0]
    file_name = param[1]
    print('start', path, file_name)

    # 파일이 저장된 경로에서 merge 파일을 제외한 파일 목록 불러오기 (png와 jpg 파일 모두 포함)
    file_names = sorted(
        [f for f in os.listdir(path) if (f.endswith('.png') or f.endswith('.jpg')) and 'merge' not in f])

    # 병합할 파일이 없다면 함수 종료
    if not file_names:
        print('병합할 파일이 없습니다.')
        return

    # 파일을 열고 이미지 리스트에 담음
    images = [Image.open(os.path.join(path, f)) for f in file_names]

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

    # 병합된 이미지 저장
    output_path = os.path.join(path, file_name)
    merged_image.save(output_path)

    # 병합에 사용된 원본 파일 삭제 (merge 파일 제외)
    for file in file_names:
        file_path = os.path.join(path, file)
        os.remove(file_path)
        print(f'병합전 파일 삭제 {file_path}')

    print(f'병합 파일 생성 완료 {output_path}')

if __name__ == "__main__":
    c = "C:/Users/Rainbow Brain/Desktop/merge_test_2323"
    d = "0005_merge.jpg"
    merge_answer([c, d])