"""
本模块定义了用于标定的数据结构，包括各类二维、三维点和参数矩阵等、
\n
This module defines the data structure used for calibration, including various two-dimensional, three-dimensional points
and parameter matrices, etc.
"""

import numpy as np


class MonoCalibData:
    """
    单目相机标定数据类，用于存储单目相机标定所需的数据
    \n
    Monocular Camera Calibration Data Class, Used to Store Data Required for Monocular Camera Calibration
    """

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
    rvecs: np.ndarray = None

    # 平移向量
    # Translation Vector
    tvecs: np.ndarray = None

    # 新的相机内参矩阵
    # New Camera Intrinsic Matrix
    new_camera_matrix: np.ndarray = None

    # 矫正ROI
    # Rectification ROI
    remap_roi: tuple = None

    # 矫正矩阵（x方向）
    # Rectification Matrix (x direction)
    map_x: np.ndarray = None

    # 矫正矩阵（y方向）
    # Rectification Matrix (y direction)
    map_y: np.ndarray = None

    def __init__(self, object_points: list, image_points: list, camera_matrix: np.ndarray,
                 dist_coeffs: np.ndarray, rvecs: np.ndarray, tvecs: np.ndarray, new_camera_matrix: np.ndarray,
                 remap_roi: tuple, img_map: tuple):
        """
        为数据对象赋值
        \n
        Assign values to data objects
        """
        self.object_points = object_points
        self.image_points = image_points
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.rvecs = rvecs
        self.tvecs = tvecs
        self.new_camera_matrix = new_camera_matrix
        self.map_x = img_map[0]
        self.map_y = img_map[1]
        self.remap_roi = remap_roi


class StereoCalibData:
    """
    双目相机标定数据类，用于存储双目相机标定所需的数据
    \n
    Stereo Camera Calibration Data Class, Used to Store Data Required for Stereo Camera Calibration
    """

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

    # 左目畸变系数
    # Left Eye Distortion Coefficients
    left_dist_coeffs: np.ndarray = None

    # 左目旋转向量
    # Left Eye Rotation Vector
    left_rvecs: np.ndarray = None

    # 左目平移向量
    # Left Eye Translation Vector
    left_tvecs: np.ndarray = None

    # 左目矫正矩阵
    # Left Eye Rectification Matrix
    left_rect_matrix: np.ndarray = None

    # 左目投影矩阵
    # Left Eye Projection Matrix
    left_projection_matrix: np.ndarray = None

    # 左目立体映射（x方向）
    # Left Eye Stereo Mapping (x direction)
    left_stereo_map_x: np.ndarray = None

    # 左目立体映射（y方向）
    # Left Eye Stereo Mapping (y direction)
    left_stereo_map_y: np.ndarray = None

    # 右目相机内参矩阵
    # Right Eye Camera Intrinsic Matrix
    right_cam_matrix: np.ndarray = None

    # 右目畸变系数
    # Right Eye Distortion Coefficients
    right_dist_coeffs: np.ndarray = None

    # 右目旋转向量
    # Right Eye Rotation Vector
    right_rvecs: np.ndarray = None

    # 右目平移向量
    # Right Eye Translation Vector
    right_tvecs: np.ndarray = None

    # 右目矫正矩阵
    # Right Eye Rectification Matrix
    right_rect_matrix: np.ndarray = None

    # 右目投影矩阵
    # Right Eye Projection Matrix
    right_projection_matrix: np.ndarray = None

    # 右目立体映射（x方向）
    # Right Eye Stereo Mapping (x direction)
    right_stereo_map_x: np.ndarray = None

    # 右目立体映射（y方向）
    # Right Eye Stereo Mapping (y direction)
    right_stereo_map_y: np.ndarray = None

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

    def __init__(self, object_points: list, left_image_points: list, right_image_points: list,
                 left_camera_matrix: np.ndarray, left_dist_coeffs: np.ndarray, left_rvecs: np.ndarray,
                 left_tvecs: np.ndarray, left_rectification_matrix: np.ndarray, left_projection_matrix: np.ndarray,
                 left_stereo_map: np.ndarray, right_camera_matrix: np.ndarray, right_dist_coeffs: np.ndarray,
                 right_rvecs: np.ndarray, right_tvecs: np.ndarray, right_rectification_matrix: np.ndarray,
                 right_projection_matrix: np.ndarray, right_stereo_map: np.ndarray, r_matrix: np.ndarray,
                 t_vector: np.ndarray, e_matrix: np.ndarray, f_matrix: np.ndarray, q_matrix: np.ndarray):
        """
        为双目标定数据对象赋值
        \n
        Assign values to stereo calibration data objects
        :param object_points: 标定板三维点 Calibration Board Three-dimensional Points
        :param left_image_points: 左目图像二维点 Left Eye Image Two-dimensional Points
        :param right_image_points: 右目图像二维点 Right Eye Image Two-dimensional Points
        :param left_camera_matrix: 左目相机内参矩阵 Left Eye Camera Intrinsic Matrix
        :param left_dist_coeffs: 左目畸变系数 Left Eye Distortion Coefficients
        :param left_rvecs: 左目旋转向量 Left Eye Rotation Vector
        :param left_tvecs: 左目平移向量 Left Eye Translation Vector
        :param left_rectification_matrix: 左目矫正矩阵 Left Eye Rectification Matrix
        :param left_projection_matrix: 左目投影矩阵 Left Eye Projection Matrix
        :param left_stereo_map: 左目立体映射 Left Eye Stereo Mapping
        :param right_camera_matrix: 右目相机内参矩阵 Right Eye Camera Intrinsic Matrix
        :param right_dist_coeffs: 右目畸变系数 Right Eye Distortion Coefficients
        :param right_rvecs: 右目旋转向量 Right Eye Rotation Vector
        :param right_tvecs: 右目平移向量 Right Eye Translation Vector
        :param right_rectification_matrix: 右目矫正矩阵 Right Eye Rectification Matrix
        :param right_projection_matrix: 右目投影矩阵 Right Eye Projection Matrix
        :param right_stereo_map: 右目立体映射 Right Eye Stereo Mapping
        :param r_matrix: 旋转矩阵 Rotation Matrix
        :param t_vector: 平移向量 Translation Vector
        :param e_matrix: 本质矩阵 Essential Matrix
        :param f_matrix: 基础矩阵 Fundamental Matrix
        :param q_matrix: Q矩阵 Q Matrix
        """

        self.obj_points = object_points
        self.left_img_points = left_image_points
        self.right_img_points = right_image_points
        self.left_cam_matrix = left_camera_matrix
        self.left_dist_coeffs = left_dist_coeffs
        self.left_rvecs = left_rvecs
        self.left_tvecs = left_tvecs
        self.left_rect_matrix = left_rectification_matrix
        self.left_projection_matrix = left_projection_matrix
        self.left_stereo_map_x = left_stereo_map[0]
        self.left_stereo_map_y = left_stereo_map[1]
        self.right_cam_matrix = right_camera_matrix
        self.right_dist_coeffs = right_dist_coeffs
        self.right_rvecs = right_rvecs
        self.right_tvecs = right_tvecs
        self.right_rect_matrix = right_rectification_matrix
        self.right_projection_matrix = right_projection_matrix
        self.right_stereo_map_x = right_stereo_map[0]
        self.right_stereo_map_y = right_stereo_map[1]
        self.r_matrix = r_matrix
        self.t_vector = t_vector
        self.e_matrix = e_matrix
        self.f_matrix = f_matrix
        self.q_matrix = q_matrix
