from browser import document, window, alert, timer
import javascript

import time
# from typing import Union
# from typing import Any


class vexEnum:
    '''Base class for all enumerated types'''
    value = 0
    name = ""

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def wait(ms: int):
    '''### delay the current thread for the provided number of seconds or milliseconds.

    #### Arguments:
        duration: The number of seconds or milliseconds to sleep for
        units:    The units of duration, optional, default is milliseconds

    #### Returns:
        None
    '''
    # window.performance.now()
    # javascript.Date.new().getTime()

    start = window.performance.now()
    while window.performance.now() - start < ms:
        pass


class Color:
    BLACK = "#000000"
    '''predefined Color black'''
    WHITE = "#FFFFFF"
    '''predefined Color white'''
    RED = "#FF0000"
    '''predefined Color red'''
    GREEN = "#00FF00"
    '''predefined Color green'''
    BLUE = "#0000FF"
    '''predefined Color blue'''
    YELLOW = "#FFFF00"
    '''predefined Color yellow'''
    ORANGE = "#ffa500"
    '''predefined Color orange'''
    PURPLE = "#ff00ff"
    '''predefined Color purple'''
    CYAN = "#00ffff"
    '''predefined Color cyan'''
    TRANSPARENT = "#000000"
    '''predefined Color transparent'''

    def rgb(self, *args):
        '''Convert RGB values to a hex color string'''
        if len(args) == 3:
            r, g, b = args
            return f"#{r:02x}{g:02x}{b:02x}"


# 创建模拟的Brain和Screen类
class Brain:
    def __init__(self):
        self.screen = Screen()


class Screen:
    def __init__(self):
        self.canvas = document["screenCanvas"]
        self.ctx = self.canvas.getContext("2d")
        self.ctx.lineWidth = 1
        self.ctx.strokeStyle = "#FFFFFF"
        self.ctx.fillStyle = "#000000"
        self.ctx.font = "12px Monospace"
        self.ctx.textAlign = "left"
        self.ctx.textBaseline = "bottom"

        self._row = 0
        self._col = 0
        self._originx = 0
        self._originy = 0
        self.pen_color = Color.WHITE
        self.fill_color = Color.BLACK

    def set_cursor(self, row: int, col: int):
        '''### Set the cursor position used for printing text on the screen

        row and column spacing will take into account the selected font.\\
        The base cell size if 10x20 pixels for the MONO20 font.\\
        text may not accurately print if using a proportional font.\\
        The top, left corner of the screen is position 1,1

        #### Arguments:
            row : The cursor row
            col : The cursor column

        #### Returns:
            None
        '''
        self._row = row
        self._col = col

    def column(self):
        '''Return the current column where text will be printed'''
        return self._col

    def row(self):
        '''Return the current row where text will be printed'''
        return self._row

    def set_origin(self, x: int, y: int):
        '''### Set the origin used for drawing graphics on the screen

        drawing functions consider the top left corner of the screen as the origin.\\
        This function can move the origin to an alternate position such as the center of the screen.

        #### Arguments:
            x : The origins x position relative to top left corner
            y : The origins y position relative to top left corner

        #### Returns:
            None
        '''
        self._originx = x
        self._originy = y

    def set_pen_width(self, width: int):
        '''### Set the pen width used for drawing lines, rectangles and circles

        #### Arguments:
            width : The pen width

        #### Returns:
            None
        '''
        self.ctx.lineWidth = width

    def clear_screen(self, color=Color.BLACK):

        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

    def draw_rectangle(self, x, y, width, height, fill=False):
        if fill:
            self.ctx.fillRect(x, y, width, height)
        else:
            self.ctx.strokeRect(x, y, width, height)

    def draw_circle(self, x, y, radius, fill=False):
        self.ctx.beginPath()
        self.ctx.arc(x, y, radius, 0, 2 * javascript.Math.PI)
        if fill:
            self.ctx.fill()
        else:
            self.ctx.stroke()

    def draw_line(self, x1, y1, x2, y2):
        self.ctx.beginPath()
        self.ctx.moveTo(x1, y1)
        self.ctx.lineTo(x2, y2)
        self.ctx.stroke()

    def draw_text(self, x, y, text):
        self.ctx.fillStyle = "#f72585"
        self.ctx.fillText(text, x, y)

    def draw_polygon(self, *points, fill=False):
        if len(points) == 0:
            return
        self.ctx.beginPath()
        self.ctx.moveTo(points[0][0], points[0][1])
        for point in points[1:]:
            self.ctx.lineTo(point[0], point[1])
        self.ctx.closePath()
        if fill:
            self.ctx.fill()
        else:
            self.ctx.stroke()


# 将Brain类添加到全局作用域
window.Brain = Brain
window.wait = wait
window.vexEnum = vexEnum
window.Color = Color


# 执行代码的函数


def run_code(ev):
    try:
        code = document["codeInput"].value
        # 清空画布
        Brain().screen.clear_screen()
        # 更新状态
        document["status"].text = "Executing code..."
        document["status"].className = "status info"
        # 执行代码
        # 提供必要的全局变量
        exec_globals = {
            "Brain": Brain,
            "wait": wait,
            "vexEnum": vexEnum,
            "Color": Color,
            "__name__": "__main__"
        }
        exec(code, exec_globals)
        # 成功消息
        document["status"].text = "Code executed successfully!"
        document["status"].className = "status success"
    except Exception as e:
        document["errorOutput"].text = f"Error: {str(e)}"
        document["errorOutput"].className = "status error"
# 清空画布的函数


def clear_canvas(ev):
    Brain().screen.clear_screen()
    document["status"].text = "Canvas cleared"
    document["status"].className = "status info"


# 绑定事件
document["runBtn"].bind("click", run_code)
document["resetBtn"].bind("click", clear_canvas)
