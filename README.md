# Full Stack Web Developer Nanodegree - P2: Tournament Results

This is the project 2 implementation for the Full Stack Web Developer
Nanodegree, implementing a relational database for tournament results.

## Prerequisites

To use this program one has to have [Vagrant](http://vagrantup.com/)
and [VirtualBox](https://www.virtualbox.org/) installed.
Using the command line, launch the Vagrant VM with the command
`vagrant up` while in the directory `vagrant`.

## Database design

I used some PostgreSQL special features for performance enhancements.
Specifically there is a materialized view to allow for performant
calculation of the order of the players.

The following enhancements are implemented, and additional test functions are provided for them:
 - allow a draw in a match
 - allow an odd number of participants
 - rematches are prevented

In addition, when the number of wins is the same the OMW (Opponent Match Wins) is used as additional criteria.

## Copyright and license

`tournament_test.py` is written by Udacity (with modifications by me).
The other files are in the public domain.