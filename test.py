from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
import numpy as np

def resize_image(imageA, imageB):
    if imageA.shape != imageB.shape:
        # 이미지 B를 이미지 A의 크기에 맞게 조정
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
    return imageB

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#                 help="first input image")
# ap.add_argument("-s", "--second", required=True,
#                 help="second")
# args = vars(ap.parse_args())

imageA = cv2.imread("C:/Users/Rainbow Brain/Desktop/comparetest/image1.PNG")
imageB = cv2.imread('C:/Users/Rainbow Brain/Desktop/comparetest/image2.PNG')
image1 = cv2.resize(imageA, (600, 600))
image2 = cv2.resize(imageB, (600, 600))
# imageB_resized = resize_image(imageA, imageB)
# DD = imageA.shape[:-1]
# print(DD)

# imageB = cv2.resize(imageB, DD)
# cv2.imshow("test11", image1)
# cv2.imshow("test22", image2)
# cv2.waitKey(0)

grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

cv2.imshow("test11", grayA)
cv2.imshow("test22", grayB)
cv2.waitKey(0)

np.set_printoptions(threshold=np.inf)
diff = cv2.absdiff(grayA, grayB) #두이미지간 절대차이값 0부터 높을수록 차이남
# print('절대값 차이 :: \n', diff)

np.set_printoptions(threshold=np.inf)
_, diff2 = cv2.threshold(diff, 150, 255, cv2.THRESH_BINARY_INV)
# print(_) #설정한임계값이니까 150으로 설정하면 절대값차이값이 151부터 255(검정)으로 표시
# print("계산한거 :: ", diff2)

cv2.imshow("result", diff2)
cv2.waitKey(0)

# 차이가 있는 부분의 좌표를 찾습니다.
coordinates = np.column_stack(np.where(diff2 == 0))
# print("0인애들 :: ", coordinates)

for i,j in coordinates:
    print('asdfasdfasdfasdf', i,j)
    image1[i,j] = [0, 0, 255]

cv2.imshow("Result", image1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# cv2.imshow("Result", coordinates)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 차이가 있는 픽셀에 직접 빨간색을 입혀줍니다.
# for x, y in coordinates:
#     image1[y, x] = [0, 0, 255]  # 빨간색 [B, G, R]
#
# image1[100, 100] = [0, 0, 255]  # 빨간색 [B, G, R]
# cv2.imshow("Result", image1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# for contour in contours:
#     (x, y, w, h) = cv2.boundingRect(contour)
#     cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
#     cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
# diff_marked = np.zeros_like(image1)
# diff_marked[diff != 0] = image1[diff != 0]
#
# cv2.imshow("Image 1 with differences", image1)
# cv2.imshow("Image 2 with differences", image2)
# cv2.waitKey(0)  # 키보드아무거나누르는거
# cv2.destroyAllWindows()  # 누르면 창닫아라

# (score, diff) = compare_ssim(grayA, grayB, full=True)
# diff = (diff * 255).astype(np.uint8)
# print("ssim:: ".format(score))
#
# thresh = cv2.threshold(diff, 0, 255,
#                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
#
# for c in cnts:
#     (x, y, w, h) = cv2.boundingRect(c)
#     cv2.rectangle(imageA, (x, y), (x+w, y+h), (0,0,255), 2)
#     cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
#
# cv2.imshow("Original", imageA)
# cv2.imshow("Modified", imageB)
# cv2.imshow("diff", diff)
# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)