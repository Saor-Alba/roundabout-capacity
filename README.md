# Roundabout Capacity Model
Python implementation of the UK Model for theoretical roundabout junction capacity

## Excel Frontend Process
1. Double click 'Create_exe.bat' to begin the pyinstaller exe creation process.
    * This will also install all required packages as per the 'rCap_env.yml' conda environment file.
2. Once created, enter parameters in the '/dist/Junction_Capacity_Calculator.xlsx' file, and paste an OD as per instructions.
3. Double click 'Capacity_Calculator.exe' to run the process.
4. This process will update the '/dist/Junction_Capacity_Calculator.xlsx' spreadsheet with your result.

### TODO:
#### execution.py
- Implement an execution of the model, consider some sort of UI?
#### modules.calibration.py
- Method for calibration target -> PCU or Queue

#### modules.optimiser.py
- Method to evaluate have much additional development traffic can be accommodated
- Translate the optimiser to a general optimiser such that it can be used on any variables