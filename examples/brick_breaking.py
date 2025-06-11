# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       mengc                                                        #
# 	Created:      2025/5/24 19:04:16                                           #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


from vex import *

brain = Brain()  # 创建主控

# 设置屏幕分辨率
WIDTH = 480
HEIGHT = 240

# 设置常量
BALL_RADIUS = 12  # 球半径
PABBLE_WIDTH = 100  # 球拍宽度
PABBLE_HEIGHT = 20  # 球拍高度
BRICK_ROW = 5  # 磁砖行数
BRICK_COL = 10  # 磁砖列数
BRICK_GAP = 8  # 磁砖间隙
BRICK_WIDTH = (WIDTH+BRICK_GAP)/BRICK_COL - BRICK_GAP   # 磁砖宽度
BRICK_HEIGHT = HEIGHT / 2.5/BRICK_ROW - BRICK_GAP/2  # 磁砖高度

# 设置初始变量
colors = [Color.PURPLE, Color.ORANGE, Color.YELLOW,
          Color.GREEN,  Color.CYAN,]  # 颜色列表
bricks = []  # 磁砖列表
for i in range(BRICK_ROW):
    bricks.append([True] * BRICK_COL)
ball_x = WIDTH // 2
ball_y = HEIGHT // 1.3
ball_speed_x = 2
ball_speed_y = -3
pabble_x = (WIDTH - PABBLE_WIDTH) // 2
game_over = False
brick_num = BRICK_ROW * BRICK_COL  # 磁砖总数


def ball_position():
    """ 更新小球位置 """
    global ball_x, ball_y, ball_speed_x, ball_speed_y, game_over
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x-BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
        ball_speed_x = -ball_speed_x

    if ball_y-BALL_RADIUS < 0:
        ball_speed_y = -ball_speed_y
    if ball_y + BALL_RADIUS > HEIGHT:

        game_over = True
        ball_speed_y = -ball_speed_y


def pabble_position():
    """ 更新球拍位置 """
    global pabble_x
    if brain.screen.pressing():
        touch_x = brain.screen.x_position()
        
        # 平滑移动球拍 (跟随触摸点)
        target_x = touch_x - PABBLE_WIDTH // 2
        if target_x < 0:
            target_x = 0
        elif target_x > WIDTH - PABBLE_WIDTH:
            target_x = WIDTH - PABBLE_WIDTH
            
        # 插值移动，更平滑
        pabble_x += min(5,max((target_x - pabble_x) * 0.2,-5))


def collision_rect(rect_x, rect_y, rect_width, rect_height):
    """ 检测小球与矩形的碰撞 """
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    x_is_col = rect_x-BALL_RADIUS < ball_x < rect_x + rect_width + BALL_RADIUS
    y_is_col = rect_y-BALL_RADIUS < ball_y < rect_y + rect_height + BALL_RADIUS
    if x_is_col and y_is_col:
        if y_is_col:
            ball_speed_y = -ball_speed_y
        elif x_is_col:
            ball_speed_x = -ball_speed_x
        return True
    return False


def collision():
    """ 碰撞检测 """
    global ball_x, ball_y, ball_speed_x, ball_speed_y, brick_num

    # 检测小球与球拍的碰撞
    if collision_rect(pabble_x, HEIGHT - PABBLE_HEIGHT, PABBLE_WIDTH, PABBLE_HEIGHT):
        ball_y = HEIGHT - PABBLE_HEIGHT - BALL_RADIUS  # 确保小球在球拍上方

    # 检测小球与磁砖的碰撞
    for i in range(BRICK_ROW):
        for j in range(BRICK_COL):
            if bricks[i][j]:  # 如果磁砖存在
                if collision_rect(j * (BRICK_WIDTH+BRICK_GAP), i * (BRICK_HEIGHT+BRICK_GAP), BRICK_WIDTH, BRICK_HEIGHT):
                    bricks[i][j] = False  # 磁砖被击中，设置为不存在
                    brick_num -= 1  # 磁砖数量减少


def draw_ball(x, y):
    """ 绘制小球 """
    brain.screen.set_pen_color(Color.RED)  # 设置画笔颜色为红色
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_circle(x, y, BALL_RADIUS)


def draw_pabble(x):
    """ 绘制球拍 """
    brain.screen.set_pen_color(Color.BLUE)  # 设置画笔颜色为蓝色
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(
        x, HEIGHT - PABBLE_HEIGHT, PABBLE_WIDTH, PABBLE_HEIGHT)


def draw_brick():
    """ 绘制磁砖 """
    for i in range(BRICK_ROW):
        brain.screen.set_pen_color(colors[i % len(colors)])
        brain.screen.set_fill_color(colors[i % len(colors)])
        for j in range(BRICK_COL):
            if bricks[i][j]:
                brain.screen.draw_rectangle(
                    j * (BRICK_WIDTH+BRICK_GAP), i * (BRICK_HEIGHT+BRICK_GAP), BRICK_WIDTH, BRICK_HEIGHT)


while True:
    if game_over or brick_num <= 0:  # 如果游戏结束或磁砖数量为0
        brain.screen.set_pen_color(Color.WHITE)  # 设置画笔颜色为白色
        brain.screen.set_font(FontType.MONO60)
        if game_over:  # 如果游戏结束
            brain.screen.print_at("Game Over", WIDTH //
                                  2 - 120, HEIGHT // 2 + 20)  # 显示游戏结束
            wait(1000)
        else:  # 如果游戏胜利
            brain.screen.print_at("Game WIN", WIDTH //
                                  2 - 120, HEIGHT // 2 + 20)  # 显示游戏胜利
            wait(1000)
        brain.screen.render()  # 刷新屏幕
        if brain.screen.pressing():  # 等待按下屏幕
            # 设置初始变量
            bricks = []  # 磁砖列表
            for i in range(BRICK_ROW):
                bricks.append([True] * BRICK_COL)
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = 2
            ball_speed_y = -2
            pabble_x = (WIDTH - PABBLE_WIDTH) // 2
            game_over = False
            brick_num = BRICK_ROW * BRICK_COL
        wait(50)  # 等待0.5秒
        continue

    brain.screen.clear_screen()  # 清屏
    ball_position()  # 更新小球位置
    pabble_position()  # 更新球拍位置
    collision()  # 碰撞检测
    draw_brick()  # 绘制磁砖
    draw_pabble(pabble_x)  # 绘制球拍
    draw_ball(ball_x, ball_y)  # 绘制小球
    brain.screen.render()  # 刷新屏幕
    wait(20)


