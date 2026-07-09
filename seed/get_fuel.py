import pandas as pd

data = {
    'Date': ['2024-01-01', '2024-01-08', '2024-01-15', '2024-01-22', '2024-01-29'],
    'Gasoline_All_Grades': [3.089, 3.078, 3.058, 3.076, 3.095],
    'Diesel_All_Types': [3.876, 3.828, 3.863, 3.838, 3.867]
}

df = pd.DataFrame(data)

output_path = 'data/raw/fuel_sample.csv'
df.to_csv(output_path, index=False)
