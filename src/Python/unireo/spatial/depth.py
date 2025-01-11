import cv2
import numpy as np
import unireo.calib.calib_data as calib_data
import unireo.cam_info.cam_params as cam_params


def generate_depth_img(left_img: np.ndarray, right_img: np.ndarray, stereo_calib_data: calib_data.StereoCalibData,
                       quality_level: int, depth_value_unit: int) -> np.ndarray:

    # 检查左右图像的尺寸是否相同
    # Check if the size of the left and right images is the same
    if left_img.shape != right_img.shape:
        raise ValueError("Left and right images must have the same shape")

    # 先预设均衡深度图精度所需的参数
    # First set the parameters required for the equal depth map accuracy
    min_disparity = 0  # 最小视差 Minimum disparity
    num_disparities = 16 * 4  # 视差范围，必须是16的倍数 Disparity range, must be a multiple of 16
    block_size = 5  # 匹配块的大小 Block size for matching
    p1 = 8 * 3 * (block_size ** 2)  # 惩罚系数1 Penalty coefficient 1
    p2 = 32 * 3 * (block_size ** 2)  # 惩罚系数2 Penalty coefficient 2
    disp12_max_diff = 3  # 左右视差最大差异，-1为不限制 Maximum difference between left and right disparity, -1 is unlimited
    uniqueness_ratio = 10  # 视差唯一性比率 Disparity uniqueness ratio
    speckle_window_size = 100  # 视差检查窗口大小 Disparity check window size
    speckle_range = 16  # 视差检查范围 Disparity check range
    pre_filter_cap = 100  # 图像预处理滤波器容量 Image preprocessing filter capacity
    mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY  # 算法模式 Algorithm mode

    # 根据不同深度图精度要求调整参数
    # Adjust parameters according to different depth map accuracy requirements
    if quality_level == cam_params.DepthQualityLevel.DEPTH_QUALITY_LOW:
        min_disparity = 0
        num_disparities = 16 * 3
        block_size = 5
        p1 = 8 * 3 * (block_size ** 2)
        p2 = 32 * 3 * (block_size ** 2)
        disp12_max_diff = -1
        uniqueness_ratio = 5
        speckle_window_size = 100
        speckle_range = 32
        pre_filter_cap = 50
        mode = cv2.STEREO_SGBM_MODE_SGBM
    elif quality_level == cam_params.DepthQualityLevel.DEPTH_QUALITY_HIGH:
        min_disparity = 0
        num_disparities = 16 * 6
        block_size = 7
        p1 = 8 * 3 * (block_size ** 2)
        p2 = 32 * 3 * (block_size ** 2)
        disp12_max_diff = 3
        uniqueness_ratio = 15
        speckle_window_size = 100
        speckle_range = 16
        pre_filter_cap = 100
        mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY
    elif quality_level == cam_params.DepthQualityLevel.DEPTH_QUALITY_ULTRA:
        min_disparity = 0
        num_disparities = 16 * 7
        block_size = 7
        p1 = 8 * 3 * (block_size ** 2)
        p2 = 32 * 3 * (block_size ** 2)
        disp12_max_diff = 5
        uniqueness_ratio = 20
        speckle_window_size = 150
        speckle_range = 8
        pre_filter_cap = 150
        mode = cv2.STEREO_SGBM_MODE_HH4

    # 创建SGBM对象
    # Create SGBM object
    sgbm = cv2.StereoSGBM.create(minDisparity=min_disparity, numDisparities=num_disparities, blockSize=block_size,
                                 P1=p1, P2=p2, disp12MaxDiff=disp12_max_diff, uniquenessRatio=uniqueness_ratio,
                                 speckleWindowSize=speckle_window_size, speckleRange=speckle_range,
                                 preFilterCap=pre_filter_cap, mode=mode)

    # 计算相对左目的视差图
    # Calculate the relative left disparity map
    disparity = sgbm.compute(left_img, right_img)

    # 对视差图中的空洞进行填充
    # Fill the holes in the disparity map
    disparity_median_blurred = cv2.medianBlur(disparity, 5)
    disparity_bt_filter = cv2.bilateralFilter(disparity_median_blurred.astype(np.float32), d=9, sigmaColor=75,
                                              sigmaSpace=75)

    # 重投影视差图到深度图
    # Reproject the disparity map to the depth map
    depth_map = cv2.reprojectImageTo3D(disparity_bt_filter, stereo_calib_data.q_matrix, handleMissingValues=True)

    depth_map = depth_map * 16 / depth_value_unit

    return depth_map
