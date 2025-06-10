#!/bin/bash

for filename in *.ui; do 
    rm ../ui/${filename%.ui}_ui.py 2> /dev/null
    pyuic6 ${filename} -o ../ui/${filename%.ui}_ui.py;
done
