#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QWheelEvent
from PyQt5.QtCore import QRectF
import numpy as np


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.is_polygon_drawing = False
        self.is_curve_drawing = False
        self.init_x = 0
        self.init_y = 0
        self.p_l = []

    def status_change(self):
        if self.is_polygon_drawing or self.is_curve_drawing:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            self.is_polygon_drawing = False
            self.is_curve_drawing = False

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.status_change()
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.status_change()
        self.temp_id = item_id
    
    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.status_change()
        self.temp_id = item_id
    
    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.status_change()
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_translate(self):
        self.status = 'translate'
        self.status_change()
        self.temp_item =  self.item_dict[self.selected_id]
        self.p_l = self.temp_item.p_list

    def start_rotate(self):
        self.status = 'rotate'
        self.status_change()
        self.temp_item = self.item_dict[self.selected_id]

    def start_scale(self):
        self.status = 'scale'
        self.status_change()
        self.temp_item = self.item_dict[self.selected_id]

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [
                                    [x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)

        elif self.status == 'polygon':
            if not self.is_polygon_drawing:
                self.temp_item = MyItem(self.temp_id, self.status, [
                                        [x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.is_polygon_drawing = True
            else:
                self.temp_item.p_list.append([x,y])
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [
                                    [x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        
        elif self.status == 'curve':
            if not self.is_curve_drawing:
                self.temp_item = MyItem(self.temp_id, self.status, [
                                        [x, y], [x, y]], self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.is_curve_drawing = True
            else:
                self.temp_item.p_list.append([x,y])
        elif self.status == 'translate':
            self.init_x, self.init_y = x, y
        elif self.status == 'rotate':
            self.init_x, self.init_y = x ,y
        elif self.status == 'scale':
            self.init_x, self.init_y = x ,y
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]
            #print(self.temp_item.p_list)
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'translate':
            self.temp_item.p_list = alg.translate(self.p_l, x-self.init_x, y-self.init_y)
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon':
            pass
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'curve':
            pass
        elif self.status == 'translate':
            self.item_dict[self.selected_id] = self.temp_item
        elif self.status == 'rotate':
            self.item_dict[self.selected_id] = self.temp_item
        elif self.status == 'scale':
            self.item_dict[self.selected_id] = self.temp_item
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        angle = event.angleDelta()
        angle /= 60

        if self.status == 'rotate':
            self.temp_item.p_list = alg.rotate(self.temp_item.p_list, self.init_x, self.init_y, angle.y())
        elif self.status == 'scale':
            s = 1+0.1*angle.y()/2
            self.temp_item.p_list = alg.scale(self.temp_item.p_list, self.init_x, self.init_y, s)
        self.updateScene([self.sceneRect()])




class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 255, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            p_l = np.array(self.p_list)
            min_x = min(p_l[:, 0])
            min_y = min(p_l[:, 1])
            max_x = max(p_l[:, 0])
            max_y = max(p_l[:, 1])
            w = max_x - min_x
            h = max_y - min_y
            return QRectF(min_x - 1, min_y - 1, w + 2, h + 2)

        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            p_l = np.array(self.p_list)
            min_x = min(p_l[:, 0])
            min_y = min(p_l[:, 1])
            max_x = max(p_l[:, 0])
            max_y = max(p_l[:, 1])
            w = max_x - min_x
            h = max_y - min_y
            return QRectF(min_x - 1, min_y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 1

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        # set_pen_act.triggered.connect = self.(set_pen_action)
        # reset_canvas_act.triggered.connect = self.(reset_canvas_action)
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        self.list_widget.currentTextChanged.connect(
            self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_bresenham_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def ellipse_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('绘制Bezier曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.item_cnt -= 1
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('绘制B-spline曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        if self.canvas_widget.selected_id:
            self.canvas_widget.start_translate()
            self.statusBar().showMessage('平移图元')

    def rotate_action(self):
        if self.canvas_widget.selected_id:
            item_type = self.canvas_widget.item_dict[self.canvas_widget.selected_id].item_type
            if item_type != 'ellipse':
                self.canvas_widget.start_rotate()
                self.statusBar().showMessage('旋转图元')
    
    def scale_action(self):
        if self.canvas_widget.selected_id:
            self.canvas_widget.start_scale()
            self.statusBar().showMessage('缩放图元')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
