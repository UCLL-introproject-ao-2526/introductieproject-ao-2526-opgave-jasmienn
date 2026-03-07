## IMPORTS

import copy
import random
import pygame
import os               #voor de card-images

pygame.init()                           #nodig voor font

'''credits
    Sound Effects by freesound_community from Pixabay
    Patroon background: https://prettywebz.com 
    Font met symbool kaart: © Hoyle 2004. All Rights Reserved // Created by Conexion // http://conexion.deviantart.com/ 
        e = diamond, q = spade, r = heart, w = club
    kaartontwerp by Victor MEUNIER. 
'''


# VARIABLES

# e = diamond, q = spade, r = heart, w = club (dit komt door het lettertype)
one_deck = [
    ['2','Hearts'], ['3','Hearts'], ['4','Hearts'], ['5','Hearts'], ['6','Hearts'], ['7','Hearts'], ['8','Hearts'], ['9','Hearts'], ['10','Hearts'], ['Jack','Hearts'], ['Queen','Hearts'], ['King','Hearts'], ['A','Hearts'],
    ['2','Pikes'], ['3','Pikes'], ['4','Pikes'], ['5','Pikes'], ['6','Pikes'], ['7','Pikes'], ['8','Pikes'], ['9','Pikes'], ['10','Pikes'], ['Jack','Pikes'], ['Queen','Pikes'], ['King','Pikes'], ['A','Pikes'],
    ['2','Clovers'], ['3','Clovers'], ['4','Clovers'], ['5','Clovers'], ['6','Clovers'], ['7','Clovers'], ['8','Clovers'], ['9','Clovers'], ['10','Clovers'], ['Jack','Clovers'], ['Queen','Clovers'], ['King','Clovers'], ['A','Clovers'],
    ['2','Tiles'], ['3','Tiles'], ['4','Tiles'], ['5','Tiles'], ['6','Tiles'], ['7','Tiles'], ['8','Tiles'], ['9','Tiles'], ['10','Tiles'], ['Jack','Tiles'], ['Queen','Tiles'], ['King','Tiles'], ['A','Tiles']
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

color_black = "#2F2D2D"
color_red = '#FF5555'
color_white ="#FFFFFF"
color_grey = "#F2E9E4"
color_green = "#27613e" 

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
results = ['','You are busted','You win', 'Dealer wins', 'Draw']

# win loss push(draw)
records = [0,0,0]
player_score = 0
dealer_score = 0 

# Media
background = pygame.image.load("Project/Media/Green.png")
card_player_y = 1000
card_dealer_y = 1000
card_speed = 0.3
deal = True



class Rectangle:
    
    def __init__(self, name, color, x, y, w):
        self.name = name
        self.color=color
        self.x = x
        self.y = y
        self.w = w
        self.h = 85

    def draw_rect(self):

        rect = pygame.Rect(0, 0, self.w, self.h)
        rect.center=(self.x, self.y)
        rechthoek = pygame.draw.rect(screen, color_white, rect)
        pygame.draw.rect(screen, self.color, rect, 5, 0)
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

        return rechthoek

class Card:
    width = 120
    height = 220
    card_radius = 15
    x_pos = 70
    def __init__(self, card_value, symbol, card_number,y_pos):
        #symbols = Tiles, Cloves, Pikes, Hearts
        self.symbol = symbol
        self.card_value = card_value
        self.card_number = card_number
        self.y_pos = y_pos

    def make_filename(self):
        name_file = self.symbol + '_' + self.card_value
        return name_file

    def draw_card(self):
        name = self.make_filename()
        if name in deck:
            screen.blit(deck[name], (self.x_pos +(70*self.card_number), self.y_pos + (5*self.card_number)))
        else: 
            screen.blit(font.render(self.card_value, True, color_red), (self.x_pos + 10 + 70* self.card_number, self.y_pos + 5 + 5*self.card_number))
        
    
# FUNCTIONS
def deck_loader():
    path = 'Project/Media/cards/'
    for filename in os.listdir(path):                                   # zoek in juiste map
        full_path = os.path.join(path, filename)                        # maak een path, inclusief .png-bestand        
        key, _ = os.path.splitext(filename)                             # de key van mijn dict is de naam van de file.
        image_surface = pygame.image.load(full_path).convert_alpha()    # laad de afbeelding en zet om in alpha om sneller te renderen
        yield key, image_surface                                        # zoals return, maar met herhaling.

def reset_game():
    global game_deck, initial_deal, my_hand, dealer_hand, active, reveal_dealer, hand_active, outcome, add_score, results, dealer_score, player_score, card_player_y, card_dealer_y
    # set variables
    active = True
    initial_deal = True                     # two cards
    deck = dict(deck_loader())                                    #deck[Clovers_2] zou nu moeten werken.
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
    screen.blit(font.render(f'You have {player}', True, color_white), (310, 430))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer has {dealer}', True, color_white),(310, 130)) 

def move_cards():
    global card_player_y, card_dealer_y
    target_player_y = 510
    target_dealer_y = 210
    
    if card_player_y > target_player_y:
       card_player_y += card_speed * -54
    if card_dealer_y > target_dealer_y:
        card_dealer_y += card_speed * -84

    else: 
        draw_scores(player_score, dealer_score)

# draw cards visueel op scherm
def draw_cards(player, dealer, reveal):
    
    for i in range(len(player)):
        card = Card(player[i][0], player[i][1], i, card_player_y)
        Card.draw_card(card)
    
    # if player hasn't finished turn, dealer will hide one card.
    for i in range(len(dealer)):
        if i != 0 or reveal:
            card = Card(dealer[i][0], dealer[i][1], i, card_dealer_y)
        else:
         card = Card("back", "card", i, card_dealer_y)
        Card.draw_card(card)
        
#get best score possible
def calculate_score(hand):
    #calculate hand score fresh every time. check Aces
    hand_score = 0
    aces_count = hand[0].count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i][0] == one_deck[j][0]:        # zoek enkel in de waardes.
                hand_score += int(hand[i][0])
        if hand[i][0] in ['10','Jack', 'Queen', 'King']:
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
        deal = Rectangle.draw_rect(Rectangle("START", color_black, 300, 80, 180))
        button_list.append(deal)

    # Game started = hit & stand tonen + win/loss-record
    else:
        if hand_act:
            hit = Rectangle.draw_rect(Rectangle("HIT ME", color_black, 150, 780, 200))
            stand = Rectangle.draw_rect(Rectangle("STAND", color_black, 450, 780, 200))
        else:
            hit = Rectangle.draw_rect(Rectangle("HIT ME", color_grey, 150, 780, 200))
            stand = Rectangle.draw_rect(Rectangle("STAND", color_grey, 450, 780, 200))
        button_list.append(hit)
        button_list.append(stand)
        
        score_text = font_small.render(f'Wins: {records[0]}   Losses: {records[1]}    Draws: {records[2]}', True, color_white)
        screen.blit(score_text,(15,840))

        # reset score
        reset_img = pygame.image.load("Project/Media/reset.png")
        reset = reset_img.get_rect(center=(550,860))
        screen.blit(reset_img, reset)
        button_list.append(reset)

    # restart when done playing
    if result != 0:
        #tekst als spel klaar
        
        if result == 1:
            text_color = color_red
            length = 340
        elif result == 2:
            text_color = color_green
            length = 190
        elif result == 3:
            text_color = color_red
            length = 270
        elif result == 4:
            text_color = color_black
            length = 140

        Rectangle.draw_rect(Rectangle(results[result], text_color, 300, 260, length))

        #opnieuw spelen?
        deal = Rectangle.draw_rect(Rectangle(" DEAL", color_black, 300, 80, 180))
        button_list.append(deal)

    return button_list

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
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

    # Als score verschilt van opgeslagen scores: update.        
    with open("Project/scores.txt", "r") as f:
        records = f.read().splitlines()
        records = [int(i) for i in records]
    if records != totals:
        with open("Project/scores.txt", "w") as f:
            for i in totals:
                f.write(str(i)+"\n")

    return result, totals, add

