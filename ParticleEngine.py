import pygame
import sys
import random
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Engine")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color, velocity, size, lifetime):
        self.x = x
        self.y = y
        self.size = size
        self.velocity = velocity
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.lifetime = lifetime
        self.alpha = 255
        self.color = color

    def update(self,g):
        self.x += self.vx
        self.y += self.vy
        if g:
            self.vy += 0.1

        self.lifetime -= 1
        self.alpha -= 255 / 60

    #lifetime 체크
    def is_alive(self): 
        return self.alpha > 0 and self.lifetime > 0

    def draw(self):
        current_color = self.get_color_over_life()
        pygame.draw.circle(screen, (current_color[0], current_color[1], current_color[2], int(self.alpha)),
                           (int(self.x), int(self.y)), int(self.size))

    # startcolor <-> endcolor
    def get_color_over_life(self):
        start_color = (255, 255, 255)
        end_color = self.color
        t = min(1, self.lifetime / 60)
        r = int((1 - t) * end_color[0] + t * start_color[0])
        g = int((1 - t) * end_color[1] + t * start_color[1])
        b = int((1 - t) * end_color[2] + t * start_color[2])
        return r, g, b

def create_particle(_color, _velocity, _size, _lifetime):
    vx,vy = (random.uniform(-1, 1) * _velocity , random.uniform(-1, 1)* _velocity) 
    color = _color
    size = random.uniform(3, 15) * _size
    lifetime = random.randint(30, 60) * _lifetime
    return Particle(*pygame.mouse.get_pos(), color, (vx,vy,), size, lifetime)

def main():
    particles = []
    velocity = 1
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    size = 1
    lifetime = 1
    spawnrate = 1
    gravity = False

    change_color_button_rect = pygame.Rect(600, 40, 100, 25)
    changegravity_button_rect = pygame.Rect(600, 80, 100, 25)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Increase 버튼 클릭
                if 400 < event.pos[0] < 430 and 40 < event.pos[1] < 60:
                    velocity = min(velocity + 0.1, 5.0)
                # Decrease 버튼 클릭
                elif 400 < event.pos[0] < 430 and 70 < event.pos[1] < 90:
                    velocity = max(velocity - 0.1, 0.0)
                # Size Increase 버튼 클릭
                elif 470 < event.pos[0] < 500 and 40 < event.pos[1] < 60:
                    size = min(size + 0.1, 5.0)
                # Size Decrease 버튼 클릭
                elif 470 < event.pos[0] < 500 and 70 < event.pos[1] < 90:
                    size = max(size - 0.1, 0.1)
                # Lifetime Increase 버튼 클릭
                elif 540 < event.pos[0] < 570 and 40 < event.pos[1] < 60:
                    lifetime = min(lifetime + 0.1, 3)
                # Lifetime Decrease 버튼 클릭
                elif 540 < event.pos[0] < 570 and 70 < event.pos[1] < 90:
                    lifetime = max(lifetime - 0.1, 0.1)
                # rate Increase 버튼 클릭
                elif 330 < event.pos[0] < 360 and 40 < event.pos[1] < 60:
                    spawnrate = min(spawnrate + 1, 10)
                # rate Decrease 버튼 클릭
                elif 330 < event.pos[0] < 360 and 70 < event.pos[1] < 90:
                    spawnrate = max(spawnrate - 1, 1)

                elif change_color_button_rect.collidepoint(event.pos):
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif changegravity_button_rect.collidepoint(event.pos):
                    if gravity:
                        gravity = False
                    else:
                        gravity = True

        screen.fill(BLACK)

        for particle in particles:
            particle.update(gravity)

        if pygame.mouse.get_pressed()[0]:
            particles.append(create_particle(color, velocity, size, lifetime))
            for i in range(spawnrate-1):
                particles.append(create_particle(color, velocity, size, lifetime))

        particles = [particle for particle in particles if particle.is_alive()]
        for particle in particles:
            particle.draw()

        # UI
        pygame.draw.rect(screen, WHITE, (10, 10, 250, 120))
        font = pygame.font.Font(None, 20)

        TitleFont = pygame.font.SysFont( "inkfree", 32, True, False)
        Title_text = TitleFont.render("Particle Engine", True, WHITE)
        screen.blit(Title_text, (730, 45))
        
        
        particle_text = font.render(f"Speed: {velocity:.1f}", True, BLACK)
        screen.blit(particle_text, (20, 45))
        particle_text = font.render(f"Size: {size:.1f}", True, BLACK)
        screen.blit(particle_text, (20, 60))
        particle_info_text = font.render(f"Color: {color}", True, BLACK)
        screen.blit(particle_info_text, (20, 75))
        particle_info_text = font.render(f"Lifetime: {lifetime:.1f}", True, BLACK)
        screen.blit(particle_info_text, (20, 90))
        particle_info_text = font.render(f"SpawnRate: {spawnrate:.1f}", True, BLACK)
        screen.blit(particle_info_text, (20, 105))

        particle_text = font.render("Rate", True, WHITE)
        screen.blit(particle_text, (330, 100))
        particle_text = font.render("Speed", True, WHITE)
        screen.blit(particle_text, (395, 100))
        particle_text = font.render("Size", True, WHITE)
        screen.blit(particle_text, (470, 100))
        particle_text = font.render("Lifetime", True, WHITE)
        screen.blit(particle_text, (535, 100))

        # Increase, Decrease 버튼 
        pygame.draw.rect(screen, WHITE, (330, 40, 30, 20))
        increase_button_text = font.render("+", True, BLACK)
        screen.blit(increase_button_text, (335, 40))
        pygame.draw.rect(screen, WHITE, (330, 70, 30, 20))
        decrease_button_text = font.render("-", True, BLACK)
        screen.blit(decrease_button_text, (335, 70))
        
        # Increase, Decrease 버튼 
        pygame.draw.rect(screen, WHITE, (400, 40, 30, 20))
        increase_button_text = font.render("+", True, BLACK)
        screen.blit(increase_button_text, (405, 40))
        pygame.draw.rect(screen, WHITE, (400, 70, 30, 20))
        decrease_button_text = font.render("-", True, BLACK)
        screen.blit(decrease_button_text, (405, 70))

        # Size Increase, Decrease 버튼 
        pygame.draw.rect(screen, WHITE, (470, 40, 30, 20))
        size_increase_button_text = font.render("+", True, BLACK)
        screen.blit(size_increase_button_text, (475, 40))
        pygame.draw.rect(screen, WHITE, (470, 70, 30, 20))
        size_decrease_button_text = font.render("-", True, BLACK)
        screen.blit(size_decrease_button_text, (475, 70))

        # Lifetime Increase, Decrease 버튼 
        pygame.draw.rect(screen, WHITE, (540, 40, 30, 20))
        lifetime_increase_button_text = font.render("+", True, BLACK)
        screen.blit(lifetime_increase_button_text, (545, 40))
        pygame.draw.rect(screen, WHITE, (540, 70, 30, 20))
        lifetime_decrease_button_text = font.render("-", True, BLACK)
        screen.blit(lifetime_decrease_button_text, (545, 70))

        # Color Change 버튼 
        pygame.draw.rect(screen, WHITE, change_color_button_rect)
        color_change_button_text = font.render("Change Color", True, BLACK)
        screen.blit(color_change_button_text, (605, 45))

        pygame.draw.rect(screen, WHITE, changegravity_button_rect)
        color_change_button_text = font.render("Gravity?", True, BLACK)
        screen.blit(color_change_button_text, (625, 85))



        info_text = font.render(f"Particles: {len(particles)}", True, BLACK)
        screen.blit(info_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
