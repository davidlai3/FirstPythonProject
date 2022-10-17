import pygame
import random
import math

pygame.font.init()
pygame.init()

# Global Variables
s_width = 800
s_height = 700
board_width = 300
board_height = 600
block_size = 30

top_left_x = (s_width - board_width) // 2
top_left_y = s_height - board_height

background = pygame.image.load('scaled bg.png')

# Piece Rotations

T = [['.....',
	   '...0.',
	   '..000',
	   '.....',
	   '.....'],
	 ['.....',
	  '...0.',
	  '...00',
	  '...0.',
	  '.....'],
	 ['.....',
	  '.....',
	  '..000',
	  '...0.',
	  '.....'],
	 ['.....',
	  '...0.',
	  '..00.',
	  '...0.',
	  '.....']]

J = [['.....',
			'..0..',
			'..000',
			'.....',
			'.....'],
			['.....',
			'...00',
			'...0.',
			'...0.',
			'.....'],
		['.....',
			'..000',
			'....0',
			'.....',
			'.....'],
		['.....',
			'....0',
			'....0',
			'...00',
			'.....']]

Z = [['.....',
	  '..00.',
	  '...00',
	  '.....',
	  '.....'],
	 ['.....',
	  '....0',
	  '...00',
	  '...0.',
	  '.....']]

O = [['.....',
	  '..00.',
	  '..00.',
	  '.....',
	  '.....']]

S = [['.....',
	  '...00',
	  '..00.',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..00.',
	  '...0.',
	  '.....']]

L = [['.....',
	  '....0',
	  '..000',
	  '.....',
	  '.....'],
	 ['.....',
	  '..0..',
	  '..0..',
	  '..00.',
	  '.....'],
	 ['.....',
	  '.....',
	  '..000',
	  '..0..',
	  '.....'],
	 ['.....',
	  '..00.',
	  '...0.',
	  '...0.',
	  '.....']]

I = [['.....',
	  '.0000',
	  '.....',
	  '.....',
	  '.....'],
	 ['..0..',
	  '..0..',
	  '..0..',
	  '..0..',
	  '.....'], ]

shapes = [T, J, Z, O, S, L, I]
shape_colors = [(128, 0, 128), (0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0), (255, 165, 0), (0, 255, 255)]


class Piece(object):
	# Allows program to identify shape and rotation
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = shape_colors[shapes.index(shape)]
		self.rotation = 0


# Creates 10x20 grid using 2d lists and keeps track of pieces placed
# Taken space parameter will keep track of piece position and color
def create_grid(taken_space={}):  # *
	grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if (j, i) in taken_space:
				c = taken_space[(j, i)]
				grid[i][j] = c
	return grid


# Returns rotated shape positions
def rotate(shape):
	positions = []
	format = shape.shape[shape.rotation % len(shape.shape)]

	# Checks for 0 in piece drawings, and adds it to a list
	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				positions.append((shape.x + j, shape.y + i))

	# Pieces fall from above screen
	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)

	return positions


# Takes all dimensions from two dimensional list and adds it into a one dimensional list
# Adds empty space into available space
def available_space(shape, grid):
	accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
	accepted_pos = [j for sub in accepted_pos for j in sub]

	formatted = rotate(shape)

	for pos in formatted:
		if pos not in accepted_pos:
			if pos[1] > -1:
				return False
	return True


# Checks for loss by checking if any pieces are above the board
def game_over(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True

	return False

pieces_placed = []

# Determines piece sequence
def get_shape():
	shape = random.choice(shapes)
	pieces_placed.append(shape)
	return Piece(5, 0, shape)


def draw_text_middle(surface, text, size, color):
	font = pygame.font.SysFont("timesnewroman", size, bold=True)
	label = font.render(text, 1, color)

	surface.blit(label, (
		top_left_x + board_width / 2 - (label.get_width() / 2), top_left_y + board_height / 2 - label.get_height() / 2))


# Draws grid lines
def draw_grid(surface, grid):
	sx = top_left_x
	sy = top_left_y

	for i in range(len(grid)):
		pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + board_width, sy + i * block_size))
		for j in range(len(grid[i])):
			pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
							 (sx + j * block_size, sy + board_height))


