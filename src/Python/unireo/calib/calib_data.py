"""
本模块定义了用于标定的数据结构，包括各类二维、三维点和参数矩阵等

This module defines the data structure used for calibration, including various two-dimensional, three-dimensional points
and parameter matrices, etc.
"""

from typing import Sequence
import numpy as np


class MonoCalibData:
    """
    单目相机标定数据类，用于存储单目相机标定所需的数据

    Monocular camera calibration data class, used to store data required for monocular camera calibration
    """

    # 标定时使用的图像尺寸
    # Image size used during calibration
    image_size: tuple = None

    # 世界坐标系中的三维点
    # Three-dimensional points in the world coordinate system
    object_points: list = None

    # 图像坐标系中的二维点
    # Two-dimensional points in the image coordinate system
    image_points: list = None

    # 相机内参矩阵
    # Camera Intrinsic Matrix
    camera_matrix: np.ndarray = None

    # 畸变系数
    # Distortion Coefficients
    dist_coeffs: np.ndarray = None

    # 旋转向量
    # Rotation Vector
    rvecs: Sequence = None

    # 平移向量
    # Translation Vector
    tvecs: Sequence = None

    # 新的相机内参矩阵
    # New Camera Intrinsic Matrix
    new_camera_matrix: np.ndarray = None

    # 矫正ROI
    # Rectification ROI
    remap_roi: Sequence = None

    def __init__(self, image_size: tuple, object_points: list, image_points: list, camera_matrix: np.ndarray,
                 dist_coeffs: np.ndarray, rvecs: Sequence, tvecs: Sequence, new_camera_matrix: np.ndarray,
                 remap_roi: Sequence):
        """
        构造单目相机标定数据对象

        Construct monocular camera calibration data object

        :param image_size: 图像尺寸 Image size
        :param object_points: 标定板三维点 Calibration board three-dimensional points
        :param image_points: 图像二维点 Image two-dimensional points
        :param camera_matrix: 相机内参矩阵 Camera intrinsic matrix
        :param dist_coeffs: 畸变系数 Distortion coefficients
        :param rvecs: 旋转向量 Rotation vector
        :param tvecs: 平移向量 Translation vector
        :param new_camera_matrix: 新的相机内参矩阵 New camera intrinsic matrix
        :param remap_roi: 矫正ROI Rectification ROI
        """
        self.image_size = image_size
        self.object_points = object_points
        self.image_points = image_points
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.rvecs = rvecs
        self.tvecs = tvecs
        self.new_camera_matrix = new_camera_matrix
        self.remap_roi = remap_roi


