import pytest
from hanamikoji.game import Player

### ChatGPT generated tests ###

@pytest.fixture
def player() -> Player:
    return Player()


def test_add_card_to_hand(player: Player) -> None:
    player.add_card_to_hand(5)
    assert player.hand == [5]
    player.add_card_to_hand(2)
    assert player.hand == [5, 2]


def test_remove_card_from_hand(player: Player) -> None:
    player.hand = [5, 2, 7]
    player.remove_card_from_hand(2)
    assert player.hand == [5, 7]
    with pytest.raises(ValueError):
        player.remove_card_from_hand(3)


def test_use_action(player: Player) -> None:
    player.actions_remaining = [1, 2, 3, 4]
    player.use_action(2)
    assert player.actions_remaining == [1, 3, 4]
    with pytest.raises(ValueError):
        player.use_action(5)


def test_reset_actions(player: Player) -> None:
    player.actions_remaining = [1, 2, 3, 4]
    player.reset_actions()
    assert player.actions_remaining == [1, 2, 3, 4]


def test_add_favor(player: Player) -> None:
    player.add_favor(4)
    assert player.favors_won[4] is True


def test_remove_favor(player: Player) -> None:
    player.favors_won = {1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True}
    player.remove_favor(3)
    assert player.favors_won[3] is False
    with pytest.raises(KeyError):
        player.remove_favor(8)


def test_has_favor(player: Player) -> None:
    player.favors_won = {1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True}
    assert player.has_favor(5) is True
    assert player.has_favor(2) is False


def test_add_cards_to_hand(player: Player) -> None:
    player.hand = [3, 6]
    player.add_cards_to_hand([2, 7])
    assert player.hand == [3, 6, 2, 7]


def test_reset_player(player: Player) -> None:
    player.hand = [3, 6]
    player.actions_remaining = [1, 2]
    player.favors_won = {1: True, 2: False, 3: True}
    player.reset_player(reset_favors=True)
    assert player.hand == []
    assert player.actions_remaining == [1, 2, 3, 4]
    assert player.favors_won == {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
    player.add_card_to_hand(5)
    assert player.hand == [5]

### User Generated Tests ###