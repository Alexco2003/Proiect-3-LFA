# Proiect 3 LFA -> NFA-LAMBDA to DFA
NFA-LAMBDA to DFA

Implemented a Python algorithm that gets as input a NFA-LAMBDA and transform it into a DFA

The NFA-LAMBDA input file needs to have the following layout :

n (total number of states)\
sigma (alphabet)\
initial state\
list of all the final states\
state symbol next_state (this represents the delta function, from state with symbol we get to next_state)

Example of input file :

7\
a b\
0\
2 6\
0 a 0\
0 a 1\
0 lambda 3\
0 b 2\
0 lambda 2\
1 lambda 2\
2 lambda 4\
2 a 3\
3 b 3\
3 lambda 5\
3 a 6\
3 b 6\
4 b 5\
4 a 6\
4 lambda 6\
5 b 2\
5 lambda 2\
5 lambda 6\
5 a 6\
6 b 6

The output file will have the following layout :

n (total number of states)\
sigma (alphabet)\
initial state\
list of all the final states\
state symbol next_state (this represents the delta function, from state with symbol we get to next_state)

Example of output :

3\
a b\
023456\
0123456 23456 023456\
023456 a 0123456\
023456 b 23456\
0123456 a 0123456\
0123456 b 23456\
23456 a 23456\
23456 b 23456
