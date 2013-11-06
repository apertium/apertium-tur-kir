#!/bin/bash

C=2
GREP='.'
if [ $# -eq 1 ]
then
    C=$1
    GREP='WORKS'
fi

bash wiki-tests.sh Pending tur kir update | grep -C $C "$GREP"

#bash wiki-tests.sh Pending kir tur update | grep -C $C "$GREP"

