import pygame
from sys import exit
import random

screen_width = 1280
screen_height = 720
pygame.init()
pygame.display.set_caption("Save the Animals!")
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_active = False
Win = None
Playing = None # Tracking the music
Sound_Played = False
Saved = 0

class Text():
    def Title():
        title_text = Font1.render("Race, Escape and Evade!", True, "Black")
        title_rect = title_text.get_rect(midbottom = (650, 300))
        return title_text, title_rect

    def Instructions():
        instr_text = Font2.render("Right Click to Start/Left click on an animal to teleport behind your vehicle!", True, "Black")
        instr_rect = instr_text.get_rect(midbottom = (640, 400))
        instr_text2 = Font2.render("Don't left click too far from your vehicle, the teleport is only so strong...", True, "Black")
        instr_rect2 = instr_text.get_rect(midbottom = (670, 500))
        return instr_text, instr_rect, instr_text2, instr_rect2
    
    def Display_Score():
        Score = Saved
        Score_Text = Font1.render(f'Saved: {Score}', False, ("green"))
        Background_Text = pygame.Surface(Score_Text.get_size())
        Background_Text.fill((64,64,64))
        Background_Text.blit(Score_Text,(0,0))
        screen.blit(Background_Text,(500,0))

    def Won():
        Score = Saved
        Win_Text = Font1.render('You Escaped the Car!', False, ("Black"))
        Win_Text2 = Font1.render(f'You Saved: {Score}', False, ("Black"))
        instr_Text_Win = Font2.render('Right Click to play again', False, ("Black"))
        Win_Rect = Win_Text.get_rect(midbottom =(650,300))
        Win_Rect2 = Win_Text.get_rect(midbottom=(820,400))
        instr_Rect_Win = instr_Text_Win.get_rect(midbottom =(650,500))
        return Win_Text, Win_Rect, Win_Text2, Win_Rect2, instr_Text_Win, instr_Rect_Win
    
    def Lost():
        Lost_Text = Font1.render(f'You lost! Try again?', False, ("Black"))
        Lost_Text2 = Font1.render('(Right Click)', False, ("Black"))
        Lost_Rect = Lost_Text.get_rect(midbottom=(650,300))
        Lost_Rect2 = Lost_Text2.get_rect(midbottom=(650,400))
        return Lost_Text, Lost_Rect, Lost_Text2, Lost_Rect2

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.BG_img = pygame.image.load('Graphics/BG1/PNG/City3/City3.png').convert()
        self.BG_img = pygame.transform.scale(self.BG_img, (screen_width, screen_height))
        self.position_x = 0

    def draw(self, screen):
        screen.fill("black")
        screen.blit(self.BG_img, (self.position_x,0))
        screen.blit(self.BG_img, (screen_width+self.position_x,0))
        if self.position_x <= -screen_width:
         self.position_x = 0
         screen.blit(self.BG_img, (screen_width+self.position_x,0))

    def update(self):
        self.position_x -= 4


class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        car_scale = 4

        car1up_img = pygame.image.load('Graphics/Cars/car1/Walk1.png').convert_alpha()
        car1down_img = pygame.image.load('Graphics/Cars/car1/Walk2.png').convert_alpha()
        self.carframes = [car1up_img, car1down_img]
        self.car_index = 0

        self.carframes = [pygame.transform.scale_by(frame, car_scale) for frame in self.carframes]
        self.image = random.choice(self.carframes)
        self.rect = self.image.get_rect(midbottom = (500, 620))

    def animation(self):
        self.car_index += random.uniform(0.01,0.1)
        if self.car_index >= len(self.carframes): 
            self.image = random.choice(self.carframes)
            self.car_index = 0

    def update(self):
        self.animation()

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        car_scale = 4

        car2up_img = pygame.image.load('Graphics/Cars/car2/Walk1.png').convert_alpha()
        car2down_img = pygame.image.load('Graphics/Cars/car2/Walk2.png').convert_alpha()
        self.carframes = [car2up_img, car2down_img]
        self.car_index = 0

        self.carframes = [pygame.transform.scale_by(frame, car_scale) for frame in self.carframes]
        self.image = random.choice(self.carframes)
        self.rect = self.image.get_rect(midbottom = (500, 680))

        self.position_x = self.rect.x # position

    def animation(self):
        self.car_index += random.uniform(0.01,0.1)
        if self.car_index >= len(self.carframes): 
            self.image = random.choice(self.carframes)
            self.car_index = 0
            
    def update(self):
        self.animation()
        self.position_x -= 0.16 # have the car slowly go back
        self.rect.x = int(self.position_x)
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -300:
            global Win
            self.kill()
            Win = True
            return False
        return True

