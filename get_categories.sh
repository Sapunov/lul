#!/bin/bash

cat messages/* | awk -F ';' '{print $2}' | sort | uniq
