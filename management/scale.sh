#! /bin/bash

source monitor/venv/bin/activate

./scaleScanner.py run --monitor-interval=10 --max-scanners=20 
