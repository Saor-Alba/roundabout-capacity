REM Create Pyinstaller executable, requires all packages as per rCap env
call conda env create -f rCap_env.yml
call conda activate rCap
pyinstaller --onefile --name Capacity_Calculator execution.py