class Animals(pygame.sprite.Sprite):
    def __init__(self, animal_type):
        super().__init__()
        self.type = animal_type
        scale_factor = 2.5
    
        if self.type == 'OrangeCat':
            orangecat_frame1 = pygame.image.load('Graphics/Animals/OrangeCat/Walk1.png').convert_alpha()
            orangecat_frame2 = pygame.image.load('Graphics/Animals/OrangeCat/Walk2.png').convert_alpha()
            orangecat_frame3 = pygame.image.load('Graphics/Animals/OrangeCat/Walk3.png').convert_alpha()
            orangecat_frame4 = pygame.image.load('Graphics/Animals/OrangeCat/Walk1.png').convert_alpha()
            self.frames = [orangecat_frame1, orangecat_frame2, orangecat_frame3, orangecat_frame4]
            y_pos = 580
        elif self.type == 'BlackCat':
            blackcat_frame1 = pygame.image.load('Graphics/Animals/BlackCat/Walk1.png').convert_alpha()
            blackcat_frame2 = pygame.image.load('Graphics/Animals/BlackCat/Walk2.png').convert_alpha()
            blackcat_frame3 = pygame.image.load('Graphics/Animals/BlackCat/Walk3.png').convert_alpha()
            blackcat_frame4 = pygame.image.load('Graphics/Animals/BlackCat/Walk4.png').convert_alpha()
            self.frames = [blackcat_frame1, blackcat_frame2, blackcat_frame3, blackcat_frame4]
            y_pos = 580
        elif self.type == 'Pigeon':
            pigeon_frame1 = pygame.image.load('Graphics/Animals/Pigeon/Walk1.png').convert_alpha()
            pigeon_frame2 = pygame.image.load('Graphics/Animals/Pigeon/Walk2.png').convert_alpha()
            pigeon_frame3 = pygame.image.load('Graphics/Animals/Pigeon/Walk3.png').convert_alpha()
            pigeon_frame4 = pygame.image.load('Graphics/Animals/Pigeon/Walk4.png').convert_alpha()
            self.frames = [pigeon_frame1, pigeon_frame2, pigeon_frame3, pigeon_frame4]
            y_pos = 550
        elif self.type == 'Crow':
            crow_frame1 = pygame.image.load('Graphics/Animals/Crow/Walk1.png').convert_alpha()
            crow_frame2 = pygame.image.load('Graphics/Animals/Crow/Walk2.png').convert_alpha()
            crow_frame3 = pygame.image.load('Graphics/Animals/Crow/Walk3.png').convert_alpha()
            crow_frame4 = pygame.image.load('Graphics/Animals/Crow/Walk4.png').convert_alpha()
            self.frames = [crow_frame1, crow_frame2, crow_frame3, crow_frame4]
            y_pos = 550

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.frames = [pygame.transform.scale_by(frame, scale_factor) for frame in self.frames]

        self.rect = self.image.get_rect(midbottom = (random.randint(1380,1580), y_pos))
    
    def animation_state(self):
            self.animation_index += 0.15
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def Teleport(self):
        self.rect.x -= 600
        Teleport_Sound = pygame.mixer.Sound('Audio/poof.mp3')
        Teleport_Sound.set_volume(0.5)
        Teleport_Sound.play()
    
    def Game_Over(self):
        global game_active, Win
        if pygame.sprite.spritecollide(Player.sprite, Animal_Group, False):
            game_active = False
            Win = False
    
    def destroy(self):
        global Saved
        if self.rect.left <= -100:
            self.kill()
            Saved += 1

    def update(self):
        self.Game_Over()
        self.animation_state()
        self.destroy()
        self.rect.x -= 8
        self.rect.x = int(self.rect.x)


