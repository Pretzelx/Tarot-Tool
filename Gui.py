import pandas as pd
import random
import streamlit as st

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

def interpret_card(card_name, orientation, tarot_deck):
    """Interpret a tarot card based on its name, orientation, and the tarot deck"""
    card = next((c for c in tarot_deck.cards if c.name.lower() == card_name.lower()), None)
    if not card:
        return "Card not found"
    if orientation == 'upright':
        return f"{card.name} (Upright): {card.upright_meaning}"
    elif orientation == 'reversed':
        return f"{card.name} (Reversed): {card.reverse_meaning}"
    else:
        return "Invalid orientation. Please enter 'upright' or 'reversed'."

# Load the tarot deck

tarot_df = pd.read_csv('Tarot Card Master Sheet.csv')

tarot_deck = TarotDeck(tarot_df)

# Streamlit App
st.title("Tarot Card Interpreter")

spread_choice = st.selectbox("Choose a Tarot Spread", ["Three Card Spread", "Celtic Cross Spread"])

if spread_choice == "Three Card Spread":
    spread_positions = ["Past", "Present", "Future"]
else:
    spread_positions = [
        "1. Present", "2. Immediate Challenge", "3. Distant Past", "4. Recent Past", "5. Best Outcome",
        "6. Immediate Future", "7. Factors Affecting Situation", "8. External Influences", "9. Hopes and Fears", "10. Final Outcome"
    ]

card_names = []
orientations = []

for position in spread_positions:
    card_name = st.text_input(f"Enter the name of the card for {position}", key=f"{position}_card")
    orientation = st.selectbox(f"Is the card Upright or Reversed?", ["upright", "reversed"], key=f"{position}_orientation")
    card_names.append(card_name)
    orientations.append(orientation)

if st.button("Get Reading"):
    reading = {}
    for i, position in enumerate(spread_positions):
        interpretation = interpret_card(card_names[i], orientations[i].lower(), tarot_deck)
        reading[position] = interpretation

    st.subheader("Your Tarot Reading:")
    for position, meaning in reading.items():
        st.write(f"**{position}**: {meaning}")
