import os
import numpy as np
import xlwings as xw
from dataclasses import dataclass, field

@dataclass
class Data_Input:
    """
    Define class to capture geometry parameters and od matrix
    """
    fpath: str = os.path.abspath("Junction_Capacity_Calculator.xlsx")
    
    def main(fpath=fpath):
        # Initiate xw app and workbook
        app = xw.App(visible=True)
        wb = xw.Book(fpath)

        # Define worksheet instance for Control and OD Input
        ctrl = wb.sheets["Control"]
        odin = wb.sheets["OD Input"]

        # Define dict of lookup cells and values for each parameter
        loc_dict = {"v": ["C10", 2.5, "C18", "Approach road half-width"],
                    "e": ["C11", 3.0, "C19", "Entry width"],
                    "l": ["C12", 0.0, "C20", "Effective flare length"],
                    "r": ["C13", 0.0, "C21", "Entry radius"],
                    "icd": ["C14", 28.0, "C22", "Inscribed circle diameter"],
                    "phi": ["C15", 0.0, "C23", "Conflict angle"]}  

        return app, wb, ctrl, odin, loc_dict  
        
    def import_params(ctrl, param, loc_dict):
        # Read parameter value
        val = ctrl[loc_dict[param][0]].value

        # Check bounds
        if val > loc_dict[param][1]:
            # If acceptable, return no warnings
            ctrl[loc_dict[param][2]].value = "No warnings advised"
        else:
            # If not, return specific warning
            ctrl[loc_dict[param][2]].value = f"Error. {loc_dict[param][3]} {val} falls below lower bound of {loc_dict[param][1]}"

        return val
    
    def import_od(ctrl, odin):
        # Find last completed row to identify number of arms
        lrow = odin.cells.last_cell.row
        yarms = odin.range((lrow, "A")).end('up').row - 1

        # Check this against the columns, to ensure symmetrical matrix
        lcol = odin.cells.last_cell.column
        xarms = odin.range(("1", lcol)).end('left').column - 1

        # If symmetrical matrix, no warnings.
        if yarms == xarms:
            ctrl["C24"].value = f"No warnings advised"
        else:
            # If not, return specific warning
            ctrl["C24"].value = f"Error. {yarms} origin arms and {xarms} destination arms. Matrix asymmetrical."

        # Use number of arms to read in matrix
        od = np.array(odin.range((2,2),(1+yarms, 1+xarms)).value)

        return od, yarms
    
    def print_out(app, wb, ctrl, rCap):
        # Print RFC to output workbook, close and save
        ctrl["B28"].value = rCap

        wb.save()
        wb.close()
        app.kill()


