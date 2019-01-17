from settings import *
import random
import sys


class Main:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.instance = True
        self.running = True
        # Switch on for  a spawn rate of 1 per frame
        self.infinite = False
    
    def new(self):
        """Call this to create a new instance of the animation"""
        self.screen.fill(WHITE)
        # Beams group
        self.beams = pg.sprite.Group()
        self.run()
    
    def run(self):
        """Main program loop"""
        while self.instance:
            self.clock.tick(FPS)
            self.events()
            self.updates()
            self.draw()

    def events(self):
        """Handles pygame events"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.instance = False
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == SPACE:
                    # Creates a beam
                    self.beams.add(Beam())
                    if self.infinite:
                        self.infinite = False
                elif event.key == ENTER:
                    self.infinite = True
    
    def updates(self):
        """Space for position updating math"""
        if self.infinite:
            # Adds a beam every frame
            self.beams.add(Beam())
        self.beams.update()
    
    def draw(self):
        """Draws everything to screen"""
        self.beams.draw(self.screen)
        pg.display.flip()


class Beam(pg.sprite.Sprite):
    """Beam fly across screen"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BEAM_SIZE, BEAM_SIZE))
        self.image.fill(self.rand_color())
        self.rect = self.image.get_rect()
        self.rect.center = self.rand_pos()
        self.velx, self.vely = self.rand_vector()
    
    def screen_collision(self):
        """Called every update to check boundry collision"""
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.vely = -self.vely
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velx = -self.velx
    
    @staticmethod
    def rand_color():
        """Returns a random RGB color"""
        return (random.randint(15, 250), random.randint(15, 250), random.randint(15, 250))
    
    @staticmethod
    def rand_pos():
        """Returns an (x, y) coordinte within 1/4 boundries"""
        return random.randint(WIDTH // 4, WIDTH // 4 * 3), random.randint(HEIGHT // 4, HEIGHT // 4 * 3)
    
    @staticmethod
    def rand_vector():
        """Returns a tuple of a randomized velocity vector"""
        return (random.uniform(-BEAM_SPEED, BEAM_SPEED), random.uniform(-BEAM_SPEED, BEAM_SPEED))
    
    def update(self):
        """Is called every frame to update position"""
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.screen_collision()


m = Main()
while m.running:
    m.new()
pg.quit()
