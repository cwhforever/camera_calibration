# coding=utf-8
# copied by cwh in 2024/03/05

import cv2

save_path = "images"


def capture_images(path=save_path):
    """
        采集图像
    :return:
    """""
    # 返回相机索引
    camera_index = find_camera_index()

    print(f"相机索引：{camera_index}")

    # 相机索引存在标志位
    flag = False

    # 选择一个相机打开
    choice = int(input(f"请输入想打开的相机索引:"))
    for i in range(len(camera_index)):
        if choice == camera_index[i]:
            print(f"启用相机{i}")
            flag = True

    if flag:
        save_images(choice,path)
        return 1
    else:
        print(f"没有索引{choice}的相机")
        return 0


def find_camera_index():
    """
        找到当前设备的所有相机索引值
    :return: 
    """""
    index = []
    # 尝试索引值从0到9
    for i in range(10):
        cap = cv2.VideoCapture(i)

        # 检查相机是否成功打开
        if cap.isOpened():
            print(f"相机名称：{cap.getBackendName()},索引值: {i}")
            index.append(i)
            cap.release()
    return index


def save_images(index,path):
    # 打开摄像头
    cap = cv2.VideoCapture(index)
    cnt = 0
    print("Esc退出程序，空格截取图片")
    while True:
        # 读取一帧图像
        ret, frame = cap.read()

        # 如果成功读取图像，则显示图像
        if ret:
            cv2.imshow(f"camera{index}", frame)

        # 等待用户按键
        key = cv2.waitKey(1) & 0xFF

        # 如果按下空格键（ASCII码为32），则保存截图
        if key == 32:
            # 设置保存路径和文件名
            filename = f"{path}/{cnt}.png"
            cnt += 1
            # 保存截图
            cv2.imwrite(filename, frame)
            print(f"截图保存 {filename}")

        # 如果按下ESC键（ASCII码为27），则退出循环
        elif key == 27:
            print("退出")
            break

    # 关闭摄像头和窗口
    cap.release()
    cv2.destroyAllWindows()

# 按装订区域中的绿色按钮以运行脚本。
