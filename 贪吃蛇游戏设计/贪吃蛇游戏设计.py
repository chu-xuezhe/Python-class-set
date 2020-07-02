import random
import pygame
import sys
import os
os.chdir(sys.path[0])#vscode中使用相对路径打开文件
from pygame.locals import *
import turtle

snake_speed = 8 #贪吃蛇的速度
windows_width = 800
windows_height = 600 #游戏窗口的大小
cell_size = 20       #贪吃蛇身体方块大小,注意身体大小必须能被窗口长宽整除

''' #初始化区
由于我们的贪吃蛇是有大小尺寸的, 因此地图的实际尺寸是相对于贪吃蛇的大小尺寸而言的
'''
map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)
BG_COLOR = black #游戏背景颜色

# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HEAD = 0 #贪吃蛇头部下标

#主函数
def main():
	pygame.init() # 模块初始化
	snake_speed_clock = pygame.time.Clock() # 创建Pygame时钟对象 可以控制游戏循环频率
	screen = pygame.display.set_mode((windows_width, windows_height)) #创建游戏的窗口
	screen.fill(white)#窗口背景颜色的填充

#背景音乐
	pygame.mixer.music.load('少年中国说.mp3')
	pygame.mixer.music.set_volume(0.5)#设置音乐音量
	pygame.mixer.music.play(loops=-1,start=0.0)#设置音乐循环与开始时间（不知为何不循环）

	pygame.display.set_caption("靓仔GOGOGO！贪吃蛇小游戏") #设置标题
	show_start_info(screen)               #欢迎信息
	while True:
		running_game(screen, snake_speed_clock)#游戏运行主体
		show_gameover_info(screen)#显示游戏结束

#游戏运行主体
def running_game(screen,snake_speed_clock):
	startx = random.randint(3, map_width - 8) #开始位置
	starty = random.randint(3, map_height - 8)
	snake_coords = [{'x': startx, 'y': starty},  #初始贪吃蛇
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
	direction = RIGHT       #  开始时向右移动
	food = get_random_location()     #实物随机位置
	while True:
		for event in pygame.event.get(): # 监听用户事件
			if event.type == QUIT:#退出
				terminate()
			elif event.type == KEYDOWN:#利用键盘移动
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()

		move_snake(direction, snake_coords) #移动蛇
		ret = snake_is_alive(snake_coords)#判断蛇是否活着
		if not ret:
			break #蛇跪了. 游戏结束
		snake_is_eat_food(snake_coords, food) #判断蛇是否吃到食物
		screen.fill(BG_COLOR)#游戏背景色
		#draw_grid(screen)
		draw_snake(screen, snake_coords)
		draw_food(screen, food)
		draw_score(screen, len(snake_coords) - 3)
		pygame.display.update()#更新屏幕显示
		snake_speed_clock.tick(snake_speed) ## 通过时钟对象指定循环频率
#将食物画出来
def draw_food(screen, food):
	x = food['x'] * cell_size
	y = food['y'] * cell_size
	appleRect = pygame.Rect(x, y, cell_size, cell_size)
	pygame.draw.rect(screen, Red, appleRect)#绘制矩形
#将贪吃蛇画出来
def draw_snake(screen, snake_coords):
	for coord in snake_coords:
		x = coord['x'] * cell_size
		y = coord['y'] * cell_size
		wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
		pygame.draw.rect(screen, dark_blue, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(                #蛇身子里面的第二层亮绿色
			x + 4, y + 4, cell_size - 8, cell_size - 8)
		pygame.draw.rect(screen, blue, wormInnerSegmentRect)

#移动贪吃蛇
def move_snake(direction, snake_coords):
    if direction == UP:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

    snake_coords.insert(0, newHead)
#判断蛇是否活着
def snake_is_alive(snake_coords):
	tag = True
	if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or \
			snake_coords[HEAD]['y'] == map_height:
		tag = False # 蛇碰壁啦
	for snake_body in snake_coords[1:]:
		if snake_body['x'] == snake_coords[HEAD]['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
			tag = False # 蛇碰到自己身体啦
	return tag
#判断贪吃蛇是否吃到食物
def snake_is_eat_food(snake_coords, food):  #如果是列表或字典，那么函数内修改参数内容，就会影响到函数体外的对象。
	if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
		food['x'] = random.randint(0, map_width - 1)
		food['y'] = random.randint(0, map_height - 1) # 实物位置重新设置
	else:
		del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉
#食物随机生成
def get_random_location():
	return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}
#开始信息显示
def show_start_info(screen):
	font = pygame.font.Font('myfont.ttf', 40)
	tip = font.render('按任意键开始游戏~~~', True, (65, 105, 225))
	gamestart = pygame.image.load('gamestart.png')
	screen.blit(gamestart, (140, 30))
	screen.blit(tip, (240, 550))
	pygame.display.update()

	while True:  #键盘监听事件
		for event in pygame.event.get():  # event handling loop
			if event.type == QUIT:
				terminate()     #终止程序
			elif event.type == KEYDOWN:
				if (event.key == K_ESCAPE):  #终止程序
					terminate() #终止程序
				else:
					return #结束此函数, 开始游戏
#游戏结束信息显示
def show_gameover_info(screen):
	font = pygame.font.Font('myfont.ttf', 40)
	tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏~', True, (65, 105, 225))
	gamestart = pygame.image.load('gameover.png')
	screen.blit(gamestart, (60, 0))
	screen.blit(tip, (80, 300))
	pygame.display.update()

	while True:  #键盘监听事件
		for event in pygame.event.get():  # event handling loop
			if event.type == QUIT:
				terminate()     #终止程序
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:  #终止程序
					terminate() #终止程序
				else:
					return #结束此函数, 重新开始游戏
#画成绩
def draw_score(screen,score):
	font = pygame.font.Font('myfont.ttf', 30)
	scoreSurf = font.render('得分: %s' % score, True, Green)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (windows_width - 120, 10)
	screen.blit(scoreSurf, scoreRect)
#程序终止
def terminate():
	pygame.quit()
	sys.exit()

main()