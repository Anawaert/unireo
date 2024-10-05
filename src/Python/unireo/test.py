import glob

import cam_info
import err_proc
import glob
import calib
import calib.mono_calib as mono_calib
import calib.stereo_calib as stereo_calib
import cv2

params = cam_info.InitParameters()

params.frame_size = cam_info.HD720
params.frame_rate = cam_info.EXTREME_60FPS
params.exposure_rate = -6
params.decode_format = cam_info.MJPG

camera = cam_info.Camera(params)
camera.open()

left_images = glob.glob('/home/adam/calib_img/left/*.png')
right_images = glob.glob('/home/adam/calib_img/right/*.png')

while True:
    retval = camera.grab_frame()
    if retval != err_proc.GRAB_IMAGE_SUCCESS:
        print("Failed to Read Image from Camera")
        break
    cv2.imshow('Left', camera.get_img(cam_info.LEFT_IMAGE))
    cv2.imshow('Right', camera.get_img(cam_info.RIGHT_IMAGE))

    # 单目标定
    # data = mono_calib.get_calib_data((11, 8), cam_info.HD720, right_images)
    # undistortion = mono_calib.undistort_img(camera.get_img(cam_info.RIGHT_IMAGE), data)
    # cv2.imshow('Undistorted_Left', undistortion)
    # print(mono_calib.reprojection_error(data))

    # 双目标定
    stereo_data = stereo_calib.get_calib_data((11, 8), 20, (1280, 720, 3), left_images, right_images)
    l, r = stereo_calib.undistort_imgs(camera.get_img(cam_info.LEFT_IMAGE), camera.get_img(cam_info.RIGHT_IMAGE),
                                       stereo_data)
    cv2.imshow('Undistorted_Left', l)
    cv2.imshow('Undistorted_Right', r)

    # 拍摄标定图像
    # ret = camera.get_img_saved(cam_info.RIGHT_IMAGE, cam_info.IMG_FMT_PNG, '/home/adam/calib_img/right/', 's')
    # if ret != err_proc.GET_IMAGE_SAVED_SUCCESS:
    #     print("Failed to Save Image")
    #     break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
