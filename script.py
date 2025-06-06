from browser import document, window, alert, timer, aio, console
import javascript
import sys
import math

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
        if len(args) == 1:
            col = args[0]
            if isinstance(col, str) and col.startswith("#") and len(col) == 7:
                return col
            elif isinstance(col, int):
                return f"#{col:06x}"
        if len(args) == 3:
            r, g, b = args
            return f"#{r:02x}{g:02x}{b:02x}"
    def hsv(self, hue: float, saturation: float, value: float):
        '''Convert HSV values to a hex color string'''
        if 0 <= hue <= 360 and 0 <= saturation <= 1 and 0 <= value <= 1:
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
            return f"#{int((r + m) * 255):02x}{int((g + m) * 255):02x}{int((b + m) * 255):02x}"
    def web(self, value: str):
        '''Convert a web color string to a hex color string'''
        if value.startswith("#") and len(value) == 7:
            return value

class FontType:
    '''A unit representing font type and size'''
    MONO20 = "20px Monospace"
    '''monotype font of size 20'''
    MONO30 = "30px Monospace"
    '''monotype font of size 30'''
    MONO40 = "40px Monospace"
    '''monotype font of size 40'''
    MONO60 = "60px Monospace"
    '''monotype font of size 60'''
    PROP20 = "20px prop"
    '''proportional font of size 20'''
    PROP30 = "30px prop, sans-serif"
    '''proportional font of size 30'''
    PROP40 = "40px prop, sans-serif"
    '''proportional font of size 40'''
    PROP60 = "60px prop, sans-serif"
    '''proportional font of size 60'''
    MONO15 = "15px prop, sans-serif"
    '''proportional font of size 15'''
    MONO12 = "12px prop, sans-serif"
    '''proportional font of size 12'''
    CJK16 = "16px cjk, sans-serif"
    '''Chinese/Japanese/Korean font of size 16'''

# 创建模拟的Brain和Screen类


class Brain:

    def __init__(self):
        self.screen = Brain.Lcd()
        self.timer = Brain.Timer()

    class Timer:
        def __init__(self):
            self.start_time = javascript.Date.now()
        def reset(self):
            self.start_time = javascript.Date.now()
        def time(self):
            return javascript.Date.now() - self.start_time

    class Lcd:
        def __init__(self):
            self._row = 1
            self._col = 1
            self._originx = 0
            self._originy = 0
            self.pen_color = Color.WHITE
            self.fill_color = Color.BLACK
            self.font_size = 20
            # 添加触摸状态和位置跟踪
            self._last_x = 0
            self._last_y = 0
            self._pressing = False

            self.canvas = document["screenCanvas"]
            self.ctx = self.canvas.getContext("2d")
            self.ctx.lineWidth = 1
            self.ctx.strokeStyle = self.pen_color
            self.ctx.fillStyle = self.fill_color
            self.ctx.font = FontType.MONO20
            self.ctx.textAlign = "left"
            self.ctx.textBaseline = "bottom"
            # 绑定触摸事件
            self.canvas.bind("mousedown", self.handle_touch_start)
            self.canvas.bind("touchstart", self.handle_touch_start)
            self.canvas.bind("mouseup", self.handle_touch_end)
            self.canvas.bind("touchend", self.handle_touch_end)
            self.canvas.bind("mousemove", self.handle_touch_move)
            self.canvas.bind("touchmove", self.handle_touch_move)
            document.bind("mouseup", self.handle_global_end)  # 处理在画布外释放

    # 新增事件处理方法
        def handle_touch_start(self, event):
            event.stopPropagation()
            event.preventDefault()
            self._pressing = True
            self.update_touch_position(event)

        def handle_touch_end(self, event):
            event.stopPropagation()
            event.preventDefault()
            self._pressing = False

        def handle_touch_move(self, event):
            if self._pressing:
                event.stopPropagation()
                event.preventDefault()
                self.update_touch_position(event)

        def handle_global_end(self, event):
            self._pressing = False

        def update_touch_position(self, event):
            # 获取触摸/鼠标位置
            if hasattr(event, 'touches') and len(event.touches) > 0:
                touch = event.touches[0]
                clientX = touch.clientX
                clientY = touch.clientY
            else:
                clientX = event.clientX
                clientY = event.clientY

            # 计算画布相对位置
            rect = self.canvas.getBoundingClientRect()
            scale_x = self.canvas.width / rect.width
            scale_y = self.canvas.height / rect.height

            self._last_x = int((clientX - rect.left) * scale_x)
            self._last_y = int((clientY - rect.top) * scale_y)

        def set_cursor(self, row: int, col: int):
            self._row = row
            self._col = col

        def column(self):
            return self._col

        def row(self):
            return self._row

        def set_origin(self, x: int, y: int):
            self._originx = x
            self._originy = y

        def set_font(self, fontname: FontType):
            self.font_size = int(str(fontname)[0:2])
            self.ctx.font = fontname

        def set_pen_width(self, width: int):
            self.ctx.lineWidth = width

        def set_fill_color(self, color: Color):
            '''Set the fill color for shapes'''
            self.fill_color = color
            self.ctx.fillStyle = color

        def set_pen_color(self, color):
            '''Set the pen color for drawing'''
            self.pen_color = color
            self.ctx.strokeStyle = color

        def clear_screen(self, color=Color.BLACK):
            self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)

        def clear_line(self, number=None, color=Color.BLACK):
            pass

        def clear_row(self, number=None, color=Color.BLACK):
            pass

        def new_line(self):
            pass

        def next_row(self):
            pass

        def draw_pixel(self, x, y):
            '''Draw a pixel at the specified coordinates'''
            self.ctx.fillStyle = self.pen_color
            self.ctx.fillRect(x, y, 1, 1)

        def draw_line(self, x1, y1, x2, y2):
            '''Draw a line from (x1, y1) to (x2, y2)'''
            self.ctx.strokeStyle = self.pen_color
            self.ctx.beginPath()
            self.ctx.moveTo(x1, y1)
            self.ctx.lineTo(x2, y2)
            self.ctx.stroke()

        def draw_rectangle(self, x, y, width, height, color=None):
            '''Draw a rectangle at (x, y) with specified width and height'''
            self.ctx.strokeStyle = self.pen_color
            self.ctx.fillStyle = color if color else self.fill_color
            self.ctx.fillRect(x, y, width, height)
            self.ctx.strokeRect(x, y, width, height)
            self.ctx.fillStyle = self.fill_color

        def draw_circle(self, x, y, radius,color=None):
            self.ctx.beginPath()
            self.ctx.arc(x, y, radius, 0, 2 * javascript.Math.PI)
            self.ctx.fillStyle = color if color else self.fill_color
            self.ctx.strokeStyle = self.pen_color
            self.ctx.fill()
            self.ctx.stroke()

        def get_string_width(self, *args):
            return 0

        def get_string_height(self, *args):
            return 0

        def print(self, *args, **kwargs):
            text = " ".join(str(arg) for arg in args)
            x = self._originx + (self._col-1) * self.font_size//2
            y = self._originy + self._row * self.font_size
            self._col += len(text)

            self.print_at(text, x, y)

        def print_at(self,text, x, y):
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



