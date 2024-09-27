#!/bin/bash

cdsupdate --log info example3.log --period 2023-04-01/2023-04-30 --cvar HImax --area India,67,98,6,36 --keep-hourly --output-dir data/

