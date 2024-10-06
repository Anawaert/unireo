"""
该模块定义了立体相机标定相关的函数
\n
This module defines functions related to stereo camera calibration
"""

import cv2
import numpy as np
import calib.calib_data as calib_data


def get_calib_data(chessboard_size: tuple, square_size: int, img_shape: tuple, left_img_series: list,
                   right_img_series: list) -> calib_data.StereoCalibData:
    """
    获取立体相机标定数据
    \n
    Get Stereo Camera Calibration Data
    :param chessboard_size: 棋盘格内角点尺寸（长 × 宽） Chessboard Inner Corner Size (a × b)
    :param square_size: 棋盘格方块大小（单位：毫米） Chessboard Square Size (Unit: mm)
    :param img_shape: 单目图像的形状（宽度 × 高度 × 通道） Image Size of Monocular (width × height × channel(s))
    :param left_img_series: 左目图像序列（列表[字符串]） Left Eye Image Sequence (List[AnyStr])
    :param right_img_series: 右目图像序列（列表[字符串]） Right Eye Image Sequence (List[AnyStr])
    :return: 立体相机标定数据 Stereo Camera Calibration Data

    示例（Example）：
    \n
    stereo_calib_data = stereo_calib.get_calib_data((11, 8), 20, (1280, 720, 3),
     ['path/to/left1.jpg', 'path/to/left2.jpg'], ['path/to/right1.jpg', 'path/to/right2.jpg'])
    """

    # 终止标准
    # Termination Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 生成棋盘格角点的世界坐标
    # Generate World Coordinates of Chessboard Corner Points
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

    # 存储棋盘格角点的世界坐标和图像坐标
    # Store World Coordinates and Image Coordinates of Chessboard Corner Points
    obj_points = []  # 世界坐标系中的三维点 Three-dimensional Points in the World Coordinate System
    left_img_points = []  # 左目图像坐标系中的二维点 Two-dimensional Points in the Left Eye Image Coordinate System
    right_img_points = []  # 右目图像坐标系中的二维点 Two-dimensional Points in the Right Eye Image Coordinate System

    # 图像变量
    # Image Variables
    left = None
    right = None
    left_gray = None
    right_gray = None

    # 迭代左目和右目图像序列
    # Iterate the Left Eye and Right Eye Image Sequences
    for left_img_path, right_img_path in zip(left_img_series, right_img_series):
        # 读取左目和右目图像
        # Read the Left Eye and Right Eye Images
        left = cv2.imread(left_img_path)
        right = cv2.imread(right_img_path)
        left_gray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

        # 查找棋盘格角点
        # Find Chessboard Corner Points
        left_ret, left_corners = cv2.findChessboardCorners(left_gray, chessboard_size, None)
        right_ret, right_corners = cv2.findChessboardCorners(right_gray, chessboard_size, None)

        # 若找到角点，则添加到世界坐标和图像坐标中
        # If the corner points are found, add them to the world coordinates and image coordinates
        if left_ret and right_ret:
            obj_points.append(objp)

            # 亚像素级角点检测
            # Subpixel Level Corner Detection
            left_corners2 = cv2.cornerSubPix(left_gray, left_corners, (11, 11), (-1, -1), criteria)
            right_corners2 = cv2.cornerSubPix(right_gray, right_corners, (11, 11), (-1, -1), criteria)

            left_img_points.append(left_corners2)
            right_img_points.append(right_corners2)

    if (left is not None) and (right is not None) and (left_gray is not None) and (right_gray is not None):
        # left_height, left_width, left_channels = left.shape
        # right_height, right_width, right_channels = right.shape

        # 标定相机
        # Calibrate the Camera
        # 首先执行单目标定
        # Execute Monocular Calibration First
        left_ret_val, left_camera_matrix, left_dist_coeffs, left_rvecs, left_tvecs = cv2.calibrateCamera(
            obj_points, left_img_points, img_shape[0:2], None, None)

        new_left_camera_matrix, left_roi = cv2.getOptimalNewCameraMatrix(left_camera_matrix, left_dist_coeffs,
                                                                         img_shape[0:2], 1, img_shape[0:2])

        right_ret_val, right_camera_matrix, right_dist_coeffs, right_rvecs, right_tvecs = cv2.calibrateCamera(
            obj_points, right_img_points, img_shape[0:2], None, None)

        new_right_camera_matrix, right_roi = cv2.getOptimalNewCameraMatrix(right_camera_matrix, right_dist_coeffs,
                                                                           img_shape[0:2], 1, img_shape[0:2])

        # 接着执行立体标定
        # Then Execute Stereo Calibration
        default_flags = 0
        default_flags |= cv2.CALIB_FIX_INTRINSIC

        (stereo_ret_val, new_left_camera_matrix, left_dist_coeffs, new_right_camera_matrix, right_dist_coeffs,
         rotation_matrix, translation_vector, essential_matrix, fundamental_matrix) = cv2.stereoCalibrate(
            obj_points, left_img_points, right_img_points, new_left_camera_matrix, left_dist_coeffs,
            new_right_camera_matrix, right_dist_coeffs, left_gray.shape[::-1], criteria, default_flags)

        # 默认矫正尺度
        # Default Correction Scale
        rectification_scale = 1
        (left_rectification_matrix, right_rectification_matrix, left_projection_matrix, right_projection_matrix,
         q_matrix, left_roi, right_roi) = cv2.stereoRectify(new_left_camera_matrix, left_dist_coeffs,
                                                            new_right_camera_matrix,
                                                            right_dist_coeffs, left_gray.shape[::-1], rotation_matrix,
                                                            translation_vector, rectification_scale, (0, 0))

        left_stereo_map = cv2.initUndistortRectifyMap(new_left_camera_matrix, left_dist_coeffs,
                                                      left_rectification_matrix,
                                                      left_projection_matrix, left_gray.shape[::-1], cv2.CV_16SC2)
        right_stereo_map = cv2.initUndistortRectifyMap(new_right_camera_matrix, right_dist_coeffs,
                                                       right_rectification_matrix,
                                                       right_projection_matrix, right_gray.shape[::-1], cv2.CV_16SC2)
        # 创建立体相机标定数据对象
        # Create Stereo Camera Calibration Data Object
        stereo_calib_data = calib_data.StereoCalibData(obj_points, left_img_points, right_img_points,
                                                       left_camera_matrix, left_dist_coeffs, left_rvecs, left_tvecs,
                                                       left_rectification_matrix, left_projection_matrix,
                                                       left_stereo_map, right_camera_matrix, right_dist_coeffs,
                                                       right_rvecs, right_tvecs, right_rectification_matrix,
                                                       right_projection_matrix, right_stereo_map, rotation_matrix,
                                                       translation_vector, essential_matrix, fundamental_matrix,
                                                       q_matrix)

        return stereo_calib_data


def undistort_imgs(left_frame: np.ndarray, right_frame: np.ndarray,
                   stereo_calib_data: calib_data.StereoCalibData) -> tuple:
    """
    双目畸变图像矫正
    \n
    Stereo Distortion Image Correction
    :param left_frame: 左目图像 Left Eye Image
    :param right_frame: 右目图像 Right Eye Image
    :param stereo_calib_data: 立体相机标定数据 Stereo Camera Calibration Data
    :return: 矫正后的左目图像和右目图像 Corrected Left Eye Image and Right Eye Image

    示例（Example）：
    \n
    undistorted_left, undistorted_right = stereo_calib.undistort_imgs(left_frame, right_frame)
    """

    ud_left = cv2.remap(left_frame, stereo_calib_data.left_stereo_map_x, stereo_calib_data.left_stereo_map_y,
                        cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    ud_right = cv2.remap(right_frame, stereo_calib_data.right_stereo_map_x, stereo_calib_data.right_stereo_map_y,
                         cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    return ud_left, ud_right
