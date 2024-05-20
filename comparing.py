import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
#OpenCV 버전 4부터는 findContours()가 값을 두 개만 리턴.
#버전 3에서는 값을 세 개 리턴하고요.
#지금사용하는건 4.9.0.80

#히스토그램
def compare(image1_path, image2_path):
    # print('비교시작')
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # img = cv2.imread(image2_path)
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # 이미지와 히스토그램 그리기
    # plt.subplot(121), plt.imshow(img, 'gray')
    # plt.title('Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.plot(hist)
    # plt.title('Histogram'), plt.xlim([0, 256])
    # plt.show()

    # 이미지 크기 조정
    image1 = cv2.resize(image1, (600, 600))
    image2 = cv2.resize(image2, (600, 600))

    # 이미지를 그레이스케일로 변환
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 히스토그램 계산
    hist1 = cv2.calcHist([image1_gray], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([image2_gray], [0], None, [256], [0, 256])

    # 히스토그램 비교 값 리턴
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

   ##################################################################################################################
    # 이미지마킹로직
    diff = cv2.absdiff(image1_gray, image2_gray) #두이미지 절대차이값, 0부터 높을수록 차이남
    _, diff = cv2.threshold(diff, 150, 255, cv2.THRESH_BINARY_INV) #설정한임계값이니까 150으로 설정하면 절대값차이값이 151부터 255(검정)으로 표시
    cv2.imshow("차이를검정으로표시", diff)
    cv2.waitKey(0)

    coordinates = np.column_stack(np.where(diff == 0))
    for i, j in coordinates:
        image1[i, j] = [0, 0, 255]
        image2[i, j] = [0, 0, 255]
    cv2.imshow("원본사진차이 빨강색으로", image1)
    cv2.imshow("비교사진차이 빨강색으로", image2)
    cv2.waitKey(0)

    ###################################################################################
    # 차이 이미지에서 윤곽선 찾기
    diffnemo = cv2.absdiff(image1_gray, image2_gray)  # 두이미지 절대차이값, 0부터 높을수록 차이남
    _, diffnemo = cv2.threshold(diffnemo, 150, 255, cv2.THRESH_BINARY)  # 설정한임계값이니까 150으로 설정하면 절대값차이값이 151부터 255(검정)으로 표시
    contours, _ = cv2.findContours(diffnemo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 이미지에 윤곽선
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 200, 0), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 200, 0), 2)

    diff_marked = np.zeros_like(image1)
    diff_marked[diff != 0] = image1[diff != 0]

    cv2.imshow("Image 1 with differences", image1)
    cv2.imshow("Image 2 with differences", image2)
    cv2.waitKey(0) #키보드아무거나누르는거
    cv2.destroyAllWindows() #누르면 창닫아라
    ##################################################################################################################

    return similarity


# 현재안씀
def compare_images(image1_path, image2_path): #컨투어로비교시 0이면 같은것 숫자가 높아질수록 다른것
    # 이미지 파일을 그레이 스케일로 읽어옴
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # image1 = cv2.resize(image1, (300, 300))
    # image2 = cv2.resize(image2, (300, 300))
    print("컨투어1의 크기:", image1.shape)
    print("컨투어2의 크기:", image2.shape)

    # 이미지의 윤곽선을 찾기 위해 컨투어를 찾음
    contours1, _ = cv2.findContours(image1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(image2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 컨투어의 유사도를 비교
    # similarity = cv2.matchShapes(contours1[0], contours2[0], cv2.CONTOURS_MATCH_I1, 0)
    if len(contours1) > 0 and len(contours2) > 0:
        # 컨투어의 유사도를 비교
        similarity = cv2.matchShapes(contours1[0], contours2[0], cv2.CONTOURS_MATCH_I1, 0)
        return similarity
    else:
        return "컨투어를 찾을 수 없습니다."

    # return similarity


image1_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/originimg.PNG'
image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/image2.PNG'
# image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/image0.jpg'
# image1_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/gotqks.jpg'
# image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/gotqks2.jpg'
# image1_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/gotqksorigin.jpg'
# image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/gotqks3.PNG'
# image1_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/hot(599x801).PNG'
# image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/hot(608x803).PNG'
# image1_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/image1.PNG'
# image2_path = 'C:/Users/Rainbow Brain/Desktop/comparetest/image1.PNG'

similarity_score = compare(image1_path, image2_path)
# similarity_score2 = compare_images(image1_path, image2_path)

similarity_percent = (similarity_score + 1) * 50
# similarity_percent2 = (1 - similarity_score) * 100

print(f"히스토그램 유사도: {similarity_score}")
print(f"히스토그램 퍼센트: {similarity_percent:.2f}%")
# 1에 가까울수록 두 이미지가 유사함
# -1에 가까울수록 두 이미지가 서로 다름
# 0은 무작위한 이미지이거나 완전히 다른 이미지
# print(f"컨투어 유사도: {similarity_score2}")
# print(f"컨투어 퍼센트: {similarity_percent2:.2f}%")