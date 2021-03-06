#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if len(p_list) != 2:
        return []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        length = max(abs(x1 - x0), abs(y1 - y0))
        if length == 0:
            delta_x = delta_y = 0
        else:
            delta_x = (x1 - x0) / length
            delta_y = (y1 - y0) / length

        x = x0 + 0.5
        y = y0 + 0.5

        i = 1
        while(i <= length):
            result.append((int(x), int(y)))
            x = x + delta_x
            y = y + delta_y
            i = i + 1

    elif algorithm == 'Bresenham':
        flag = False
        delta_x = abs(x1 - x0)
        delta_y = abs(y1 - y0)
        result.append((x0, y0))
        if delta_x == 0 and delta_y == 0:  # only a dot
            return result
        if(delta_x < delta_y):
            flag = True
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            delta_x, delta_y = delta_y, delta_x

        if x1 - x0 > 0:
            tx = 1
        else:
            tx = -1
        if y1 - y0 > 0:
            ty = 1
        else:
            ty = -1

        x = x0
        y = y0
        e = 2 * delta_y - delta_x
        while x != x1:
            if e < 0:  # right
                e = e + 2 * delta_y
            else:  # top_right
                e = e + 2 * delta_y - 2 * delta_x
                y = y + ty
            x = x + tx
            if flag:
                result.append((y, x))
            else:
                result.append((x, y))

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_polygon_gui(p_list, algorithm):
    """绘制多边形 in gui

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list) - 1):
        line = draw_line([p_list[i], p_list[i + 1]], algorithm)
        result += line
    return result

# https://www.geogebra.org/
# https://blog.csdn.net/orbit/article/details/7496008?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    xc = (x0 + x1) // 2
    yc = (y0 + y1) // 2  # the center of ellipse
    rx = abs((x1 - x0)) // 2
    ry = abs((y1 - y0)) // 2
    flag = False  # 焦点是否在y轴上
    if rx < ry:
        rx, ry = ry, rx
        flag = True
    x = 0
    y = ry
    ry_sq = ry * ry
    rx_sq = rx * rx
    p1 = ry_sq - rx_sq * ry + rx_sq / 4
    res = []
    while ry_sq * x < rx_sq * y:
        # section 1
        if flag:
            xk, yk = y, x
        else:
            xk, yk = x, y
        res.extend([(xk + xc, yk + yc), (xc - xk, yk + yc),
                    (xk + xc, yc - yk), (xc - xk, yc - yk)])

        if p1 < 0:
            p1 = p1 + 2 * ry_sq * x + 3 * ry_sq
            x = x + 1
        else:
            p1 = p1 + 2 * ry_sq * x - 2 * rx_sq * y + 2 * rx_sq + 3 * ry_sq
            x = x + 1
            y = y - 1

    p2 = ry_sq * (x + 0.5) * (x + 0.5) + rx_sq * \
        (y - 1) * (y - 1) - rx_sq * ry_sq
    while y > 0:
        # section 2
        if flag:
            xk, yk = y, x
        else:
            xk, yk = x, y
        res.extend([(xk + xc, yk + yc), (xc - xk, yk + yc),
                    (xk + xc, yc - yk), (xc - xk, yc - yk)])
        if p2 >= 0:
            p2 = p2 - 2 * rx_sq * y + 3 * rx_sq
            y = y - 1
        else:
            p2 = p2 + 2 * ry_sq * x - 2 * rx_sq * y + 2 * ry_sq + 3 * rx_sq
            x = x + 1
            y = y - 1

    if flag:
        res.extend([(xc, rx + yc), (xc, yc - rx)])
    else:
        res.extend([(rx + xc, yc), (xc - rx, yc)])
    return res


def Bezier_Point(t, p_list):
    """针对某个t值计算出对应点

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param t: (float) 比例
    :return: (list of int:[x,y]) 对应t值下Bezier曲线生成的点
    """
    new_list = []
    while (len(p_list) > 1):
        for i in range(0, len(p_list) - 1):
            # Q is a point between p_list[i] and p_list[i+1], parametised by t.
            Qx = (1 - t) * p_list[i][0] + t * p_list[i + 1][0]
            Qy = (1 - t) * p_list[i][1] + t * p_list[i + 1][1]
            new_list.append([Qx, Qy])
        p_list = new_list
        new_list = []

    x = int(p_list[0][0])
    y = int(p_list[0][1])
    return x, y


def Basefunction(i, k, u):
    """计算B样条曲线的基函数取值

    :param i:(int)index of base function
    :param k:(int)阶数 degree+1
    :param u:parameter
    :return:the value of base function
    """
    Nik_u = 0.0
    if k == 1:
        if u < i + 1 and u >= i:
            Nik_u = 1.0
        else:
            Nik_u = 0.0
    else:
        Nik_u = ((u - i) / (k - 1)) * Basefunction(i, k - 1, u) + \
            ((i + k - u) / (k - 1)) * Basefunction(i + 1, k - 1, u)

    return Nik_u


# https://github.com/torresjrjr/Bezier.py
# https://en.wikipedia.org/wiki/B%C3%A9zier_curve
# https://blog.csdn.net/xiaozhangcsdn/article/details/98963937
# https://www.cnblogs.com/nobodyzhou/p/5451528.html

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    res = []
    if algorithm == "Bezier":
        # 绘制贝塞尔曲线
        t_step = 0.0005
        t = 0
        while t <= 1:
            res.append(Bezier_Point(t, p_list))
            t = t + t_step
    elif algorithm == "B-spline":
        # 绘制3次均匀B样条曲线
        k = 3
        n = len(p_list) - 1  # num of control points is n+1
        u = k
        step = 0.001
        while u <= n + 1:
            p_x = 0.0
            p_y = 0.0
            for i in range(n + 1):
                Nik = Basefunction(i, k + 1, u)
                p_x = p_x + p_list[i][0] * Nik
                p_y = p_y + p_list[i][1] * Nik
            u = u + step
            res.append([int(p_x), int(p_y)])
    return res

# https://blog.csdn.net/a3631568/article/details/53637473


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res = []
    for x, y in p_list:
        res.append((x + dx, y + dy))
    return res


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res = []
    r = math.radians(360 + r)
    for x0, y0 in p_list:
        new_x = x + (x0 - x) * math.cos(r) - (y0 - y) * math.sin(r)
        new_y = y + (x0 - x) * math.sin(r) + (y0 - y) * math.cos(r)
        res.append([round(new_x), round(new_y)])
    return res


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    res = []
    for x0, y0 in p_list:
        new_x = x + (x0 - x) * s
        new_y = y + (y0 - y) * s
        res.append([round(new_x), round(new_y)])
    return res


def encode(x_min, y_min, x_max, y_max, x, y):
    LEFT   = 0b0001
    RIGHT  = 0b0010
    BOTTOM = 0b0100
    TOP    = 0b1000
    code   = 0
    if x < x_min:
        code += LEFT
    elif x > x_max:
        code += RIGHT
    if y > y_max:
        code += BOTTOM
    elif y < y_min:
        code += TOP
    return code
# https://www.cnblogs.com/cnblog-wuran/p/9813841.html
# https://www.cnblogs.com/iamfatotaku/p/12496937.html


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    if len(p_list) != 2:
        return []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    res = []
    if algorithm == 'Cohen-Sutherland':
        LEFT   = 0b0001
        RIGHT  = 0b0010
        BOTTOM = 0b0100
        TOP    = 0b1000
        code   = [0, 0]
        code[0] = encode(x_min, y_min, x_max, y_max, x0, y0)
        code[1] = encode(x_min, y_min, x_max, y_max, x1, y1)
        res = p_list
        while code[0] | code[1] != 0:
            if code[0] & code[1] != 0:
                return []  # empty
            for i in range(2):
                x, y = res[i]
                if code[i] == 0:
                    continue
                else:
                    if LEFT & code[i] != 0:
                        x = x_min
                        if x0 == x1:
                            y = y0
                        else:
                            y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                    elif RIGHT & code[i] != 0:
                        x = x_max
                        if x0 == x1:
                            y = y0
                        else:
                            y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                    elif BOTTOM & code[i] != 0:
                        y = y_max
                        x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                    elif TOP & code[i] != 0:
                        y = y_min
                        x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                    code[i] = encode(x_min, y_min, x_max, y_max, x, y)
                    res[i] = [int(x), int(y)]

    elif algorithm == 'Liang-Barsky':
        dx = x1 - x0
        dy = y1 - y0
        p = [-dx, dx, -dy, dy]
        q = [x0 - x_min, x_max - x0, y0 - y_min, y_max - y0]
        u0, u1 = 0, 1
        for k in range(4):
            if p[k] == 0:
                if q[k] < 0:
                    return []
            else:
                u = q[k] / p[k]
                if p[k] < 0:
                    u0 = max(u0, u)
                else:
                    u1 = min(u1, u)
        if u0 > u1:
            return []
        x_0 = round(x0 + u0 * dx)
        y_0 = round(y0 + u0 * dy)
        x_1 = round(x0 + u1 * dx)
        y_1 = round(y0 + u1 * dy)
        res = [[x_0, y_0], [x_1, y_1]]

    return res
