#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM matches")
    cur.close()
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM matches")
    cur.execute("DELETE FROM players")
    cur.close()
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    count = cur.fetchone()
    cur.close()
    db.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    cur.close()
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute("REFRESH MATERIALIZED VIEW standings")
    cur.execute("SELECT * FROM ordered_standings")
    standings = cur.fetchall()
    cur.close()
    db.commit()
    db.close()
    return standings


def reportMatch(winner, loser, is_draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      is_draw: boolean to indicate if the outcome was a draw
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO matches(winner, loser, is_draw)"
                " VALUES (%s,%s,%s)", (winner, loser, is_draw))
    cur.close()
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cur = db.cursor()
    cur.execute("REFRESH MATERIALIZED VIEW standings")
    cur.execute("SELECT id, name FROM ordered_standings")
    players = cur.fetchall()
    # get previous matches to avoid repeating old pairings
    cur.execute("SELECT winner, loser FROM matches")
    matches = cur.fetchall()
    cur.close()
    db.commit()
    db.close()
    # we will collect the set of pairs, and every player we put
    # in here will be deleted in the players list
    pairs = []
    # do we have an even number of players?
    if len(players) % 2 != 0:
        # we will insert a "you won" at the first player
        # who never got one
        i = 0
        found = False
        while i < len(players):
            if (players[i][0], None) not in matches:
                # great - this player never got a "you won"
                # we add the player to the pairings and delete
                # the player from the list of unpaired players
                pairs.append(players[i] + (None, None))
                del players[i]
                found = True
                break
            i += 1
        if not found:
            # no one found? The best one gets a lucky ticket
            pairs.append(players[0] + (None, None))
            del players[0]
    # for each player try to find the first they did not play against
    # when a player is taken we delete them
    # it should end with an empty list
    while len(players) > 0:
        i = 1
        found = False
        while i < len(players):
            if (players[0][0], players[i][0]) in matches:
                i += 1
                continue
            if (players[i][0], players[0][0]) in matches:
                i += 1
                continue
            # hurray we found a pair!
            pairs.append(players[0] + players[i])
            del players[i]
            del players[0]
            found = True
            break
        if not found:
            # no pairing found which was never played?
            # so we take the next one
            pairs.append(players[0] + players[1])
            del players[1]
            del players[0]
    # this should end - we started with an even list
    # and always deleted a pair
    return pairs
