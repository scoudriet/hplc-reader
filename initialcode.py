''' CSCI 203 Final Project
Shane Coudriet
Hannah Sims
HPLC Calculation and Ploting software
'''

import csv
import matplotlib.pyplot as plt

def readPoints(filename):
    """
    Reads a data file starting from 'Inj. No. 2', extracts 'Area' as x-values, 
    and prompts the user for the corresponding y-values (concentrations).
    Returns two lists: x_values (Areas) and y_values (Concentrations).
    """
    x_values = []
    y_values = []

    try:
        # Process the file
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')  # Assuming tab-separated values
            next(reader)  # Skip the header line
            
            for line in reader:
                columns = line[0].split('\t')  # Split columns
                try:
                    inj_no = columns[0]
                    
                    # Skip rows before "Inj. No. 2"
                    if not inj_no.isdigit() or int(inj_no) < 2:
                        continue
                    
                    area = float(columns[6])  # Area column
                    concentration = float(input(f"Enter the concentration for Area {area}: "))
                    
                    x_values.append(area)
                    y_values.append(concentration)
                except (ValueError, IndexError):
                    # Skip rows with invalid data
                    continue
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return x_values, y_values


def plotCalibration(xpts,ypts):
    

    plt.plot(x, y, 'o-', label='Calibration Data')
    plt.xlabel('Area')
    plt.ylabel('Concentration')
    plt.title('Calibration Curve')
    plt.legend()
    plt.show()



def getUnknowConcentrations(unkonws):
    pass



def printFinalReport(CalPlot,unkonwsFound, calPts):
    pass
