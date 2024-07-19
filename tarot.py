
import pandas as pd
import random
import json
# import PIL
# from PIL import Image
import logging 


tarot_df = pd.read_csv ('Tarot-Tool/Tarot Card Master Sheet.csv')

tarot_df.tail(5)
tarot_df.dropna(axis=1)



class TarotCard:
    def __init__(self, name, number, arcana, suit, image, fortune, keywords_upright, keywords_reversed, upright_meaning, reverse_meaning, archetype, numerology, elements_planets, mythical, questions):
        self.name = name
        self.number = number
        self.arcana = arcana
        self.suit = suit
        self.image = image
        self.fortune = fortune
        self.keywords_upright = keywords_upright.split(',') if pd.notna(keywords_upright) else []
        self.keywords_reversed = keywords_reversed.split(',') if pd.notna(keywords_reversed) else []
        self.upright_meaning = upright_meaning if pd.notna(upright_meaning) else "No meaning available."
        self.reverse_meaning = reverse_meaning if pd.notna(reverse_meaning) else "No meaning available."
        self.archetype = archetype if pd.notna(archetype) else "No archetype."
        self.numerology = numerology if pd.notna(numerology) else "No numerology."
        self.elements_planets = elements_planets if pd.notna(elements_planets) else "No elements or planets."
        self.mythical = mythical if pd.notna(mythical) else "No mythical reference."
        self.questions = questions if pd.notna(questions) else "No questions available."

    def __repr__(self):
       return f"TarotCard(name={self.name}, arcana={self.arcana}, suit={self.suit})"

class TarotDeck:
    def __init__(self, tarot_df):
        self.cards = self.load_deck(tarot_df)

    def load_deck(self, tarot_df):
        cards = []
        for _, row in tarot_df.iterrows():
            card = TarotCard(
                name=row['Name'],
                number=row['Number with MA or mA'],
                arcana=row['Major Arcana or Minor Arcana'],
                suit=row['Suit of Cards'],
                image=row['Image'],
                fortune=row['Fortune'],
                keywords_upright=row.get('Key Words Upright', ''),
                keywords_reversed=row.get('Key words Reversed', ''),
                upright_meaning=row.get('Upright Meaning', ''),
                reverse_meaning=row.get('Reverse Meaning', ''),
                archetype=row.get('Archetype', ''),
                numerology=row.get('Numerology', ''),
                elements_planets=row.get('Elements and Planets', ''),
                mythical=row.get('Mythical', ''),
                questions=row.get('Questions to ask', '')
            )
            cards.append(card)
        return cards

    def draw_cards(self, num_cards):
        return random.sample(self.cards, num_cards)
tarot_df.columns

## Interpret the cards based on the cards orientation - Upright or Reversed

def interpret_card(card_name, orientation, tarot_df):

    """Interpreting a tarot card based on its name, orientation, and the tarot deck"""
    

    card = next((c for c in tarot_deck.cards if c.name.lower() == card_name.lower()), None)
    
    if not card: 
        return "Card not found"
    
    if orientation == 'upright':
        return f"{card.name} (Upright):{card.upright_meaning}"
    
    elif orientation == 'reversed':
        return f"{card.name} (Reversed):{card.reverse_meaning}"
    
    else: 
        return "Invalid orientation. Please eneter 'upright' or 'reversed'."
    
    
## Choosing the tarot spread

## 1. Celtic cross - a 10 card spread that provides a comprehensive reading that symbolizes the persons underlying feelings associated with situation asked.

## 2. Past, Present, Future - A simple 3 card spread depicting learnings from the past, the current situation at hand and how to navigate it and then what the future outcame may hold if you make the decisions aligned to your path. 


def tarot_reading(tarot_deck):
   
    spread_choice = input("Do you want a 'Celtic Cross' spread or a 'Past, Present, Future' reading?")


    if spread_choice == 'celtic cross':
        spread = {
            "1. Present": None,
            "2. Immediate Challenge": None,
            "3. Distant Past": None,
            "4. Recent Past": None,
            "5. Best Outcome": None,
            "6. Immediate Future": None,
            "7. Factors Affecting Situation": None,
            "8. External Influences": None,
            "9. Hopes and Fears": None,
            "10. Final Outcome": None
        }
    elif spread_choice == '3-card':
        spread = {
            "Past": None,
            "Present": None,
            "Future": None
        }

    else:
        print("Invalid choice. Please select either 'Celtic Cross' or '3-card'.")
        return
    
    for position in spread.keys():
        card_name = input (f"Enter the name of the card for {position}; ")
        orientation = input(f"Is the card Upright or Reversed? ").strip().lower()
        interpretation = interpret_card(card_name, orientation, tarot_deck)
        spread[position] = interpretation

    print("Your Tarot Reading:")
    for position, meaning in spread.items():
        print(f"{position}: {meaning}")

## Main Execution

tarot_df['Name'] = tarot_df['Name'].str.strip()

tarot_deck = TarotDeck(tarot_df)

tarot_reading(tarot_deck)
