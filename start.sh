#!/bin/bash
export $(grep -v '^#' config.env | xargs)
python3 motivator.py
