Totaal: 
Tutorial: 2u
Updating: 3u30

# 22/02

Het eerste halfuur van de tutorial zit erop. Het werkt zoals het moet werken tot nu toe.

# 27/02

De blackjack-game-tutorial is af. Er zitten nog enkele bugs in, die zijn voor morgen. 
* als ik een nieuw spel begin, staat de dealer op reveal.
* controleer de scores

# 28/02 (3u)
## 8.30
Tijd voor eigen werk. Ik bedenk eerst graag wat ik wil doen, om dan uit te vogelen hoe ik het doe. 
Ik wil vooral mooiere kaarten > https://www.youtube.com/watch?v=rHEnZfq_zEQ 

## 9.30
Jack, Queen en King hebben nu een mooie kaart.
Het ziet er nog altijd allemaal heel 'paint' uit. Voor tkinter bestaat ttk om het mooier te maken.
Ik kom uit op PySimpleGUI, waar tkinter inzit. https://realpython.com/pysimplegui-python/ 
Blijkbaar is het wel moeilijk om die te combineren, dus ik ga toch maar gewoon prutsen in pygame. 

## 10.45
Het ziet er al beter (of toch anders) uit. Het is helaas nog niet duidelijk wanneer je en knop kan indrukken en wanneer niet. 

## 11.30
Genoeg gewerkt voor nu. 
* Ik heb kaarten met J,Q,K
* Ik heb een geluidje bij 'hit me' en 'succes'
* Ik heb de lay-out wat aangepast.

Ideetjes voor later:
* Kaarten met 4 kaartsoorten
* meer geluidjes
* transformeffectje

# 01/03 (0u30)
## 13.15
Ik heb de vier symbolen toegevoegd op de kaarten via een lettertype. 
Dit was maar een halfuurtje werk, minder dan verwacht. 
Volgende keer ga ik proberen om de kaarten ook zichtbaar uit te delen, dus via transform. 

# 03/03
## 19.30
Ik wil graag dat de kaarten 'binnenvliegen'. https://www.youtube.com/watch?v=DWRjdrGaADg 
Dit was het niet.. 
https://www.youtube.com/watch?v=sfniTyS9yHo 

## 21.00
Het was toch anders dan in het filmpje, omdat ik het niet met een key deed. 
Met de hulp van Lumo is het toch gelukt. 
Je scherm 60 keer per seconde wordt gerefresht, dus worden je kaarten steeds opnieuw getekend. 
Je moet ze dus telkens een beetje hoger tekenen tot ze staan waar je ze wil (target).

De keys vind ik wel interessant, dus ga ik het spel speelbaar maken zonder muis:
- H(it)
- S(tand)
- Enter (deal)

## 21.30
Het is gelukt, maar nu heb ik dubbele code. Volgende stap: code opruimen. 

