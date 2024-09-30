"""
本模块定义相机启动参数的类型和预定义常量
\n
This module defines the type of camera startup parameters and predefined constants
"""


# 预定义常亮
# Predefined Constants
VGA: tuple = (640, 480)
"""
VGA分辨率，大小为640x480
\n
VGA Resolution, Size is 640x480
"""

HD720: tuple = (1280, 720)
"""
HD720分辨率，大小为1280x720
\n
HD720 Resolution, Size is 1280x720
"""

FHD1080: tuple = (1920, 1080)
"""
FHD1080分辨率，大小为1920x1080
\n
FHD1080 Resolution, Size is 1920x1080
"""

EXTREME_60FPS: int = 60
"""
极限帧率，为60fps
\n
Extreme Frame Rate, is 60fps
"""

FLUENT_30FPS: int = 30
"""
流畅帧率，为30fps
\n
Fluent Frame Rate, is 30fps
"""

BALANCED_15FPS: int = 15
"""
平衡帧率，为15fps
\n
Balanced Frame Rate, is 15fps
"""

SLOW_8FPS: int = 8
"""
慢速帧率，为8fps
\n
Slow Frame Rate, is 8fps
"""

MJPG: str = 'MJPG'
"""
MJPG编码格式
\n
MJPG Encoding Format
"""

YUYV: str = 'YUYV'
"""
YUYV编码格式
\n
YUYV Encoding Format
"""

MILLIMETER: int = 0
"""
毫米单位
\n
Millimeter Unit
"""


class InitParameters:
    """
    相机启动时的参数类型
    \n
    The Type of Parameters when Camera Start
    """

    frame_size: tuple = HD720
    """
    相机读取画面时的（单目）图像大小，默认为HD规格
    \n
    Image Size (Monocular) when Reading Picture, Default is HD Specification
    """

    frame_rate: int = FLUENT_30FPS
    """
    相机读取画面的帧率，默认为30fps
    \n
    Frame Rate when Reading Picture, Default is 30fps
    """

    exposure_rate: int = -6
    """
    相机读取画面时曝光率，使用OpenCV的度量，默认为-6
    \n
    Exposure Rate when Reading Picture, Using OpenCV's Measurement, Default is -6
    """

    decode_format: str = MJPG
    """
    相机读取画面时的解码格式，默认为MJPG
    \n
    Decoding Format when Reading Picture, Default is MJPG
    """

    depth_size: tuple = HD720
    """
    相机读取深度图时的图像大小，默认为HD规格
    \n
    Image Size when Reading Depth Picture, Default is HD Specification
    """

    depth_unit: int = MILLIMETER
    """
    相机读取深度图时的单位，默认为毫米
    \n
    Unit when Reading Depth Picture, Default is Millimeter
    """


