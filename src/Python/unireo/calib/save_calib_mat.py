"""
本模块用于操作相机标定文件，保存标定文件中的的标定数据
This module is used to operate the camera calibration file and save the calibration data in the calibration file
"""

# import yaml
# import calib.calib_data as calib_data


# def save_mono_calib_data(mono_calib_data: calib_data.MonoCalibData, left_calib_file_path: str) -> bool:
#     """
#     保存单目相机标定数据
#
#     Save Monocular Camera Calibration Data
#
#     :param mono_calib_data: 单目相机标定数据 Monocular camera calibration data
#     :param left_calib_file_path: 保存路径 Save path
#     """
#
#     try:
#         data = {
#             'camera_matrix': mono_calib_data.camera_matrix.tolist(),
#             'dist_coeffs': mono_calib_data.dist_coeffs.tolist(),
#             'rvecs': mono_calib_data.rvecs,
#             'tvecs': mono_calib_data.tvecs,
#             'new_camera_matrix': mono_calib_data.new_camera_matrix.tolist(),
#             'remap_roi': mono_calib_data.remap_roi,
#             'map_x': mono_calib_data.map_x.tolist(),
#             'map_y': mono_calib_data.map_y.tolist()
#         }
#
#         with open(left_calib_file_path, 'w') as f:
#             yaml.dump(data, f)
#
#         return True
#     except Exception as e:
#         print("Failed to save monocular camera calibration data: ", e)
#         return False


# def save_stereo_calib_date(stereo_calib_data: calib_data.StereoCalibData, stereo_calib_file_path: str) -> bool:
#     """
#     保存双目相机标定数据
#
#     Save Stereo Camera Calibration Data
#
#     :param stereo_calib_data: 双目相机标定数据 Stereo camera calibration data
#     :param stereo_calib_file_path: 保存路径 Save path
#     """
#
#     try:
#         data = {
#             'obj_points': stereo_calib_data.obj_points,
#             'left_img_points': stereo_calib_data.left_img_points,
#             'right_img_points': stereo_calib_data.right_img_points,
#             'left_cam_matrix': stereo_calib_data.left_cam_matrix.tolist(),
#             'left_dist_coeffs': stereo_calib_data.left_dist_coeffs.tolist(),
#             'left_rvecs': stereo_calib_data.left_rvecs,
#             'left_tvecs': stereo_calib_data.left_tvecs,
#             'left_rect_matrix': stereo_calib_data.left_rect_matrix.tolist(),
#             'left_projection_matrix': stereo_calib_data.left_projection_matrix.tolist(),
#             'left_stereo_map_x': stereo_calib_data.left_stereo_map_x.tolist(),
#             'left_stereo_map_y': stereo_calib_data.left_stereo_map_y.tolist(),
#             'right_cam_matrix': stereo_calib_data.right_cam_matrix.tolist(),
#             'right_dist_coeffs': stereo_calib_data.right_dist_coeffs.tolist(),
#             'right_rvecs': stereo_calib_data.right_rvecs,
#             'right_tvecs': stereo_calib_data.right_tvecs,
#             'right_rect_matrix': stereo_calib_data.right_rect_matrix.tolist(),
#             'right_projection_matrix': stereo_calib_data.right_projection_matrix.tolist(),
#             'right_stereo_map_x': stereo_calib_data.right_stereo_map_x.tolist(),
#             'right_stereo_map_y': stereo_calib_data.right_stereo_map_y.tolist(),
#             'r_matrix': stereo_calib_data.r_matrix.tolist(),
#             't_vector': stereo_calib_data.t_vector.tolist(),
#             'e_matrix': stereo_calib_data.e_matrix.tolist(),
#             'f_matrix': stereo_calib_data.f_matrix.tolist(),
#             'q_matrix': stereo_calib_data.q_matrix.tolist()
#         }
#
#         with open(stereo_calib_file_path, 'w') as f:
#             yaml.dump(data, f)
#
#         return True
#     except Exception as e:
#         print("Failed to save stereo camera calibration data: ", e)
#         return False
