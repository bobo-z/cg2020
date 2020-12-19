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
    QStyleOptionGraphicsItem,
    QColorDialog,
    QDialog,
    QPushButton,
    QSpinBox,
    QFormLayout,
    QLabel,
    QFileDialog,
)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QWheelEvent
from PyQt5.QtCore import QRectF, Qt, QPoint
import numpy as np


# https://mp.weixin.qq.com/s/Wy1iTYoX7_O81ChMflXXfg

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
        self.is_line_drawing = False
        self.is_ellipse_drawing = False
        self.init_x = 0
        self.init_y = 0
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.p_l = []
        self.color = QColor(0, 0, 0)
        self._item = None

    def status_change(self):
        if self.is_polygon_drawing:
            self.temp_item.p_list.append(self.temp_item.p_list[0])
            self.updateScene([self.sceneRect()])
        if self.is_polygon_drawing or self.is_curve_drawing:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            self.is_polygon_drawing = False
            self.is_curve_drawing = False
            self.is_rotate = False
            self.is_scale = False

    def start_set_pen(self, color):
        self.status = ''
        self.color = color

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self):
        self.status = 'translate'
        self.temp_item = self.item_dict[self.selected_id]
        self.p_l = self.temp_item.p_list

    def start_rotate(self):
        self.status = 'rotate'
        self.temp_item = self.item_dict[self.selected_id]

    def start_scale(self):
        self.status = 'scale'
        self.temp_item = self.item_dict[self.selected_id]

    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_algorithm = algorithm
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
        if event.button() == Qt.RightButton:
            self.status_change()
        elif event.button() == Qt.LeftButton:
            if self.status == 'line':
                self.temp_item = MyItem(self.temp_id, self.status, [
                                        [x, y], [x, y]], self.temp_algorithm, self.color)
                self.scene().addItem(self.temp_item)
                self.is_line_drawing = True
            elif self.status == 'polygon':
                if not self.is_polygon_drawing:
                    self.temp_item = MyItem(self.temp_id, self.status, [
                                            [x, y], [x, y]], self.temp_algorithm, self.color)
                    self.scene().addItem(self.temp_item)
                    self.is_polygon_drawing = True
                else:
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'ellipse':
                self.temp_item = MyItem(self.temp_id, self.status, [
                                        [x, y], [x, y]], self.temp_algorithm, self.color)
                self.scene().addItem(self.temp_item)
                self.is_ellipse_drawing = True
            elif self.status == 'curve':
                if not self.is_curve_drawing:
                    self.temp_item = MyItem(self.temp_id, self.status, [
                                            [x, y], [x, y]], self.temp_algorithm, self.color)
                    self.scene().addItem(self.temp_item)
                    self.is_curve_drawing = True
                else:
                    self.temp_item.p_list.append([x, y])
            elif self.status == 'translate':
                self.init_x, self.init_y = x, y
            elif self.status == 'rotate':
                self.is_rotate = True
                self.init_x, self.init_y = x, y
                self._item = MyItem('dot', self.status, [
                    [x, y]], '', QColor(0, 0, 0))
                self.scene().addItem(self._item)
            elif self.status == 'scale':
                self.is_sca1e = True
                self.init_x, self.init_y = x, y
                self._item = MyItem('dot', self.status, [
                    [x, y]], '', QColor(0, 0, 0))
                self.scene().addItem(self._item)
            elif self.status == 'clip':
                self.init_x, self.init_y = x, y
                self._item = MyItem('clip_rect', self.status, [
                    [x, y], [x, y]], '', QColor(0, 0, 0))
                self.scene().addItem(self._item)

            elif self.status == 'modify':  # TODO
                pass
        else:
            pass
        self.updateScene([self.sceneRect()])

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' and self.is_line_drawing:
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon' and self.is_polygon_drawing:
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse' and self.is_ellipse_drawing:
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve' and self.is_curve_drawing:
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'translate':
            self.temp_item.p_list = alg.translate(
                self.p_l, x - self.init_x, y - self.init_y)
        elif self.status == 'clip':
            self._item.p_list[1] = [x, y]
            if self.init_x < x:
                self.x_min, self.x_max = self.init_x, x
            else:
                self.x_min, self.x_max = x, self.init_x
            if self.init_y < y:
                self.y_min, self.y_max = self.init_y, y
            else:
                self.y_min, self.y_max = y, self.init_y

        elif self.status == 'modify':  # TODO
            pass

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton:
            return
        if self.status == 'line' and self.is_line_drawing:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.is_line_drawing = False
            self.finish_draw()
        elif self.status == 'polygon':
            pass
        elif self.status == 'ellipse' and self.is_ellipse_drawing:
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.is_ellipse_drawing = False
            self.finish_draw()
        elif self.status == 'curve':
            pass
        elif self.status == 'translate':
            self.item_dict[self.selected_id] = self.temp_item
        elif self.status == 'rotate':
            self.is_rotate = False
            self.item_dict[self.selected_id] = self.temp_item
            self.scene().removeItem(self._item)
        elif self.status == 'scale':
            self.is_sca1e = False
            self.item_dict[self.selected_id] = self.temp_item
            self.scene().removeItem(self._item)
        elif self.status == 'clip':
            print(self.temp_item.p_list)
            print(self.x_min, self.y_min, self.x_max, self.y_max)
            p_l = self.temp_item.p_list
            self.temp_item.p_list = alg.clip(
                p_l,
                self.x_min,
                self.y_min,
                self.x_max,
                self.y_max,
                self.temp_algorithm)

            self.scene().removeItem(self._item)
        elif self.status == 'modify':  # TODO
            pass
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        angle = event.angleDelta()
        angle /= 60

        if self.status == 'rotate' and self.is_rotate:
            self.temp_item.p_list = alg.rotate(
                self.temp_item.p_list, self.init_x, self.init_y, angle.y())
        elif self.status == 'scale' and self.is_sca1e:
            s = 1 + 0.1 * angle.y() / 2
            self.temp_item.p_list = alg.scale(
                self.temp_item.p_list, self.init_x, self.init_y, s)
        self.updateScene([self.sceneRect()])


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(
            self,
            item_id: str,
            item_type: str,
            p_list: list,
            algorithm: str = '',
            color: QColor = QColor(
                0,
                0,
                0),
            parent: QGraphicsItem = None):
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
        self.color = color

    def drawPoint(self, painter: QPainter, x):
        painter.setPen(QColor(0, 0, 0))
        point_range = 2
        i = 1
        for i in range(point_range + 1):
            painter.drawPoint(x[0] - i, x[1])
            painter.drawPoint(x[0] + i, x[1])
            painter.drawPoint(x[0], x[1] - i)
            painter.drawPoint(x[0], x[1] + i)
            painter.drawPoint(x[0] - i, x[1] - i)
            painter.drawPoint(x[0] + i, x[1] + i)
            painter.drawPoint(x[0] + i, x[1] - 1)
            painter.drawPoint(x[0] - i, x[1] + 1)
        painter.drawPoint(*x)

    def paint(
            self,
            painter: QPainter,
            option: QStyleOptionGraphicsItem,
            widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.color)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon_gui(self.p_list, self.algorithm)
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
        elif self.item_type == 'clip':
            painter.setPen(QColor(0, 0, 255))
            painter.drawRect(self.boundingRect())
            item_pixels = []
        elif self.item_type == 'rotate':
            self.drawPoint(painter, self.p_list[0])
            item_pixels = []
        elif self.item_type == 'scale':
            self.drawPoint(painter, self.p_list[0])
            item_pixels = []

        for p in item_pixels:
            painter.drawPoint(*p)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(self.boundingRect())
            for x in self.p_list:
                self.drawPoint(painter, x)

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            if len(self.p_list) != 2:
                return QRectF()
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
        elif self.item_type == 'clip':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'rotate':
            return QRectF()
        elif self.item_type == 'scale':
            return QRectF()


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
        self.scene_color = QColor(255, 255, 255)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(605, 605)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
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
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
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
        clip_cohen_sutherland_act.triggered.connect(
            self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
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

    def set_pen_action(self):
        self.statusBar().showMessage('设置画笔')
        color = QColorDialog.getColor()
        self.canvas_widget.start_set_pen(color)

    def set_scene_color(self):
        self.scene_color = QColorDialog.getColor()

    def reset_canvas_action(self):
        self.statusBar().showMessage('重置画布')
        dialog = QDialog()
        dialog.setWindowTitle('重置画布信息')
        dialog.setWindowModality(Qt.WindowModal)
        dialog.resize(300, 300)

        btn1 = QPushButton(dialog)
        btn1.setText('确定')
        btn1.move(175, 250)
        btn1.clicked.connect(lambda: dialog.accept())

        btn2 = QPushButton(dialog)
        btn2.setText('取消')
        btn2.move(50, 250)
        btn2.clicked.connect(lambda: dialog.reject())

        width_box = QSpinBox()
        width_box.setRange(100, 1100)
        width_box.setValue(600)

        height_box = QSpinBox()
        height_box.setRange(100, 1100)
        height_box.setValue(600)

        color_btn = QPushButton('画布颜色', dialog)
        color_btn.clicked.connect(self.set_scene_color)

        formlayout = QFormLayout(dialog)
        formlayout.addRow(QLabel('宽'), width_box)
        formlayout.addRow(QLabel('高'), height_box)
        formlayout.addRow(color_btn)

        res = dialog.exec()
        if res == 1:
            width = width_box.value()
            height = height_box.value()
            self.canvas_widget.resize(width + 5, height + 5)
            # both scene and canvas should be changed
            self.scene.setSceneRect(0, 0, width, height)
            self.scene.setBackgroundBrush(self.scene_color)
            self.canvas_widget.setFixedSize(width, height)
            self.list_widget.clearSelection()
            self.canvas_widget.clear_selection()
            self.scene.clear()
            self.list_widget.clear()
            self.item_cnt = 1

    def save_canvas_action(self):
        self.statusBar().showMessage('保存画布')
        filename = QFileDialog.getSaveFileName(
            self, '保存画布', './', 'Images (*.png *.bmp *.jpg)')
        if filename[0]:
            pix = self.canvas_widget.grab(
                self.canvas_widget.sceneRect().toRect())
            pix.save(filename[0])

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

    def clip_cohen_sutherland_action(self):
        if self.canvas_widget.selected_id:
            item_type = self.canvas_widget.item_dict[self.canvas_widget.selected_id].item_type
            if item_type == 'line':
                self.canvas_widget.start_clip('Cohen-Sutherland')
                self.statusBar().showMessage('Cohen_Sutherland算法裁剪图元')

    def clip_liang_barsky_action(self):
        if self.canvas_widget.selected_id:
            item_type = self.canvas_widget.item_dict[self.canvas_widget.selected_id].item_type
            if item_type == 'line':
                self.canvas_widget.start_clip('Liang-Barsky')
                self.statusBar().showMessage('Liang-Barsky算法裁剪图元')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
