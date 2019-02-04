#!/usr/bin/env python
import re, glob

# A Simple script for detecting if any bibliography entries in citelist.bib are unused
# since latex will still add unused ones to the pdf

with open('citelist.bib','r') as f :
  lines = [ l.rstrip() for l in f.readlines() ]

keys = []
for lin in lines :
  if lin.startswith('@') :
    print(lin)
    p = re.search('{(\w+)',lin)
    if p :
      keys += [ p.group(1) ]
print(keys)

thesis = []
for fname in glob.glob('chapter-*.tex') :
  with open( fname, 'r') as f :
    thesis += [ l.rstrip() for l in f.readlines() ]

for k in keys :
  found = False
  for lin in thesis :
    if k in lin :
      found = True
      break
  if not found :
    print('could not find key %s anywhere...'%k)
