# LA Crime Trends Causal Analysis

This project analyzes crime trends in Los Angeles and surrounding areas, combining crime data with demographic information to explore potential causal relationships.

## Project Overview

The analysis covers multiple regions including:

- Los Angeles
- San Fernando Valley
- Santa Monica
- South Bay Cities
- South Gate-East Los Angeles

## Data Sources

### Crime Data

- LA Crime Data from 2010 to 2019
- LA Crime Data from 2020 to Present
- Crime categories include:
  - Violent Crimes
  - Theft Crimes
  - Sexual Crimes
  - Property Crimes
  - Fraud Crimes
  - Public Disorder Crimes
  - Drug-Related Crimes
  - Child-Related Crimes
  - Animal Crimes
  - Arson & Explosives
  - Other Categories

### Demographic Data

- American Community Survey (ACS) Data:
  - DP05: Demographic and Housing Estimates (2010-2023)
  - S1401: School Enrollment Data (2010-2023)

## Project Structure

```
├── data/
│   ├── processed-data/
│   │   ├── DP05_combined.csv       # Processed demographic data
│   │   ├── S1401_combined.csv      # Processed school enrollment data
│   │   └── weekly_crime_summary.csv # Processed weekly crime statistics
│   └── raw-data/
│       ├── DP05/                   # Raw demographic data files
│       ├── LA_crime_data/          # Raw crime data files
│       └── S1401/                  # Raw school enrollment data files
├── crime_processing.py             # Crime data processing script
├── DP05_processing.py             # Demographic data processing script
├── S1401_processing.py            # School enrollment processing script
└── Causal_Analysis_Notebook.ipynb # Main analysis notebook
```

## Data Processing

The project includes several Python scripts for data processing:

- `crime_processing.py`: Processes and categorizes crime data into weekly summaries
- `DP05_processing.py`: Processes demographic data from ACS DP05 datasets
- `S1401_processing.py`: Processes school enrollment data from ACS S1401 datasets

## Analysis

The main analysis is conducted in `Causal_Analysis_Notebook.ipynb`, which combines the processed datasets to explore relationships between demographic factors and crime trends across different areas of Los Angeles.
