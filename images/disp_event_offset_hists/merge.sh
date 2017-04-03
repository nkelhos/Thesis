#!/usr/bin/env bash
montage Cut-NTel2-ExtendedSource-Hard.sgra.GeomDispComparison.eventoffsethist.png Cut-NTel2-ExtendedSource-Hard.crab.GeomDispComparison.eventoffsethist.png -tile x1 -geometry +2+2 disp_event_offset_hist.png
convert disp_event_offset_hist.png disp_event_offset_hist.eps
