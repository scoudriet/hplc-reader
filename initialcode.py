"""
Purpose: Reading HPLC Data From a CSV file
Author: Shane Coudriet & Hannah Sims
Date: December 4, 2024
CSCI 203, Fall 2024
"""

import csv
import matplotlib.pyplot as plt
import numpy as np


def readCalibrationPoints(filename):
    """Reads calibration standards from the specified CSV file.
    
    Parameters:
        filename: the name of the csv file that you would like to have read *must be in same folder as program
    Return value:
        areas: list of the peak areas directly from the CSV file
        Concentrations: the list of user entered values of known concentrations
    """
    areas = []
    concentrations = []

    
    dataFile = open(filename,'r', encoding = 'utf-8')
    for step in range(5): #skip the first five lines to get to the actual data
        header = dataFile.readline()
    numCal = int(input('Please enter the number of calibration points: '))
    for step in range(numCal):
        line = dataFile.readline()
        row = line.split(',')
        areas.append(float(row[6]))
        cons =  float(input('Please enter the concentration of the calibration standard: '))
        concentrations.append(cons)
    dataFile.close()
    return areas, concentrations, numCal

def plotCalibration(areas, concentrations):
    """Plots calibration curve with linear regression and R² value. This is also where the slope and y intercepts are calculated for later use
    
    Parameters:
        areas: list of the peak areas directly from the CSV file 
        Concentrations: the list of user entered values of known concentrations
    Return value:
            slope: this returns the float value of the slope of the best fit line
            y_intercept: this returns the float balue of the y intercept of the best fit line
            r_squared: this returns the R squared value of the line of best fit.
    """
    # Plot data points and regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(areas, concentrations, color='blue', label='Calibration Points')
    
    
    plt.xlabel('Area')
    plt.ylabel('Concentration (ppm)')
    plt.title('HPLC Calibration Curve')
    plt.legend()
    #calculate equation for trendline
    x = areas
    y = concentrations
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

#add trendline to plot
    plt.plot(x, p(x))
    # Fit the data to a linear model
    z = np.polyfit(areas, concentrations, 1)  # Degree 1 for linear fit
    p = np.poly1d(z)  # Create polynomial from coefficients

    # Calculate R-squared
    y_pred = p(areas)  # Predicted y-values from the trendline
    residuals = concentrations - y_pred
    ss_res = np.sum(residuals**2)  # Sum of squares of residuals
    ss_tot = np.sum((concentrations - np.mean(concentrations))**2)  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)  # Coefficient of determination
    print('The R squared value is', r_squared)
    # Add R² value to plot
    plt.text(0.05, 0.95, f'R² = {r_squared:.4f}', 
             transform=plt.gca().transAxes, 
             bbox=dict(facecolor='white', alpha=0.8))
    slope = z[0]
    y_intercept = z[1]
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
    return slope , y_intercept, r_squared

def findUnknown(slope, yint, numCal,filename):
    """
    Finds the unknown concetrations.
    Returns three lists: areas, sample names, and unknown concentrations.
    """
    areas = []
    unknowns = []
    sampleNames = []
    dataFile = open(filename,'r', encoding = 'utf-8')
    for step in range(6+numCal): #Skip the header and calibration points, start at the unknown samples.
        header = dataFile.readline()
    numSample = int(input('Please enter the number of samples in the trial : '))
    descion = input('Was there a dilution in this Y/N: ')
    if descion == 'Y' or descion == 'y':
        dilFact = int(input('What was the dilution in parts: '))
        assert dilFact > 0, f"number greater than 0 expected, got: {dilFact}"
        for step in range(numCal):
            line = dataFile.readline()
            row = line.split(',')
            sampleNames.append(row[1])
            areas.append(float(row[6]))
            unknown = dilFact*(slope * (float(row[6])) + yint)
            unknowns.append(unknown) 


    elif descion == 'N' or descion == 'n':
        for step in range(numCal):
            line = dataFile.readline()
            row = line.split(',')
            sampleNames.append(row[1])
            areas.append(float(row[6]))
            unknown = slope * (float(row[6])) + yint
            unknowns.append(unknown) 
    dataFile.close()
    return unknowns , areas , sampleNames

def writeReport(rsquare, areasCon, concentrations, areaUK, unknowns, sampleNames):
    """
    Writes and prints a report in a way that is legible and organized.
    Returns six lists: r squared, areas of known concentration, known concentrations, areas of unknown, unknown concentrations, and sample names.
    """
    output_file = "report.txt"
    

    file = open(output_file, "w")
    # Write the content to the file
    file.write("=== Analysis Report ===\n\n")
    file.write(f"R-Square Value: {rsquare}\n\n")
        
    file.write("=== AreasCon ===\n")
    for i, area in enumerate(areasCon):
        file.write(f"  {i+1}. {area}\n")
        
    file.write("\n=== Concentrations ===\n")
    for i, conc in enumerate(concentrations):
        file.write(f"  {i+1}. {conc}\n")
        
    file.write("\n=== AreaUK ===\n")
    file.write(f"  {areaUK}\n")
        
    file.write("\n=== Unknowns ===\n")
    for i, unknown in enumerate(unknowns):
        file.write(f"  {i+1}. {unknown}\n")
    file.write("\n=== Sample Names ===\n")
    for i, sample in enumerate(sampleNames):
        file.write(f"  {i+1}. {sample}\n")
        
    file.write("\n=== End of Report ===\n")
    
    # Notify the user that the file has been created
    print(f"Report written to '{output_file}'.") 
   
        




def main():
    filename = "data.csv"  # Using the provided CSV file
    areasCon, concentrations, numCal = readCalibrationPoints(filename)
    slope , y_intercept, r_squared = plotCalibration(areasCon, concentrations)
    unknowns , areasUK, sampleName = findUnknown(slope, y_intercept, numCal,filename )
    writeReport(r_squared, areasCon, concentrations, areasUK, unknowns, sampleName)
main()




