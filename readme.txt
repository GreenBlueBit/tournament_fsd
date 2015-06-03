I've designed the tables in such a way that the same players can participate in multiple tournaments along the years.

There's also keeping track of rounds in the matches table, which I thought would be kept track of in a program (adding +1 after the amount of matches in the current round are done).

Also to be noticed is that p_two_id in matches is able to be null, this is made in that
way in case the swiss pairings would do an odd number of players, one would get a free win with no challenger, this way it would be kept track of so it only happen once.

I tried to use views for the standings and swiss pairing, views are great because they turn extremly complicated queries into very simple things, so it's a great thing to use especially when you're in a team with people of lower experience in the field.

If I were to make this into an actual project, first of all I would try to avoid deleting anything, I always prefer to instead just deactivate/trash whatever needs to be deleted, so I can still keep the info in the system, just not make it available in day to day operaitons. If that's not possible I'd make all the foreign key Cascade deletion so if you delete an object which is required for a foreign key, the object which needs it gets deleted instantly too, avoids a lot of issues. (would probably Cascade updates too if ever needed, though since I like working with views a lot, probably not an issue).

I have documented all of the changes in the tournament_test.py in the file itself, and respectively in tournament.py for the deeper level explanation.


INSTRUCTIONS :

-Go to your Vagrant Folder.

-Open Bash.

-If it's the first time, type 'vagrant init' and press enter.

-Type 'vagrant up' and press enter.

-Type 'vagrant ssh' and press enter

#How about we agree that instead of saying type.... and press enter I just say enter .... ? Let's try that.

-Enter cd /vagrant/tournament

-Enter psql

-Enter DROP DATABASE IF EXISTS tournament;

-Enter CREATE DATABASE tournament;

-Press and hold Ctrl and then press D.

-Enter psql tournament < tournament.sql

-Enter python

-Enter import tournament_test

-Do your tests.

