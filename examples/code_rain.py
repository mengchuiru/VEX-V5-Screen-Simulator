# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       mengc                                                        #
# 	Created:      2025/3/8 21:08:52                                            #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #


from vex import *
import random

brain=Brain()


text = "ILoveVEX "
colors = [Color(0,255-i,0)for i in range(0,256,255//len(text))]
brain.screen.set_font(FontType.MONO15)
char_height = 15
char_width = char_height//1
columns = 480 // char_width
drap_speeds = [random.randint(2,5) for _ in range(columns)]
drap_y = [0 for _ in range(columns)]
while True:
    brain.screen.clear_screen()

    for j in range(len(text)):
        brain.screen.set_pen_color(colors[j%len(colors)])
        for col in range(columns):
            brain.screen.print_at(text[j], x=col*char_width,y=drap_y[col]-20*j)
            drap_y[col] += drap_speeds[col]
            if drap_y[col] > random.randint(200,280):
                drap_y[col] = 0
                drap_speeds[col] = random.randint(2,5)
    brain.screen.render()
    wait(1000//30)


        