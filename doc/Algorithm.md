Final implementation
============
Algorithm
------------
### Genome : ###
    Coordinates x and y
    Iteration index
    Rotation
    4 sides ids

### Population generation : ###
    Loop on time, generation number or both
    Border and corner restrictions
    Random position and rotation inside

### Fitness : ###
    Individual fitness : range [0, 4] based on well placed sides
    Group fitness : range [0, 4] * nb = [0, (1024)] nb is number of individual

### Reproduction: ###
* Select :
~~~
Never move the top left corner
A corner or a border individual must stay on their side
Elitism ratio must evolve
Exclude individual with individual fitness egal 4
Random iteration on inside individuals
Update elitism on generation fitness
~~~
* Crossover :
~~~
A corner must be placed on a corner position only
A border must be placed on a border position only
Replace all other individuals exclude by the elitism with a roulette placement and the restrictions
On replace, test all rotations and keep the best one
~~~
### Mutation : ###
~~~
Use a mutation ratio
With this ratio, select random individuals
Mutate selected individuals rotation from this ratio
Exchange individual position with an other with this ratio
Use the same reproduction restrictions
Mutate corner and border individuals but only with themselves
Variable mutation between 0 and 20 percent
~~~
***
Around the algorithm
------------
### Statistics and logbook : ###

* Logbook.txt (text version) :
~~~
connections_completions
score
selected
~~~
* Logbook.pkl (bin version) :
~~~
Actual iteration
Individual fitness : minimum, maximum, average
Group fitness : minimum, maximum, average
Individuals mutate number
Generation mutation percentage
4/4 individual sides match number
Connections_completions
Score
Selected (number of selected/removed tils during select operation)
~~~
* Images statistics :
~~~
Individual and group fitness on each generation
Generation representation
~~~
### Optimization : ###
    Separate algorithm and graph rendering

### Algorithm evaluation : ###
    Algorithm test on little size puzzle
    Benchmark script to test different puzzle size
    Write in logbook 4/4 sides match pieces

### Tested / Resolved : ###
- [x] \(2\*2\)
- [x] \(3\*3\)
- [ ] \(4\*4\)
- [ ] \(16\*16\)
