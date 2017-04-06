
# Eternity II

## Introduction

  [Current Algorithm](doc/Algorithm.md)

## Setup

### Requirements

  Using pip

  ```bash
  $ pip install -r requirements.txt
  ```

  Download the [images](https://intra.epitech.eu/module/2016/M-IAR-752/PAR-9-2/acti-235553/project/file/eternityII_data.zip)
  and unzip them in the working directory.

### Configuration and population

Inside the config file config.py you will find a lot of interesting settings:

```python
population_file_base="e2pieces.txt"
NGEN = 2000
mutate_inpd=0.01
selection_ind_value_step=1
elitism_percentage_start=10
elitism_percentage_up=4
gen_modulo_elitism=100
```

- population_file_base: filename containing the tiles to play with.
  - Few files have been written already `test_4pieces.txt` `test_9pieces.txt` `test_16pieces.txt`
- NGEN: Default maximum number of iterations to do. See [iteration](doc/Algorithm.md#iteration)
- mutate_inpd: Percentage of mutation. (between 0 and 1) See [iteration](doc/Algorithm.md#mutation)

### Workflows. Running Scripts


#### The workflow starts by running the script called main then the script render.

  ```text
  $ python main.py
  [Error 183] Cannot create a file when that file already exists: './gen/'
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.14m.46s/
  No Solution Look at the logbook.
  ```

#### Look at the path given for your puzzle. All the stats will be logged there.

  ``` text
  $ python render.py gen/lumy_13-02-2017_13h.14m.46s/
  (it take few time before an ouput arrive because it's loading big binary file).
  progression Bar 1 #################
  progression Bar 2 ########________#
  ```
  > If you do not see any progress bar it might be because you're not in a real tty
  (the package we use seems to work perfectly under all unix/linux but seems
  still in dev for windows and others).

#### Generate video if you have ffmpeg.
  ``` text
  $ ./gen/generations_images_to_video.bash gen/lumy_13-02-2017_13h.14m.46s/
  ```

#### To benchmark our algorithm you can simply launch algo_benchmark.py as:

  ```text
  $ python algo_benchmark.py
  nb_parallel_executions 1
  nb_executions_per_grid_size 4

  launching benchmark...
  [Error 183] Cannot create a file when that file already exists: './gen/'
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.36m.53s/
  No Solution Look at the logbook.
  0 	| test_4pieces.txt 	| resolution time: 0:00:16.057000
  [Error 183] Cannot create a file when that file already exists: './gen/'
  ord() expected a character, but string of length 0 found
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.37m.09s/
  No Solution Look at the logbook.
  1 	| test_4pieces.txt 	| resolution time: 0:00:16.368000
  [Error 183] Cannot create a file when that file already exists: './gen/'
  ord() expected a character, but string of length 0 found
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.37m.25s/
  No Solution Look at the logbook.
  2 	| test_4pieces.txt 	| resolution time: 0:00:16.205000
  [Error 183] Cannot create a file when that file already exists: './gen/'
  ord() expected a character, but string of length 0 found
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.37m.41s/
  No Solution Look at the logbook.
  3 	| test_4pieces.txt 	| resolution time: 0:00:16.149000

  computing stats from benchmark records...
  test_4pieces.txt 	| min: 0:00:16.057000 avg: 0:00:16.194750 max: 0:00:16.368000
  ```

## Codes

The e2pieces.txt file contains the pieces per line with direction ordered as (n, s, w, e).
For convienience we order them as (n, e, s, w).

We have now our class and function.
An Individual class in the ind.py file contain:
```python
>>> i = Ind(lambda x: (0, [1, 0, 0, 17]), None) # Represents the first line of the file
>>> i.mask([0, None, None, 0) # Returns True if the mask corresponds to the individual. We check here the 0 to the right side
False
>>> i.rotate() # Rotate the individual in clock wise (to check)

>>> i.count(0) # Returns the number of 0 in individual
2
>>> i[0]
1
>>> i[3]
17
```

Then some usefull functions in Puzzle:

```python
>>> Puzzle.fit_to_border # Rotate an individual until it corresponds to a mask
```

You can easily draw or save a Puzzle:

 ```python
 >>> eternity.draw(puzzle)
 >>> eternity.draw(puzzle.population)
 >>> eternity.save(puzzle, gen=0)
 >>> eternity.save(puzzle, gen=1)
 ```



