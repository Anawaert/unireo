"""
该模块定义了错误码
\n
This module defines error codes
"""

from enum import Enum


class ErrCode(Enum):
    OPEN_CAMERA_FAILED = 0
    """
    打开相机失败的错误码
    \n
    Error Code of Opening Camera Failed
    """

    OPEN_CAMERA_SUCCESS = 1
    """
    打开相机成功的错误码
    \n
    Error Code of Opening Camera Successfully
    """
    GRAB_IMAGE_FAILED = 0
    """
    读取图像失败的错误码
    \n
    Error Code of Reading Image Failed
    """

    GRAB_IMAGE_SUCCESS = 1
    """
    读取图像成功的错误码
    \n
    Error Code of Reading Image Successfully
    """

    GET_IMAGE_SAVED_FAILED = 0
    """
    获取保存的图像失败的错误码
    \n
    Error Code of Getting Saved Image Failed
    """

    GET_IMAGE_SAVED_SUCCESS = 1
    """
    获取保存的图像成功的错误码
    \n
    Error Code of Getting Saved Image Successfully
    """

    GET_IMAGE_SAVED_NO_OPERATION = 2

    RELEASE_CAMERA_FAILED = 0
    """
    释放相机失败的错误码
    \n
    Error Code of Releasing Camera Failed
    """

    RELEASE_CAMERA_SUCCESS = 1
    """
    释放相机成功的错误码
    \n
    Error Code of Releasing Camera Successfully
    """
