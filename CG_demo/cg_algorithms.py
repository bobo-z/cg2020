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
        length = max(abs(x1-x0), abs(y1-y0))
        if length == 0:
            delta_x = delta_y = 0
        else:
            delta_x = (x1-x0)/length
            delta_y = (y1-y0)/length

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
        delta_x = abs(x1-x0)
        delta_y = abs(y1-y0)
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
        e = 2*delta_y-delta_x
        while x != x1:
            if e < 0:  # right
                e = e + 2*delta_y
            else:  # top_right
                e = e + 2*delta_y - 2*delta_x
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


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    xc = (x0+x1)//2
    yc = (y0+y1)//2  # the center of ellipse
    rx = (x1-x0)//2
    ry = (y1-y0)//2
    flag = False  # 焦点是否在y轴上
    if rx < ry:
        rx, ry = ry, rx
        flag = True
    x = 0
    y = ry
    ry_sq = ry*ry
    rx_sq = rx*rx
    p1 = ry_sq-rx_sq*ry+rx_sq/4
    res = []
    if flag:
        res.extend([(ry+xc, yc), (xc-ry, yc)])
    else:
        res.extend([(xc, ry+yc), (xc, yc-ry)])
    while ry_sq*x < rx_sq*y:
        # section 1
        if p1 < 0:
            p1 = p1 + 2*ry_sq*x+3*ry_sq
            x = x + 1
        else:
            p1 = p1 + 2*ry_sq*x - 2*rx_sq*y+2*rx_sq+3*ry_sq
            x = x + 1
            y = y-1
        
        if flag:
            res.extend([(y+xc, x+yc), (y+xc, yc-x), (xc-y, yc+x), (xc-y, yc-x)])
        else:
            res.extend([(x+xc, y+yc), (xc-x, y+yc), (x+xc, yc-y), (xc-x, yc-y)])
        

    p2 = ry_sq*(x+0.5)*(x+0.5)+rx_sq*(y-1)*(y-1)-rx_sq*ry_sq
    while y > 0:
        # section 2
        if p2 >= 0:
            p2 = p2-2*rx_sq*y+3*rx_sq
            y = y-1
        else:
            p2 = p2+2*ry_sq*x-2*rx_sq*y+2*ry_sq+3*rx_sq
            x=x+1
            y = y-1

        if flag:
            res.extend([(y+xc, x+yc), (y+xc, yc-x), (xc-y, yc+x), (xc-y, yc-x)])
        else:
            res.extend([(x+xc, y+yc), (xc-x, y+yc), (x+xc, yc-y), (xc-x, yc-y)])

    if flag:
        res.extend([(xc, rx+yc), (xc, yc-rx)])
    else:
        res.extend([(rx+xc,yc),(xc-rx,yc)])
    
    return res
        





def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


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
    pass
