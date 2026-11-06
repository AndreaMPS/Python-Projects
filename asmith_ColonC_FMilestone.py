#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Install Faker Package
pip install faker


# In[2]:


#Import faker package & create funtion to assign colon cancer symptoms to patients
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()

def create_data(x):

    patient_data = {}

    #Initialize Screening Questions Options
    Bowel_changes = ['None', 'Constipation', 'Diarrhea', 'Diarrhea and Constipation']#Experienced Bowel Movement changes from norm or healthy movements
    Rectal_bleeding = ['Yes', 'No']#Experienced Rectal bleeding
    Family_history = ['Yes', 'No']#History of Colon Cancer
    Abdominal_pain = ['Yes', 'No']#Experienced pain in any quadrant of abdomen
    Iron_Deficiency_Anemia = ['Yes', 'No']#Experienced iron-deficiency anemia
    Unexplained_weight_loss = ['Yes', 'No']#Experienced unaccounted/involuntary weight loss

    for i in range(0,x):
        patient_data[i]= {}
        patient_data[i]['Name']= fake.name()
        patient_data[i]['Address']= fake.address()
        patient_data[i]['Birthdate']= fake.date_of_birth(minimum_age= 20, maximum_age = 44)#Target Population for screening survey
        patient_data[i]['Email Address']= fake.company_email()
        patient_data[i]['Bowel Changes']= np.random.choice(Bowel_changes)
        patient_data[i]['Rectal Bleeding'] = np.random.choice(Rectal_bleeding)
        patient_data[i]['Family History']= np.random.choice(Family_history)
        patient_data[i]['Abdominal Pain']= np.random.choice(Abdominal_pain)
        patient_data[i]['Iron Deficiency Anemia']= np.random.choice(Iron_Deficiency_Anemia)
        patient_data[i]['Unexplained Weight Loss']= np.random.choice(Unexplained_weight_loss)

    return patient_data#Return dataset with patient data and screening responses

#Compile Data and export into csv file called Patient Data
df = pd.DataFrame(create_data(50)).transpose()
df.to_csv('HCIP5376_PatientData.csv')
df.head()


# In[3]:


import csv

with open("HCIP5376_PatientData.csv") as patientdata:
    filtered = (line.replace('\n',' ') for line in patientdata) #Filtering through each line in the csv file to replace the newline character in the address variable with a space
    for row in csv.reader(filtered):
        ptname = row[1] #Storing patient's name in a variable
        ptemail = row[4] #Extracting patient emails so that an email can be sent to each patient
        ptsymptoms = row[5:] #Extracting the colon cancer variables for each patient

        ##Calculating bowel changes risk for each patient##

        if ptsymptoms[0] == 'None':
            bowelrisk = 0
        else:
            bowelrisk = 1 #Patients have risk factor associated with bowel changes if they have experienced diarrhea, constipation, or diarrhea and constipation.

        #Calculating patient risk for rectal bleeding

        if ptsymptoms[1] == 'Yes':
            bleedingrisk = 1

        else:
            bleedingrisk = 0

        #Calculating patient risk from family history
        if ptsymptoms[2] == 'Yes':
            familyhistory = 1 #Patients only have a risk from family history if they answered 'Yes'

        else:
            familyhistory = 0

        #Assigning patient risk from abdominal pain variable
        if ptsymptoms[3] == 'Yes':
            abdominalpain = 1

        else:
            abdominalpain = 0
            
        #Assigning patient risk from abdominal pain variable
        if ptsymptoms[4] == 'Yes':
            irondeficiencyanemia = 1

        else:
            irondeficiencyanemia = 0

        #Assigning patient risk from unexplained weight loss
        if ptsymptoms[5] == 'Yes':
            weightloss = 1

        else:
            weightloss = 0

        #Calculating a patient's total risk by summing the individual risk variables

        totalrisk = bowelrisk + bleedingrisk + familyhistory + abdominalpain + irondeficiencyanemia + weightloss


        #Patients recommended to pursue screening if they exhibit at least 60% of risk factors

        if totalrisk > 3:
            print(f"The patient, {ptname} at {ptemail}, is reccommended to pursue CRC screening")

        else:
            print(f"The patient, {ptname} at {ptemail}, is not reccommended to pursue CRC screening")


# In[19]:


import csv
import matplotlib.pyplot as plt

# Initialize counts for recommended and not recommended patients
recommended_count = 0
not_recommended_count = 0

with open("HCIP5376_PatientData.csv") as patientdata:
    filtered = (line.replace('\n', ' ') for line in patientdata)  # Filter through each line in the csv file to replace the newline character in the address variable with a space
    for row in csv.reader(filtered):
        ptname = row[1]  # Storing patient's name in a variable
        ptemail = row[4]  # Extracting patient emails so that an email can be sent to each patient
        ptsymptoms = row[5:]  # Extracting the colon cancer variables for each patient

        # Calculating bowel changes risk for each patient
        bowelrisk = 1 if ptsymptoms[0] != 'None' else 0

        # Calculating patient risk for rectal bleeding
        bleedingrisk = 1 if ptsymptoms[1] == 'Yes' else 0

        # Calculating patient risk from family history
        familyhistory = 1 if ptsymptoms[2] == 'Yes' else 0

        # Calculating patient risk from abdominal pain variable
        abdominalpain = 1 if ptsymptoms[3] == 'Yes' else 0

        # Calculating patient risk from abdominal pain variable
        irondeficiencyanemia = 1 if ptsymptoms[4] == 'Yes' else 0

        # Calculating patient risk from unexplained weight loss
        weightloss = 1 if ptsymptoms[5] == 'Yes' else 0

        # Calculating a patient's total risk by summing the individual risk variables
        totalrisk = bowelrisk + bleedingrisk + familyhistory + abdominalpain + irondeficiencyanemia + weightloss

        # Update counts based on total risk
        if totalrisk > 3:
            recommended_count += 1
        else:
            not_recommended_count += 1

# Plotting the counts
categories = ['Screening Recommended', 'Screening Not Recommended']
counts = [recommended_count, not_recommended_count]

plt.bar(categories, counts, color=['green', 'red'])
plt.xlabel('Recommendation')
plt.ylabel('Number of Patients')
plt.title('CRC Screening Recommendation')
plt.show()


# In[ ]:




