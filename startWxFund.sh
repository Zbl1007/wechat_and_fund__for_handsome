#!/bin/bash
app_name='main.py'
nohup python3 ${app_name}>startLog.out 2>&1 &
