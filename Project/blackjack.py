## IMPORTS

import copy
import random
import pygame

pygame.init()                           #nodig voor font

# VARIABLES

cards = ['2','3','4', '5', '6', '7', '8', '9', '10','J','Q','K','A']
one_deck = 4*cards
decks = 4

# screen
WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Blackjack!")
fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font("Project/FreeSansBold.ttf",44)
font_small = pygame.font.Font("Project/FreeSansBold.ttf",32)

# setting deck & hands
game_deck = copy.deepcopy(decks*one_deck)
initial_deal = True
my_hand=[]
dealer_hand=[]
active = False
reveal_dealer = False 
hand_active = False
outcome = 0 
add_score = False
results = ['','player busted','You win', 'You lose', 'Draw']

# win loss push(draw)
records = [0,0,0]
player_score = 0
dealer_score = 0 

# images
jack_img = pygame.image.load("Project/Images/Jack.png")
queen_img = pygame.image.load("Project/Images/Queen.png")
king_img = pygame.image.load("Project/Images/King.png")
card_x = 70
card_player_y = 460
card_dealer_y = 160

# FUNCTIONS

# deal cards by selecting randomnly from deck
def deal_cards(current_hand, current_deck):
    card = random.randint(0,len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    # print(current_hand,current_deck)
    return current_hand, current_deck

def draw_scores(player,dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350,400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'),(350,100)) 

def draw_figure_card(card, i,  x, y):
    #als J/Q/K > afbeelding
    if card == 'J':
        screen.blit(jack_img, ((x + 5 +70*i, y + 10 +5*i)))
    elif card == 'Q':
        screen.blit(queen_img, ((x + 5 + 70*i, y+ 10 + 5*i)))
    elif card == 'K':
        screen.blit(king_img, ((x + 5 + 70*i, y+ 10 +5*i)))

# draw cards visueel op scherm
def draw_cards(player, dealer, reveal):
    
    for i in range(len(player)):
        pygame.draw.rect(screen,'white', [card_x +(70*i), card_player_y + (5*i), 120,220], 0, 5 )
        screen.blit(font.render(player[i], True, 'black'), (card_x + 10 +70*i, card_player_y + 5 +5*i))
        screen.blit(font.render(player[i], True, 'black'), (card_x + 10 +70*i, card_player_y +115 +5*i))
        pygame.draw.rect(screen,'red', [card_x +(70*i), 460 + (5*i),120,220], 5, 5 )
        #teken figuur op kaart
        draw_figure_card(player[i], i, card_x, card_player_y)
    
    # if player hasn't finished turn, dealer will hide one card.
    for i in range(len(dealer)):
        pygame.draw.rect(screen,'white', [card_x +(70*i), card_dealer_y + (5*i), 120,220], 0, 5 )
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (card_x + 10 +70*i, card_dealer_y + 5 +5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (card_x + 10 +70*i, card_dealer_y + 115 +5*i))
            draw_figure_card(dealer[i], i, card_x, card_dealer_y)
            
        else:
            screen.blit(font.render('???', True, 'black'), (card_x + 10 +70*i, card_dealer_y + 5 +5*i))
            screen.blit(font.render('???', True, 'black'), (card_x + 10 +70*i, card_dealer_y + 115 +5*i))
        
        pygame.draw.rect(screen,'blue', [70 +(70*i), 160 + (5*i),120,220], 5, 5 )

#get best score possible
def calculate_score(hand):
    #calculate hand score fresh every time. check Aces
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        if hand[i] in ['10','J', 'Q', 'K']:
            hand_score += 10
        elif hand[i] == 'A':
            hand_score += 11
    
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score-=10
    
    return hand_score


# conditions en buttons voor draw game
def draw_game(act, records, result):
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

    # restart when done playing
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15,25))
        deal = pygame.draw.rect(screen, 'white', [150,220,300,100], 0, 5)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, 'green', [150,220,300,100], 3, 5)  
        pygame.draw.rect(screen, 'black', [154,224,294,94], 3, 5)           # grotere rechthoek > border in groen 
        deal_text = font.render('DEAL AGAIN', True, 'black')
        screen.blit(deal_text, (165,250))
        button_list.append(deal)

    return button_list

def check_endgame(hand_act,deal_score,play_score,result,totals, add):
    # 1: busted 2: win 3: lose 4: draw
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <=21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

        

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
    if active:
        player_score = calculate_score(my_hand)
        if reveal_dealer == True:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               #quit = stop programma
            run = False

        if event.type == pygame.MOUSEBUTTONUP:               #start game bij klik op Deal
            if not active:
                if buttons[0].collidepoint(event.pos):
                    # set variables
                    active = True
                    initial_deal = True                     # two cards
                    game_deck = copy.deepcopy(decks*one_deck)       # making an original deck. 
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
            else:
                #you can hit
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                #you can stand
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        # set variables
                        active = True
                        initial_deal = True                     # two cards
                        game_deck = copy.deepcopy(decks*one_deck)       # making an original deck. 
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        add_score = True
                        reveal_dealer = False
                        dealer_score = 0
                        player_score = 0

    #check ending
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score,outcome, records, add_score)

            


    pygame.display.flip()       


pygame.quit()

    