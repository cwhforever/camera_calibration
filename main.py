# coding=utf-8
# copied by cwh in 2024/03/06
"""
    主要修改参数：
        XX,YY,L    git
        test        测试标志位        
        images_path 采集的标定板图片所在路径

"""""

import numpy as np
import cv2
import os
from capture_images import capture_images

np.set_printoptions(precision=8, suppress=True)

# 弧度转度系数
RTA = 180 / 3.1415926

images_path = 'images'  # 手眼标定采集的标定板图片所在路径

# 角点的个数以及棋盘格间距
XX = 10  # 标定板中的长度对应的角点的个数
YY = 7  # 标定板中的宽度对应的角点的个数
L = 0.015  # 标定板一格的长度  单位为米

test = True  # 测试标志位


def camera_calibration(xx=XX, yy=YY, ll=L, test_flag=True):
    """
        获取相机的内参，标定板的旋转、平移向量
    :param xx: 标定板长边角点个数
    :param yy: 标定板宽边角点个数
    :param ll: 标定板一格长度,单位米
    :param test_flag: 测试标志位，True：打印图片，False:不打印
    :return: 相机内参，畸变系数
    """""
    # 设置寻找亚像素角点的参数，采用的停止准则是最大循环次数30和最大误差容限0.001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)

    # 获取标定板角点的位置
    objp = np.zeros((xx * yy, 3), np.float32)
    objp[:, :2] = np.mgrid[0:xx, 0:yy].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
    objp = ll * objp

    obj_points = []  # 存储3D点
    img_points = []  # 存储2D点
    err_images = []  # 存储未识别的图片标

    for i in range(0, 50):  # 标定好的图片在images_path路径下，从0.jpg到x.jpg   一次采集的图片最多不超过50张，我们遍历从0.jpg到50.jpg ，选择能够读取的到的图片
        # image = f"images_path\\{i}.jpg"
        image = f"images/{i}.png"
        # 若图片存在
        if os.path.exists(image):
            print(f"通过 {image}")
            # 读取图片，返回图像矩阵
            img = cv2.imread(image)

            # 将BGR格式转换成灰度图片，返回图像矩阵
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 获取图像的行列数
            size = gray.shape[::-1]
            # 确认是否存在标定板，参数：(灰度图像，标定板对角个数(长个数，宽个数),检测到的角点的输出数组)
            ret, corners = cv2.findChessboardCorners(gray, (xx, yy), None)
            # 若存在标定板
            if ret:
                # 将值添加到数组末尾
                obj_points.append(objp)
                # 在原角点的基础上寻找亚像素角点
                corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
                if [corners2]:
                    img_points.append(corners2)
                    img = cv2.drawChessboardCorners(img, (xx, yy), corners2, ret)
                else:
                    img_points.append(corners)
                    img = cv2.drawChessboardCorners(img, (xx, yy), corners, ret)
            else:
                print("ret = ", ret)
            # 显示角点
            if test_flag:
                cv2.imshow('img', img)
                cv2.waitKey(0)

    cv2.destroyAllWindows()

    num = len(img_points)  # 标定的图片数量

    # 标定,得到图案在相机坐标系下的位姿
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, size, None, None)

    return mtx, dist


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    capture_images(images_path)
    camera_mat, camera_dist = camera_calibration(XX, YY, L, test)
    print(f"相机内参\n{camera_mat}")
    print(f"畸变系数\n{camera_dist}")
