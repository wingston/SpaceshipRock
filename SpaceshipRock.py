# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    global score
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def update(self):
        foward = angle_to_vector(self.angle)
        if self.thrust:
            self.image_center = [135, 45]
            #ship_thrust_sound.rewind()
            ship_thrust_sound.play()
            self.vel[0] += foward[0]*(1+score/100)/2
            self.vel[1] += foward[1]*(1+score/100)/2
        else:
            self.image_center = [45, 45]
            ship_thrust_sound.pause()
            self.vel[0] *=.99
            self.vel[1] *=.99
            
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0]%WIDTH
        self.pos[1] = self.pos[1]%HEIGHT
    def shoot(self):
        global missile_group
        a_missile = Sprite(self.pos,[self.vel[0]+angle_to_vector(self.angle)[0]*6,self.vel[1]+angle_to_vector(self.angle)[1]*6], self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        # Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def get_position(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def draw(self, canvas):
        if self.animated:
            
            global time
            explosion_index = time % 25
            explosion_sound.rewind()
            explosion_sound.play()
            canvas.draw_image(explosion_image, 
                    [explosion_info.get_center()[0] + explosion_index * explosion_info.get_size()[0], 
                     explosion_info.get_center()[1]], 
                     explosion_info.get_size(), self.pos, explosion_info.get_size())
            time += 1
            
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    
    def collide(self, other_objects):
        distance = math.sqrt((self.get_position()[0]-other_objects.get_position()[0])**2+(self.get_position()[1]-other_objects.get_position()[1])**2)
        if distance<=self.get_radius()+other_objects.get_radius():
            return True
        else:
            return False
        
    def update(self):
        self.angle += self.angle_vel        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0]%WIDTH
        self.pos[1] = self.pos[1]%HEIGHT
        self.age += 1
        if self.age <= self.lifespan:
            return False
        else:
            return True
def keydown(key):
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = .05
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = -.05
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP["space"]:
         my_ship.shoot()   
     
        
def keyup(key):
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
    
def group_collide(group,other_object):
    group_copy = set(group)
    for sprite in group_copy:
        if sprite.collide(other_object):
            an_explosion = Sprite(sprite.get_position(),[0,0] , 0, 0, explosion_image, explosion_info,explosion_sound)
            explosion_group.add(an_explosion)
            
            group.remove(sprite)
            return True
    return False
def group_group_collide(group1, group2):
    global score
    group1_copy = set(group1)
    for sprite in group1_copy:
        if group_collide(group2,sprite):
            group1.discard(sprite)
            score += 5
            
def draw(canvas):
    global time, started, rock_group, lives, score, my_ship
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if group_collide(rock_group,my_ship):
        lives -= 1
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas,missile_group)
    process_sprite_group(canvas,explosion_group)
    canvas.draw_text("Score: "+str(score),[600,50],30,"White")
    canvas.draw_text("Lives: "+str(lives),[20,50],30,"White")
    canvas.draw_text("Press space to shoot",[20,80],20,"White")
    canvas.draw_text("Press left or right arrow to spin",[20,110],20,"White")
    canvas.draw_text("Press up arrow to move forward",[20,140],20,"White")
    # draw ship and sprites
    my_ship.draw(canvas)
 
    # update ship and sprites
    my_ship.update()
    group_group_collide(rock_group,missile_group)
    if lives == 0:
        started = False
        rock_group = set([])
        lives = 3
        score = 0
        
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size()) 
        
        soundtrack.rewind()
        soundtrack.play()
# timer handler that spawns a rock  
def process_sprite_group(canvas, group):
    group_copy = set(group)
    for single in group_copy:
        single.draw(canvas)
        single.update()
        if single.update():
            group.remove(single)
def rock_spawner():
    global rock_group, started
    if started and len(rock_group)<=12:
        
        a_rock = Sprite([WIDTH * random.random(), HEIGHT * random.random()], [random.random()*.6-.3, random.random()*.6-.3], 0, random.random()*0.2-0.1, asteroid_image, asteroid_info)
        if dist(a_rock.get_position(),my_ship.get_position())>a_rock.get_radius()+my_ship.get_radius():
            rock_group.add(a_rock)

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    print started
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
time = 0
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()