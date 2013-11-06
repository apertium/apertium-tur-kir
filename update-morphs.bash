#!/bin/bash

# Assuming that you have the whole apertium tree in your source dir and you are in tur-kir directory.

# You have to compile apertium-tur and apertium-kir first.

cp ../../incubator/apertium-tur/tur.automorf.att.gz apertium-tur-kir.tur-kir.LR.att.gz
cp ../../incubator/apertium-tur/tur.autogen.att.gz apertium-tur-kir.kir-tur.RL.att.gz
cp ../../languages/apertium-kir/kir.automorf.att.gz apertium-tur-kir.kir-tur.LR.att.gz
cp ../../languages/apertium-kir/kir.autogen.att.gz apertium-tur-kir.tur-kir.RL.att.gz

DIFF=$(diff ../../incubator/apertium-tur/apertium-tur.tur.rlx apertium-tur-kir.tur-kir.rlx)
if [ "$DIFF" != "" ]; then
        cp ../../incubator/apertium-tur/apertium-tur.tur.rlx apertium-tur-kir.tur-kir.rlx
fi;

DIFF=$(diff ../../languages/apertium-kir/apertium-kir.kir.rlx apertium-tur-kir.kir-tur.rlx)
if [ "$DIFF" != "" ]; then
        cp ../../languages/apertium-kir/apertium-kir.kir.rlx apertium-tur-kir.kir-tur.rlx
fi;

exit 0


