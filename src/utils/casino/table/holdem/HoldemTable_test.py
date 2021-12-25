from src.utils.casino.table.holdem.HoldemTable import HoldemTable


def test_Story1():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()
    # Game start
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    # pre-flop (round 1) start
    holdemTable.rise(1, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.rise(3, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 1
    assert holdemTable.mainPot == 152500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 5
    # Round 1 end
    holdemTable.flop()
    # Round 2 start
    holdemTable.rise(1, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.fold(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.fold(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.rise(5, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.fold(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2

    # Round 2 end

    holdemTable.turnOrRiver()
    # Round 3 start
    holdemTable.rise(4, 1000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 2232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # Round 3 end

    holdemTable.turnOrRiver()
    # Round 3 start

    holdemTable.rise(4, 10000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.fold(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn is None
    assert holdemTable.mainPot == 12232500
    assert holdemTable.numberOfPlayersNotFold == 1
    # End


def test_story2():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()
    # Game start
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    # pre-flop (round 1) start
    holdemTable.rise(1, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.rise(3, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 1
    assert holdemTable.mainPot == 152500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 5
    # Round 1 end
    holdemTable.flop()
    # Round 2 start
    holdemTable.rise(1, 20000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.fold(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.fold(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.rise(5, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    holdemTable.fold(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2

    # Round 2 end

    holdemTable.turnOrRiver()
    # Round 3 start
    holdemTable.rise(4, 1000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 2232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # Round 3 end

    holdemTable.turnOrRiver()
    # Round 3 start

    holdemTable.rise(4, 10000000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 4
    assert holdemTable.mainPot == 22232500
    for playerID in holdemTable.players:
        assert holdemTable.players[playerID]['tempPot'] == 0
    assert holdemTable.currentBet == 0
    assert holdemTable.numberOfPlayersNotFold == 2
    # End


def test_Story3():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()

    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[1]['moneyInvested'] == holdemTable.ante
    holdemTable.rise(2, 1000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 1000
    holdemTable.callOrCheck(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    assert holdemTable.players[3]['moneyInvested'] == holdemTable.ante + 1000
    holdemTable.callOrCheck(4)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    assert holdemTable.players[4]['moneyInvested'] == holdemTable.ante + 1000
    holdemTable.callOrCheck(5)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    assert holdemTable.players[5]['moneyInvested'] == holdemTable.ante + 1000
    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 1
    assert holdemTable.players[1]['moneyInvested'] == holdemTable.ante + 1000

    holdemTable.flop()

    holdemTable.callOrCheck(1)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[1]['moneyInvested'] == holdemTable.ante + 1000
    holdemTable.rise(2, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 11000
    holdemTable.callOrCheck(3)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    assert holdemTable.players[3]['moneyInvested'] == holdemTable.ante + 11000
    holdemTable.allIn(4, 100)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    assert holdemTable.players[4]['moneyInvested'] == holdemTable.ante + 1100
    holdemTable.allIn(5, 100000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 1
    assert holdemTable.players[5]['moneyInvested'] == holdemTable.ante + 101000
    holdemTable.allIn(1, 100)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[1]['moneyInvested'] == holdemTable.ante + 1100
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 101000
    holdemTable.callOrCheck(3)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[3]['moneyInvested'] == holdemTable.ante + 101000

    holdemTable.turnOrRiver()

    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 101000
    holdemTable.callOrCheck(3)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[3]['moneyInvested'] == holdemTable.ante + 101000

    holdemTable.turnOrRiver()

    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 101000
    holdemTable.rise(3, 2000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[3]['moneyInvested'] == holdemTable.ante + 103000
    holdemTable.callOrCheck(2)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn == 2
    assert holdemTable.players[2]['moneyInvested'] == holdemTable.ante + 103000



def test_Story4():
    class MemberTest:
        id = 1
    owner = MemberTest()
    holdemTable = HoldemTable(None, owner)
    holdemTable.addPlayer(1)
    holdemTable.addPlayer(2)
    holdemTable.addPlayer(3)
    holdemTable.addPlayer(4)
    holdemTable.addPlayer(5)
    holdemTable.gameStart()

    holdemTable.allIn(1, 100000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 2
    holdemTable.allIn(2, 120000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 3
    holdemTable.allIn(3, 10000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 4
    holdemTable.allIn(4, 12000)
    assert holdemTable.toNext() is False
    assert holdemTable.whosTurn == 5
    holdemTable.allIn(5, 20000)
    assert holdemTable.toNext() is True
    assert holdemTable.whosTurn is None

    holdemTable.flop()

    holdemTable.turnOrRiver()

    holdemTable.turnOrRiver()
