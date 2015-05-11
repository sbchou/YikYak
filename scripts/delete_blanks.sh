#!/bin/sh
files="../data/text/*.csv"
for i in $files
do
      sed '/^$/d' $i > $i.out
        mv  $i.out $i
    done
     
