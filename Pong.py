import pygame,sys,random

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

def ball_animation():
    # acknowleding local scope of variables
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collisions
    # collisions for vertical axis
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    # collisions for horizontal axis
    if ball.left <= 0:
        # ball_restart()
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        # ball_restart()
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_movement():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.top > ball.y:
        opponent.top -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 1000: 
        number_three = my_font.render("3",True, black)
        screen.blit(number_three,(screen_width/2 - 18, screen_height/2 + 20))
    if 1000 < current_time - score_time < 2000: 
        number_two = my_font.render("2",True, black)
        screen.blit(number_two,(screen_width/2 - 18, screen_height/2 + 20))
    if 2000 < current_time - score_time < 3000: 
        number_one = my_font.render("1",True, black)
        screen.blit(number_one,(screen_width/2 - 18, screen_height/2 + 20))
    if current_time - score_time < 3000: 
        ball_speed_x = 0
        ball_speed_y = 0

    else:
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None

# Setting up pygame
pygame.init()
clock = pygame.time.Clock()

# Set up the game window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong Game')

# Making the rectangles for the objects using pygame.Rect()
# Making a rectangle for the ball: 30x30 px and starting in the center
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
# Making a rectangle for the player and opp
player = pygame.Rect(screen_width - 20,screen_height/2 - 70,10,140)
opponent = pygame.Rect(10, screen_height/2 - 70,10,140)

background_color = pygame.Color('azure4')
azure3 = pygame.Color('azure3')
white = (255,255,255)
black = (0,0,0)

ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 6

# Text
player_score = 0
opponent_score = 0
# freesansbold comes loaded with pygame
my_font = pygame.font.Font("freesansbold.ttf", 64)
pause_font = pygame.font.Font("freesansbold.ttf", 36)

# Score Timer
score_time = True

#Paused Game
game_paused = True
# game_won = False

while True:
    # updating the window: refresh rate
    pygame.display.flip()
    clock.tick(60)

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -=7
            if event.key == pygame.K_SPACE:
                if game_paused == False:
                    game_paused = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed +=7

    # Visuals
    screen.fill(background_color)
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, opponent)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (screen_width/2,0), (screen_width/2,screen_height))

    # Player text score is anti-aliased while opponent's is not to show 
    # the difference of when text is antialiased or not
    player_text = my_font.render(f"{player_score}", True, white)
    screen.blit(player_text,(660,50))
    opponent_text = my_font.render(f"{opponent_score}", False, white)
    screen.blit(opponent_text,(580,50))

    if game_paused == True:
        draw_text("Press space to continue game", pause_font, azure3, 380,350)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = False
  
    if game_paused == False:
        # Game Logic
        ball_animation()
        player_animation()
        opponent_movement()
        if score_time:
            ball_restart()
