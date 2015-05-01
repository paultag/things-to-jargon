#!/usr/bin/env python

with open("Glossary", 'r') as fd:
    for line in (x.rstrip() for x in fd):
        if line == "" or line.startswith(" ") or line.startswith("\t"):
            print(line)
            continue
        print(":{}:".format(line))
