"""
本模块定义了一些异常类
\n
This module defines some exception classes
"""


class CameraError(Exception):
    """
    相机错误异常类
    \n
    Camera Error Exception Class
    """

    message: str = None
    """
    相机异常的信息
    \n 
    Exception Information of Camera
    """

    def __str__(self):
        """
        相机异常类的字符串输出
        \n
        The String Output of the Exception Class of Camera
        :return: 异常信息 Exception Information
        """
        return self.message

    def __init__(self, message: str):
        """
        初始化异常类
        \n
        Initialize Exception Class
        :param message: 异常信息 Exception Information
        """
        self.message = message
