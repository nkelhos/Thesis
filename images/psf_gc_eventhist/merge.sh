#!/usr/bin/env bash

montage ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.sgra.eventpsfhist.png ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.crab.eventpsfhist.png -tile x1 -geometry +2+2 eventpsfhist.png
convert eventpsfhist.png eventpsfhist.eps