# Fonts
Font1 = pygame.font.Font("Graphics/Font/PixelFont/Font.TTF", 50)
Font2 = pygame.font.Font("Graphics/Font/PixelFont2/Font2.TTF", 30)
# Timers
Obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(Obstacle_timer,1000)

# Instances
background = Background()
Animal_Group = pygame.sprite.Group()
Enemy = pygame.sprite.GroupSingle()
Enemy.add(EnemyCar())
Player = pygame.sprite.GroupSingle()
Player.add(PlayerCar())

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif pygame.mouse.get_pressed()[2]:
            game_active = True
            Win = None
            Saved = 0
            Sound_Played = False

            Animal_Group.empty()
            Enemy.empty()
            Enemy.add(EnemyCar())
            Player.add(PlayerCar())

        if game_active == True:
            if event.type == Obstacle_timer:
                Animal = Animals(random.choice(["OrangeCat", "BlackCat", "Crow", "Pigeon", "Pigeon"]))
                Animal_Group.add(Animal)

            if pygame.mouse.get_pressed()[0]:
             for animal in Animal_Group:
                extended_rect = animal.rect.inflate(50,50)
                if extended_rect.collidepoint((pygame.mouse.get_pos())):
                    animal.Teleport()
                    Animal_Group.update()
                    break # one a successful click has been made

    # Music
    if not game_active and Playing != "Menu":
        pygame.mixer_music.stop()
        pygame.mixer_music.load('Music/Menu.mp3')
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(loops= -1)
        Playing = "Menu"
    elif game_active and Playing != "Game":
        pygame.mixer_music.stop()
        pygame.mixer_music.load('Music/Game2.mp3')
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(loops= -1)
        Playing = "Game"

    # Instances
    if game_active:

        if Enemy.sprite is None:
         game_active = False

        background.draw(screen)
        background.update()
        Animal_Group.update()
        Animal_Group.draw(screen)
        Player.draw(screen)
        Player.update()
        Enemy.draw(screen)
        Enemy.update()
        Text.Display_Score()
    
    elif not game_active:
        Animal_Group.empty()
        Player.empty()
        Enemy.empty()
        screen.fill("yellow")
        Title_Text, Title_Rect = Text.Title()
        screen.blit(Title_Text, Title_Rect)
        instr_Text, instr_Rect, instr_Text2, instr_Rect2 = Text.Instructions()
        screen.blit(instr_Text, instr_Rect)
        screen.blit(instr_Text2, instr_Rect2)

        if Win == False:
            Animal_Group.empty()
            Player.empty()
            Enemy.empty()
            screen.fill("red")
            if not Sound_Played:
                Lose_Sound = pygame.mixer.Sound('Audio/Lose.mp3')
                Lose_Sound.set_volume(0.5)
                Lose_Sound.play()
                Sound_Played = True
            Lost_Text, Lost_Rect, Lost_Text2, Lost_Rect2 = Text.Lost()
            screen.blit(Lost_Text, Lost_Rect)
            screen.blit(Lost_Text2, Lost_Rect2)
            
        elif Win == True:
            Animal_Group.empty()
            Player.empty()
            Enemy.empty()
            screen.fill("green")
            if not Sound_Played:
                Win_Sound = pygame.mixer.Sound('Audio/Win.mp3')
                Win_Sound.set_volume(0.5)
                Win_Sound.play()
                Sound_Played = True
            Win_Text, Win_Rect, Win_Text2, Win_Rect2, instru_Text_Win, instru_Rect_Win = Text.Won()
            screen.blit(Win_Text, Win_Rect)
            screen.blit(Win_Text2, Win_Rect2)
            screen.blit(instru_Text_Win, instru_Rect_Win)

    pygame.display.update()
    clock.tick(60)