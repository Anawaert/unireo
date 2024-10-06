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
import cam_info.cam_params as cam_params
import err_proc.error_code as err_code
import err_proc.exceptions as exceptions


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

    def __del__(self):
        """
        释放相机资源
        \n
        Release Camera Resources
        """
        pass

    def open(self) -> int:
        """
        以指定参数打开相机
        \n
        Open the Camera with Specified Parameters

        :return: 错误码 Error Code

        示例（Example）：
        \n
        err_code = camera.open()
        """

        # 尝试打开相机，循环遍历所有相机编号
        # Try to Open the Camera, Loop through all Camera Numbers
        for index in range(1, cam_params.MAX_CAM_NUM):
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

        # 恢复OpenCV的日志级别
        # Restore OpenCV Log Level
        return err_code.OPEN_CAMERA_SUCCESS

    def grab_frame(self) -> int:
        """
        从相机抓取一帧图像
        \n
        Grab a Frame from the Camera

        :return: int型错误码 Error Code Integer Value

        示例（Example）：
        \n
        err_code = camera.grab_frame()
        """

        # 读取一帧图像
        # Read a Frame
        is_grabbed = self.__camera.grab()
        if not is_grabbed:
            raise exceptions.CameraError("Failed to Grab Image from Camera")

        # 解码一帧图像
        # Decode a Frame
        is_retrieved, frame = self.__camera.retrieve()
        if not is_retrieved:
            raise exceptions.CameraError("Failed to Retrieve Image from Camera")

        # 存储画面，并分割为左右画面
        # Save the Image and Split it into Left and Right Images
        self.__frame = frame
        self.__left_frame = frame[:, 0:self.__frame_size[0] // 2]
        self.__right_frame = frame[:, self.__frame_size[0] // 2:self.__frame_size[0]]
        return err_code.GRAB_IMAGE_SUCCESS

    def get_img(self, image_type: int) -> np.ndarray:
        """
        获取指定类型的图像
        \n
        Get the Image of Specified Type

        :param image_type: 图像类型（左/右/双目/深度） Image Type (Left/Right/Stereo/Depth)
        :return: 图像数组 Image Array

        示例（Example）：
        \n
        left_img = camera.get_img(cam_info.LEFT_IMAGE)
        """

        # 根据图像类型返回对应的图像
        # Return the Corresponding Image According to the Image Type
        # 若内部图像为空，则返回全零图像
        # Return Zero Image if the Internal Image is Empty
        if image_type == cam_params.LEFT_IMAGE:
            if self.__left_frame is not None:
                return self.__left_frame
            else:
                return np.zeros(self.__frame_size[0] // 2, self.__frame_size[1], 3)
        elif image_type == cam_params.RIGHT_IMAGE:
            if self.__right_frame is not None:
                return self.__right_frame
            else:
                return np.zeros(self.__frame_size[0] // 2, self.__frame_size[1], 3)
        elif image_type == cam_params.STEREO_IMAGE:
            if self.__frame is not None:
                return self.__frame
            else:
                return np.zeros(self.__frame_size[0], self.__frame_size[1], 3)
        else:
            raise exceptions.CameraError("Invalid Image Type")

    def get_img_saved(self, image_type: int, saved_format: int, saved_dir: str, key: str) -> int:
        """
        保存指定类型的图像
        \n
        Save the Image of Specified Type

        :param image_type: 图像类型（左/右/双目/深度） Image Type (Left/Right/Stereo/Depth)
        :param saved_format: 图像类型（PNG/JPG） Image Type (PNG/JPG)
        :param saved_dir: 保存图像的目录 Save the Directory of the Image
        :param key: 保存图像时按下的按键 Save the Key Pressed when the Image is Saved
        :return: 错误码 Error Code

        示例（Example）：
        \n
        err_code = camera.get_img_saved(cam_info.LEFT_IMAGE, cam_info.IMG_FMT_PNG, '/path/to/save/', 's')
        """

        # 按下指定按键后保存图像
        # Save Image after Pressing the Specified Key
        if cv2.waitKey(1) & 0xFF == ord(key):
            # 获取当前时间
            # Get Current Time
            current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            # 依据传入参数联合判断
            # Joint Judgment Based on Incoming Parameters
            if image_type == cam_params.LEFT_IMAGE:
                if self.__left_frame is not None:
                    if saved_format == cam_params.IMG_FMT_PNG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_left" + ".png"), self.__left_frame)
                        print("Saved Left Image: " + os.path.join(saved_dir, current_time + "_left" + ".png"))
                    elif saved_format == cam_params.IMG_FMT_JPG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_left" + ".jpg"), self.__left_frame)
                        print("Saved Left Image: " + os.path.join(saved_dir, current_time + "_left" + ".jpg"))
                    else:
                        raise exceptions.CameraError("Invalid Format of Saved Image")
                else:
                    return err_code.GET_IMAGE_SAVED_FAILED
            elif image_type == cam_params.RIGHT_IMAGE:
                if self.__right_frame is not None:
                    if saved_format == cam_params.IMG_FMT_PNG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_right" + ".png"), self.__right_frame)
                        print("Saved Right Image: " + os.path.join(saved_dir, current_time + "_right" + ".png"))
                    elif saved_format == cam_params.IMG_FMT_JPG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_right" + ".jpg"), self.__right_frame)
                        print("Saved Right Image: " + os.path.join(saved_dir, current_time + "_right" + ".jpg"))
                    else:
                        raise exceptions.CameraError("Invalid Format of Saved Image")
                else:
                    return err_code.GET_IMAGE_SAVED_FAILED
            elif image_type == cam_params.STEREO_IMAGE:
                if self.__frame is not None:
                    if saved_format == cam_params.IMG_FMT_PNG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_stereo" + ".png"), self.__frame)
                        print("Saved Stereo Image: " + os.path.join(saved_dir, current_time + "_stereo" + ".png"))
                    elif saved_format == cam_params.IMG_FMT_JPG:
                        cv2.imwrite(os.path.join(saved_dir, current_time + "_stereo" + ".jpg"), self.__frame)
                        print("Saved Stereo Image: " + os.path.join(saved_dir, current_time + "_stereo" + ".jpg"))
                    else:
                        raise exceptions.CameraError("Invalid Format of Saved Image")
                else:
                    return err_code.GET_IMAGE_SAVED_FAILED
            else:
                raise exceptions.CameraError("Invalid Image Type")

        return err_code.GET_IMAGE_SAVED_SUCCESS

    def get_stereo_img_saved(self, saved_format: int, left_saved_dir: str, right_saved_dir: str, key: str) -> int:
        """
        分别保存左右目图像
        \n
        Save Left and Right Eye Images Separately

        :param saved_format: 图像类型（PNG/JPG） Image Type (PNG/JPG)
        :param left_saved_dir: 保存左目图像的目录 Save the Directory of the Left Eye Image
        :param right_saved_dir: 保存右目图像的目录 Save the Directory of the Right Eye Image
        :param key: 保存图像时按下的按键 Save the Key Pressed when the Image is Saved
        :return: 错误码 Error Code

        示例（Example）：
        \n
        err_code = camera.get_stereo_img_saved(cam_info.IMG_FMT_PNG, '/path/to/save/left/', '/path/to/save/right/', 's')
        """

        # 按下指定按键后保存图像
        # Save Image after Pressing the Specified Key
        if cv2.waitKey(1) & 0xFF == ord(key):
            # 获取当前时间
            # Get Current Time
            current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            if (self.__left_frame is not None) and (self.__right_frame is not None):
                if saved_format == cam_params.IMG_FMT_PNG:
                    cv2.imwrite(os.path.join(left_saved_dir, current_time + "_left" + ".png"), self.__left_frame)
                    print("Saved Left Image: " + os.path.join(left_saved_dir, current_time + "_left" + ".png"))
                    cv2.imwrite(os.path.join(right_saved_dir, current_time + "_right" + ".png"), self.__right_frame)
                    print("Saved Right Image: " + os.path.join(right_saved_dir, current_time + "_right" + ".png"))
                elif saved_format == cam_params.IMG_FMT_JPG:
                    cv2.imwrite(os.path.join(left_saved_dir, current_time + "_left" + ".jpg"), self.__left_frame)
                    print("Saved Left Image: " + os.path.join(left_saved_dir, current_time + "_left" + ".jpg"))
                    cv2.imwrite(os.path.join(right_saved_dir, current_time + "_right" + ".jpg"), self.__right_frame)
                    print("Saved Right Image: " + os.path.join(right_saved_dir, current_time + "_right" + ".jpg"))
                else:
                    raise exceptions.CameraError("Invalid Format of Saved Image")
            else:
                return err_code.GET_IMAGE_SAVED_FAILED

        return err_code.GET_IMAGE_SAVED_SUCCESS

    def release(self) -> int:
        """
        释放相机资源
        \n
        Release Camera Resources

        :return: 错误码 Error Code

        示例（Example）：
        \n
        err_code = camera.release()
        """
        try:
            self.__camera.release()
            self.__del__()
            return err_code.RELEASE_CAMERA_SUCCESS
        except RuntimeError:
            return err_code.RELEASE_CAMERA_FAILED

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
