# Full Stack Web Developer Nanodegree - P2: Tournament Results

This is the project 2 implementation for the Full Stack Web Developer
Nanodegree, implementing a relational database for tournament results.

## Prerequisites

To use this program one has to have [Vagrant](http://vagrantup.com/)
and [VirtualBox](https://www.virtualbox.org/) installed.

## Running the application

Use the command line (e.g. Terminal app on OSX or Linux, or CMD on Windows).
Go to the subdirectoy directory `vagrant` and start the Vagrant VM with the
command `vagrant up`. Then connect to the VM with `vagrant ssh`:
```
  cd vagrant
  vagrant up
  vagrant ssh
```
Instead of `vagrant ssh` you can use an SSH client (e.g. putty) and connect with `localhost` on port `2222`.
Use username `vagrant` and password `vagrant` when asked for login details.

In the virtual machine, first you have to create the database, tables and views.
```
  cd /vagrant/tournament
  psql -f ./tournament.sql
```

To run the test scripts use the following command on the virtual machine's commandline while in the directory `/vagrant/tournament`:
```
  python tournament_test.py
```
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