import pandas as pd

# Load the xlsx file
excel_data = pd.read_excel('/home/harshad/Downloads/dividends-QG4344-2020_2021.xlsx')
data = excel_data.values

print("The content of the file is:\n", data)
