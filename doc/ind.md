# ind

Use to represent an individual a 4 int direction and a rotation. (and an uid to keep the line reference)




# Class
## Ind(self, f, l)

The Individual reorganize the line in CLOCKWORK MOD (orange ?) so it can easily rotate them.


- uid: Represant the id of the tile for final pr[int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex)ing
- line: Line in order North South Weast East.

### \_mask_(self, mask, c_index=0)

return True if the mask is ok with the content

- mask: [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of None and 0

- return:



### best_value_of_mask(self, mask)


- mask:

- return:



### count(self, obj)

Use to count how many occurencences of the color in the current ind

- obj:

- return:



### mask(self, mask, c_index=0)






### rotate(self)






### rotates(self, nb)








# Functions


### get_population()

Load the basic Population from the file e2pieces.txt


- return: a [list](https://docs.python.org/2/tutorial/datastructures.html#more-on-lists) of [int](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-[float](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex)-long-complex)

