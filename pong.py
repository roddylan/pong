# pong.py
# 2 player pong game
# score goes up to 11, points given to player if ball reaches opposite wall
# player 1 controls: q up | a down
# player 2 controls: p up | l down



import pygame

def main():
    # initialize pygame modules
    pygame.init()
    # create pygame display window
    pygame.display.set_mode((500, 400))
    # set title of display window
    pygame.display.set_caption('Pong')
    # get display surface
    w_surface = pygame.display.get_surface()
    # instantiate game
    game = Game(w_surface)
    # play game, start main gameplay loop
    game.play()
    # quit pygame and clean up pygame window
    pygame.quit()
    
class Game:
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = pygame.Color('black')
        # game variables
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True 
        
        # paddle variables
        self.paddle_width = 10
        self.paddle_height = 50
        self.middle_y = self.surface.get_height()/2 - self.paddle_height/2        
        self.object_color = pygame.Color('white')
        self.paddle_velocity_increment = 8
        
        # instantiate paddle objects
        self.player1 = Paddle(90,self.middle_y,self.paddle_width,self.paddle_height,self.object_color,self.surface) #q up | a down
        self.player2 = Paddle(400,self.middle_y,self.paddle_width,self.paddle_height,self.object_color,self.surface) #p up | l down
        
        self.initial_ball_x_velocity = 4
        self.initial_ball_y_velocity = 2
        # instantiate ball object
        self.ball = Ball(self.object_color,5,[self.surface.get_width()/2,self.surface.get_height()/2],[self.initial_ball_x_velocity,self.initial_ball_y_velocity],self.surface)
        
        # variables for scoring
        player1_score = 0
        player2_score = 0
        self.scores = [player1_score,player2_score]
        self.max_score = 11
           
        
    def play(self):
        # main gameplay loop
        while not self.close_clicked:
            self.handle_events()
            self.draw()
            if self.continue_game:            
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)
    
    def handle_events(self):
        # handle game events (user inputs)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            if event.type == pygame.KEYUP:
                self.handle_keyup(event)
    
    def handle_keydown(self, event):
        # player 1 key handling
        if event.key == pygame.K_q:
            self.player1.set_velocity(-self.paddle_velocity_increment)
        if event.key == pygame.K_a:
            self.player1.set_velocity(self.paddle_velocity_increment)
        # player 2 key handling
        if event.key == pygame.K_p:
            self.player2.set_velocity(-self.paddle_velocity_increment)
        if event.key == pygame.K_l:
            self.player2.set_velocity(self.paddle_velocity_increment)
        
    
    def handle_keyup(self, event):
        # player 1 key handling
        if event.key == pygame.K_q or event.key == pygame.K_a:
            self.player1.set_velocity(0)
        # player 2 key handling
        if event.key == pygame.K_p or event.key == pygame.K_l:
            self.player2.set_velocity(0)        
    
    def draw(self):
        # draw all game objects
        self.surface.fill(self.bg_color)
        self.print_score()
        self.player1.draw()
        self.player2.draw()
        self.ball.draw()
        pygame.display.update()
        
    
    def update(self):
        # update game objects for next frame
        self.player1.move()
        self.player2.move()
        self.check_collision()
        self.ball.move()
    

    
    def decide_continue(self):
        # check scores of players to see if game is over
        for i in range(2):
            if self.scores[i] >= self.max_score:
                self.continue_game = False
            
    
    def check_collision(self):
        # change velocity of ball if it hits paddle coming from center
        if self.player1.rect.collidepoint(self.ball.center): 
            if self.ball.velocity[0] == -self.initial_ball_x_velocity:
                self.ball.set_velocity('x')
        if self.player2.rect.collidepoint(self.ball.center): 
            if self.ball.velocity[0] == self.initial_ball_x_velocity:
                self.ball.set_velocity('x')
        # ball bounce off walls
        # update score when hitting left/right walls
        if self.ball.center[0]-self.ball.radius <= 0:
            self.ball.set_velocity('x')
            self.update_score(0)
        if self.ball.center[0]+self.ball.radius >= self.surface.get_width():
            self.ball.set_velocity('x')
            self.update_score(1)
        if self.ball.center[1]-self.ball.radius <= 0 or self.ball.center[1]+self.ball.radius >= self.surface.get_height():
            self.ball.set_velocity('y')
            
    def update_score(self,i):
        #update score of player
        self.scores[i] += 1

    def print_score(self):
        # display scores of both players on screen
        p1_score = str(self.scores[1])
        p2_score = str(self.scores[0])
        # text appearance
        text_color = pygame.Color('white')
        text_font = pygame.font.SysFont('',80)
        text_font.bold = True
        # render score text
        p1_score_image = text_font.render(p1_score,True,text_color)
        p2_score_image = text_font.render(p2_score,True,text_color)
        # set positions of player scores to top left/right corners
        p1_score_position = [0,0]
        p2_score_position = [self.surface.get_width()-text_font.size(p2_score)[0],0]
        # display scores
        self.surface.blit(p1_score_image,p1_score_position)
        self.surface.blit(p2_score_image,p2_score_position)
        
class Paddle:
    def __init__(self,x,y,width,height,color,surface):
        # initialize paddle variables
        self.rect = pygame.Rect(x,y,width,height)
        self.surface = surface
        self.color = pygame.Color(color)
        self.velocity = 0        
        
    def move(self):
        # move paddle using velocity
        self.rect.move_ip(0,self.velocity)
        # prevent paddle from going out of screen
        self.fix_points()
        
    
    def draw(self):
        # draw paddle
        pygame.draw.rect(self.surface,self.color,self.rect)
        
    
    def fix_points(self):
        # keep top and bottom of paddle in screen
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.surface.get_height():
            self.rect.bottom = self.surface.get_height()
    
    def set_velocity(self,new_velocity):
        # change velocity of paddle
        self.velocity = new_velocity

        
class Ball:
    def __init__(self,ball_color,ball_radius,ball_center,ball_velocity, surface):
        # initialize ball variables
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface
        
        
    def move(self):
        # move ball on x and y axis using velocity
        for i in range(2):
            self.center[i] = self.center[i]+self.velocity[i]
        
    
    def draw(self):
        # draw ball
        pygame.draw.circle(self.surface,self.color,self.center,self.radius)
        
    def set_velocity(self,axis):
        # change ball velocity
        if axis == 'x':
            self.velocity[0] = -self.velocity[0]
        if axis == 'y':
            self.velocity[1] = -self.velocity[1]        
    
    
main()
