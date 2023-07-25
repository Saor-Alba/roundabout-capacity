@echo off

(call install)2>&1>"logfile.log"

py -m venv env
.\env\scripts\activate
pip install .
builder.bat