# VEX-V5 屏幕模拟器
**[[English]](README.md)**
**[[中文]](README_zh.md)**


点击访问 [VEX-V5屏幕模拟器](https://mengchuiru.github.io/VEX-V5-Screen-Simulator) 开始使用。

![VEX-V5 屏幕模拟器截图](./assets/screenshot.png)

## 概述

VEX-V5 屏幕模拟器是一个基于浏览器的交互式工具，允许用户通过Python编程模拟VEX V5机器人的屏幕显示和交互功能。该项目提供了完整的开发环境，包括代码编辑器、实时预览和输出控制台，是VEX机器人初学者和教育者的理想工具。

你可以使用VEX的类有： 
`Brain` 
`FontType` 
`Color`

## 主要功能

- **实时屏幕模拟**：480x240像素的VEX V5屏幕模拟
- **Python编程环境**：内置代码编辑器支持Python语法高亮和自动完成
- **示例程序**：提供多个预置示例程序，包括：
  - 旋转立方体
  - 打砖块游戏
  - 代码雨效果
- **触摸交互**：支持画布上的触摸/鼠标交互
- **运行计时器**：显示程序运行时间
- **输出控制台**：实时显示程序输出和错误信息
- **文件管理**：支持上传本地Python文件

## 技术栈

- **前端框架**：纯HTML/CSS/JavaScript
- **Python运行时**：Brython (浏览器中运行Python)
- **代码编辑器**：CodeMirror
- **图形渲染**：HTML5 Canvas

## 快速开始

### 在线使用

直接访问 [VEX-V5屏幕模拟器](https://mengchuiru.github.io/VEX-V5-Screen-Simulator) 开始使用。

### 本地运行

1. 克隆仓库：
```bash
git clone https://github.com/mengchuiru/vex-v5-simulator.git
cd vex-v5-simulator
```

2. 启动本地服务器：
```bash
# 使用Python内置服务器
python -m http.server 8000
```

3. 在浏览器中打开：
```
http://localhost:8000
```

## 使用指南

### 界面介绍

1. **屏幕模拟区域**：显示VEX V5屏幕模拟效果
2. **代码编辑器**：编写和编辑Python代码
3. **控制按钮**：
   - ▶ 运行代码
   - ⏹ 停止运行并清空画布
4. **示例选择器**：加载预置示例程序
5. **输出控制台**：显示程序输出和错误信息
6. **运行计时器**：显示程序运行时间

### 基本操作

1. 从示例选择器中选择一个示例程序
2. 点击▶按钮运行程序
3. 与画布交互（触摸/点击）
4. 点击⏹按钮停止程序
5. 修改代码后再次运行查看效果

### 自定义开发

编写Python代码使用以下API：

```python
from vex import *

# 初始化大脑
brain = Brain()

# 设置颜色
brain.screen.set_pen_color(Color.RED)
brain.screen.set_fill_color(Color.BLUE)

# 绘制图形
brain.screen.draw_rectangle(100, 100, 50, 50)
brain.screen.draw_circle(200, 120, 30)

# 显示文本
brain.screen.print_at("Hello VEX!", 50, 50)

# 等待
wait(1000)

# 清屏
brain.screen.clear_screen()
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建Pull Request

## 许可证

本项目采用 [MIT许可证](LICENSE)。

## 联系方式

如有任何问题或建议，请联系：
- 邮箱：mengchuiru@qq.com
- 项目地址：https://github.com/mengchuiru/vex-v5-simulator

---

**让VEX机器人编程更直观、更高效！** 🚀