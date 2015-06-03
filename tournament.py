#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, re


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        print "Connected!"
        return conn
    except psycopg2.Error as e:
        print e

def deleteWins():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM wins;")
    DB.commit()
    print "Task Done!"

def deleteMatches():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()

def deletePlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()


def countWins():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM wins;")
    DB.commit()
    return int(c.fetchone()[0])


def countPlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    DB.commit()
    return int(c.fetchone()[0])


#In the next two functions I try to escape ' by adding two of them, noticed the name O'Neil needed it.
def registerPlayer(name):
    DB = connect()
    c = DB.cursor()
    chars_to_remove = ["'"]
    rx = '[' + re.escape(''.join(chars_to_remove))+']'
    name = re.sub(rx, '"', name)
    c.execute("INSERT INTO players (name) VALUES ('%s') RETURNING id;" % ( name,))
    DB.commit()
    returnable = int(c.fetchone()[0])
    return returnable

#creates a new tournament for the players to have fun in
def createTournament(name):
    DB = connect()
    c = DB.cursor()
    chars_to_remove = ["'"]
    rx = '[' + re.escape(''.join(chars_to_remove))+']'
    name = re.sub(rx, "''", name)
    c.execute("INSERT INTO tournaments (name) VALUES ('%s') RETURNING id;" % (name,))
    DB.commit()
    returnable = int(c.fetchone()[0])
    return returnable

def deleteTournaments():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournaments;")
    DB.commit()

def countTournaments():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM tournaments;")
    DB.commit()
    return int(c.fetchone()[0])

# registers a participant to a tournament from the already existing tournaments and players.
def registerParticipant(t_id, p_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO participates (t_id, p_id) VALUES (%s, %i);" % (t_id, p_id,))
    DB.commit()

def deleteParticipates():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM participates")
    DB.commit()

def countParticipates():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM participates;")
    DB.commit()
    return int(c.fetchone()[0])

# has a tournament id to take players standings from a certain tournament
def playerStandings(t_id):
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player_info where tournaments = %s;" % (t_id,))
    DB.commit()
    return c.fetchall()


#NOTE TO SELF, ADD t_id in reportMatch and reportMatchWithRound

# added the boolean for tie, which if true, adds a win for the other player as well.
# first argumment, if the game is not a tie, should be considered as the winner
# used 
def reportMatch(first, second, tie):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id) VALUES( %s, %i, %d) RETURNING id;" % (0,first, second ))
    match_id = int(c.fetchone()[0])
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, first,))
    if tie:
        c.execute("INSERT INTO wins (m_id, p_id) VALUES (%s, %i);" % (match_id, second,))
    DB.commit()

#used to setup preliminary matches
def setupMatch(first, second):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id) VALUES( %s, %i, %d) RETURNING id;" % (0,first, second ))
    DB.commit()

#used to report wins separately from creating matches
def reportWin(player_id, match_id):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, player_id,))

# added the boolean for tie, which if true, adds a win for the other player as well.
# first argumment, if the game is not a tie, should be considered as the winner
# the round argumment is to keep track when the match happen.
def reportMatchWithRound(round, first, second, tie):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (round, p_one_id, p_two_id) VALUES( %s, %i, %d) RETURNING id;" % (round,first, second ))
    match_id = int(c.fetchone()[0])
    c.execute("INSERT INTO wins (m_id, p_id) VALUES(%s, %i);" % (match_id, first,))
    if tie:
        c.execute("INSERT INTO wins (m_id, p_id) VALUES (%s, %i);" % (match_id, second,))
    DB.commit()

"""Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        wins1: the amount of wins the first player has

        id2: the second player's unique id
        name2: the second player's name
        wins2: the amount of wins the second player has
    """
def swissPairings():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM player_pairs;")
    DB.commit()
    return c.fetchall()
    

    