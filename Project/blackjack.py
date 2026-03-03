## IMPORTS

import copy
import random
import pygame

pygame.init()                           #nodig voor font

'''credits
    Sound Effects by freesound_community from Pixabay
    Afbeeldingenn van OpenClipart-Vectors via Pixabay
    Font met symbool kaart: © Hoyle 2004. All Rights Reserved // Created by Conexion // http://conexion.deviantart.com/ 
        e = diamond, q = spade, r = heart, w = club
'''


# VARIABLES

# e = diamond, q = spade, r = heart, w = club (dit komt door het lettertype)
one_deck = [
    ['2','r'], ['3','r'], ['4','r'], ['5','r'], ['6','r'], ['7','r'], ['8','r'], ['9','r'], ['10','r'], ['J','r'], ['Q','r'], ['K','r'], ['A','r'],
    ['2','q'], ['3','q'], ['4','q'], ['5','q'], ['6','q'], ['7','q'], ['8','q'], ['9','q'], ['10','q'], ['J','q'], ['Q','q'], ['K','q'], ['A','q'],
    ['2','w'], ['3','w'], ['4','w'], ['5','w'], ['6','w'], ['7','w'], ['8','w'], ['9','w'], ['10','w'], ['J','w'], ['Q','w'], ['K','w'], ['A','w'],
    ['2','e'], ['3','e'], ['4','e'], ['5','e'], ['6','e'], ['7','e'], ['8','e'], ['9','e'], ['10','e'], ['J','e'], ['Q','e'], ['K','e'], ['A','e']
]


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
font_symbol = pygame.font.Font("Project/HoylePlayingCards.ttf",70)

color_black = "#1E1A1A"
color_red = '#702D2D'
color_white ="#C1AFAF"
color_grey = "#726F6F"
color_green = "#2B5B26"

success_sound = 'Project/Media/success.mp3'
hitme_sound = 'Project/Media/hitme.mp3'

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
results = ['','You are busted','You win', 'You lose', 'Draw']

# win loss push(draw)
records = [0,0,0]
player_score = 0
dealer_score = 0 

# Media
jack_img = pygame.image.load("Project/Media/Jack.png")
queen_img = pygame.image.load("Project/Media/Queen.png")
king_img = pygame.image.load("Project/Media/King.png")
card_x = 70
card_player_y = 1000
card_dealer_y = 1000
card_speed = 0.3
deal = True



# FUNCTIONS
def reset_game():
    global game_deck, initial_deal, my_hand, dealer_hand, active, reveal_dealer, hand_active, outcome, add_score, results, dealer_score, player_score, card_player_y, card_dealer_y
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
    # reset cards naar outside 
    card_player_y = 1000
    card_dealer_y = 1000

# deal cards by selecting randomnly from deck
def deal_cards(current_hand, current_deck):
    
    card = random.randint(0,len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    # print(current_hand,current_deck)
    return current_hand, current_deck

def draw_scores(player,dealer):
    screen.blit(font.render(f'Score[{player}]', True, color_white), (350,400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, color_white),(350,100)) 

def draw_figure_card(card, i,  x, y):
    #als J/Q/K > afbeelding
    if card[0] == 'J':
        screen.blit(jack_img, ((x + 5 +70*i, y + 10 +5*i)))
    elif card[0] == 'Q':
        screen.blit(queen_img, ((x + 5 + 70*i, y+ 10 + 5*i)))
    elif card[0] == 'K':
        screen.blit(king_img, ((x + 5 + 70*i, y+ 10 +5*i)))

def move_cards():
    global card_player_y, card_dealer_y
    target_player_y = 460
    target_dealer_y = 160
    

    if card_player_y > target_player_y:
       card_player_y += card_speed * -54
    if card_dealer_y > target_dealer_y:
        card_dealer_y += card_speed * -84


    

# draw cards visueel op scherm
def draw_cards(player, dealer, reveal):
    
    for i in range(len(player)):
        pygame.draw.rect(screen,color_white, [card_x +(70*i), card_player_y + (5*i), 120,220], 0, 5 )
        if player[i][1] in ['e','r']:
            screen.blit(font.render(player[i][0], True, color_red), (card_x + 10 +70*i, card_player_y + 5 +5*i))
            screen.blit(font_symbol.render(player[i][1], True, color_red), (card_x + 10 +70*i, card_player_y + 145 +5*i))
        else:
            screen.blit(font.render(player[i][0], True, color_black), (card_x + 10 +70*i, card_player_y + 5 +5*i))
            screen.blit(font_symbol.render(player[i][1], True, color_black), (card_x + 10 +70*i, card_player_y + 145 +5*i))
        pygame.draw.rect(screen, color_black, [card_x +(70*i), card_player_y + (5*i),120,220], 5, 5 )
        #teken figuur op kaart
        draw_figure_card(player[i], i, card_x, card_player_y)
    
    # if player hasn't finished turn, dealer will hide one card.
    for i in range(len(dealer)):
        pygame.draw.rect(screen,color_white, [card_x +(70*i), card_dealer_y + (5*i), 120,220], 0, 5 )
        if i != 0 or reveal:
            if dealer[i][1] in ['e','r']:
                screen.blit(font.render(dealer[i][0], True, color_red), (card_x + 10 +70*i, card_dealer_y + 5 +5*i))
                screen.blit(font_symbol.render(dealer[i][1], True, color_red), (card_x + 10 +70*i, card_dealer_y + 145 +5*i))
            else:
                screen.blit(font.render(dealer[i][0], True, color_black), (card_x + 10 +70*i, card_dealer_y + 5 +5*i))
                screen.blit(font_symbol.render(dealer[i][1], True, color_black), (card_x + 10 +70*i, card_dealer_y + 145 +5*i))

            draw_figure_card(dealer[i], i, card_x, card_dealer_y)
            
        else:
            screen.blit(font.render('???', True, color_black), (card_x + 10 +70*i, card_dealer_y + 5 +5*i))
            screen.blit(font.render('???', True, color_black), (card_x + 10 +70*i, card_dealer_y + 150 +5*i))
        
        pygame.draw.rect(screen,color_black, [70 +(70*i), card_dealer_y + (5*i),120,220], 5, 5 )
        

#get best score possible
def calculate_score(hand):
    #calculate hand score fresh every time. check Aces
    hand_score = 0
    aces_count = hand[0].count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i][0] == one_deck[j][0]:        # zoek enkel in de waardes.
                hand_score += int(hand[i][0])
        if hand[i][0] in ['10','J', 'Q', 'K']:
            hand_score += 10
        elif hand[i][0] == 'A':
            hand_score += 11
    
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score-=10
    
    return hand_score


