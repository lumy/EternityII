
# Eternity II

## Introduction

  some research have been made have a look at our gdoc (link is coming)

## Setup

### requirements

  using pip

  ```bash
  $ pip install -r requirements.txt
  ```

  Download the [images](https://intra.epitech.eu/module/2016/M-IAR-752/PAR-9-2/acti-235553/project/file/eternityII_data.zip)
  and unzip it in the working directory.

### configuration and population



## Codes

The e2pieces.txt contain the pieces per line by direction as (n, s, w, e)
for easier use we sort them as (n, e, s, w).

We have now very usefull class and function.
An Individual in the ind.py file contain:
```python
$ i = Ind(lambda x: (0, [1, 0, 0, 17]), None) # Represent the firt line of the file
$ i.mask([0, None, None, 0) # return True if the mask correspond to the ind. we check here the 0 to the right side.
False
$ i.rotate() # Rotate the ind in clock way (to check)

$ i.count(0) # Return the number of 0 in ind
2
$
```

Then some usefull in Puzzle:

```python
$ Puzzle.fit_to_border # rotate an ind until it correspond to a mask
```

You can easily draw or save a Puzzle:

 ```python
 $ eternity.draw(puzzle)
 $ eternity.draw(puzzle.population)
 $ eternity.save(puzzle, gen=0)
 $ eternity.save(puzzle, gen=1)
 ```

And finally have a look at our runner __call__ method:
```python
  def __call__(self, *args, **kwargs):
    pop = self.get_population(kwargs.get("verbose", False))

    for i in range(0, kwargs.get("evals", CONFIG.NGEN)):

      # We May be Preselecting some puzzle to save and "Reproduce"

      for puzzle in pop:
        puzzle.save_picture(gen=i)
        puzzle.select()
        puzzle.mutate(config.mutate_inpd)
      self.crossover()
      fitnesses = self.eval(pop, eval=i, verbose=True)

      record = self.stats.compile(pop)
      self.logbook.record(eval=i, fitnesses=fitnesses, population=pop, **record)
      self.famous.update(pop)


    gen = self.logbook.select("eval")
    #self.logbook.header = "population"
    fits = self.logbook.select("fitnesses")
    self.generate_graph(gen, fits)
    map(lambda x: x.writeLogbook(), pop)
    with open("gen/%s/logbook.txt" % self.pid, "w") as f:
      f.write(str(self.logbook))
```