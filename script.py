
from browser import document, window, alert
import javascript
# 创建模拟的Brain和Screen类
class Brain:
    def __init__(self):
        self.screen = Screen()
class Screen:
    def __init__(self):
        self.canvas = document["screenCanvas"]
        self.ctx = self.canvas.getContext("2d")
        self.ctx.lineWidth = 1
        self.ctx.strokeStyle = "#4cc9f0"
        self.ctx.fillStyle = "#4361ee"
        self.ctx.font = "16px Arial"
        self.ctx.textAlign = "left"
    def clear(self):
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
        self.ctx.fillStyle = "#4361ee"
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
# 执行代码的函数
def run_code(ev):
    try:
        code = document["codeInput"].value
        # 清空画布
        Brain().screen.clear()
        # 更新状态
        document["status"].text = "Executing code..."
        document["status"].className = "status info"
        # 执行代码
        exec(code, {"__name__": "__main__", "Brain": Brain})
        # 成功消息
        document["status"].text = "Code executed successfully!"
        document["status"].className = "status success"
    except Exception as e:
        document["status"].text = f"Error: {str(e)}"
        document["status"].className = "status error"
# 清空画布的函数
def clear_canvas(ev):
    Brain().screen.clear()
    document["status"].text = "Canvas cleared"
    document["status"].className = "status info"
# 绑定事件
document["runBtn"].bind("click", run_code)
document["clearBtn"].bind("click", clear_canvas)