# conditions en buttons voor draw game
def draw_game(act, records, result, hand_act):
    button_list = []
    # initially on startup (not act). You can only deal
    if not act:
        deal = pygame.draw.rect(screen, color_white, [150,20,300,100], 0, 25)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, color_black, [150,20,300,100], 8, 25)             # grotere rechthoek > border in groen 
        deal_text = font.render('DEAL HAND', True, color_black)
        screen.blit(deal_text, (170,45))
        button_list.append(deal)

    # Game started = hit & stand tonen + win/loss-record
    else:
        if hand_act:
            hit_text = font.render('HIT ME', True, color_black)
            stand_text = font.render('STAND', True, color_black)
        else:
            hit_text = font.render('HIT ME', True, color_grey)
            stand_text = font.render('STAND', True, color_grey)

        hit = pygame.draw.rect(screen, color_white, [25,700,250,100], 0, 25)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, color_black, [25,700,250,100], 3, 25)             # grotere rechthoek > border in groen 
        screen.blit(hit_text, (65,720))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, color_white, [325,700,250,100], 0, 25)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, color_black, [325,700,250,100], 3, 25)             # grotere rechthoek > border in groen 
        screen.blit(stand_text, (375,720))
        button_list.append(stand)
        
        score_text = font_small.render(f'Wins: {records[0]}   Losses: {records[1]}    Draws: {records[2]}', True, color_white)
        screen.blit(score_text,(15,840))

    # restart when done playing
    if result != 0:
        #tekst als je wint
        if result== 1:
            pygame.draw.rect(screen, color_white, [5,15,350,85], 0, 5)
            pygame.draw.rect(screen, color_red, [5,15,350,85], 8, 5)
            screen.blit(font.render(results[result], True, color_red), (20,25))
        elif result == 2:
            pygame.draw.rect(screen, color_white, [5,15,200,85], 0, 5)
            pygame.draw.rect(screen, color_green, [5,15,200,85], 8, 5)
            screen.blit(font.render(results[result], True, color_green), (20,25))
        elif result == 3:
            pygame.draw.rect(screen, color_white, [5,15,230,85], 0, 5)
            pygame.draw.rect(screen, color_red, [5,15,230,85], 8, 5)
            screen.blit(font.render(results[result], True, color_red), (20,25))
        elif result == 4:
            pygame.draw.rect(screen, color_white, [5,15,150,85], 0, 5)
            pygame.draw.rect(screen, color_black, [5,15,150,85], 8, 5)
            screen.blit(font.render(results[result], True, color_black), (20,25))
            
        

        #opnieuw spelen?
        deal = pygame.draw.rect(screen, color_white, [150,220,300,100], 0, 25)      # teken rechthoek op positie x,y en grootte W,H, no border, 5 border-radius
        pygame.draw.rect(screen, color_black, [150,220,300,100], 8, 25)  
        deal_text = font.render('DEAL AGAIN', True, color_black)
        screen.blit(deal_text, (165,245))
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
                pygame.mixer.music.load(success_sound)
                pygame.mixer.music.play()
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
    screen.fill(color_grey)


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
        move_cards()
    
    draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome, hand_active)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               #quit = stop programm
            run = False

        if event.type == pygame.MOUSEBUTTONUP:               #start game bij klik op Deal
            if not active:                                   # er is maar 1 rectangle
                if buttons[0].collidepoint(event.pos):
                    reset_game()
            else:
                #you can hit
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                #you can stand
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                       reset_game()

        if event.type == pygame.KEYDOWN:               #start game bij klik op Deal
            if event.key == pygame.K_RETURN:
                    reset_game()
            else:
                #you can hit
                if event.key == pygame.K_h and player_score < 21 and hand_active:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                #you can stand
                elif event.key == pygame.K_s and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                

    #check ending
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score,outcome, records, add_score)

    pygame.display.flip()       


pygame.quit()

    