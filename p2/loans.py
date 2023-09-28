race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

import json
from io import TextIOWrapper
from zipfile import ZipFile
import pandas as pd
import csv

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r not in race_lookup:
                continue
            self.race.add(race_lookup[r])
    def __repr__(self):
        return f"Applicant{self.age, list(self.race)}"
    def lower_age(self):
        if '<' in self.age:
            low_age = self.age.replace('<', ' ')
        if '>' in self.age:
            low_age = self.age.replace('>', ' ')
        if '-' in self.age:
            low_age = self.age.split('-')[0]
        return int(low_age)
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
class Loan:
    
    def __init__(self, fields):
        applicant_list = []
        main_applicant_races = []
        co_applicant_races = []
        for key in fields:
            if fields[key] == "NA" or fields[key] == "Exempt":
                fields[key] = -1
            
            elif 'applicant_race-' in key and 'co' not in key:
                if fields[key] == '':
                    continue
                else:
                    main_applicant_races.append(fields[key])
                                                     
            elif fields['co-applicant_age'] != '9999':
                if 'co-applicant_race-' in key:
                    if fields[key] == '':
                        continue
                    else:
                        co_applicant_races.append(fields[key])
        
        if len(main_applicant_races) > 0:
            app_1 = Applicant(fields['applicant_age'], main_applicant_races)  
            applicant_list.append(app_1)
        
        if len(co_applicant_races) > 0:
            app_2 = Applicant(fields['co-applicant_age'], co_applicant_races)
            applicant_list.append(app_2)
                                           
        self.loan_amount = float(fields["loan_amount"])
        self.property_value = float(fields["property_value"])
        self.interest_rate = float(fields["interest_rate"])                
        self.applicants = applicant_list
        
        
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return self.__str__()
    
    def yearly_amounts(self, yearly_payment):
    # TODO: assert interest and amount are positive
        assert self.interest_rate > 0
        assert self.loan_amount > 0
        amt = self.loan_amount

        while amt > 0:
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            yearly_interest = self.interest_rate / 100 * amt
            amt += yearly_interest
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment
            
class Bank:
    def __init__(self, name):
        with open("banks.json") as f:
            bank_data = json.load(f)
            

        for dic in bank_data:
            if name == dic['name']:
                self.name = name
                self.lei = dic['lei']
            
        loans_list = []                
        with ZipFile('wi.zip') as zf:
            with zf.open("wi.csv") as f:
                reader = csv.DictReader(TextIOWrapper(f))
                for row in reader:
                    if row['lei'] == self.lei:
                        loan = Loan(row)
                        loans_list.append(loan)
                        
        self.loans = loans_list
        
    def __len__(self):
        return len(self.loans)
    
    def __getitem__(self, lookup):
        return self.loans[lookup]
            
        
            
        
        
            
           
