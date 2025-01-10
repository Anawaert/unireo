"""
该模块用于进行相机的操作，包括相机的初始化、相机的参数设置、相机的图像采集等

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

    Instance class of Camera Object, all camera operations and readings are defined in this class
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

    # 相机运行的平台
    # Platform on which the Camera Runs
    __platform: int = None

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

    def open(self) -> err_code.ErrCode:
        """
        以指定参数打开相机

        Open the camera with the specified parameters

        :return: 错误码 Error code

        示例（Example）：

        err_code = camera.open()
        """

        # 尝试打开相机，循环遍历所有相机编号
        # Try to Open the Camera, Loop through all Camera Numbers
        for index in range(0, cam_params.CameraIndex.MAX_CAM_NUM):
            try:
                temp_video = cv2.VideoCapture(index, self.__platform)
                if temp_video.isOpened():
                    self.__camera = temp_video
                    break
                else:
                    temp_video.release()
                    continue
            except IndexError:
                continue

        if self.__camera is None:
            return err_code.ErrCode.OPEN_CAMERA_FAILED

        # 设置相机参数
        # Set Camera Parameters
        self.__camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.__frame_size[0])
        self.__camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__frame_size[1])
        self.__camera.set(cv2.CAP_PROP_FPS, self.__frame_rate)
        self.__camera.set(cv2.CAP_PROP_EXPOSURE, self.__exposure_rate)
        self.__camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(self.__decode_format[0], self.__decode_format[1],
                                                                      self.__decode_format[2], self.__decode_format[3]))
        # 试着抓取一帧图像，如果成功则返回成功
        # Try to Capture a Frame, Return Successfully if Succeed
        retval, frame = self.__camera.read()
        if not retval:
            return err_code.ErrCode.OPEN_CAMERA_FAILED
        else:
            return err_code.ErrCode.OPEN_CAMERA_SUCCESS

    def grab_frame(self) -> err_code.ErrCode:
        """
        从相机抓取一帧图像

        Grab a frame from the camera

        :return: 错误码 Error code

        示例（Example）：

        err_code = camera.grab_frame()
        """

        # 读取一帧图像
        # Read a Frame
        is_grabbed = self.__camera.grab()
        if not is_grabbed:
            raise exceptions.CameraError("Failed to grab the image, please check the camera status!")

        # 解码一帧图像
        # Decode a Frame
        is_retrieved, frame = self.__camera.retrieve()
        if not is_retrieved:
            raise exceptions.CameraError("Failed to retrieve the image, please check the camera status!")

        # 存储画面，并分割为左右画面
        # Save the Image and Split it into Left and Right Images
        if frame is None:
            raise exceptions.CameraError("Failed to split the stereo image, please check the camera status!")

        self.__frame = frame
        self.__left_frame = frame[:, 0:self.__frame_size[0] // 2]
        self.__right_frame = frame[:, self.__frame_size[0] // 2:self.__frame_size[0]]
        return err_code.ErrCode.GRAB_IMAGE_SUCCESS

    def get_img(self, image_type: int) -> np.ndarray:
        """
        获取指定类型的图像

        Get the image of the specified type

        :param image_type: 图像类型（左/右/双目/深度） Image type (left/right/binocular/depth)
        :return: 图像数组 Image array
        :exception: 相机错误 CameraError

        示例（Example）：

        left_img = camera.get_img(cam_info.GetImageType.LEFT_IMAGE)
        """

        # 根据图像类型返回对应的图像
        # Return the Corresponding Image According to the Image Type
        # 若内部图像为空，则返回全零图像
        # Return Zero Image if the Internal Image is Empty
        if image_type == cam_params.GetImageType.LEFT_IMAGE:
            if self.__left_frame is not None:
                return self.__left_frame
            else:
                return np.zeros(self.__frame_size[0] // 2, self.__frame_size[1], 3)
        elif image_type == cam_params.GetImageType.RIGHT_IMAGE:
            if self.__right_frame is not None:
                return self.__right_frame
            else:
                return np.zeros(self.__frame_size[0] // 2, self.__frame_size[1], 3)
        elif image_type == cam_params.GetImageType.STEREO_IMAGE:
            if self.__frame is not None:
                return self.__frame
            else:
                return np.zeros(self.__frame_size[0], self.__frame_size[1], 3)
        else:
            raise exceptions.CameraError("Invalid image type, please check the image type flag!")

    def get_img_saved(self, image_type: int, saved_format: int, saved_dir: str, key: str) -> err_code.ErrCode:
        """
        保存指定类型的图像

        Save the image of the specified type

        :param image_type: 图像类型（左/右/双目） Image type (left/right/binocular)
        :param saved_format: 保存图像的格式（PNG/JPG） Image format of the saved image (PNG/JPG)
        :param saved_dir: 保存图像的目录 Save the directory of the saved image
        :param key: 保存图像时按下的按键 Save the key pressed when the image is saved
        :return: 错误码 ErrCode
        :exception: 相机错误 CameraError

        示例（Example）：

        err_code = camera.get_img_saved(cam_info.SavedImageFormat.LEFT_IMAGE, cam_info.SavedImageFormat.IMG_FMT_PNG, '/path/to/save/', 's')
        """

        # 按下指定按键后保存图像
        # Save Image after Pressing the Specified Key
        if cv2.waitKey(1) & 0xFF == ord(key):
            # 获取当前时间
            # Get Current Time
            current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            # 依据传入参数联合判断
            # Joint Judgment Based on Incoming Parameters
            if image_type == cam_params.GetImageType.LEFT_IMAGE:
                if self.__left_frame is not None:
                    if saved_format == cam_params.SavedImageFormat.IMG_FMT_PNG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_left" + ".png"), self.__left_frame)
                            print("Saved left image: " + os.path.join(saved_dir, current_time + "_left" + ".png"))
                        except cv2.error as e:
                            print("Error occurred when saving left image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    elif saved_format == cam_params.SavedImageFormat.IMG_FMT_JPG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_left" + ".jpg"), self.__left_frame)
                            print("Saved left image: " + os.path.join(saved_dir, current_time + "_left" + ".jpg"))
                        except cv2.error as e:
                            print("Error occurred when saving left image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    else:
                        raise exceptions.CameraError("Invalid format of saved image, please check the format flag!")
                else:
                    raise exceptions.CameraError("Left image is not available, please check the camera status!")
            elif image_type == cam_params.GetImageType.RIGHT_IMAGE:
                if self.__right_frame is not None:
                    if saved_format == cam_params.SavedImageFormat.IMG_FMT_PNG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_right" + ".png"), self.__right_frame)
                            print("Saved right image: " + os.path.join(saved_dir, current_time + "_right" + ".png"))
                        except cv2.error as e:
                            print("Error occurred when saving right image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    elif saved_format == cam_params.SavedImageFormat.IMG_FMT_JPG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_right" + ".jpg"), self.__right_frame)
                            print("Saved right image: " + os.path.join(saved_dir, current_time + "_right" + ".jpg"))
                        except cv2.error as e:
                            print("Error occurred when saving right image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    else:
                        raise exceptions.CameraError("Invalid format of saved image, please check the format flag!")
                else:
                    raise exceptions.CameraError("Right image is not available, please check the camera status!")
            elif image_type == cam_params.GetImageType.STEREO_IMAGE:
                if self.__frame is not None:
                    if saved_format == cam_params.SavedImageFormat.IMG_FMT_PNG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_stereo" + ".png"), self.__frame)
                            print("Saved stereo image: " + os.path.join(saved_dir, current_time + "_stereo" + ".png"))
                        except cv2.error as e:
                            print("Error occurred when saving stereo image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    elif saved_format == cam_params.SavedImageFormat.IMG_FMT_JPG:
                        try:
                            cv2.imwrite(os.path.join(saved_dir, current_time + "_stereo" + ".jpg"), self.__frame)
                            print("Saved stereo image: " + os.path.join(saved_dir, current_time + "_stereo" + ".jpg"))
                        except cv2.error as e:
                            print("Error occurred when saving stereo image: " + str(e))
                            return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                    else:
                        raise exceptions.CameraError("Invalid format of saved image, please check the format flag!")
                else:
                    raise exceptions.CameraError("Camera image is not available, please check the camera status!")
            else:
                raise exceptions.CameraError("Invalid image type, please check the flag to grab the image!")

            return err_code.ErrCode.GET_IMAGE_SAVED_SUCCESS

        return err_code.ErrCode.GET_IMAGE_SAVED_NO_OPERATION

    def get_stereo_img_saved(self, saved_format: int, left_saved_dir: str, right_saved_dir: str,
                             key: str) -> err_code.ErrCode:
        """
        分别同步保存左右目图像

        Save left and right eye images separately and synchronously

        :param saved_format: 图像类型（PNG/JPG） Image type (PNG/JPG)
        :param left_saved_dir: 保存左目图像的目录 Save the directory of the left eye image
        :param right_saved_dir: 保存右目图像的目录 Save the directory of the right eye image
        :param key: 保存图像时按下的按键 Save the key pressed when the image is saved
        :return: 错误码 ErrCode
        :exception 相机错误 CameraError

        示例（Example）：

        err_code = camera.get_stereo_img_saved(cam_info.SavedImageFormat.IMG_FMT_PNG, '/path/to/save/left/', '/path/to/save/right/', 's')
        """

        # 按下指定按键后保存图像
        # Save Image after Pressing the Specified Key
        if cv2.waitKey(1) & 0xFF == ord(key):
            # 获取当前时间
            # Get Current Time
            current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            if (self.__left_frame is not None) and (self.__right_frame is not None):
                if saved_format == cam_params.SavedImageFormat.IMG_FMT_PNG:
                    try:
                        cv2.imwrite(os.path.join(left_saved_dir, current_time + "_left" + ".png"), self.__left_frame)
                        print("Saved left image: " + os.path.join(left_saved_dir, current_time + "_left" + ".png"))
                        cv2.imwrite(os.path.join(right_saved_dir, current_time + "_right" + ".png"), self.__right_frame)
                        print("Saved right image: " + os.path.join(right_saved_dir, current_time + "_right" + ".png"))
                    except cv2.error as e:
                        print("Error occurred when saving stereo image: " + str(e))
                        return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                elif saved_format == cam_params.SavedImageFormat.IMG_FMT_JPG:
                    try:
                        cv2.imwrite(os.path.join(left_saved_dir, current_time + "_left" + ".jpg"), self.__left_frame)
                        print("Saved left image: " + os.path.join(left_saved_dir, current_time + "_left" + ".jpg"))
                        cv2.imwrite(os.path.join(right_saved_dir, current_time + "_right" + ".jpg"), self.__right_frame)
                        print("Saved right image: " + os.path.join(right_saved_dir, current_time + "_right" + ".jpg"))
                    except cv2.error as e:
                        print("Error occurred when saving stereo image: " + str(e))
                        return err_code.ErrCode.GET_IMAGE_SAVED_FAILED
                else:
                    raise exceptions.CameraError("Invalid format of saved image, please check the format flag!")
            else:
                raise exceptions.CameraError("Stereo images are not available, please check the camera status!")

            return err_code.ErrCode.GET_IMAGE_SAVED_SUCCESS

        return err_code.ErrCode.GET_IMAGE_SAVED_NO_OPERATION

    def release(self) -> err_code.ErrCode:
        """
        释放相机资源

        Release camera resources

        :return: 错误码 Error code

        示例（Example）：

        err_code = camera.release()
        """
        try:
            self.__camera.release()
            return err_code.ErrCode.RELEASE_CAMERA_SUCCESS
        except RuntimeError:
            return err_code.ErrCode.RELEASE_CAMERA_FAILED

    def __init__(self, init_parameters: cam_params.InitParameters):
        """
        初始化相机对象

        Initialize camera object

        :param init_parameters: 初始参数对象 Initial parameter object
        """

        # 为私有变量赋值
        # Assign Values to Private Variables
        self.__frame_size = (init_parameters.frame_size[0] * 2, init_parameters.frame_size[1])
        self.__frame_rate = init_parameters.frame_rate
        self.__exposure_rate = init_parameters.exposure_rate
        self.__decode_format = init_parameters.decode_format
        self.__depth_size = init_parameters.depth_size
        self.__depth_unit = init_parameters.depth_unit
        if init_parameters.platform == cam_params.PlatformType.WINDOWS:
            self.__platform = cv2.CAP_MSMF
        elif init_parameters.platform == cam_params.PlatformType.LINUX:
            self.__platform = cv2.CAP_V4L2
        elif init_parameters.platform == cam_params.PlatformType.MACOS:
            self.__platform = cv2.CAP_AVFOUNDATION


# 本模块仅作为模块使用，无法直接运行
# This module is for module use only and cannot be run directly
if __name__ == '__main__':
    print("This script is not for direct running!")
    pass
