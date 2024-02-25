import pygame
import pygwidgets
from pygame.locals import *
import math
import random
import itertools
from settings import *


POKER_GREEN = '#00512c'
DISABLED = '#002816'
ranks = 'A234567898TJQK'
suits = 'SDHC'
deck = [str(rank) + str(suit) for rank, suit in itertools.product(ranks, suits)]
random.shuffle(deck)

pygame.init()
screen = pygame.display.set_mode([1000, 680])
class Card:
    def __init__(self, name):
        self.surf = pygame.Surface((120, 174))
        self.rect = self.surf.get_rect()
        self.rect.x = 120
        self.rect.y = 480
        self.name = name
        self.rank = name[0]
        self.surf.fill(POKER_GREEN)
        self.back_img = pygame.image.load('../assets/red_back.png').convert()
        self.front_img = pygame.image.load(f'../assets/cardsjpg2/{self.name}.jpg').convert()
        self.current_side = self.front_img
        self.flipping = False
        self.angle = 0
        self.surf.blit(self.current_side, (0,0))
        if self.rank =='A':
            self.value = 1
        elif self.rank.isdigit():
            self.value = int(self.rank)
        else:
            self.value = 10
    def update(self):
        if self.flipping:
            self.angle += 25
            if self.angle > 180:
                self.angle = 180
            if self.angle <90:
                self.current_side = self.back_img
            else:
                self.current_side = self.front_img
            self.surf.fill(POKER_GREEN)
            width = abs(int(math.cos(math.pi * self.angle/180) * 120))
            self.current_img = pygame.transform.scale(self.current_side, (width, 174))
            self.surf.blit(self.current_img, (int(60- width/2),0))
            if self.angle == 180:
                self.angle = 0
                self.flipping = False
            print(width)
        else:
            self.surf.blit(self.current_side, (0,0))
    def flip(self):
        self.flipping = True

class card_space():
    def __init__(self, position):
        self.surf = pygame.Surface((120, 174))
        self.surf.fill(POKER_GREEN)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = position
dealer_spaces = []
player_spaces = []
for i in range(7):
    dealer_spaces.append(card_space((20 + i* 140, 30)))
    player_spaces.append(card_space((20 + i * 140, 480)))
all_spaces = dealer_spaces + player_spaces
dealer_spaces.extend(player_spaces)

player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0

def dealer_flip(self=None):
    dealer_hand[0].flip()


btn_hit = pygwidgets.TextButton(screen, (20, 240), 'Hit',
                                upColor= POKER_GREEN,
                                overColor='green',
                                textColor = 'white',
                                fontSize= 28)
btn_stand = pygwidgets.TextButton(screen, (20, 285), 'Stand',
                                upColor= POKER_GREEN,
                                overColor='green',
                                textColor = 'white',
                                fontSize= 28)
btn_new = pygwidgets.TextButton(screen, (20, 330), 'New deal',
                                upColor= POKER_GREEN,
                                downColor=DISABLED,
                                textColor = 'white',
                                overColor='green',
                                fontSize= 28)
dealer_text = pygwidgets.DisplayText(screen, (300, 240),
                                     textColor='white',
                                     fontName='helvetica',
                                     fontSize=32)
player_text = pygwidgets.DisplayText(screen, (300, 415),
                                     textColor='white',
                                     fontName='helvetica',
                                     fontSize=32)
winner_text = pygwidgets.DisplayText(screen, (300, 328),
                                     textColor='white',
                                     fontName='helvetica',
                                     fontSize=32)

def deal():
    player_hand.append(Card(deck.pop()))
    player_hand.append(Card(deck.pop()))
    dealer_hand.append(Card(deck.pop()))
    dealer_hand.append(Card(deck.pop()))
    dealer_hand[0].current_side = dealer_hand[0].back_img
    dealer_hand[0].surf.blit(dealer_hand[0].current_side, (0, 0))
    global player_score
    player_score = score_hand(player_hand)
    player_text.setValue(f'Player has {player_score}')
    if player_score == 21:
        btn_hit.disable()

def hit():
    player_hand.append(Card(deck.pop()))
    global player_score
    player_score = score_hand(player_hand)
    if player_score > 22:
        player_text.setValue(f'Player busts with {player_score}')
        winner_text.setValue(("Dealer wins"))
        btn_hit.disable()
        btn_stand.disable()
        dealer_hand[0].flip()
    else:
        player_text.setValue(f'Player has {player_score}')
    if player_score == 21:
        btn_hit.disable()

def score_hand(hand):
    score = sum([card.value for card in hand])
    if 'A' in [card.rank for card in hand] and score <12:
        score += 10
    return score
def stand():
    btn_hit.disable()
    btn_stand.disable()
    dealer_hand[0].flip()
    dealer_score = score_hand(dealer_hand)
    print(f'dealer: {dealer_score}')
    while dealer_score < 17:
        dealer_hand.append(Card(deck.pop()))
        dealer_score = score_hand(dealer_hand)
    if dealer_score < 22:
        dealer_text.setValue(f'Dealer stands with {dealer_score}')
    else:
        dealer_text.setValue(f'Dealer busts with {dealer_score}')
    if dealer_score <22 and dealer_score >= player_score:
        winner_text.setValue(f"Dealer wins")
    else:
        winner_text.setValue("Player wins")
def new_deal():
    player_hand.clear()
    dealer_hand.clear()
    btn_hit.enable()
    btn_stand.enable()
    player_text.setValue("")
    dealer_text.setValue("")
    winner_text.setValue("")
    global player_score
    global dealer_score
    player_score = 0
    dealer_score = 0
    for space in all_spaces:
        space.surf.fill(POKER_GREEN)
    deal()


running = True
clock = pygame.time.Clock()
deal()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                dealer_hand[0].flip()
            if event.key == K_DOWN:
                card2.flip()

        if btn_stand.handleEvent(event):
            stand()
        if btn_hit.handleEvent(event):
            hit()
        if btn_new.handleEvent(event):
            new_deal()
    screen.fill(POKER_GREEN)


    for space in all_spaces:
        screen.blit(space.surf, space.rect)
    for index, card in enumerate(player_hand):
        player_spaces[index + 2].surf.blit(card.surf, (0,0))
    for index, card in enumerate(dealer_hand):
        dealer_spaces[index + 2].surf.blit(card.surf, (0,0))


    dealer_hand[0].update()
    btn_hit.draw()
    btn_stand.draw()
    btn_new.draw()
    dealer_text.draw()
    player_text.draw()
    winner_text.draw()
    #card2.update()
    pygame.display.flip()
    clock.tick(30)