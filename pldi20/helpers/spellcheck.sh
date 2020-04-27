#!/bin/bash

find ./text -name "*.tex" -exec aspell --lang=en --mode=tex check "{}" \;

