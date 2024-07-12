import base64  # base64 모듈을 사용하여 이미지를 Base64로 인코딩 및 디코딩
import os  # os 모듈을 사용하여 파일 경로 및 파일 존재 여부 확인


# 이미지 파일을 Base64 문자열로 인코딩하는 함수
def image_to_base64(info):
    try:
        image_path = info[0]
        with open(image_path, "rb") as image_file:  # 이미지 파일을 바이너리 읽기 모드로 열기
            encoded_string = base64.b64encode(image_file.read())  # 파일 내용을 Base64로 인코딩
            return encoded_string.decode('utf-8')  # 인코딩된 문자열을 UTF-8로 디코딩하여 반환
    except FileNotFoundError:
        print(f"오류: 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        return None  # 파일이 없을 경우 None 반환
    except Exception as e:
        print(f"오류: 예기치 않은 오류가 발생했습니다: {e}")
        return None  # 그 외 예외 처리
    finally:
        # 파일 처리가 끝나면 항상 실행되는 코드
        print("이미지를 Base64로 변환하는 작업이 완료되었습니다.")


def base64_to_image(info):
    try:
        image_path = info[0]
        base64_string = info[1]

        # Base64 문자열을 디코딩하여 바이너리 데이터로 변환
        image_data = base64.b64decode(base64_string)

        # 출력 경로에서 디렉토리와 파일 이름 분리
        directory, file_name = os.path.split(image_path)
        # 파일 이름에서 확장자 분리
        file_name_only, file_extension = os.path.splitext(file_name)
        # 새로운 파일 이름 생성
        image_file_name = f"{file_name_only}_result{file_extension}"
        # 새로운 출력 경로 설정
        image_path = os.path.join(directory, image_file_name)

        # 출력 경로에 바이너리 쓰기 모드로 파일 열기
        with open(image_path, "wb") as image_file:
            # 디코딩된 바이너리 데이터를 파일에 쓰기
            image_file.write(image_data)

        # 저장된 파일의 경로 반환
        return image_path

    except FileNotFoundError:
        print(f"오류: 파일을 저장할 디렉토리 '{directory}'가 존재하지 않습니다.")
        return None

    except Exception as e:
        print(f"오류: 예기치 않은 오류가 발생했습니다: {e}")
        return None

    finally:
        # 파일 처리가 끝나면 항상 실행되는 코드
        print("Base64를 이미지로 변환하는 작업이 완료되었습니다.")

##
result = image_to_base64(["C:/Users/Rainbow Brain/Desktop/22.jpg"])

if result is not None:
    print(result)  # 변환된 Base64 문자열 출력
else:
    print("이미지 변환에 실패했습니다.")

base64_to_image(["C:/Users/Rainbow Brain/Desktop/22.jpg", result])