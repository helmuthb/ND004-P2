-- Table definitions for the tournament project.
--

-- 1. create database (drop if it exists)
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- 2. use the newly created database
\c tournament;

-- 3. create tables

-- players: participants in the tournament
CREATE TABLE players (
	id             serial PRIMARY KEY,
	name           varchar(50) NOT NULL CHECK (name <> '')
);

-- matches: outcomes of matches
CREATE TABLE matches (
    winner         integer NOT NULL references players(id),
    loser          integer references players(id),
    is_draw        boolean NOT NULL
);

-- create indexes to improve speed at joins
CREATE INDEX ON matches (winner);
CREATE INDEX ON matches (loser);

-- 4. create views

-- view_standing: view which gives the number of wins
-- This is created as a materialized view for performance reasons.
-- Otherwise the next view omw_standings would effectively a join
-- on four tables.
CREATE MATERIALIZED VIEW standings (id, name, won, played) AS
    SELECT players.id as id,
    	   players.name as name,
    	   count(m_won.winner) as won,
    	   count(m.winner) as played
      FROM players
      LEFT OUTER JOIN matches AS m_won ON
          (m_won.winner = players.id AND m_won.is_draw = FALSE)
      LEFT OUTER JOIN matches AS m ON
          ((m.winner = players.id AND m.loser IS NOT NULL) OR m.loser = players.id)
      GROUP BY players.id;

-- since a materialized view is actually a table we can add an index for it
CREATE UNIQUE INDEX ON standings(id);

-- omw_standing: total number of wins by opponents
CREATE VIEW omw_standings (id, omw) AS
    SELECT players.id AS id, sum(won) AS omw
      FROM players, standings, matches
      WHERE
        (players.id = matches.winner AND
       	 matches.loser = standings.id)
       OR
        (players.id = matches.loser AND
       	 matches.winner = standings.id)
     GROUP BY players.id;

-- sorted standings: sort by won, and then by omw
CREATE VIEW ordered_standings (id, name, won, played) AS
	SELECT standings.id, name, won, played
	FROM standings
	LEFT OUTER JOIN omw_standings ON (standings.id = omw_standings.id)
	ORDER BY won DESC, omw DESC;