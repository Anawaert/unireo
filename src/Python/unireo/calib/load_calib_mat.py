"""
本模块用于操作相机标定文件，读取标定文件中的标定数据
This module is used to operate the camera calibration file and read the calibration data in the calibration file
"""

# import yaml
# import numpy as np
# import calib.calib_data as calib_data


# def load_mono_calib_data(left_calib_file_path: str) -> calib_data.MonoCalibData:
#     """
#     读取单目相机标定数据
#     Read Monocular Camera Calibration Data
#
#     :param left_calib_file_path: 标定文件路径 Calibration file path
#     :return: 单目相机标定数据 Monocular camera calibration data
#     """
#     try:
#         with open(left_calib_file_path, 'r') as f:
#             data = yaml.load(f, Loader=yaml.FullLoader)
#
#             object_points = data['object_points']
#             image_points = data['image_points']
#             camera_matrix = data['camera_matrix']
#             dist_coeffs = data['dist_coeffs']
#             rvecs = data['rvecs']
#             tvecs = data['tvecs']
#             new_camera_matrix = data['new_camera_matrix']
#             remap_roi = data['remap_roi']
#             map_x = data['map_x']
#             map_y = data['map_y']
#
#             return calib_data.MonoCalibData(object_points, image_points, camera_matrix, dist_coeffs, rvecs, tvecs,
#                                             new_camera_matrix, remap_roi, (map_x, map_y))
#     except Exception as e:
#         print("Failed to load monocular camera calibration data: ", e)
#         raise e
#
#
# def load_stereo_calib_data(stereo_calib_file_path: str) -> calib_data.StereoCalibData:
#     """
#     读取双目相机标定数据
#     Read Stereo Camera Calibration Data
#
#     :param stereo_calib_file_path: 标定文件路径 Calibration file path
#     :return: 双目相机标定数据 Stereo camera calibration data
#     """
#
#     try:
#         with open(stereo_calib_file_path, 'r') as f:
#             data = yaml.load(f, Loader=yaml.FullLoader)
#
#             obj_points = data['obj_points']
#             left_img_points = data['left_img_points']
#             right_img_points = data['right_img_points']
#             left_cam_matrix = data['left_cam_matrix']
#             left_dist_coeffs = data['left_dist_coeffs']
#             left_rvecs = data['left_rvecs']
#             left_tvecs = data['left_tvecs']
#             left_rect_matrix = data['left_rect_matrix']
#             left_projection_matrix = data['left_projection_matrix']
#             left_stereo_map_x = data['left_stereo_map_x']
#             left_stereo_map_y = data['left_stereo_map_y']
#             right_cam_matrix = data['right_cam_matrix']
#             right_dist_coeffs = data['right_dist_coeffs']
#             right_rvecs = data['right_rvecs']
#             right_tvecs = data['right_tvecs']
#             right_rect_matrix = data['right_rect_matrix']
#             right_projection_matrix = data['right_projection_matrix']
#             right_stereo_map_x = data['right_stereo_map_x']
#             right_stereo_map_y = data['right_stereo_map_y']
#             r_matrix = data['r_matrix']
#             t_vector = data['t_vector']
#             e_matrix = data['e_matrix']
#             f_matrix = data['f_matrix']
#             q_matrix = data['q_matrix']
#
#             return calib_data.StereoCalibData(obj_points, left_img_points, right_img_points, left_cam_matrix,
#                                               left_dist_coeffs, left_rvecs, left_tvecs, left_rect_matrix,
#                                               left_projection_matrix,
#                                               (left_stereo_map_x, left_stereo_map_y), right_cam_matrix,
#                                               right_dist_coeffs,
#                                               right_rvecs, right_tvecs, right_rect_matrix, right_projection_matrix,
#                                               (right_stereo_map_x, right_stereo_map_y), r_matrix,
#                                               t_vector, e_matrix, f_matrix, q_matrix)
#     except Exception as e:
#         print("Failed to load stereo camera calibration data: ", e)
#         raise e
