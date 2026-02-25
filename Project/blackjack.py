## IMPORTS

import copy
import random
import pygame

pygame.init()                           #nodig voor font

# VARIABLES

cards = ['2','3','4', '5', '6', '7', '8', '9', '10','J','Q','K','A']
one_deck = 4*cards
decks = 4

WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Blackjack!")
fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font("FreeSansBold.ttf",44)
font_small = pygame.font.Font("FreeSansBold.ttf",32)

active = False
#win loss push(draw)
records = [0,0,0]
player_score = 0
dealer_score = 0 

# FUNCTIONS

# deal cards by selecting randomnly from deck
def deal_cards(current_hand, current_deck):
    card = random.randint(0,len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    # print(current_hand,current_deck)
    return current_hand, current_deck
# conditions en buttons voor draw game
def draw_game(act, records):
    button_list = []
    # initially on startup (not act). You can only deal
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150,20,300,100], 0, 5)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, 'green', [150,20,300,100], 3, 5)             # grotere rechthoek > border in groen 
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165,50))
        button_list.append(deal)

    # Game started = hit & stand tonen + win/loss-record
    else:
        hit = pygame.draw.rect(screen, 'white', [0,700,300,100], 0, 5)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, 'green', [0,700,300,100], 3, 5)             # grotere rechthoek > border in groen 
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (60,725))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300,700,300,100], 0, 5)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, 'green', [300,700,300,100], 3, 5)             # grotere rechthoek > border in groen 
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (360,725))
        button_list.append(stand)

        score_text = font_small.render(f'Wins: {records[0]}   Losses: {records[1]}    Draws: {records[2]}', True, 'white')
        screen.blit(score_text,(15,840))

    return button_list


# MAIN GAME LOOP 

run = True
while run:
    # run the game at fps & fill screen with bg-color
    timer.tick(fps)
    screen.fill('black')
    #initial deal
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    #once game is activated & dealt > calculate scores & display cards
    buttons = draw_game(active, records)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               #quit = stop programma
            run = False

        if event.type ==pygame.MOUSEBUTTONUP:               #start game bij klik op Deal
            if not active:
                if buttons[0].collidepoint(event.pos):
                    # set variables
                    active = True
                    initial_deal = True                     # two cards
                    game_deck = copy.deepcopy(decks*one_deck)       # making an original deck. 
                    my_hand = []
                    dealer_hand = []
                    outcome = 0

    pygame.display.flip()       


pygame.quit()

    