def clear_rows(grid, locked):
	lines_cleared = 0
	for i in range(len(grid) - 1, -1, -1):  # Loops through grid backwards
		row = grid[i]
		if (0, 0, 0) not in row:
			lines_cleared += 1
			ind = i
			for j in range(len(row)):
				try:
					del locked[(j, i)]
				except:
					continue
	# clears line and shifts all pieces down
	if lines_cleared > 0:
		for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				new_key = (x, y + lines_cleared)
				locked[new_key] = locked.pop(key)
	return lines_cleared


def show_next(shape, surface):
	font = pygame.font.SysFont('timesnewroman', 30)
	label = font.render('NEXT', 5, (255, 255, 255))

	sx = top_left_x + board_width + 50
	sy = top_left_y + board_height / 2 - 100
	pygame.draw.rect(surface, (0, 0, 0), (sx - 10, sy, 150, 170), 0)
	pygame.draw.rect(surface, (135, 206, 250), (sx - 10, sy, 150, 170), 5)
	format = shape.shape[shape.rotation % len(shape.shape)]

	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				pygame.draw.rect(surface, shape.color, (sx + j * block_size - 40, sy + i * block_size + 40, block_size, block_size), 0)

	surface.blit(label, (sx + 25, sy + 10))


def draw_type_a(surface):
	font = pygame.font.SysFont('timesnewroman', 40)
	label = font.render('A - TYPE', 5, (255, 255, 255))
	pygame.draw.rect(surface, (0, 0, 0), (40, 130, 200, 50), 0)
	pygame.draw.rect(surface, (135, 206, 250), (40, 130, 200, 50), 5)
	surface.blit(label, (60, 140))


def draw_statistics(surface):
	pygame.draw.rect(surface, (0, 0, 0), (40, 200, 200, 450), 0)
	pygame.draw.rect(surface, (135, 206, 250), (40, 200, 200, 450), 5)

	font = pygame.font.SysFont('timesnewroman', 30)
	label = font.render('STATISTICS', 5, (255, 255, 255))
	surface.blit(label, (60, 210))


# Draws icons next to statistic shapes
def draw_statistic_shapes(surface):
	for shape in shapes:
		for i, line in enumerate(shape[0]):
			row = list(line)
			for j, column in enumerate(row):
				if column == '0':
					pygame.draw.rect(surface, shape_colors[shapes.index(shape)], (j * 20 + 30, 220 + i * 20 + (shapes.index(shape) * 60), 20, 20), 0)


# Finds and draws statisic nums
# This could probably be coded way better but I ran out of time
def draw_statistic_nums(surface):
	t_count = pieces_placed.count(T)
	j_count = pieces_placed.count(J)
	z_count = pieces_placed.count(Z)
	o_count = pieces_placed.count(T)
	s_count = pieces_placed.count(S)
	l_count = pieces_placed.count(L)
	i_count = pieces_placed.count(I)

	font = pygame.font.SysFont('timesnewroman', 30)
	
	t_num = font.render(str(t_count), 5, (255, 255, 255))
	j_num = font.render(str(j_count), 5, (255, 255, 255))
	z_num = font.render(str(z_count), 5, (255, 255, 255))
	o_num = font.render(str(o_count), 5, (255, 255, 255))
	s_num = font.render(str(s_count), 5, (255, 255, 255))
	l_num = font.render(str(l_count), 5, (255, 255, 255))
	i_num = font.render(str(i_count), 5, (255, 255, 255))

	labels = [t_num, j_num, z_num, o_num, s_num, l_num, i_num]

	for i in labels:
		surface.blit(i, (180, 240 + (labels.index(i) * 60)))

def draw_level(surface, score):
	level_num = math.floor(score/100) + 1
	sx = top_left_x + board_width + 50
	sy = top_left_y + board_height / 2 - 100

	font = pygame.font.SysFont('timesnewroman', 30)
	level = font.render('LEVEL', 5, (255, 255, 255))
	level_number = font.render(str(level_num), 5, (255, 255, 255))

	pygame.draw.rect(surface, (0, 0, 0), (sx - 10, sy + 170, 150, 120), 0)
	pygame.draw.rect(surface, (135, 206, 250), (sx - 10, sy + 170, 150, 120), 5)

	surface.blit(level, (sx + 10, sy + 175))
	surface.blit(level_number, (sx + 10, sy + 205))


# Updates highscore if player beats it
def update_score(new_score):
	score = highscore()
	with open('score.txt', 'w') as f:
		if int(score) < new_score:
			f.write(str(new_score))
		else:
			f.write(str(score))


