#!/bin/bash

OUT="example.tex"

cat preamble.tex > $OUT

echo "\\begin{document}" >> $OUT

for FILE in $(ls *.txt)
do
    python3 ../truthtable.py $FILE >> $OUT
    echo "" >> $OUT
    echo "\\vspace{1cm}" >> $OUT
    echo "" >> $OUT
done

#python3 ../truthtable.py 1.txt >> 

echo "\\end{document}" >> $OUT

pdflatex $OUT

rm $OUT *.log *.aux
