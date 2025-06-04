from browser import document, window, alert, timer, aio, console
import javascript
import sys

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

# 简单实现wait函数
def wait(ms):
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
        self._row = 0
        self._col = 0
        self._originx = 0
        self._originy = 0
        self.pen_color = Color.WHITE
        self.fill_color = Color.BLACK

        self.canvas = document["screenCanvas"]
        self.ctx = self.canvas.getContext("2d")
        self.ctx.lineWidth = 1
        self.ctx.strokeStyle = self.pen_color
        self.ctx.fillStyle = self.fill_color
        self.ctx.font = "12px Monospace"
        self.ctx.textAlign = "left"
        self.ctx.textBaseline = "bottom"

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

    def set_pen_width(self, width: int):
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

# 将Brain类添加到全局作用域
window.Brain = Brain
window.wait = wait
window.vexEnum = vexEnum
window.Color = Color

# 执行代码的函数
def run_code(ev):
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
        code = document["codeInput"].value
        
        # 准备全局变量
        exec_globals = {
            "Brain": Brain,
            "wait": wait,
            "__name__": "__main__",
            "brain": brain
        }
        
        # 执行用户代码
        document["status"].text = "执行代码中..."
        exec(code, exec_globals)
        document["status"].text = "代码执行成功!"
    except Exception as e:
        document["status"].text = f"错误: {str(e)}"
        # 将错误信息输出到控制台
        sys.stderr.write(f"错误: {str(e)}\n")
        sys.stderr.flush()

def clear_canvas(ev):
    # 清空画布和输出
    Brain().screen.clear_screen()
    document["output"].innerHTML = ""
    document["status"].text = "已重置"
    document["status"].className = "status info"

# 绑定事件
document["runBtn"].bind("click", run_code)
document["resetBtn"].bind("click", clear_canvas)