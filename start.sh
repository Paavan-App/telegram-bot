#!/bin/bash
echo "Starting 5 processes of main.py"
for i in {1..5}
  do
      python main.py "$i"
  done
    echo "Started " + "$i" + " processes of main.py"

