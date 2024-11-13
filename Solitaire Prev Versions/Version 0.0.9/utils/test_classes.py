import unittest
from classes import Card, Standard_Deck, Tableau, Foundation, Stock, Klondike, GameRenderer

import pygame

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        card = Card('Hearts', 'A')
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.rank, 'A')
        self.assertFalse(card.selected)
        self.assertFalse(card.facing_up)
        self.assertEqual(card.id, '01H')

    def test_invalid_card_initialization(self):
        with self.assertRaises(ValueError):
            Card('InvalidSuit', 'A')
        with self.assertRaises(ValueError):
            Card('Hearts', 'InvalidRank')

    def test_card_comparison(self):
        card1 = Card('Hearts', 'A')
        card2 = Card('Hearts', 'A')
        card3 = Card('Diamonds', 'A')
        self.assertTrue(card1.is_same_card(card2))
        self.assertFalse(card1.is_same_card(card3))

    def test_card_flip(self):
        card = Card('Hearts', 'A')
        card.flip()
        self.assertTrue(card.is_face_up())
        card.flip()
        self.assertFalse(card.is_face_up())

    def test_card_selection(self):
        card = Card('Hearts', 'A')
        card.select()
        self.assertTrue(card.is_selected())
        card.deselect()
        self.assertFalse(card.is_selected())

class TestStandardDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Standard_Deck()

    def test_deck_initialization(self):
        self.assertEqual(self.deck.length(), 52)
        self.assertTrue(self.deck.is_legal())

    def test_deck_shuffle(self):
        original_order = self.deck.cards[:]
        self.deck.shuffle()
        self.assertNotEqual(original_order, self.deck.cards)

    def test_deck_sort(self):
        self.deck.shuffle()
        self.deck.sort()
        self.assertEqual(self.deck.cards[0].id, '01C')
        self.assertEqual(self.deck.cards[-1].id, '13S')

    def test_draw_top_card(self):
        top_card = self.deck.cards[-1]
        drawn_card = self.deck.draw_top_card()
        self.assertEqual(top_card, drawn_card)
        self.assertEqual(self.deck.length(), 51)

    def test_draw_random_card(self):
        random_card = self.deck.draw_random_card()
        self.assertNotIn(random_card, self.deck.cards)
        self.assertEqual(self.deck.length(), 51)

    def test_draw_specific_card(self):
        specific_card = self.deck.draw_specific_card('A', 'Hearts')
        self.assertEqual(specific_card.rank, 'A')
        self.assertEqual(specific_card.suit, 'Hearts')
        self.assertEqual(self.deck.length(), 51)

    def test_add_card(self):
        card = Card('Hearts', 'A')
        self.deck.add_card(card, False)
        self.assertIn(card, self.deck.cards)
        self.assertEqual(self.deck.length(), 53)

    def test_reset_deck(self):
        self.deck.draw_top_card()
        self.deck.reset_deck()
        self.assertEqual(self.deck.length(), 52)
        self.assertTrue(self.deck.is_legal())

class TestTableau(unittest.TestCase):
    def setUp(self):
        self.deck = Standard_Deck()
        self.tableau = Tableau()

    def test_deal_initial_cards(self):
        self.deck.shuffle()
        self.tableau.deal_initial_cards(self.deck)
        self.assertEqual(len(self.tableau.tableau[0]), 1)
        self.assertEqual(len(self.tableau.tableau[-1]), 7)

    def test_fetch_single_card(self):
        self.deck.shuffle()
        self.tableau.deal_initial_cards(self.deck)
        card = self.tableau.fetch_single_card(0)
        self.assertIsNotNone(card)
        self.assertEqual(len(self.tableau.tableau[0]), 0)

    def test_fetch_multiple_cards(self):
        self.deck.shuffle()
        self.tableau.deal_initial_cards(self.deck)
        cards = self.tableau.fetch_multiple_cards(0, 1)
        self.assertEqual(len(cards), 1)
        self.assertEqual(len(self.tableau.tableau[0]), 0)

    def test_add_single_card(self):
        card = Card('Hearts', 'K')
        self.tableau.add_single_card(card, 0)
        self.assertIn(card, self.tableau.tableau[0])

    def test_add_multiple_cards(self):
        cards = [Card('Hearts', 'K'), Card('Clubs', 'Q')]
        self.tableau.add_multiple_cards(cards, 0)
        self.assertIn(cards[0], self.tableau.tableau[0])
        self.assertIn(cards[1], self.tableau.tableau[0])

class TestFoundation(unittest.TestCase):
    def setUp(self):
        self.foundation = Foundation()

    def test_add_card(self):
        card = Card('Hearts', 'A')
        self.assertTrue(self.foundation.add_card(card))
        self.assertIn(card, self.foundation.pile)

    def test_is_complete(self):
        for rank in Card.RANKS:
            if not self.foundation.add_card(Card('Hearts', rank)):
                raise ValueError('Card could not be added to foundation. Current status: {}'.format(self.foundation.pile))
        self.assertTrue(self.foundation.is_complete())

class TestStock(unittest.TestCase):
    def setUp(self):
        self.deck = Standard_Deck()
        self.stock = Stock()

    def test_populate_stock(self):
        self.deck.shuffle()
        self.stock.populate_stock(self.deck)
        self.assertEqual(len(self.stock.stock), 52)

    def test_draw_card(self):
        self.deck.shuffle()
        self.stock.populate_stock(self.deck)
        self.stock.draw_card()
        self.assertEqual(len(self.stock.waste), 1)

class TestKlondike(unittest.TestCase):
    def setUp(self):
        self.klondike = Klondike()

    def test_initialize_game(self):
        self.assertEqual(self.klondike.deck.length(), 0)
        self.assertEqual(len(self.klondike.tableau.tableau[0]), 1)
        self.assertEqual(len(self.klondike.stock.stock), 24)

    def test_is_game_won(self):
        for foundation in self.klondike.foundation:
            for rank in Card.RANKS:
                foundation.add_card(Card(foundation.SUITS[0], rank))
        self.assertTrue(self.klondike.is_game_won())

class TestGameRenderer(unittest.TestCase):
    def setUp(self):
        self.klondike = Klondike()
        self.screen = pygame.display.set_mode((800, 600))
        self.images = {card.id: pygame.Surface((50, 70)) for card in self.klondike.deck.cards}
        self.images['back'] = pygame.Surface((50, 70))
        self.renderer = GameRenderer(self.klondike, self.screen, self.images)

    def test_set_dimensions(self):
        self.renderer.set_dimensions()
        self.assertIn("screen", self.renderer.dimensions)
        self.assertIn("card", self.renderer.dimensions)

    def test_pos_cards(self):
        self.renderer.pos_cards()
        # Since pos_cards is not fully implemented, we can't assert much here
        # This is a placeholder for future tests

    def test_draw(self):
        self.renderer.draw()
        # We can't assert much here since it's a visual output
        # This is a placeholder for future tests

    def test_draw_tableau(self):
        self.renderer.draw_tableau()
        # We can't assert much here since it's a visual output
        # This is a placeholder for future tests

    def test_draw_foundations(self):
        self.renderer.draw_foundations()
        # We can't assert much here since it's a visual output
        # This is a placeholder for future tests

    def test_draw_stock(self):
        self.renderer.draw_stock()
        # We can't assert much here since it's a visual output
        # This is a placeholder for future tests

    def test_draw_waste(self):
        self.renderer.draw_waste()
        # We can't assert much here since it's a visual output
        # This is a placeholder for future tests

if __name__ == "__main__":
    unittest.main()
    
    
