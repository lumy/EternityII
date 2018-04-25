## ind

 - Load all tils.

 - Ind objet is the representation of a unique tile. See [Ind](#Ind) description.

A schema is an int representing a color/schema for a til.

### mask-description
      
A mask is a list of None (No-Color specify) or a schema (0 is border: grey)

eg: [None, None, 1, 1]



## Class
### Ind(self, func, lines)

Ind class represent a til:

- Ind.uid unique id for schema repr
- Ind.content list int [schema:int, schema:int, schema:int, schema:int] directions in order North Est South Weast
- Ind.rotation number of clockwork rotation apploied (range 0, 3)



The func, lines args are actually gonna be change, for an iterator or for simple uid,content, rotation arguments.
The idea was to not initialize on the file but on randomized lines.


- func: function that take lines in params and return one line -> uid, [North-schema South-schema Weast-schema East-schema].
- lines: Lines|arg to be given to func

#### \_mask_(self, mask, c_index=0)


- mask: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of None and 0.
- c_index: See [Mask](#mask)

- return: value of fitness [0-4].



#### best_value_of_mask(self, mask)

Find the best value possible for a mask.

- mask: mask to test against.

- return: value between 0 and 4 that represant individual connection/score.



#### count(self, obj)

Use to count how many occurencences of the schema in the current ind

- obj:

- return:



#### mask(self, mask, c_index=0)

test a [Mask](#mask-description)

- mask: [Mask](#mask-description)
- c_index: index content to start at, this simulate rotation.

- return: True if the mask fit.



#### rotate(self)

Rotate the ind.




#### rotates(self, nb)


- nb: rotates nb times.





## Functions


#### get_population()

Load the basic Population from the file e2pieces.txt


- return: a [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of (UID:[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex), [schema:[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex), schema:[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex), schema:[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex), schema:[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex)]

