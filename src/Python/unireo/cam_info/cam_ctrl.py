"""
该模块用于进行相机的操作，包括相机的初始化、相机的参数设置、相机的图像采集等
\n
The module is used for camera operation, including camera initialization, camera parameter setting, camera image
acquisition, etc.
"""

import cv2
import numpy as np
import os
import time
import cam_params
import err_proc.error_code as err_code
import err_proc.exceptions as exceptions

MAX_CAM_NUM: int = 10
"""
相机的最大编号为10
\n
The maximum number of cameras is 10
"""


class Camera:
    """
    相机对象的实例类，所有相机的操作读取都在本类中定义
    \n
    Instance Class of Camera Object, All Camera Operation Reading are Defined in this Class
    """

    # 相机启动时的双目图像大小
    # Image Size of Binocular when Camera Starts
    __frame_size: tuple = None

    # 相机启动时的帧率
    # Frame Rate when Camera Starts
    __frame_rate: int = None

    # 相机启动时的曝光率
    # Exposure Rate when Camera Starts
    __exposure_rate: int = None

    # 相机启动时的解码格式
    # Decode Format when Camera Starts
    __decode_format: str = None

    # 相机启动时的深度图大小
    # Depth Map Size when Camera Starts
    __depth_size: tuple = None

    # 相机启动时的深度图单位
    # Depth Map Unit when Camera Starts
    __depth_unit: int = None

    # 内部维护的OpenCV相机对象
    # OpenCV Camera Object Internally Maintained
    __camera: cv2.VideoCapture = None

    # 相机画面
    # Camera Image
    __frame: np.ndarray = None

    # 左目画面
    # Left Eye Image
    __left_frame: np.ndarray = None

    # 右目画面
    # Right Eye Image
    __right_frame: np.ndarray = None

    def open(self) -> int:
        """
        以指定参数打开相机
        \n
        Open the Camera with Specified Parameters
        :return: 错误码整型值 Error Code Integer Value
        """

        # 尝试打开相机，循环遍历所有相机编号
        # Try to Open the Camera, Loop through all Camera Numbers
        for index in range(MAX_CAM_NUM):
            try:
                temp_video = cv2.VideoCapture(index, cv2.CAP_ANY)
                if temp_video.isOpened():
                    self.__camera = temp_video
                    break
                else:
                    continue
            except IndexError:
                continue

        if self.__camera is None:
            return err_code.OPEN_CAMERA_FAILED

        # 设置相机参数
        # Set Camera Parameters
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.__frame_size[0])
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__frame_size[1])
        self.__camera.set(cv2.CAP_PROP_FPS, self.__frame_rate)
        self.__camera.set(cv2.CAP_PROP_EXPOSURE, self.__exposure_rate)
        self.__camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(self.__decode_format[0], self.__decode_format[1],
                                                                      self.__decode_format[2], self.__decode_format[3]))
        # 试着抓取一帧图像，如果成功则返回成功
        # Try to Capture a Frame, Return Successfully if Succeed
        retval, frame = self.__camera.read()
        if not retval:
            return err_code.OPEN_CAMERA_FAILED

        return err_code.OPEN_CAMERA_SUCCESS

    def read_img(self) -> tuple:
        """
        从相机抓取一帧图像
        \n
        Grab a Frame from the Camera
        :return: tuple，第一个为错误码，第二个为图像数据 tuple, the first is the error code, the second is the image data
        """

        # 读取一帧图像
        # Read a Frame
        is_grabbed = self.__camera.grab()
        if not is_grabbed:
            raise exceptions.CameraError("Failed to Grab Frame from Camera")

        # 解码一帧图像
        # Decode a Frame
        is_retrieved, frame = self.__camera.retrieve()
        if not is_retrieved:
            raise exceptions.CameraError("Failed to Retrieve Frame from Camera")

        # 存储画面，并分割为左右画面
        # Save the Image and Split it into Left and Right Images
        self.__frame = frame
        self.__left_frame = frame[:, 0:self.__frame_size[0] // 2]
        self.__right_frame = frame[:, self.__frame_size[0] // 2:self.__frame_size[0]]
        return err_code.READ_IMAGE_SUCCESS, frame

    def __init__(self, init_parameters: cam_params.InitParameters):
        """
        初始化相机对象
        \n
        Initialize Camera Object
        :param init_parameters: 初始参数对象 Initial Parameter Object
        """

        # 为私有变量赋值
        # Assign Values to Private Variables
        self.__frame_size = (init_parameters.frame_size[0] * 2, init_parameters.frame_size[1])
        self.__frame_rate = init_parameters.frame_rate
        self.__exposure_rate = init_parameters.exposure_rate
        self.__decode_format = init_parameters.decode_format
        self.__depth_size = init_parameters.depth_size
        self.__depth_unit = init_parameters.depth_unit
