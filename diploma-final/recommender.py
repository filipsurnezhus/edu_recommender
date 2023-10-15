import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = stopwords.words('russian')

df_courses = pd.read_csv('data/coursesv3.csv')

df_courses['content'] = df_courses['title'] + ' ' + df_courses['description']

vectorizer = TfidfVectorizer(stop_words=stop_words)
content_matrix = vectorizer.fit_transform(df_courses['content'])

def recommend_courses_based_on_skills(user_skills, df=df_courses, n=3):
    user_skills_vector = vectorizer.transform([' '.join(user_skills)])

    cosine_sim_skills = cosine_similarity(user_skills_vector, content_matrix)

    sorted_course_indices = cosine_sim_skills.argsort().flatten()[::-1]

    recommended_courses = [df_courses.iloc[i]['title'] for i in sorted_course_indices][:n]
    return recommended_courses