class StereoCalibData:
    """
    双目相机标定数据类，用于存储双目相机标定所需的数据

    Stereo camera calibration data class, used to store data required for stereo camera calibration
    """

    # 标定时使用的图像形状（单目图像的高 × 宽 × 通道数）
    # Image shape used during calibration (height × width × number of channels of monocular image)
    image_shape: tuple = None

    # 世界坐标系中的三维点
    # Three-dimensional points in the world coordinate system
    obj_points: list = None

    # 左目图像坐标系中的二维点
    # Two-dimensional points in the left eye image coordinate system
    left_img_points: list = None

    # 右目图像坐标系中的二维点
    # Two-dimensional points in the right eye image coordinate system
    right_img_points: list = None

    # 左目相机内参矩阵
    # Left Eye Camera Intrinsic Matrix
    left_cam_matrix: np.ndarray = None

    # 左目相机的修正内参矩阵
    # Left Eye Camera Rectified Intrinsic Matrix
    left_new_camera_matrix: np.ndarray = None

    # 左目畸变系数
    # Left Eye Distortion Coefficients
    left_dist_coeffs: np.ndarray = None

    # 左目旋转向量
    # Left Eye Rotation Vector
    left_rvecs: Sequence = None

    # 左目平移向量
    # Left Eye Translation Vector
    left_tvecs: Sequence = None

    # 左目矫正矩阵
    # Left Eye Rectification Matrix
    left_rect_matrix: np.ndarray = None

    # 左目投影矩阵
    # Left Eye Projection Matrix
    left_projection_matrix: np.ndarray = None

    # 右目相机内参矩阵
    # Right Eye Camera Intrinsic Matrix
    right_cam_matrix: np.ndarray = None

    # 右目相机的修正内参矩阵
    # Right Eye Camera Rectified Intrinsic Matrix
    right_new_camera_matrix: np.ndarray = None

    # 右目畸变系数
    # Right Eye Distortion Coefficients
    right_dist_coeffs: np.ndarray = None

    # 右目旋转向量
    # Right Eye Rotation Vector
    right_rvecs: Sequence = None

    # 右目平移向量
    # Right Eye Translation Vector
    right_tvecs: Sequence = None

    # 右目矫正矩阵
    # Right Eye Rectification Matrix
    right_rect_matrix: np.ndarray = None

    # 右目投影矩阵
    # Right Eye Projection Matrix
    right_projection_matrix: np.ndarray = None

    # 旋转矩阵
    # Rotation Matrix
    r_matrix: np.ndarray = None

    # 平移向量
    # Translation Vector
    t_vector: np.ndarray = None

    # 本质矩阵
    # Essential Matrix
    e_matrix: np.ndarray = None

    # 基础矩阵
    # Fundamental Matrix
    f_matrix: np.ndarray = None

    # Q矩阵
    # Q Matrix
    q_matrix: np.ndarray = None

    def __init__(self, image_shape: tuple, object_points: list, left_image_points: list, right_image_points: list,
                 left_camera_matrix: np.ndarray, left_new_camera_matrix: np.ndarray, left_dist_coeffs: np.ndarray,
                 left_rvecs: Sequence, left_tvecs: Sequence, left_rectification_matrix: np.ndarray,
                 left_projection_matrix: np.ndarray, right_camera_matrix: np.ndarray,
                 right_new_camera_matrix: np.ndarray, right_dist_coeffs: np.ndarray,
                 right_rvecs: Sequence, right_tvecs: Sequence, right_rectification_matrix: np.ndarray,
                 right_projection_matrix: np.ndarray, r_matrix: np.ndarray, t_vector: np.ndarray, e_matrix: np.ndarray,
                 f_matrix: np.ndarray, q_matrix: np.ndarray):
        """
        构造双目相机标定数据对象

        Construct stereo camera calibration data object

        :param image_shape: 图像形状 Image shape
        :param object_points: 标定板三维点 Calibration board three-dimensional points
        :param left_image_points: 左目图像二维点 Left eye image two-dimensional points
        :param right_image_points: 右目图像二维点 Right eye image two-dimensional points
        :param left_camera_matrix: 左目相机内参矩阵 Left eye camera intrinsic matrix
        :param left_new_camera_matrix: 左目相机的修正内参矩阵 Left eye camera rectified intrinsic matrix
        :param left_dist_coeffs: 左目畸变系数 Left eye distortion coefficients
        :param left_rvecs: 左目旋转向量 Left eye rotation vector
        :param left_tvecs: 左目平移向量 Left eye translation vector
        :param left_rectification_matrix: 左目矫正矩阵 Left eye rectification matrix
        :param left_projection_matrix: 左目投影矩阵 Left eye projection matrix
        :param right_camera_matrix: 右目相机内参矩阵 Right eye camera intrinsic matrix
        :param right_new_camera_matrix: 右目相机的修正内参矩阵 Right eye camera rectified intrinsic matrix
        :param right_dist_coeffs: 右目畸变系数 Right eye distortion coefficients
        :param right_rvecs: 右目旋转向量 Right eye rotation vector
        :param right_tvecs: 右目平移向量 Right eye translation vector
        :param right_rectification_matrix: 右目矫正矩阵 Right eye rectification matrix
        :param right_projection_matrix: 右目投影矩阵 Right eye projection matrix
        :param r_matrix: 旋转矩阵 Rotation matrix
        :param t_vector: 平移向量 Translation vector
        :param e_matrix: 本质矩阵 Essential matrix
        :param f_matrix: 基础矩阵 Fundamental matrix
        :param q_matrix: 立体解算矩阵 Q matrix
        """

        self.image_shape = image_shape
        self.obj_points = object_points
        self.left_img_points = left_image_points
        self.right_img_points = right_image_points
        self.left_cam_matrix = left_camera_matrix
        self.left_new_camera_matrix = left_new_camera_matrix
        self.left_dist_coeffs = left_dist_coeffs
        self.left_rvecs = left_rvecs
        self.left_tvecs = left_tvecs
        self.left_rect_matrix = left_rectification_matrix
        self.left_projection_matrix = left_projection_matrix
        self.right_cam_matrix = right_camera_matrix
        self.right_new_camera_matrix = right_new_camera_matrix
        self.right_dist_coeffs = right_dist_coeffs
        self.right_rvecs = right_rvecs
        self.right_tvecs = right_tvecs
        self.right_rect_matrix = right_rectification_matrix
        self.right_projection_matrix = right_projection_matrix
        self.r_matrix = r_matrix
        self.t_vector = t_vector
        self.e_matrix = e_matrix
        self.f_matrix = f_matrix
        self.q_matrix = q_matrix
