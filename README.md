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

¯\\_(ツ)_/¯

## Structure

¯\\_(ツ)_/¯
