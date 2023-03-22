import pygame
from sys import exit
from random import randint


# Player Objects
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surf = pygame.image.load('graphics/PongPaddle.png').convert_alpha()
        self.movement = 0
        self.image = player_surf
        self.rect = self.image.get_rect(center=(30, 300))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top >= 0:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.bottom <= 600:
            self.rect.y += 5

    def update(self):
        self.player_input()


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_surf = pygame.image.load('graphics/PongPaddle.png').convert_alpha()
        self.movement = 0
        self.image = player_surf
        self.rect = self.image.get_rect(center = (770, 300))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom <= 600:
            self.rect.y += 5

    def update(self):
        self.player_input()


# Ball Object
class Ball(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()

        # initialize ball
        ball_surf = pygame.image.load('graphics/PongBall.png').convert_alpha()
        self.movement = 0
        self.side_ball = side
        self.image = ball_surf
        self.rect = self.image.get_rect(center = (50, player_1.sprite.rect.y + 35))

        self.speed = 5
        self.bounce_count = 0

        # randomize if ball goes up or down
        if randint(0, 1):
            self.up_down = True  # true is up, false is down
        else:
            self.up_down = False

        self.initialize_state = True  # when true, we are serving the ball

        if side == 1:
            self.which_way = True  # true is right, false is left
            self.serve_ball(1)
        else:
            self.which_way = False  # start depends on which player is serving
            self.serve_ball(2)

    def side_helper(self):
        # up and down movement for ball
        if self.up_down:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        # top and bottom out of bounds for ball, if reached, set up_down to opposite
        if self.rect.top <= 0:
            self.up_down = False
        elif self.rect.bottom >= 600:
            self.up_down = True

    def side_to_side(self):
        # side to side movement for ball, depending on which_way boolean
        if self.which_way:
            self.rect.x += self.speed
            self.side_helper()
        else:
            self.rect.x -= self.speed
            self.side_helper()

    def bounce(self):
        # check if sprite collides from either player, switch directions depending on which one
        if pygame.sprite.spritecollide(player_1.sprite, ball, False):
            self.which_way = True
            self.bounce_helper()
        elif pygame.sprite.spritecollide(player_2.sprite, ball, False):
            self.which_way = False
            self.bounce_helper()

    def bounce_helper(self):
        # increase speed every 5 times the ball hits a paddle
        self.bounce_count += 1
        if self.bounce_count == 5:
            self.speed += 1
            self.bounce_count = 0

    def serve_ball(self, side):
        # checks if we are in a serving state, if so we will not perform any other function and loop this function
        if self.initialize_state:
            if side == 1:  # set ball in front of player 1 paddle
                self.rect = self.image.get_rect(center = (50, player_1.sprite.rect.y + 35))
            elif side == 2:  # set ball in front of player 2 paddle
                self.rect = self.image.get_rect(center = (750, player_2.sprite.rect.y + 35))

            # serve keys, if pressed proceed with game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d] and side == 1:
                self.initialize_state = False
            elif keys[pygame.K_LEFT] and side == 2:
                self.initialize_state = False
        else:
            # use normal game functions when we are not serving
            self.side_to_side()
            self.bounce()
            self.destroy()

    def destroy(self):
        # get rid of ball in group if reached left or right side of screen
        if self.rect.x <= 0:
            self.kill()
            score[1] += 1
        elif self.rect.x >= 800:
            self.kill()
            score[0] += 1

    def update(self):
        self.serve_ball(self.side_ball)


# Show scores
def display_score():
    score_p1_surf = text_font.render(f'{score[0]}', False, (255, 255, 255))
    score_p1_surf = pygame.transform.rotozoom(score_p1_surf, 0, 2)
    score_p1_rect = score_p1_surf.get_rect(center = (350, 50))
    screen.blit(score_p1_surf, score_p1_rect)

    score_p2_surf = text_font.render(f'{score[1]}', False, (255, 255, 255))
    score_p2_surf = pygame.transform.rotozoom(score_p2_surf, 0, 2)
    score_p2_rect = score_p2_surf.get_rect(center=(450, 50))
    screen.blit(score_p2_surf, score_p2_rect)


# Player win
def player_win(player):
    win_text = text_font.render(f'Player {player} wins!', False, (255, 255, 255))
    win_text = pygame.transform.rotozoom(win_text, 0, 2)
    win_text_rect = win_text.get_rect(center = (400, 300))
    screen.blit(win_text, win_text_rect)


# How to play description
def how_to_play():
    description_text = text_font.render('Player 1: Move up and down with w and s, press d to serve', False, (255, 255, 255))
    description_text2 = text_font.render('Player 2: Move up and down with up and down keys, press left to serve', False, (255, 255, 255))
    description_text = pygame.transform.rotozoom(description_text, 0, 0.75)
    description_text2 = pygame.transform.rotozoom(description_text2, 0, 0.75)
    description_text_rect = description_text.get_rect(center = (400, 275))
    description_text2_rect = description_text2.get_rect(center = (400, 325))
    screen.blit(description_text, description_text_rect)
    screen.blit(description_text2, description_text2_rect)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong')
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
clock = pygame.time.Clock()
game_active = False

# Initialize scores
score = [0, 0]  # index 0 is player 1, index 1 is player 2
score1 = 0  # these determine who will serve next
score2 = 0

# Intro Screen initialize
game_name = text_font.render('Pong', False, (255, 255, 255))
game_name = pygame.transform.rotozoom(game_name, 0, 2)
game_name_rect = game_name.get_rect(center = (400, 150))

click_start = text_font.render('Click Here To Start', False, (255, 255, 255))
click_start_rect = click_start.get_rect(center = (400, 450))

menu_count = 0

# Pong Visual
pong_net = pygame.image.load('graphics/PongNet.png').convert_alpha()
pong_net_rect = pong_net.get_rect(center = (400, 300))

# Players
player_1 = pygame.sprite.GroupSingle()
player_1.add(Player1())

player_2 = pygame.sprite.GroupSingle()
player_2.add(Player2())

# Ball
ball = pygame.sprite.Group()
ball.add(Ball(randint(1, 2)))

while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # click here animation when user is hovered over text
        if event.type == pygame.MOUSEMOTION:
            if menu_count == 0:
                if click_start_rect.collidepoint(event.pos):
                    click_start = text_font.render('Click Here To Start', False, (255, 255, 255))  # re-add text so it doesn't lose quality
                    click_start = pygame.transform.rotozoom(click_start, 0, 1.5)
                    click_start_rect = click_start.get_rect(center = (400, 450))
                    menu_count += 1
            if menu_count == 1:
                if not click_start_rect.collidepoint(event.pos):
                    click_start = text_font.render('Click Here To Start', False, (255, 255, 255))
                    click_start_rect = click_start.get_rect(center=(400, 450))
                    menu_count -= 1

        # if press menu button start game
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_start_rect.collidepoint(event.pos):
                score[0] = 0
                score[1] = 0
                game_active = True

    # background is always going to be black
    screen.fill((0, 0, 0))

    if game_active:
        # if any player reaches a score of 5, they win
        if score[0] == 5 or score[1] == 5:
            game_active = False

        # run game and draw sprites needed
        display_score()
        screen.blit(pong_net, pong_net_rect)

        player_1.draw(screen)
        player_1.update()

        player_2.draw(screen)
        player_2.update()

        # if empty, create new ball on side that lost that point
        if not ball.sprites():
            if score1 < score[0]:
                ball.add(Ball(2))
                score1 += 1
            else:
                ball.add(Ball(1))
                score2 += 1

        ball.draw(screen)
        ball.update()

    else:
        # set menu screen
        screen.blit(game_name, game_name_rect)
        screen.blit(click_start, click_start_rect)

        # change view screen depending on who won or if new game
        if score[0] == 5:
            player_win(1)
        elif score[1] == 5:
            player_win(2)
        else:
            how_to_play()

    pygame.display.update()
    clock.tick(60)
