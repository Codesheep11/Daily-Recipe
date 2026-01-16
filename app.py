import streamlit as st
from configs.settings import DEFAULT_USER_ID
from core.dining_agent import DiningAgent
import os

# 页面配置
st.set_page_config(page_title="DineMind IR System", layout="wide")
st.title("🤖 DineMind: 记忆增强型美食检索 Agent")

# Sidebar: 配置与调试
with st.sidebar:
    st.header("⚙️ System Config")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.subheader("💾 Memory Vector Store")
    # 只有输入Key后才初始化 Agent
    if api_key:
        try:
            if "agent" not in st.session_state:
                st.session_state.agent = DiningAgent(api_key)
            
            # 可视化展示记忆库内容
            memories = st.session_state.agent.memory_manager.get_all(DEFAULT_USER_ID)
            if memories:
                for m in memories:
                    st.code(m['memory'], language="text")
            else:
                st.info("Vector store is empty.")
                
            if st.button("Reset Memory"):
                st.session_state.agent.memory_manager.memory.delete_all(user_id=DEFAULT_USER_ID)
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_proposal" not in st.session_state:
    st.session_state.last_proposal = None

# 展示历史对话
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入区
if prompt := st.chat_input("今天吃什么？"):
    if not api_key:
        st.error("Please enter API Key first.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        agent = st.session_state.agent
        with st.spinner("Analyzing memory & searching corpus..."):
            # 调用核心 Agent
            response, food_name, logs = agent.decide_what_to_eat(DEFAULT_USER_ID, prompt)
            
            # 这里的 Expander 是给老师看的加分项
            with st.expander("🛠️ Internal Execution Trace (IR Process)"):
                for log in logs:
                    st.write(log)
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.last_proposal = food_name

# 反馈闭环 (Relevance Feedback)
if st.session_state.last_proposal:
    if st.button(f"✅ 决定去吃 {st.session_state.last_proposal}"):
        st.session_state.agent.commit_choice(DEFAULT_USER_ID, st.session_state.last_proposal)
        st.success("User choice indexed into Vector Memory!")
        st.session_state.last_proposal = None
        st.rerun()