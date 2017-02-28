
# Eternity II

## Introduction

  [Current Algorithm](doc/Algorithm.md)

## Setup

### requirements

  using pip

  ```bash
  $ pip install -r requirements.txt
  ```

  Download the [images](https://intra.epitech.eu/module/2016/M-IAR-752/PAR-9-2/acti-235553/project/file/eternityII_data.zip)
  and unzip it in the working directory.

### configuration and population

The config file config.py got a lot of interesting setting:

```python
population_file_base="e2pieces.txt"
NGEN = 2000
mutate_inpd=0.01
selection_ind_value_step=1
elitism_percentage_start=10
elitism_percentage_up=4
gen_modulo_elitism=100
```

- population_file_base: filename containing the tils to play with.
  - Few file have been wrote alyready `test_4pieces.txt` `test_9pieces.txt` `test_16pieces.txt`
- NGEN: Number of default iteration to do. See [iteration](doc/Algorithm.md#iteration)
- mutate_inpd: Percentage of mutation. (between 0 and 1) See [iteration](doc/Algorithm.md#mutation)

### Workflows. Running Scripts


#### The workflow starts by running the script called main then the script render

  ```text
  $ python main.py
  [Error 183] Cannot create a file when that file already exists: './gen/'
  Personal Path used for this Puzzle: gen/lumy_13-02-2017_13h.14m.46s/
  No Solution Look at the logbook.
  ```

#### Look at the path given for your puzzle. All the stats will be looged there.

  ``` text
  $ python render.py gen/lumy_13-02-2017_13h.14m.46s/
  (it take few time before an ouput arrive because it's loading big binary file).
  progression Bar 1 #################
  progression Bar 2 ########________#
  ```
  > If you do not see any progressbar it might be because you're not in a real tty
  (the package we use seems to work perfectly under all unix/linux but seems
  still in dev for windows and others).

#### Generate video if you have ffmpeg.
  ``` text
  $ ./gen/generations_images_to_video.bash gen/lumy_13-02-2017_13h.14m.46s/
  ```

#### benchmark our algorithm you can simply launch algo_benchmark.py as:

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

The e2pieces.txt contain the pieces per line by direction as (n, s, w, e)
for easier use we sort them as (n, e, s, w).

We have now very usefull class and function.
An Individual in the ind.py file contain:
```python
>>> i = Ind(lambda x: (0, [1, 0, 0, 17]), None) # Represent the firt line of the file
>>> i.mask([0, None, None, 0) # return True if the mask correspond to the ind. we check here the 0 to the right side.
False
>>> i.rotate() # Rotate the ind in clock way (to check)

>>> i.count(0) # Return the number of 0 in ind
2
>>> i[0]
1
>>> i[3]
17
```

Then some usefull in Puzzle:

```python
>>> Puzzle.fit_to_border # rotate an ind until it correspond to a mask
```

You can easily draw or save a Puzzle:

 ```python
 >>> eternity.draw(puzzle)
 >>> eternity.draw(puzzle.population)
 >>> eternity.save(puzzle, gen=0)
 >>> eternity.save(puzzle, gen=1)
 ```



