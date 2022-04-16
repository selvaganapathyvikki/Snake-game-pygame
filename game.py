import pygame
import random
 
pygame.init()

#colors to display 
white = (255, 255, 255) # background
black = (0, 0, 0) # blocks colour
red = (213, 50, 80) # food colour
green = (0, 255, 0) # for text
blue = (50, 153, 213) # for snake

#basic game details
snake_block = 10
snake_speed = 15
top_score = 0
moving_direction = ""

#getting window size
print("Maximum width is 1000 and maximum height is 650")
display_width = int(input("Enter width of the screen : "))
display_height = int(input("Enter heigth of the screen : "))

#getting difficulty level
print("Difficulty level")
print("Enter 1 for easy 2 for medium 3 for hard")
difficulty_level = input("Enter difficulty level : ")

while difficulty_level not in ["1","2","3"] :
    print("invalid input, please enter 1 for easy 2 for medium and 3 for difficulty")
    difficulty_level = input("Enter difficulty level : ")
if(difficulty_level == "1") :
    snake_speed = 10
elif difficulty_level == "2" :
    snake_speed = 15
elif difficulty_level == "3" :
    snake_speed = 23

dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')
 
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 25)
 
#displaying score and top score in top left corner
def display_score(score):
    value = font_style.render("Hey you got " + str(score)+" score :)   Top score : "+str(top_score)+"", True, green)
    dis.blit(value, [1, 0])

#for placing the blocks 
def draw_blocks(blocks_list) : 
    for i in blocks_list :
        pygame.draw.rect(dis,black,[i[0],i[1],10,10])

#drawing snake in grid 
def draw_snake(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])
 
#displaying message
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 9, display_height / 5])
 
#main function to start the game
def startGame():
    
    global top_score
    global moving_direction

    game_quit = False
    current_game_over = False
 
    x = display_width / 2
    y = display_height / 2
 
    x_change = 0
    y_change = 0
 
    snake_list = []
    snake_length = 1
    blocks_list = []
    if difficulty_level == "2" :
        #randomly placing 25 blocks to increase difficulty
        for i in range(display_width//40) :
            blockx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            blocky = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            blocks_list.append([blockx,blocky])
        
        pygame.display.update()
    if difficulty_level == "3" :
        #randomly placing 40 blocks to inrease difficulty
        for i in range(1000//25) :
            blockx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            blocky = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            blocks_list.append([blockx,blocky])
       
        pygame.display.update()

    #generating food in random place
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
    while [foodx,foody] in blocks_list :
        foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
    
    moving_direction = ""
    while not game_quit:
        
        while current_game_over == True:
            dis.fill(white)
            display_message("You lost :( :Press ENTER-replay game or ESC-quit", green)
            display_score(snake_length - 1)
            pygame.display.update()

            #checking for replay or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_quit = True
                        current_game_over = False
                    if event.key == pygame.K_RETURN:
                        startGame()
 
        #for directions and avoid clash between turns
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if(moving_direction == "right") :
                        continue
                    x_change = -snake_block
                    y_change = 0
                    moving_direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if moving_direction == "left" :
                        continue
                    x_change = snake_block
                    y_change = 0
                    moving_direction = "right"
                elif event.key == pygame.K_UP:
                    if moving_direction == "down" :
                        continue
                    y_change = -snake_block
                    x_change = 0
                    moving_direction = "up"
                elif event.key == pygame.K_DOWN:
                    if moving_direction == "up" :
                        continue
                    y_change = snake_block
                    x_change = 0
                    moving_direction = "down"

        #checking if it hits the wall
        if x >= display_width or x < 0 or y >= display_height or y < 0:
            current_game_over = True

        x += x_change
        y += y_change

        #drawing food
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        #checking it hits its own body
        for i in snake_list[:-1]:
            if i == snake_head:
                current_game_over = True
                score = snake_length-1
                top_score = max(score,top_score)

        #checking if the snake hits any of the block
        for i in blocks_list :
            if i == snake_head :
                score = snake_length-1
                top_score = max(score,top_score)
                current_game_over = True

        #drawing the snake with updated length and blocks
        draw_snake(snake_block, snake_list)
        draw_blocks(blocks_list)
        display_score(snake_length - 1)
 
        pygame.display.update()

        #checking if the food is eaten by snake
        if x == foodx and y == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            snake_length += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
startGame()