import pytest
import uuid
from decimal import Decimal
from sportsbook_class import Sportsbook, Player, Bet

@pytest.fixture
def sportsbook():
    return Sportsbook("Betby", "betby.com")

@pytest.fixture
def player(sportsbook):
    return Player(name="John", balance=Decimal('100.00'), sportsbook=sportsbook)

def test_player_creation(sportsbook, player):

    assert player.name == "John"
    assert player.balance == Decimal("100.00")
    assert player.id in sportsbook.players

def test_valid_bet(player,mocker,capsys):
    mocker.patch('builtins.input', return_value='50.00')
    mocker.patch('random.uniform', return_value = 2.5)

    initial_bet_count = len(player.bet_history)

    player.place_bet()

    captured = capsys.readouterr()

    assert len(player.bet_history) == initial_bet_count + 1
    assert "Bet placed:" in captured.out
    assert "Amount=50.00" in captured.out
    assert "Odds=2.5" in captured.out
    assert player.balance == Decimal("50.00")
    bet = player.bet_history[-1]
    assert isinstance(bet, Bet)
    assert bet.amount == Decimal("50.00")
    assert bet.k == 2.5


def test_invalid_bet_input(player, mocker, capsys):
    mocker.patch('builtins.input', return_value='abc')

    player.place_bet()

    captured = capsys.readouterr()

    assert "Invalid input. Please enter a valid number" in captured.out

def test_negative_amount_bet(player, mocker, capsys):
    mocker.patch('builtins.input', return_value='-1.00')

    player.place_bet()

    captured = capsys.readouterr()

    assert "Amount must be greater than 0" in captured.out

def test_amount_bigger_then_balance_bet(player, mocker, capsys):
    mocker.patch('builtins.input', return_value='200.00')

    player.place_bet()

    captured = capsys.readouterr()

    assert "Not enough money to place bet" in captured.out

def test_betting_disabled(player, mocker, capsys):
    player.place_bets = False

    mocker.patch('builtins.input', return_value='50.00')

    player.place_bet()

    captured = capsys.readouterr()

    assert "Betting is not available now" in captured.out

def test_settle_bet_win(player,sportsbook, mocker, capsys):
    bet = Bet(amount=Decimal('10.00'), k=Decimal('1.5'))
    bet.id = 123
    player.bet_history.append(bet)

    mocker.patch('builtins.input', return_value=str(bet.id))
    mocker.patch('random.choice', return_value=True)

    initial_balance = player.balance

    sportsbook.settle_bet()

    expected_balance = initial_balance + (bet.amount * bet.k)
    assert player.balance == expected_balance
    assert bet.is_settled is True

def test_settle_bet_lost(player,sportsbook, mocker, capsys):
    bet = Bet(amount=Decimal('10.00'), k=Decimal('1.5'))
    bet.id = 123
    player.bet_history.append(bet)

    mocker.patch('builtins.input', return_value=str(bet.id))
    mocker.patch('random.choice', return_value=False)

    initial_balance = player.balance

    sportsbook.settle_bet()

    expected_balance = initial_balance
    assert player.balance == expected_balance
    assert bet.is_settled is False

def test_settle_bet_not_found(player,sportsbook, mocker, capsys):
    bet = Bet(amount=Decimal('10.00'), k=Decimal('1.5'))
    bet.id = 123
    player.bet_history.append(bet)

    mocker.patch('builtins.input', return_value=str(456))
    mocker.patch('random.choice', return_value=False)

    sportsbook.settle_bet()

    captured = capsys.readouterr()
    assert "Bet not found" in captured.out

