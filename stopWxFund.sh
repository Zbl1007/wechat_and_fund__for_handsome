#!/bin/bash
app_name='main.py'
ps -ef | grep ${app_name} | grep -v grep| awk '{print $2}' | xargs kill -9