# 重定向print输出


class OutputRedirector:
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


# 在全局作用域中定义
stop_flag = {'value': False}


async def wait(ms):
    """等待指定的毫秒数，这是一个异步操作"""
    start_time = javascript.Date.now()
    while (javascript.Date.now() - start_time) < ms:
        if stop_flag['value']:
            raise SystemExit("程序被用户中断")
        await aio.sleep(0.01)  # 检查间隔


# 执行代码的函数
def run_code(ev):
    stop_flag['value'] = False  # 重置停止标志

    async def execute_code():
        try:
            # 清空画布和输出
            brain = Brain()
            brain.screen.clear_screen()

            # 清空输出区域
            output_div = document["output"]
            output_div.innerHTML = ""

            # 设置输出重定向
            sys.stdout = OutputRedirector(output_div)
            sys.stderr = OutputRedirector(output_div)

            # 获取代码
            # code = document["codeInput"].textContent
            code = document["codeInput"].value
            code = code.replace("from vex import *", "")
            code = code.replace("wait(", "await wait(") # 替换wait调用以检查停止标志
            code = code.replace("global", "nonlocal")

            # 准备全局变量
            exec_globals = {
                "FontType": FontType,
                "Color": Color,
                "vexEnum": vexEnum,
                "Brain": Brain,
                "wait": wait,
                "__name__": "__main__",
                "brain": brain,
                "aio": aio,
                "stop_flag": stop_flag,
                "__builtins__": __import__('builtins')
            }

            # 执行用户代码
            document["status"].text = "执行代码中..."

            # 检查用户代码是否包含await
            has_await = 'await' in code

            if has_await:
                # 为包含await的代码创建异步包装器
                wrapped_code = """
async def __user_async_code():
    
    """ + "\n    ".join(code.splitlines()) + """

aio.run(__user_async_code())
"""
                # 编译并执行包装后的代码
                compiled_code = compile(wrapped_code, "<string>", "exec")
                exec(compiled_code, exec_globals)
            else:
                # 普通代码直接执行
                compiled_code = compile(code, "<string>", "exec")
                exec(compiled_code, exec_globals)

            document["status"].text = "代码执行成功!"
        except SystemExit as e:
            document["status"].text = "程序已停止"
        except Exception as e:
            document["status"].text = f"错误: {str(e)}"
            # 将错误信息输出到控制台
            sys.stderr.write(f"错误: {str(e)}\n")
            sys.stderr.flush()

    # 启动异步执行
    aio.run(execute_code())


def clear_canvas(ev):
    

    # 清空画布和输出
    try:
        brain = Brain()
        brain.screen.clear_screen()
    except:
        pass  # 忽略可能的错误

    document["output"].innerHTML = ""
    document["status"].text = "已重置"
    document["status"].className = "status info"
    stop_flag['value'] = True


# 将Brain类添加到全局作用域
window.Brain = Brain
window.wait = wait
window.vexEnum = vexEnum
window.Color = Color
window.FontType = FontType


# 绑定事件
document["runBtn"].bind("click", run_code)
document["resetBtn"].bind("click", clear_canvas)
