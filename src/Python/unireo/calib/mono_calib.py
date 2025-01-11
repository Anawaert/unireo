"""
本模块定义了单目相机标定对象与畸变矫正函数，用于获取与使用单目相机的内参

This module defines the monocular camera calibration object and distortion correction function, which are used to
obtain and use the intrinsic parameters of the monocular camera
"""

import cv2
import numpy as np
import unireo.calib.calib_data as calib_data


def get_calib_data(chessboard_size: tuple, img_size: tuple, img_series: list) -> calib_data.MonoCalibData:
    """
    获取单目相机标定数据

    Get monocular camera calibration data

    :param chessboard_size: 棋盘格内角点尺寸（长 × 宽） Chessboard inner corner size (a × b)
    :param img_size: 图像大小（宽度 × 高度） Image size (width × height)
    :param img_series: 图像序列（列表[字符串]） Image sequence (List[AnyStr])
    :return: 单目相机标定数据 Monocular camera calibration data

    示例（Example）：

    mono_calib_data = mono_calib.get_calib_data((9, 6), (640, 480), ['path/to/image1.jpg', 'path/to/image2.jpg])
    """
    # 生成棋盘格角点的世界坐标
    # Generate World Coordinates of Chessboard Corner Points
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # 生成终止标准
    # Generate Termination Criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 存储棋盘格角点的世界坐标和图像坐标
    # Store World Coordinates and Image Coordinates of Chessboard Corner Points
    obj_points = []  # 世界坐标系中的三维点 World Coordinates of Three-dimensional Points
    img_points = []  # 图像坐标系中的二维点 Two-dimensional Points in the Image Coordinate System

    # 遍历图像序列
    # Traverse the Image Sequence
    for image in img_series:
        # 读取图像
        # Read Image
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 查找棋盘格角点
        # Find Chessboard Corner Points
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # 若找到角点，则添加到世界坐标和图像坐标中
        # If the corner points are found, add them to the world coordinates and image coordinates
        if ret:
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

    # 标定相机
    # Calibrate the Camera
    ret_val, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, img_size, None,
                                                                            None)

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, img_size, 1, img_size)

    # 创建单目相机标定数据对象
    # Create Monocular Camera Calibration Data Object
    mono_calib_data = calib_data.MonoCalibData(img_size, obj_points, img_points, camera_matrix, dist_coeffs, rvecs, tvecs,
                                               new_camera_matrix, roi)

    return mono_calib_data


def undistort_img(img: np.ndarray, mono_calib_data: calib_data.MonoCalibData) -> np.ndarray:
    """
    单目图像畸变矫正

    Monocular image distortion correction

    :param img: 待矫正图像 Image to be Corrected
    :param mono_calib_data: 单目相机标定数据 Monocular camera calibration data
    :return: 矫正后的图像 Corrected image

    示例（Example）：

    undistorted_img = mono_calib.undistort_img(img, mono_calib_data)
    """

    remap = cv2.initUndistortRectifyMap(mono_calib_data.camera_matrix, mono_calib_data.dist_coeffs,
                                        None, mono_calib_data.new_camera_matrix, mono_calib_data.image_size, cv2.CV_32FC1)
    map_x = remap[0]
    map_y = remap[1]

    # 畸变矫正
    # Distortion Correction
    undistorted_img = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

    # 裁剪图像有效区域
    # Crop the Effective Area of the Image
    x1, y1, w, h = mono_calib_data.remap_roi
    undistorted_img = undistorted_img[y1:y1 + h, x1:x1 + w]

    return undistorted_img


def reprojection_error(mono_calib_data: calib_data.MonoCalibData) -> float:
    """
    计算投影误差

    Calculate the reprojection error

    :param mono_calib_data: 单目相机标定数据 Monocular camera calibration data
    :return: 投影误差 Reprojection error

    示例（Example）：

    reprojection_error = mono_calib.reprojection_error(mono_calib_data)
    """

    total_error: float = 0.0
    for i in range(len(mono_calib_data.object_points)):
        img_points_val, _ = cv2.projectPoints(mono_calib_data.object_points[i], mono_calib_data.rvecs[i],
                                              mono_calib_data.tvecs[i], mono_calib_data.camera_matrix,
                                              mono_calib_data.dist_coeffs)
        error = cv2.norm(mono_calib_data.image_points[i], img_points_val, cv2.NORM_L2) / len(img_points_val)
        total_error += error

    return total_error / len(mono_calib_data.object_points)
