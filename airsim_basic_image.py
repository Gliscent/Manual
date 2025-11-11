import airsim
import numpy as np
import cv2
import time
# check change change changes
client = airsim.MultirotorClient()
client.confirmConnection()

while True:
    '''
    airsim.ImageType.Scene : 일반적 RGB 이미지
    airsim.ImageType.DepthPlanar : 직교 투영 깊이 # 깊이 (m)로 출력,
    airsim.ImageType.DepthPerspective : 원근 투영 깊이 # 깊이 (m)로 출력
    airsim.ImageType.DepthVis : 깊이 이미지
    airsim.ImageType.Segmentation : 객체 세그멘테이션 이미지
    airsim.ImageType.SurfaceNormals : 표면 법선 # 객체의 방향 분석 이미지
    airsim.ImageType.Infrared : 적외선 이미지
    airsim.ImageType.DisparityNormalized : 스테레오 disparity (상이성) 이미지
    airsim.ImageType.OpticalFlow : 광류 이미지
    '''

    '''
        camera_name "0" : 앞
        camera_name "1" : 앞
        camera_name "2" : 앞
        camera_name "3" : 아래
        camera_name "4" : 후방
        '''

    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, False),
        airsim.ImageRequest("0", airsim.ImageType.Segmentation, False, False),
        airsim.ImageRequest("0", airsim.ImageType.DisparityNormalized, False, False),
        airsim.ImageRequest("0", airsim.ImageType.OpticalFlow, False, False),
        airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, True),  # Float, in meters
    ])

    # 1. responses[0]
    img1_1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
    img1 = img1_1d.reshape(responses[0].height, responses[0].width, 3)

    # 2. responses[1]
    img2_1d = np.frombuffer(responses[1].image_data_uint8, dtype=np.uint8)
    img2 = img2_1d.reshape(responses[0].height, responses[0].width, 3)

    # 3. responses[2]
    img3_1d = np.frombuffer(responses[2].image_data_uint8, dtype=np.uint8)
    img3 = img3_1d.reshape(responses[0].height, responses[0].width, 3)

    # 4. responses[3]
    img4_1d = np.frombuffer(responses[3].image_data_uint8, dtype=np.uint8)
    img4 = img4_1d.reshape(responses[0].height, responses[0].width, 3)

    # 5. responses[4]
    # depth_img = np.array(responses[4].image_data_float, dtype=np.float32)
    # depth_img = depth_img.reshape(responses[4].height, responses[4].width)
    # center_x = responses[2].width // 2
    # center_y = responses[2].height // 2
    # center_depth = depth_img[center_y, center_x]
    # print(f"[중심 ({center_x},{center_y})] 깊이: {center_depth:.2f}m | 평균: {np.mean(depth_img):.2f}m")


    # 창 띄우기
    cv2.imshow("Image1", img1)
    cv2.imshow("Image2", img2)
    cv2.imshow("Image3", img3)
    cv2.imshow("Image4", img4)


    # 종료 조건
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
