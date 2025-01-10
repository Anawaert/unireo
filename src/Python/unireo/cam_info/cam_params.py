"""
本模块定义相机启动参数的类型和预定义常量

This module defines the type of camera startup parameters and predefined constants
"""


# 预定义参数常亮
# Predefined parameter constants

class CameraResolution:
    """
    相机分辨率的常量

    Constants of camera resolution
    """

    VGA: tuple = (640, 480)
    """
    VGA分辨率，大小为640x480

    VGA resolution, size is 640x480
    """

    HD720: tuple = (1280, 720)
    """
    HD720分辨率，大小为1280x720

    HD720 resolution, size is 1280x720
    """

    FHD1080: tuple = (1920, 1080)
    """
    FHD1080分辨率，大小为1920x1080

    FHD1080 resolution, size is 1920x1080
    """


class CameraFPS:
    """
    相机帧率的常量

    Constants of camera frame rate
    """

    EXTREME_60FPS: int = 60
    """
    极限帧率，为60fps

    Extreme frame rate, is 60fps
    """

    FLUENT_30FPS: int = 30
    """
    流畅帧率，为30fps

    Fluent frame rate, is 30fps
    """

    BALANCED_15FPS: int = 15
    """
    平衡帧率，为15fps

    Balanced frame rate, is 15fps
    """

    SLOW_8FPS: int = 8
    """
    慢速帧率，为8fps

    Slow frame rate, is 8fps
    """


class ExposureRate:
    """
    曝光率的常量

    Constants of exposure rate
    """

    MAX_EXPOSURE_RATE: int = 0
    """
    最大曝光率

    Maximum exposure rate
    """

    SEMI_EXPOSURE_RATE: int = -3
    """
    次最大曝光率

    Semi-maximum exposure rate
    """

    BALANCED_EXPOSURE_RATE: int = -6
    """
    平衡曝光率

    Balanced exposure rate
    """

    MIN_EXPOSURE_RATE: int = -10
    """
    最小曝光率
    
    Minimum exposure rate
    """


class DecodingFormat:
    """
    解码格式的常量

    Constants of decoding format
    """

    MJPG: str = 'MJPG'
    """
    MJPG编码格式

    MJPG encoding format
    """

    YUYV: str = 'YUYV'
    """
    YUYV编码格式

    YUYV encoding format
    """


class DepthUnit:
    """
    深度图单位的常量

    Constants of depth map unit
    """

    MILLIMETER: int = 1
    """
    毫米单位

    Millimeter unit
    """

    CENTIMETER: int = 10
    """
    厘米单位

    Centimeter unit
    """

    METER: int = 1000
    """
    米单位

    Meter unit
    """


class CameraIndex:
    """
    相机编号的常量

    Constants of camera index
    """

    MAX_CAM_NUM: int = 10
    """
    相机的最大编号为10

    The maximum number of cameras is 10
    """


class GetImageType:
    """
    抓取相机图像的类型

    Type of grabbing camera image
    """

    LEFT_IMAGE = 0b0001
    """
    左目图像标志

    Left eye image flag
    """

    RIGHT_IMAGE = 0b0010
    """
    右目图像标志

    Right eye image flag
    """

    STEREO_IMAGE = 0b0011
    """
    双目图像标志

    Binocular image flag
    """

    DEPTH_IMAGE = 0b0100
    """
    深度图像标志

    Depth image flag
    """


class SavedImageFormat:
    """
    保存至本地图像的格式

    Format of saving image to local
    """

    IMG_FMT_PNG = 0b0001
    """
    PNG图像格式

    PNG image format
    """

    IMG_FMT_JPG = 0b0010
    """
    JPG图像格式

    JPG image format
    """


class DepthQualityLevel:
    """
    深度图质量等级

    Depth map quality level
    """

    DEPTH_QUALITY_LOW = 0
    """
    低质量深度图

    Low quality depth map
    """

    DEPTH_QUALITY_BALANCED = 0b0001
    """
    平衡质量深度图

    Balanced quality depth map
    """

    DEPTH_QUALITY_HIGH = 0b0010
    """
    高质量深度图

    High quality depth map
    """

    DEPTH_QUALITY_ULTRA = 0b0011
    """
    极高质量深度图

    Ultra high quality depth map
    """

class PlatformType:
    """
    平台类型

    Platform type
    """

    WINDOWS = 0
    """
    Windows平台

    Windows platform
    """

    LINUX = 1
    """
    Linux平台

    Linux platform
    """

    MACOS = 2
    """
    MacOS平台

    MacOS platform
    """


class InitParameters:
    """
    相机启动时的参数类型

    The type of parameters when the camera is started
    """

    frame_size: tuple = CameraResolution.HD720
    """
    相机读取画面时的（单目）图像大小，默认为HD规格

    Image size when reading pictures from the camera (monocular), default is HD specification
    """

    frame_rate: int = CameraFPS.FLUENT_30FPS
    """
    相机读取画面的帧率，默认为30fps

    Frame rate when reading pictures from the camera, default is 30fps
    """

    exposure_rate: int = ExposureRate.BALANCED_EXPOSURE_RATE
    """
    相机读取画面时曝光率，使用OpenCV的度量，默认为-6

    Exposure rate when reading pictures from the camera, using OpenCV's measurement, default is -6
    """

    decode_format: str = DecodingFormat.MJPG
    """
    相机读取画面时的解码格式，默认为MJPG

    Decoding format when reading pictures from the camera, default is MJPG
    """

    depth_size: tuple = CameraResolution.HD720
    """
    相机读取深度图时的图像大小，默认为HD规格

    Image size when reading depth pictures from the camera, default is HD specification
    """

    depth_unit: int = DepthUnit.MILLIMETER
    """
    相机读取深度图时的单位，默认为毫米

    Unit when reading depth pictures from the camera, default is millimeter
    """

    platform: int = PlatformType.LINUX
    """
    系统平台，默认为Linux
    
    System platform, default is Linux
    """
