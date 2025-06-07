# rotating_cube.py
# Library imports
from vex import *
import math
import random
# Brain should be defined by default
brain = Brain()


class Cube:
    def __init__(self, x0, y0, scale, angle_x=0, angle_y=0):
        # 定义立方体的顶点坐标
        self.vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]
        # 定义立方体的边
        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),  # 底面
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),  # 顶面
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),  # 侧边
        ]
        # 定义立方体的中心坐标和缩放比例
        self.x0 = x0
        self.y0 = y0
        self.scale = scale
        # 定义旋转角度和旋转速度
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_x_speed = 0.02
        self.angle_y_speed = 0.03

    def project_3d_to_2d(self, x, y, z):
        """3D坐标投影到2D平面"""

        # 应用旋转矩阵
        rotated_y = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        rotated_z = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        rotated_x = x * math.cos(self.angle_y) + rotated_z * math.sin(self.angle_y)
        rotated_z = -x * math.sin(self.angle_y) + rotated_z * math.cos(self.angle_y)

        # 正交投影到2D平面
        return rotated_x * self.scale, rotated_y * self.scale

    def draw_cube(self):
        """绘制立方体线框"""

        # 更新旋转角度
        self.angle_x += self.angle_x_speed
        self.angle_y += self.angle_y_speed
        # 清屏
        brain.screen.set_pen_color(Color.BLACK)
        brain.screen.draw_circle(
            self.x0, self.y0, self.scale * math.sqrt(3.3), Color.BLACK
        )
        # 绘制立方体的每条边
        for edge in self.edges:
            start = self.vertices[edge[0]]
            end = self.vertices[edge[1]]
            # 转换起点坐标
            x1, y1, z1 = start
            proj_x1, proj_y1 = self.project_3d_to_2d(x1, y1, z1)

            # 转换终点坐标
            x2, y2, z2 = end
            proj_x2, proj_y2 = self.project_3d_to_2d(x2, y2, z2)

            # 绘制线段
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.draw_line(
                self.x0 + proj_x1,
                self.y0 + proj_y1,
                self.x0 + proj_x2,
                self.y0 + proj_y2,
            )


# 动画循环

# 创建两个立方体对象
cube1 = Cube(120, 120, 60, 90, 90)
cube2 = Cube(360, 120, 40)
while True:

    # 绘制并更新画面
    cube1.draw_cube()
    cube2.draw_cube()
    brain.screen.render()
    wait(20)  # 等待20ms
                        