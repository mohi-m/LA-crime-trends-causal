import pandas as pd

crime_data_2020_to_present = pd.read_csv('data/Crime_Data_from_2020_to_Present_20250303.csv')
crime_data_2010_to_2019 = pd.read_csv('data/Crime_Data_from_2010_to_2019_20250304.csv')

crime_data = pd.concat([crime_data_2020_to_present, crime_data_2010_to_2019], ignore_index=True)

def preprocess_crime_data(crime_data):
    columns_of_interest = [
    "Date Rptd",  # Date reported (date)
    "DATE OCC",  # Date occurred (date)
    "TIME OCC",  # Time occurred (time in military format)
    "AREA NAME",  # Area name (text)
    "Rpt Dist No",  # Reporting District Number (number but should be treated as categorical)
    "Crm Cd Desc",  # Crime Code Description (text)
    "Vict Age",  # Victim Age (number)
    "Vict Sex",  # Victimes Sex (char) F - Female M - Male X - Unknown H - ?
    "Vict Descent",  # Descent Code (char) A - Other Asian B - Black C - Chinese D - Cambodian F - Filipino G - Guamanian H - Hispanic/Latin/Mexican I - American Indian/Alaskan Native J - Japanese K - Korean L - Laotian O - Other P - Pacific Islander S - Samoan U - Hawaiian V - Vietnamese W - White X - Unknown Z - Asian Indian
    "Premis Desc",  # Premises Description (text)
    "Weapon Desc",  # Weapon Description (text)
    "Status Desc",  # Status of the case (text)
    # Not using the following columns for now
    # "LOCATION",  # Street address of crime incident rounded to the nearest hundred block to maintain anonymity (text)
    # "Cross Street",  # Cross Street (text)
    # "LAT",  # Latitude (number)
    # "LON",  # Longitude (number)
]

# Select columns of interest
    crime_data = crime_data[columns_of_interest]

# Handle missing values
    median_age = crime_data[crime_data['Vict Age'] > 0]['Vict Age'].median()
    crime_data['Vict Age'] = crime_data['Vict Age'].apply(lambda x: median_age if x < 1 else x)
    crime_data['Vict Sex'] = crime_data['Vict Sex'].replace(["", "-", None, "Unknown", "H", "X"], "Unknown")
    crime_data['Vict Descent'] = crime_data['Vict Descent'].replace(["", None, "Unknown", "X"], "Unknown")
    crime_data['Premis Desc'] = crime_data['Premis Desc'].replace(["", None, "Unknown"], "Unknown")
    crime_data['Weapon Desc'] = crime_data['Weapon Desc'].replace(["", None, "Unknown"], "Unknown")

# Convert date columns to datetime
    crime_data['Date Rptd'] = pd.to_datetime(crime_data['Date Rptd'])
    crime_data['DATE OCC'] = pd.to_datetime(crime_data['DATE OCC'])

    crime_data = crime_data[crime_data['DATE OCC'] < pd.to_datetime('2023-01-02')]
    return crime_data

cleaned_crime_data = preprocess_crime_data(crime_data)

# Crime categories
violent_crimes = [
    'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT', 'BATTERY - SIMPLE ASSAULT',
    'INTIMATE PARTNER - SIMPLE ASSAULT', 'INTIMATE PARTNER - AGGRAVATED ASSAULT',
    'ROBBERY', 'ATTEMPTED ROBBERY', 'OTHER ASSAULT', 'CRIMINAL HOMICIDE',
    'CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT', 'CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT',
    'MANSLAUGHTER, NEGLIGENT', 'ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER',
    'BATTERY POLICE (SIMPLE)', 'BATTERY WITH SEXUAL CONTACT', 'STALKING'
]