# Reads highscore file and returns it
def highscore():
	with open('score.txt', 'r') as f:
		lines = f.readlines()
		top = lines[0].strip()
	return top


# Creates box for scores
def draw_score(surface):
	font = pygame.font.SysFont('timesnewroman', 30)
	highscore = font.render('TOP', 5, (255, 255, 255))
	current_score = font.render('SCORE', 5, (255, 255, 255))

	sx = top_left_x + board_width + 50
	pygame.draw.rect(surface, (0, 0, 0), (sx - 10, s_height - board_height, 150, 200), 0)
	pygame.draw.rect(surface, (135, 206, 250), (sx - 10, s_height - board_height, 150, 200), 5)

	surface.blit(highscore, (sx + 10, 120))
	surface.blit(current_score, (sx + 10, 190))


# Creates title, main play window, and draws scores
def draw_window(surface, grid, score = 0, last_score = 0):
	surface.fill((0, 0, 0))
	win.blit(background,(20, 20))
	draw_score(win)
	pygame.font.init()
	font = pygame.font.SysFont('timesnewroman', 60)
	label = font.render('TETRIS', 1, (255, 255, 255))
	surface.blit(label, (top_left_x + board_width / 2 - (label.get_width() / 2), 30))
	
	sx = top_left_x + board_width + 50

	font = pygame.font.SysFont('timesnewroman', 30)
	label = font.render(str(score), 1, (255, 255, 255))
	surface.blit(label, (sx+10, 215))
	label = font.render(str(last_score), 1, (255, 255, 255))
	surface.blit(label, (sx+10, 150))

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

	pygame.draw.rect(surface, (135, 206, 250), (top_left_x, top_left_y, board_width, board_height), 5)

	draw_grid(surface, grid)


# Main loop
def main(win):
	last_score = highscore()
	taken_space = {}
	grid = create_grid(taken_space)

	change_piece = False
	run = True
	current_piece = get_shape()
	next_piece = get_shape()
	clock = pygame.time.Clock()
	fall_time = 0
	fall_speed = 0.27
	level_time = 0
	score = 0

	while run:
		grid = create_grid(taken_space)
		fall_time += clock.get_rawtime()
		level_time += clock.get_rawtime()
		clock.tick()

		if level_time / 1000 > 5:
			level_time = 0
			if level_time > 0.12:
				level_time -= 0.005

		if fall_time / 1000 > fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not (available_space(current_piece, grid)) and current_piece.y > 0:
				current_piece.y -= 1
				change_piece = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.display.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_piece.x -= 1
					if not (available_space(current_piece, grid)):
						current_piece.x += 1
				if event.key == pygame.K_RIGHT:
					current_piece.x += 1
					if not (available_space(current_piece, grid)):
						current_piece.x -= 1
				if event.key == pygame.K_DOWN:
					current_piece.y += 1
					if not (available_space(current_piece, grid)):
						current_piece.y -= 1
				if event.key == pygame.K_UP:
					current_piece.rotation += 1
					if not (available_space(current_piece, grid)):
						current_piece.rotation -= 1
				if event.key == pygame.K_z:
					current_piece.rotation -= 1
					if not (available_space(current_piece, grid)):
						current_piece -= 1

		shape_pos = rotate(current_piece)

		for i in range(len(shape_pos)):
			x, y = shape_pos[i]
			if y > -1:
				grid[y][x] = current_piece.color

		if change_piece:
			for pos in shape_pos:
				p = (pos[0], pos[1])
				taken_space[p] = current_piece.color
			pieces_placed.append(current_piece)
			current_piece = next_piece
			next_piece = get_shape()
			change_piece = False
			score += int(clear_rows(grid, taken_space)) * 10

		draw_window(win, grid, score, last_score)
		show_next(next_piece, win)
		draw_type_a(win)
		draw_statistics(win)
		draw_statistic_shapes(win)
		draw_statistic_nums(win)
		draw_level(win, score)
		pygame.display.update()

		if game_over(taken_space):
			draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
			pygame.display.update()
			pygame.time.delay(1500)
			run = False
			update_score(score)
			win.fill((0, 0, 0))


# Creates starting screen
# Quits pygame if closed
def main_menu(win):
	run = True
	win.fill((0, 0, 0))
	while run:
		draw_text_middle(win, 'Press P To Play', 60, (255, 255, 255))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					main(win)

	pygame.display.quit()


# Starts game
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
