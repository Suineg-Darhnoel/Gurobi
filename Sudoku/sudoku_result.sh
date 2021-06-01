#!/bin/bash

SOLUTION_FILE=$1
awk '{if ($2!=0) print $0}' $SOLUTION_FILE | sort