theft_crimes = [
    'VEHICLE - STOLEN', 'BIKE - STOLEN', 'BURGLARY', 'BURGLARY FROM VEHICLE', 
    'BURGLARY FROM VEHICLE, ATTEMPTED', 'VEHICLE - ATTEMPT STOLEN',
    'SHOPLIFTING-GRAND THEFT ($950.01 & OVER)', 'SHOPLIFTING - PETTY THEFT ($950 & UNDER)',
    'BUNCO, GRAND THEFT', 'BUNCO, PETTY THEFT', 'BUNCO, ATTEMPT', 'PURSE SNATCHING', 
    'PURSE SNATCHING - ATTEMPT', 'PICKPOCKET', 'PICKPOCKET, ATTEMPT',
    'THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD',
    'THEFT PLAIN - PETTY ($950 & UNDER)', 'THEFT PLAIN - ATTEMPT',
    'THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)', 
    'THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)', 'THEFT FROM MOTOR VEHICLE - ATTEMPT',
    'THEFT, PERSON', 'THEFT OF IDENTITY', 'THEFT FROM PERSON - ATTEMPT',
    'THEFT, COIN MACHINE - PETTY ($950 & UNDER)', 'THEFT, COIN MACHINE - GRAND ($950.01 & OVER)',
    'THEFT, COIN MACHINE - ATTEMPT', 'TILL TAP - GRAND THEFT ($950.01 & OVER)',
    'TILL TAP - PETTY ($950 & UNDER)', 'DISHONEST EMPLOYEE - GRAND THEFT', 
    'DISHONEST EMPLOYEE - PETTY THEFT', 'DISHONEST EMPLOYEE ATTEMPTED THEFT',
    'DEFRAUDING INNKEEPER/THEFT OF SERVICES, $950 & UNDER', 
    'DEFRAUDING INNKEEPER/THEFT OF SERVICES, OVER $950.01'
]

fraud_crimes = [
    'CREDIT CARDS, FRAUD USE ($950.01 & OVER)', 'CREDIT CARDS, FRAUD USE ($950 & UNDER)',
    'DOCUMENT FORGERY / STOLEN FELONY', 'DOCUMENT WORTHLESS ($200.01 & OVER)',
    'DOCUMENT WORTHLESS ($200 & UNDER)', 'GRAND THEFT / INSURANCE FRAUD',
    'UNAUTHORIZED COMPUTER ACCESS', 'EXTORTION', 'BRIBERY'
]

sexual_crimes = [
    'RAPE, FORCIBLE', 'RAPE, ATTEMPTED', 'SODOMY/SEXUAL CONTACT B/W PENIS OF ONE PERS TO ANUS OTH',
    'SEXUAL PENETRATION W/FOREIGN OBJECT', 'BATTERY WITH SEXUAL CONTACT',
    'INDECENT EXPOSURE', 'LEWD CONDUCT', 'ORAL COPULATION', 'PEEPING TOM',
    'CHILD PORNOGRAPHY', 'LEWD/LASCIVIOUS ACTS WITH CHILD', 'CHILD ANNOYING (17YRS & UNDER)',
    'SEX OFFENDER REGISTRANT OUT OF COMPLIANCE', 'HUMAN TRAFFICKING - COMMERCIAL SEX ACTS',
    'HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE', 'INCEST (SEXUAL ACTS BETWEEN BLOOD RELATIVES)',
    'SEX,UNLAWFUL(INC MUTUAL CONSENT, PENETRATION W/ FRGN OBJ)'
]

property_crimes = [
    'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)', 
    'VANDALISM - MISDEAMEANOR ($399 OR UNDER)', 'TRESPASSING', 'ILLEGAL DUMPING', 
    'RECKLESS DRIVING', 'FIREARMS RESTRAINING ORDER (FIREARMS RO)',
    'FIREARMS EMERGENCY PROTECTIVE ORDER (FIREARMS EPO)', 
    'WEAPONS POSSESSION/BOMBING', 'DISCHARGE FIREARMS/SHOTS FIRED', 
    'SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT', 'SHOTS FIRED AT INHABITED DWELLING', 
    'THROWING OBJECT AT MOVING VEHICLE'
]

child_crimes = [
    'CHILD STEALING', 'KIDNAPPING', 'KIDNAPPING - GRAND ATTEMPT', 
    'CHILD ABANDONMENT', 'CHILD NEGLECT (SEE 300 W.I.C.)', 'CRM AGNST CHLD (13 OR UNDER) (14-15 & SUSP 10 YRS OLDER)'
]

arson_and_explosives = [
    'ARSON', 'BOMB SCARE'
]

