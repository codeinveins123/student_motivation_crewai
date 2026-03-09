import streamlit as st
import yaml, os
from datetime import datetime
from iws2.src.iws2.crew import Iws2
from dotenv import load_dotenv
import pandas as pd
import shutil

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_PATH = os.path.join(BASE_DIR, "iws2/src/iws2/config", "agents.yaml")
TASKS_PATH = os.path.join(BASE_DIR, "iws2/src/iws2/config", "tasks.yaml")

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
def save_yaml(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

agents_data = load_yaml(AGENTS_PATH)
tasks_data = load_yaml(TASKS_PATH)

st.set_page_config(layout="wide")
st.title("Настройка и запуск агентов")

st.sidebar.header("Файлы для постфикса роли")
uploaded_csv = st.sidebar.file_uploader("CSV файл", type="csv")
uploaded_txt = st.sidebar.file_uploader("TXT файл", type="txt")
csv_content = ""
txt_content = ""
if uploaded_csv:
    try: csv_content = pd.read_csv(uploaded_csv).to_csv(index=False)
    except: st.sidebar.error("Ошибка CSV")
if uploaded_txt:
    try: txt_content = uploaded_txt.read().decode("utf-8")
    except: st.sidebar.error("Ошибка TXT")
postfix = (csv_content + txt_content).replace("\n", "\\n") if (csv_content + txt_content) else ""

col1, col2 = st.columns(2)

role_inputs, goal_inputs, backstory_inputs = {}, {}, {}
description_inputs, expected_inputs, agent_inputs = {}, {}, {}

with col1:
    st.header("Агенты")
    for name, info in agents_data.items():
        with st.expander(f"Агент: {name}"):
            role_inputs[name] = st.text_input("Role", value=info.get('role',''), key=f"r_{name}")
            goal_inputs[name] = st.text_area("Goal", value=info.get('goal',''), key=f"g_{name}")
            backstory_inputs[name] = st.text_area("Backstory", value=info.get('backstory',''), key=f"b_{name}")

with col2:
    st.header("Задачи")
    for name, info in tasks_data.items():
        with st.expander(f"Задача: {name}"):
            description_inputs[name] = st.text_area("Определение", value=info.get('description',''), key=f"d_{name}")
            expected_inputs[name] = st.text_area("Ожидаемый результат", value=info.get('expected_output',''), key=f"o_{name}")
            agent_inputs[name] = st.selectbox("Назначенный агент", options=list(agents_data.keys()),
                                              index=(list(agents_data.keys()).index(info.get('agent')) 
                                                     if info.get('agent') in agents_data else 0),
                                              key=f"agent_{name}")

topic = st.text_input("Тема (topic):", value="An individualized rescue plan for a struggling student")

if st.button("Запустить"):
    shutil.copyfile(AGENTS_PATH, AGENTS_PATH+".bak")
    shutil.copyfile(TASKS_PATH, TASKS_PATH+".bak")

    for name in agents_data.keys():
        agents_data[name]['role'] = f"{{topic}}: {role_inputs[name]}{postfix}"
        agents_data[name]['goal'] = goal_inputs[name]
        agents_data[name]['backstory'] = backstory_inputs[name]

    for name in tasks_data.keys():
        tasks_data[name]['description'] = description_inputs[name]
        tasks_data[name]['expected_output'] = expected_inputs[name]
        tasks_data[name]['agent'] = agent_inputs[name]

    save_yaml(agents_data, AGENTS_PATH)
    save_yaml(tasks_data, TASKS_PATH)

    st.write("Выполнение...")
    result = Iws2Crew().crew().kickoff(inputs={'topic': topic, 'current_year': str(datetime.now().year)})
    st.subheader("Результат:")
    st.markdown(result.raw)

    shutil.move(AGENTS_PATH+".bak", AGENTS_PATH)
    shutil.move(TASKS_PATH+".bak", TASKS_PATH)