import base64  # base64 모듈을 사용하여 이미지를 Base64로 인코딩 및 디코딩
import os
import sys


# 이미지 파일을 Base64 문자열로 인코딩하고 결과를 파일에 저장하는 함수
def image_to_base64_and_save(image_path):
    with open(image_path, "rb") as image_file:  # 이미지 파일을 바이너리 읽기 모드로 열기
        encoded_string = base64.b64encode(image_file.read())  # 파일 내용을 Base64로 인코딩
    base64_string = encoded_string.decode('utf-8')  # 인코딩된 문자열을 UTF-8로 디코딩하여 저장

    output_path = f"{os.path.splitext(image_path)[0]}_base64.txt"  # 출력 파일 경로 설정
    with open(output_path, "w") as file:  # 지정된 경로에 파일을 쓰기 모드로 열기
        file.write(base64_string)  # Base64 문자열을 파일에 쓰기

    print(f"Base64 string saved to: {output_path}")  # 결과 메시지 출력

# def base64_to_image(base64_string, output_path):
#     image_data = base64.b64decode(base64_string)  # Base64 문자열을 디코딩하여 바이너리 데이터로 변환
#     with open(output_path, "wb") as image_file:  # 출력 경로에 바이너리 쓰기 모드로 파일 열기
#         image_file.write(image_data)  # 디코딩된 바이너리 데이터를 파일에 쓰기
#     return output_path  # 저장된 파일의 경로 반환

# 예시 함수 호출
# image_to_base64_and_save("C:/Users/Rainbow Brain/Desktop/test.jpg")


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print('cli 아규먼트 다시확인')

    a = sys.argv[0] #실행파일
    b = sys.argv[1] #인코드인지 디코드인지
    c = sys.argv[2] #이미지경로 || txt경로 || base64문자열
    d = sys.argv[3] #디코딩일때만 저장경로
    print('인자 :: ', a)
    print('인자 :: ', b)
    print('인자 :: ', c)
    print('인자 :: ', d)

    if b == "encode":
        image_to_base64_and_save(c)
    elif b == "decode":
        print('dd')
        # base64_to_image(c, d)

# python onefile/imgende.py encode "C:/Users/Rainbow Brain/Desktop/test.jpg"
# python onefile/imgende.py decode "C:/Users/Rainbow Brain/Desktop/test_result.txt" "C:/Users/Rainbow Brain/Desktop/comp_result.jpg"



def base64_to_image(info):
    base64_string = info[0]
    output_path = info[1]
    image_data = base64.b64decode(base64_string)  # Base64 문자열을 디코딩하여 바이너리 데이터로 변환

    directory, file_name = os.path.split(output_path)
    file_name_only, file_extension = os.path.splitext(file_name)
    output_file_name = f"{file_name_only}_result{file_extension}"
    output_path = os.path.join(directory, output_file_name)

    with open(output_path, "wb") as image_file:  # 출력 경로에 바이너리 쓰기 모드로 파일 열기
        image_file.write(image_data)  # 디코딩된 바이너리 데이터를 파일에 쓰기

    return output_path  # 저장된 파일의 경로 반환