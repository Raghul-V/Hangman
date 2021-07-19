import pygame
import sys
import random
from words import words


SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

LETTER_KEYS = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z"
}



class Button:
    radius = 12.5

    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y

    def is_hovered(self):
        cursor_x, cursor_y = pygame.mouse.get_pos()
        return (self.x - self.radius <= cursor_x <= self.x + self.radius and
            self.y - self.radius <= cursor_y <= self.y + self.radius)

    def display(self, surface):
        # Border
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius, width=3)
        # Letter
        letter = render_text(self.letter, int(self.radius * 1.5), BLACK)
        surface.blit(letter, letter.get_rect(center=(self.x, self.y)))



def render_text(text, font_size, font_color):
    font = pygame.font.SysFont("Courier", font_size, bold=True)
    rendered_text = font.render(text, True, font_color)
    return rendered_text


def display_text(surface, text, y, font_size):
    rendered_text = render_text(text, font_size, BLACK)
    x = (SCREEN_WIDTH - rendered_text.get_width()) / 2
    surface.blit(rendered_text, (x, y))


def hide_word(word):
    hidden = ""
    for i in word:
        hidden += i if i.isspace() else "_"
    return hidden


def reveal_letter(word, hidden, letter):
    new_hidden = ""
    for i in range(len(word)):
        if word[i].lower() == letter:
            new_hidden += word[i]
        else:
            new_hidden += hidden[i]
    return new_hidden


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")

hangman_logo = pygame.image.load("images/hangman-logo.png").convert_alpha()
game_over_logo = pygame.image.load("images/gameover.png").convert_alpha()
awesome_logo = pygame.image.load("images/awesome.png").convert_alpha()

word = random.choice(words)

wrong_guess = 0
hangman_images = [pygame.image.load(f"images/hangman-{i}.png").convert_alpha() for i in range(7)]
hangman_image = hangman_images[0]

hidden = hide_word(word)
guesses = set()

buttons = [Button(l, 45 + i*30, 500) for i, l in enumerate("ABCDEFGHIJKLM")] + [Button(l, 45 + i*30, 535) for i, l in enumerate("NOPQRSTUVWXYZ")]


while True:
    screen.fill(GREY)

    if hidden == word or wrong_guess == 6:
        pygame.time.wait(500)
        if hidden == word:
            screen.blit(awesome_logo, (50, 40))
            y1, y2 = 380, 430
        else:
            screen.blit(game_over_logo, (60, 55))
            y1, y2 = 340, 390
        display_text(screen, "The word was", y1, 42)
        display_text(screen, f"'{word}'", y2, 40)
        pygame.display.update()
        pygame.time.wait(2000)
        
        wrong_guess = 0
        hangman_image = hangman_images[0]
        word = random.choice(words)
        hidden = hide_word(word)
        guesses = set()
        continue

    guess = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in LETTER_KEYS:
                if guess != "":
                    continue
                guess = LETTER_KEYS[event.key]
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_hovered():
                    guess = button.letter.lower()
                    break

    if guess != "" and guess not in guesses:
        guesses.add(guess)
        if guess in word.lower():
            hidden = reveal_letter(word, hidden, guess)
        else:
            wrong_guess += 1
            if wrong_guess > 6:
                wrong_guess = 6
            hangman_image = hangman_images[wrong_guess]

    screen.blit(hangman_logo, (90, 50))
    screen.blit(hangman_image, (140, 160))
    spaced = " ".join(list(hidden))
    display_text(screen, spaced, 420, 35)

    for button in buttons:
        if button.letter.lower() in guesses:
            continue
        button.display(screen)

    pygame.display.update()


pygame.quit()


