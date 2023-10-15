import streamlit as st
import pandas as pd
from criteries import create_profession_skills_dict
import streamlit.components.v1 as components
from recommender import recommend_courses_based_on_skills


df_criteries = pd.read_csv('data/criteries_test.csv')
df_courses = pd.read_csv('data/coursesv3.csv')

def load_saved_courses():
    try:
        df = pd.read_csv('saved_courses.csv')
        if 'course' in df.columns:
            saved_courses = df['course'].tolist()
        else:
            saved_courses = []
    except (FileNotFoundError, pd.errors.EmptyDataError):
        saved_courses = []
    return saved_courses


def save_saved_courses(saved_courses):
    df = pd.DataFrame({'course': saved_courses})
    df.to_csv('saved_courses.csv', index=False)

saved_courses = load_saved_courses()

st.set_page_config(page_title="Рекомендательная система", layout="wide")

menu = ["Логин/регистрация", "Личный кабинет", "Рекомендации", "О проекте"]
choice = st.sidebar.selectbox("Меню", menu)


if 'logged_in_username' not in st.session_state:
    st.session_state['logged_in_username'] = ""

if choice == "Логин/регистрация":
    st.header("Логин/регистрация")
    
    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    
    def authenticate(username, password):
        users_df = pd.read_json('users.json')
        if username in users_df['username'].values:
            user_row = users_df[users_df['username'] == username].iloc[0]
            if password == user_row['password']:
                return True
        return False
    
    if st.button("Войти"):
        if authenticate(username, password):
            st.success("Вход выполнен успешно")
            st.session_state['logged_in_username'] = username
            st.sidebar.success(f"Вход выполнен успешно.")
        else:
            st.error("Неправильное имя пользователя или пароль")
    
    st.button("Регистрация")
    

elif choice == "Личный кабинет":
    st.header("Личный кабинет")
    
    if st.session_state['logged_in_username']:
        st.subheader(f"Добро пожаловать, {st.session_state['logged_in_username']}!")
        st.subheader("Сохраненные курсы")
        for course in saved_courses:
            course_link = df_courses[df_courses['title'] == course]['link'].values[0]
            st.markdown(f"[{course}]({course_link})")
            if st.button('Удалить', key=course):
                saved_courses.remove(course)
                save_saved_courses(saved_courses)
    else:
        st.error("Для доступа к личному кабинету выполните вход.")


elif choice == "Рекомендации":
    st.header("Рекомендации")
    profession_skills = create_profession_skills_dict(df_criteries)

    professions = list(profession_skills.keys())
    selected_profession = st.selectbox('Выберите профессию:', professions)

    if selected_profession:
        st.subheader(f'Выберите навыки для профессии {selected_profession}:')
        selected_skills = [skill for skill in profession_skills[selected_profession] if st.checkbox(skill)]

        providers = df_courses['provider'].unique().tolist()
        selected_providers = st.multiselect('Выберите площадку, на которой реализуется онлайн-курс:', providers)

        n_courses = st.number_input('Введите количество рекомендуемых курсов:', min_value=1, value=1, step=1)

        if selected_skills:
            recommended_courses = recommend_courses_based_on_skills(selected_skills, n=n_courses)
            st.subheader(f'Рекомендованные курсы для выбранных навыков:')

            if selected_providers:
                recommended_courses = [course for course in recommended_courses if
                                       df_courses[df_courses['title'] == course]['provider'].values[0] in selected_providers]

            for course in recommended_courses:
                course_link = df_courses[df_courses['title'] == course]['link'].values[0]
                st.markdown(f"[{course}]({course_link})")
                if st.button('Сохранить курс', key=course):
                    saved_courses.append(course)
                    save_saved_courses(saved_courses)
                    st.success("Курс успешно добавлен в избранное!")


elif choice == "О проекте":
    st.header("О проекте")
    st.write("Здесь вы можете добавить информацию о вашем проекте.")


st.write("")
if 'logout' not in st.session_state:
    st.session_state['logout'] = False

if st.session_state['logout']:
    save_saved_courses(saved_courses)
    st.session_state['logout'] = False
