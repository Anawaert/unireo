"""
本模块定义了一些常用的扩展函数，便于程序流程的控制
\n
This module defines some common extension functions for controlling the program flow
"""

import cv2
import unireo.utils.shared_vars as sv


def global_waitKey() -> int:
    """
    返回按键值并更新最后按键值的记录
    \n
    Return the key value and update the record of the last key value
    """

    sv.latest_key = cv2.waitKey(1) & 0xFF
    return sv.latest_key