def ask_reset(records):
    while True:
        pygame.draw.rect(screen, color_green, (0, 0, WIDTH, HEIGHT- 60))
        Rectangle.draw_rect(Rectangle("Reset scores?", color_black, 300, 300, 400))
        reset_button = Rectangle.draw_rect(Rectangle("RESET", color_red, 125, 400,200))
        cancel_button = Rectangle.draw_rect(Rectangle("CANCEL", color_grey, 450, 400, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                raise SystemExit
        
            if event.type == pygame.MOUSEBUTTONUP:               
                if reset_button.collidepoint(event.pos):
                    with open("Project/scores.txt", "w") as f:
                        for i in range(3):
                            f.write("0\n")
                    with open("Project/scores.txt", "r") as f:
                        records = f.read().splitlines()
                        records = [int(i) for i in records]
                    return records
                elif cancel_button.collidepoint(event.pos):
                    return records

# MAIN GAME LOOP 

run = True
# haal records op
with open("Project/scores.txt", "r") as f:
    records = f.read().splitlines()
    records = [int(i) for i in records]

while run:
    # run the game at fps & fill screen with bg-color
    timer.tick(fps)
    screen.blit(background, (0, 0))
    deck = dict(deck_loader()) 
    
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
    
    buttons = draw_game(active, records, outcome, hand_active)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               #quit = stop programm
            run = False

        if event_type == pygame.MOUSEMOTION:
            

        if event.type == pygame.MOUSEBUTTONUP:               #start game bij klik op Deal
            if not active:                                   # er is maar 1 rectangle
                if buttons[0].collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
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
                #you can reset
                elif buttons[2].collidepoint(event.pos):
                    records = ask_reset(records)

                elif len(buttons) == 4:
                    if buttons[3].collidepoint(event.pos):
                        pygame.mixer.music.load(hitme_sound)
                        pygame.mixer.music.play()
                        reset_game()

        if event.type == pygame.KEYDOWN:               #start game bij enter
            if not active or len(buttons) == 4:
                if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load(hitme_sound)
                        pygame.mixer.music.play()
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

    