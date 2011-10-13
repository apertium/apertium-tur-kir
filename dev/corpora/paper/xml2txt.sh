#!/bin/bash

mkdir kywp
pushd kywp
ln -s ../kywp.xml ./
popd
../xml2txt.py kywp kywp.txt

mkdir rferl
pushd rferl
ln -s ../rferl.xml ./
popd
../xml2txt.py rferl rferl.txt

