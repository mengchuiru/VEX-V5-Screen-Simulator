# vex_api.py
from browser import document, window, aio, timer
import javascript
import sys
import math


class vexEnum:
    '''Base class for all enumerated types'''
    __slots__ = ('value', 'name')  # 优化内存使用

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}>"


class Color:
    # 预定义颜色常量
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    ORANGE = "#ffa500"
    PURPLE = "#ff00ff"
    CYAN = "#00ffff"
    TRANSPARENT = "#00000000"  # 添加透明度

    __slots__ = ('value')  # 优化内存使用

    def __init__(self, *args):
        if len(args) == 1:
            self.value = self._parse_single_arg(args[0])
        elif len(args) == 3:
            self.value = self.rgb(*args)
        else:
            raise ValueError("Invalid arguments for Color")

    def _parse_single_arg(self, arg):
        if isinstance(arg, str) and arg.startswith("#"):
            if len(arg) == 7:  # #RRGGBB
                return arg
            elif len(arg) == 9:  # #RRGGBBAA
                return arg
            elif len(arg) == 4:  # #RGB
                return f"#{arg[1]}{arg[1]}{arg[2]}{arg[2]}{arg[3]}{arg[3]}"
        elif isinstance(arg, int):
            return f"#{arg:06x}"
        return self.BLACK

    @staticmethod
    def rgb(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def rgba(r, g, b, a=255):
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"

    @staticmethod
    def hsv(hue, saturation, value):
        '''Convert HSV to RGB (hue: 0-360, sat: 0-1, val: 0-1)'''
        if not (0 <= hue <= 360 and 0 <= saturation <= 1 and 0 <= value <= 1):
            return Color.BLACK

        c = value * saturation
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = value - c

        if hue < 60:
            r, g, b = c, x, 0
        elif hue < 120:
            r, g, b = x, c, 0
        elif hue < 180:
            r, g, b = 0, c, x
        elif hue < 240:
            r, g, b = 0, x, c
        elif hue < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return Color.rgb(
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )

    def web(self, value):
        return value if value.startswith("#") else self.BLACK


class FontType:
    # 字体常量
    MONO20 = "20px Monospace"
    MONO30 = "30px Monospace"
    MONO40 = "40px Monospace"
    MONO60 = "60px Monospace"
    PROP20 = "20px prop"
    PROP30 = "30px prop"
    PROP40 = "40px prop"
    PROP60 = "60px prop"
    MONO15 = "15px prop"
    MONO12 = "12px prop"
    CJK16 = "16px cjk"


class Brain:
    '''模拟VEX V5大脑'''
    __slots__ = ('screen', 'timer')  # 优化内存使用

    def __init__(self):
        self.screen = self.Lcd()
        self.timer = self.Timer()

    class Timer:
        __slots__ = ('start_time',)  # 优化内存使用

        def __init__(self):
            self.reset()

        def reset(self):
            self.start_time = javascript.Date.now()

        def time(self):
            return javascript.Date.now() - self.start_time

    class Lcd:
        '''模拟VEX V5屏幕'''
        __slots__ = (
            '_row', '_col', '_originx', '_originy', 'pen_color', 'fill_color',
            'font_size', '_last_x', '_last_y', '_pressing', 'canvas', 'ctx'
        )  # 优化内存使用

        def __init__(self):
            self._row = 1
            self._col = 1
            self._originx = 0
            self._originy = 0
            self.pen_color = Color.WHITE
            self.fill_color = Color.BLACK
            self.font_size = 20

            # 触摸状态
            self._last_x = 0
            self._last_y = 0
            self._pressing = False

            # 获取Canvas上下文
            self.canvas = document["screenCanvas"]
            self.ctx = self.canvas.getContext("2d")
            self.ctx.lineWidth = 1
            self.ctx.strokeStyle = self.pen_color
            self.ctx.fillStyle = self.fill_color
            self.ctx.font = FontType.MONO20
            self.ctx.textAlign = "left"
            self.ctx.textBaseline = "bottom"

            # 绑定触摸事件
            self._bind_touch_events()

        def _bind_touch_events(self):
            '''绑定所有触摸/鼠标事件'''
            events = {
                "mousedown": self._handle_touch_start,
                "touchstart": self._handle_touch_start,
                "mouseup": self._handle_touch_end,
                "touchend": self._handle_touch_end,
                "mousemove": self._handle_touch_move,
                "touchmove": self._handle_touch_move
            }

            for event_type, handler in events.items():
                self.canvas.bind(event_type, handler)

            document.bind("mouseup", self._handle_global_end)

        def _handle_touch_start(self, event):
            event.stopPropagation()
            event.preventDefault()
            self._pressing = True
            self._update_touch_position(event)

        def _handle_touch_end(self, event):
            event.stopPropagation()
            event.preventDefault()
            self._pressing = False

        def _handle_touch_move(self, event):
            if self._pressing:
                event.stopPropagation()
                event.preventDefault()
                self._update_touch_position(event)

        def _handle_global_end(self, event):
            self._pressing = False

        def _update_touch_position(self, event):
            '''更新触摸位置'''
            if hasattr(event, 'touches') and event.touches.length > 0:
                clientX = event.touches[0].clientX
                clientY = event.touches[0].clientY
            else:
                clientX = event.clientX
                clientY = event.clientY

            rect = self.canvas.getBoundingClientRect()
            scale_x = self.canvas.width / rect.width
            scale_y = self.canvas.height / rect.height

            self._last_x = int((clientX - rect.left) * scale_x)
            self._last_y = int((clientY - rect.top) * scale_y)

        def set_cursor(self, row, col):
            self._row = row
            self._col = col

        def column(self):
            return self._col

        def row(self):
            return self._row

        def set_origin(self, x, y):
            self._originx = x
            self._originy = y

        def set_font(self, fontname):
            self.font_size = int(fontname.split("px")[0])
            self.ctx.font = fontname

        def set_pen_width(self, width):
            self.ctx.lineWidth = width

        def set_fill_color(self, color):
            self.fill_color = color.value if isinstance(
                color, Color) else color
            self.ctx.fillStyle = self.fill_color

        def set_pen_color(self, color):
            self.pen_color = color.value if isinstance(color, Color) else color
            self.ctx.strokeStyle = self.pen_color

        def clear_screen(self, color=Color.BLACK):
            self.ctx.fillStyle = color.value if isinstance(
                color, Color) else color
            self.ctx.fillRect(0, 0, self.canvas.width, self.canvas.height)
            self.ctx.fillStyle = self.fill_color

        def clear_line(self, number=None, color=Color.BLACK):
            # 情况当前行，如果指定行号则清除该行，否则清除当前行
            if number is not None:
                # 简化实现
                self.ctx.fillStyle = color.value if isinstance(
                    color, Color) else color
                self.ctx.fillRect(0, (number - 1) * self.font_size,
                                  self.canvas.width, self.font_size)
            else:
                # 清除当前行
                self.ctx.fillStyle = color.value if isinstance(
                    color, Color) else color
                self.ctx.fillRect(0, (self._row - 1) * self.font_size,
                                  self.canvas.width, self.font_size)

        def clear_row(self, number=None, color=Color.BLACK):
            # 简化实现
            pass

        def new_line(self):
            # 简化实现
            pass

        def next_row(self):
            # 简化实现
            pass

        def draw_pixel(self, x, y):
            self.ctx.fillStyle = self.pen_color
            self.ctx.fillRect(x, y, 1, 1)

        def draw_line(self, x1, y1, x2, y2):
            self.ctx.beginPath()
            self.ctx.moveTo(x1, y1)
            self.ctx.lineTo(x2, y2)
            self.ctx.stroke()

        def draw_rectangle(self, x, y, width, height, color=None):
            fill_color = color if color else self.fill_color
            self.ctx.fillStyle = fill_color.value if isinstance(
                fill_color, Color) else fill_color
            self.ctx.fillRect(x, y, width, height)
            self.ctx.strokeRect(x, y, width, height)
            self.ctx.fillStyle = self.fill_color

        def draw_circle(self, x, y, radius, color=None):
            fill_color = color if color else self.fill_color
            self.ctx.beginPath()
            self.ctx.arc(x, y, radius, 0, 2 * javascript.Math.PI)
            self.ctx.fillStyle = fill_color.value if isinstance(
                fill_color, Color) else fill_color
            self.ctx.fill()
            self.ctx.stroke()
            self.ctx.fillStyle = self.fill_color

        def get_string_width(self, text):
            return self.ctx.measureText(text).width

        def get_string_height(self):
            return self.font_size

        def print(self, *args, **kwargs):
            text = " ".join(str(arg) for arg in args)
            x = self._originx + (self._col - 1) * self.font_size // 2
            y = self._originy + self._row * self.font_size
            self._col += len(text)
            self.print_at(text, x, y)

        def print_at(self, text, x, y):
            self.ctx.fillStyle = self.pen_color
            self.ctx.fillText(text, x, y)

        def x_position(self):
            return self._last_x

        def y_position(self):
            return self._last_y

        def pressing(self):
            return self._pressing

        def render(self):
            return True


class OutputRedirector:
    '''重定向标准输出到HTML元素'''
    __slots__ = ('output_element', 'buffer')  # 优化内存使用

    def __init__(self, output_element):
        self.output_element = output_element
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        if '\n' in text:
            self.flush()

    def flush(self):
        if self.buffer:
            # 创建新的输出行
            line = document.createElement("div")
            line.className = "output-line"
            line.textContent = self.buffer.rstrip()
            self.output_element.appendChild(line)
            # 自动滚动到底部
            self.output_element.scrollTop = self.output_element.scrollHeight
            self.buffer = ""


# 全局控制变量
stop_flag = {'value': False, "current_task": None}  # 使用字典模拟可变对象


async def wait(ms):
    '''模拟VEX wait函数'''
    start_time = javascript.Date.now()
    while (javascript.Date.now() - start_time) < ms:
        if stop_flag['value']:
            raise SystemExit("Program stopped by user")
        await aio.sleep(0.01)


def run_code(ev):
    '''运行用户代码'''
    # 停止之前的执行
    stop_flag['value'] = True
        # 在JavaScript中重置计时器
    # window.resetTimer = window.resetTimer or None
    # if window.resetTimer:
    #     window.resetTimer()


    async def execute_code():
        try:
            # await aio.sleep(0.1)
            # 初始化大脑和输出
            brain = Brain()
            brain.screen.clear_screen()
            output_div = document["output"]
            output_div.innerHTML = ""

            # 重定向标准输出
            sys.stdout = OutputRedirector(output_div)
            sys.stderr = OutputRedirector(output_div)

            # 获取并预处理代码
            code = document.querySelector(".CodeMirror").CodeMirror.getValue()
            code = code.replace("from vex import *", "")
            code = code.replace("wait(", "await wait(")
            code = code.replace("global", "nonlocal")

            # 创建执行环境
            exec_globals = {
                "Brain": Brain,
                "wait": wait,
                "brain": brain,
                "Color": Color,
                "FontType": FontType,
                "vexEnum": vexEnum,
                "aio": aio,
                "__name__": "__main__",
                "stop_flag": stop_flag,
                "__builtins__": __import__('builtins')
            }

            # 检测异步代码
            if 'await' in code:
                # 包装异步代码
                wrapped_code = (
                    "async def __user_async_code():\n"
                    f"{_indent_code(code)}\n"
                    "aio.run(__user_async_code())"
                )
                exec(wrapped_code, exec_globals)
            else:
                # 执行同步代码
                exec(code, exec_globals)

            document["status"].text = "Code Running..."
        except SystemExit:
            document["status"].text = "Code Stopped!"
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            sys.stderr.flush()

    stop_flag['value'] = False

    # 使用aio.run执行异步函数
    aio.run(execute_code())


def _indent_code(code, indent=8):
    '''为代码添加缩进'''
    return "\n".join(" " * indent + line for line in code.splitlines())


def clear_canvas(ev):
    '''停止执行并清空画布'''
    stop_flag['value'] = True
    try:
        brain = Brain()
        brain.screen.clear_screen()
    except Exception:
        pass
    document["output"].innerHTML = ""
    document["status"].text = "Code Stopped!"


# 初始化全局对象和事件绑定
window.Brain = Brain
window.wait = wait
window.vexEnum = vexEnum
window.Color = Color
window.FontType = FontType

document["runBtn"].bind("click", run_code, True)
# document["runBtn"].bind("click", clear_canvas)  # 清空画布
document["resetBtn"].bind("click", clear_canvas)
