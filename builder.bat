REM Create Pyinstaller executable, requires all packages as per rCap env
REM call conda env create -f rCap_env.yml
REM call conda activate rCap
pyinstaller --onefile --name Capacity_Calculator execution.py