import argparse  # argparse 모듈을 사용하여 명령줄 인수를 처리
import base64  # base64 모듈을 사용하여 이미지를 Base64로 인코딩 및 디코딩
import os  # os 모듈을 사용하여 파일 경로 및 파일 존재 여부 확인

# 이미지 파일을 Base64 문자열로 인코딩하는 함수
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:  # 이미지 파일을 바이너리 읽기 모드로 열기
        encoded_string = base64.b64encode(image_file.read())  # 파일 내용을 Base64로 인코딩
    return encoded_string.decode('utf-8')  # 인코딩된 문자열을 UTF-8로 디코딩하여 반환

# Base64 문자열을 파일에 저장하는 함수
def save_base64_to_file(base64_string, output_path):
    with open(output_path, "w") as file:  # 지정된 경로에 파일을 쓰기 모드로 열기
        file.write(base64_string)  # Base64 문자열을 파일에 쓰기

# Base64 문자열을 이미지 파일로 디코딩하는 함수
def base64_to_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string)  # Base64 문자열을 디코딩하여 바이너리 데이터로 변환
    with open(output_path, "wb") as image_file:  # 출력 경로에 바이너리 쓰기 모드로 파일 열기
        image_file.write(image_data)  # 디코딩된 바이너리 데이터를 파일에 쓰기
    return output_path  # 저장된 파일의 경로 반환

# 스크립트의 메인 부분
if __name__ == "__main__":
    # 명령줄 인수 파서를 설정
    parser = argparse.ArgumentParser(description="Encode or Decode images to/from Base64")
    parser.add_argument("action", choices=["encode", "decode"], help="Specify whether to encode or decode an image")
    parser.add_argument("input_path", help="Path to the input file (image for encode, base64 text file for decode)")
    parser.add_argument("--output_path", help="Path to the output file (required for decode)")

    # 명령줄 인수를 파싱
    args = parser.parse_args()

    # 인코딩 작업 처리
    if args.action == "encode":
        if not os.path.exists(args.input_path):  # 입력 파일 존재 여부 확인
            print("Error: The input file does not exist.")  # 파일이 존재하지 않으면 오류 메시지 출력
        else:
            base64_string = image_to_base64(args.input_path)  # 이미지 파일을 Base64로 인코딩
            output_path = f"{os.path.splitext(args.input_path)[0]}_result.txt"  # 출력 파일 경로 설정
            save_base64_to_file(base64_string, output_path)  # Base64 문자열을 파일에 저장
            print(f"Base64 string saved to: {output_path}")  # 결과 메시지 출력

    # 디코딩 작업 처리
    elif args.action == "decode":
        if not args.output_path:  # 출력 경로가 제공되지 않은 경우
            print("Error: output_path is required for decoding")  # 오류 메시지 출력
        else:
            if not os.path.exists(args.input_path):  # 입력 파일 존재 여부 확인
                print("Error: The input file does not exist.")  # 파일이 존재하지 않으면 오류 메시지 출력
            else:
                with open(args.input_path, "r") as file:  # Base64 텍스트 파일을 읽기 모드로 열기
                    base64_string = file.read()  # 파일 내용을 읽어서 문자열로 저장
                saved_path = base64_to_image(base64_string, args.output_path)  # Base64 문자열을 이미지 파일로 디코딩
                print(f"Image saved to: {saved_path}")  # 결과 메시지 출력

# 명령줄에서 스크립트를 실행하는 예시:
# python onefile/imgEnDecoding.py encode "C:/Users/Rainbow Brain/Desktop/test.jpg"
# python onefile/imgEnDecoding.py decode "C:/Users/Rainbow Brain/Desktop/test_result.txt" --output_path "C:/Users/Rainbow Brain/Desktop/ai_result.jpg"
