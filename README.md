# truthtable
A LaTeX truthtable generator.

truthtable reads in a logical expression and generates from that a LaTeX tabular truthtable listing the evaluations of the given formula and all it's parts for all possible input combinations.

## Example
`\neg a \AND b` generates

| a | b | &not; | a | &and; | b |
|---|---|-------|---|-------|---|
| `0` | `0` | 1 | 0 | **0** | 0 | 
| `0` | `1` | 1 | 0 | **1** | 1 | 
| `1` | `0` | 0 | 1 | **0** | 0 | 
| `1` | `1` | 0 | 1 | **0** | 1 |

For more examples, look into the [example folder](../master/example).

## Input Syntax
The program supports a number of logical operators and their notation:
- disjunction
  - `or`, `|`, `\or`, `\vee`, `\lor`
- conjunction
  - `and`, `&`, `\and`, `\wedge`, `\land`
- negation
  - `not`, `!`, `\neg`, `\lnot`
- xor
  - `xor`, `^`, `\oplus`, `\veebar`
- implication
  - `>`, `\imp`, `\rightarrow`, `\implies`
- equivalence
  - `=`, `\aeq`, `\leftrightarrow`
  
Please note that the output will use the same token representation as your input.

## Running the program. 

The expression for which the truthtable is to be build is input via one of two ways:
1. first line of the standard input
```
$ python3 truthtable.py
a or b
[output is printed...]
```
2. a file
```
$ python3 truthtable.py examples/1.txt
[output is printed...]
```
3. commandline argument
```
$ python3 truthtable.py "a or b"
[output is printed...]
```

## Structure

¯\\_(ツ)_/¯