public_disorder = [
    'DISTURBING THE PEACE', 'CONTEMPT OF COURT', 'VIOLATION OF COURT ORDER',
    'VIOLATION OF TEMPORARY RESTRAINING ORDER', 'VIOLATION OF RESTRAINING ORDER',
    'THREATENING PHONE CALLS/LETTERS', 'CRIMINAL THREATS - NO WEAPON DISPLAYED',
    'FALSE POLICE REPORT', 'BLOCKING DOOR INDUCTION CENTER', 'FAILURE TO YIELD',
    'FAILURE TO DISPERSE', 'INCITING A RIOT', 'PROWLER'
]

conspiracy_and_other = [
    'CONSPIRACY', 'TRAIN WRECKING', 'LYNCHING', 'LYNCHING - ATTEMPTED', 'BIGAMY'
]

animal_crimes = [
    'CRUELTY TO ANIMALS', 'BEASTIALITY, CRIME AGAINST NATURE SEXUAL ASSLT WITH ANIM'
]

drug_related_crimes = [
    'DRUGS, TO A MINOR', 'DRUNK ROLL', 'DRUNK ROLL - ATTEMPT'
]

# Add a new column to the dataset to categorize the crimes
cleaned_crime_data['Crime Category'] = "Other"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(violent_crimes), 'Crime Category'] = "Violent Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(theft_crimes), 'Crime Category'] = "Theft Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(fraud_crimes), 'Crime Category'] = "Fraud Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(sexual_crimes), 'Crime Category'] = "Sexual Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(property_crimes), 'Crime Category'] = "Property Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(child_crimes), 'Crime Category'] = "child_crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(arson_and_explosives), 'Crime Category'] = "Arson & Explosives"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(public_disorder), 'Crime Category'] = "Public Disorder Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(conspiracy_and_other), 'Crime Category'] = "Conspiracy & Miscellaneous"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(animal_crimes), 'Crime Category'] = "Animal Crimes"
cleaned_crime_data.loc[cleaned_crime_data['Crm Cd Desc'].isin(drug_related_crimes), 'Crime Category'] = "Drug-Related Crimes"


lapd_to_census = {
    'Wilshire': 'Los Angeles',
    'Central': 'Los Angeles',
    'Southwest': 'Los Angeles',
    'Van Nuys': 'San Fernando Valley',
    'Hollenbeck': 'Los Angeles',
    'Rampart': 'Los Angeles',
    'Newton': 'Los Angeles',
    'Northeast': 'Los Angeles',
    '77th Street': 'Los Angeles',
    'Hollywood': 'Los Angeles',
    'Harbor': 'South Bay Cities',
    'West Valley': 'San Fernando Valley',
    'West LA': 'Los Angeles',
    'N Hollywood': 'San Fernando Valley',
    'Pacific': 'Santa Monica',
    'Devonshire': 'San Fernando Valley',
    'Mission': 'San Fernando Valley',
    'Southeast': 'South Gate-East Los Angeles',
    'Olympic': 'Los Angeles',
    'Foothill': 'San Fernando Valley',
    'Topanga': 'San Fernando Valley'
}

# Map LAPD area names to census areas
cleaned_crime_data['Area'] = cleaned_crime_data['AREA NAME'].map(lapd_to_census)
cleaned_crime_data['Area'] = cleaned_crime_data['Area'].fillna('Other')

# Resample the data at a weekly level
weekly_crime_data = cleaned_crime_data.copy()

# Add a 'Date' column to group by week ending on Sunday
weekly_crime_data['Date'] = (weekly_crime_data['DATE OCC'] + pd.offsets.Week(weekday=6)).dt.floor('D')

# Group by 'Date' and 'Area', and count each crime category
weekly_summary = weekly_crime_data.groupby(['Date', 'Area', 'Crime Category']).size().unstack(fill_value=0)

# Add a 'Total Crimes' column
weekly_summary['Total Crimes'] = weekly_summary.sum(axis=1)

# Reset the index to make it a flat DataFrame
weekly_summary = weekly_summary.reset_index()

# Save the weekly summary to a new CSV file
weekly_summary.to_csv('data/processed-data/weekly_crime_summary.csv', index=False)