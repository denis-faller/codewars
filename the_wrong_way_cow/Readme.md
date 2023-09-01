Have you ever noticed that cows in a field are always facing in the same direction?

Reference: http://bfy.tw/7fgf

Well.... not quite always.

One stubborn cow wants to be different from the rest of the herd - it's that damn Wrong-Way Cow!

Task
Given a field of cows find which one is the Wrong-Way Cow and return her position.

Notes:

There are always at least 3 cows in a herd
There is only 1 Wrong-Way Cow!
Fields are rectangular
The cow position is zero-based [x,y] of her head (i.e. the letter c)
There are no diagonal cows -- they only face North/South/East/West (i.e. up/down/right/left)
Examples
Ex1

cow.cow.cow.cow.cow
cow.cow.cow.cow.cow
cow.woc.cow.cow.cow
cow.cow.cow.cow.cow
Answer: [6,2]

Ex2

c..........
o...c......
w...o.c....
....w.o....
......w.cow
Answer: [8,4]

Notes
The test cases will NOT test any situations where there are "imaginary" cows, so your solution does not need to worry about such things!

To explain - Yes, I recognise that there are certain configurations where an "imaginary" cow may appear that in fact is just made of three other "real" cows. In the following field you can see there are 4 real cows (3 are facing south and 1 is facing north). There are also 2 imaginary cows (facing east and west).

But such a field will never be tested by this Kata.

...w...
..cow..
.woco..
.ow.c..
.c.....