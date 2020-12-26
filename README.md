<!--
 * @Description: 
 * @version: 
 * @Author: ybzhang
 * @Date: 2020-12-26 21:30:13
 * @LastEditors: ybzhang
 * @LastEditTime: 2020-12-26 22:25:05
-->
# 《计算机图形学》系统使用说明书

181860141 张玉波
804422812@qq.com

## 开发环境
* Ubuntu 18.04 x86_64

* Python 3.7.3

## 系统功能说明
### 命令行界面
接受两个参数，分别是`input_path`和`output_dir`。

* input_path: 写有指令的.txt文件路径。具体的文件内命令格式参考大作业实验要求。

* output_dir: 图片的输出文件夹路径

通过以下命令来运行：
>```
>python cg_cli.py input_path output_dir
>```
### 图形界面
在命令行中运行以下指令：
>```
>python cg_gui.py
>```
即可运行gui画图程序。

图形界面总览：
![](https://github.com/bobo-z/cg2020/blob/main/img/1.png)
####  图元绘制
在菜单栏绘制一栏下即可选择绘制的图元类型，对于线段、多边形、曲线还可以选择绘制图元的算法。

![](https://github.com/bobo-z/cg2020/blob/main/img/2.png)

* 绘制直线
  
    选择绘制线段算法Naive, DDA, Bresenham之一。此时窗口左下角会显示`xxx算法绘制直线`字样。

    在空白处使用鼠标左键点击，拖动鼠标，并在合适位置释放，即可画出直线。

![](https://github.com/bobo-z/cg2020/blob/main/img/3.png)

* 绘制多边形

    选择绘制多边形的算法之后即可开始绘制多边形。

    在空白处用鼠标左键点击，拖动，并在合适位置释放以画出多边形的第一条边。若要继续添加边，则点击鼠标左键，拖动并释放，程序会继续添加边；若结束绘画，则单击鼠标右键，多边形首尾自动相连。

![](https://github.com/bobo-z/cg2020/blob/main/img/4.png)

* 绘制椭圆

    点击绘制->椭圆即可开始绘制。

    单击鼠标左键并拖动，在合适位置释放。即可得到点下鼠标和松开鼠标位置下构成的矩形的内切椭圆。

![](https://github.com/bobo-z/cg2020/blob/main/img/5.img)

* 绘制曲线

    选择绘制曲线的算法。

    点击鼠标左键添加第一个控制点，拖动并在合适位置释放以添加第二个控制点。若要继续绘制，则可以按住鼠标左键拖动并释放，来添加控制点；若要结束绘制，则单击鼠标右键即可。



![](https://github.com/bobo-z/cg2020/blob/main/img/6.png)
> 由于绘制B样条曲线所需的程序开销较大，在绘制过程中以及绘制结束之后，都会造成程序的卡顿，若要测试功能建议最后再绘制B样条曲线，以免对后续测试造成不流畅的体验。

#### 图元编辑

若要编辑图元，首先须在窗口右侧点击图元编号以选中图元。

> 选中图元时会显示其边界与控制点

其次，点击菜单栏编辑选项，选择对图元进行平移、旋转（除椭圆）、缩放与裁剪（仅线段）。

* 平移
  
  选中图元之后，在屏幕上点击，然后拖动并释放。点击与释放鼠标的位置构成的直线，即为图元所要平移的方向以及距离。

* 旋转
  
  在画布内用鼠标左键单击以选择旋转中心，不要释放鼠标（可以移动），并用鼠标滚轮来对图元进行旋转。向前滚逆时针旋转、向后顺时针旋转。释放鼠标左键，则旋转结束。
  
> 若选中的图元为椭圆，则无法进行旋转

* 缩放
  
  在画布内用鼠标左键单击以选择缩放中心，不要释放鼠标（可以移动），并用鼠标滚轮来对图元进行缩放。向前滚放大、向后滚缩小。释放鼠标左键，则旋转结束。

* 裁剪

  点击、拖动鼠标左键即可得到一个蓝色的裁剪窗口，在合适的位置释放，将会对裁剪窗口内选中图元进行裁剪。

> 裁剪操作仅支持线段

#### 文件操作

* 设置画笔

点击菜单栏`文件->设置画笔`即会弹出此对话框。选择颜色并点击`OK`则会将画笔设置为对应颜色

![](https://github.com/bobo-z/cg2020/blob/main/img/7.png)

* 重置画布

点击菜单栏`文件->重置画布`即会弹出此对话框。可以点击箭头或直接输入来设置画布的长、宽。

点击画布颜色会弹出选择颜色对话框。

点击确定，则会按照设置的长、宽、颜色重置画布。

![](https://github.com/bobo-z/cg2020/blob/main/img/8.png)

* 保存画布

点击菜单栏`文件->保存画布`即会弹出此窗口，可以选择文件的保存路径与文件名。点击确定即可完成画布的保存

![](https://github.com/bobo-z/cg2020/blob/main/img/9.png)
