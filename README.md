NOTES (PREVIOUSLY dev-notes.txt)
----
Notes about the development process for use in the final report (because we have
to talk about a difficult bug, etc)

Bugs:
- Needed to call barrier.wait() when a organism died before it ended the thread
- Were trying to override start() function when we actually needed to override 
run() function
- Not exactly a bug, but had to get the order of stuff write with organisms
getting to the barrier and the ecosystem printing statuses (ended up using
phase1 v phase2)
- Size of orgsList Set was getting changed in the middle of loop, so we added
a lock

Miscellaneous:
- BEN SWAPPED THE ORDER OF Organism constructor arguments, beware!!
	-> (he did this because he needed to make location argument optional)
- EATING:
    - a predator might try to eat an organism when it's asleep or in the middle
       of an action. To deal with this, when a predator calls prey.beEaten(), it
       just sets the prey's wasEaten variable to True. At the beginning of each
       loop, an organism checks if it wasEaten and if it was, it dies or
       decrements its population

- REPRODUCTION:
    - If we reach the system's thread limit, some baby organisms won't get to
        live. We essentially destroy them and no new organisms will be able to
        be added unless other organisms die.
        - We do this by catching the exception raised when we try to start a
            new thread but have reached the limit. There are probably better
            ways to deal with this, but attempts at terminating random organism
            threads and not just newborns resulted in deadlock. This is probably
            the simplest way.
    - To reproduce, call ecosystem.addNewborn(babyOrganism), e.g. in the Shark
        class:
        baby = Shark(self.ecosystem, self.location)
        self.ecosystem.addNewborn(baby)


TIME
----
1 tick (loosely what an organism can do in one minute)



SPACE 
-----
2D (for Now, according to Nathan)



TO DO
-----
- Add lock for printing to stdout (actually we don't need this if we're only printing when organisms are done with a tick
- Better output
- More organisms
    - turtle
    - tiny fish
    - whale
    - krill?
    - octopus
    - starfish
    - crab
    - lobster
    - pipefish
    - anglerfish
    - american herring
    - salmon
    - cod
    - sardines
    - squid
    - algae
    - coral
- Do we need to do more things with time?
- More mutexes?
- Affect and/or use seablock's variables? e.g. oxygen
- Deal with case where there are too many threads at start of simulation

