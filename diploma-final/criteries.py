import pandas as pd

def create_profession_skills_dict(df):
    profession_skills = {}
    for index, row in df.iterrows():
        profession = row['profession']
        skills = row['skills'].split(', ')
        profession_skills[profession] = skills
    return profession_skills
