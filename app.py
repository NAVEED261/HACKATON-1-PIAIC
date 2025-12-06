import streamlit as st

# Page config
st.set_page_config(
    page_title="Physical AI & Humanoid Robotics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_demo_answer(question):
    """Demo answers - works without any API"""
    q_lower = question.lower()

    if "ros" in q_lower or "robot operating system" in q_lower:
        return """**ROS 2 (Robot Operating System 2)**

ROS 2 is an open-source framework for building robot applications.

**Key Features:**
- ⚡ Real-time performance for critical tasks
- 🔒 Enhanced security features
- 🤖 Better support for multi-robot systems
- 💻 Cross-platform (Linux, Windows, macOS)

**Core Concepts:**
- **Nodes**: Independent processes
- **Topics**: Named buses for messages
- **Services**: Synchronous RPC calls
- **Actions**: Long-running tasks with feedback

ROS 2 uses DDS for communication, making it production-ready!"""

    elif "humanoid" in q_lower:
        return """**Humanoid Robotics**

Humanoid robots resemble the human body with:
- 👤 Torso and head
- 🦾 Two arms for manipulation
- 🦿 Two legs for bipedal locomotion

**Key Challenges:**
- ⚖️ Balance and dynamic walking
- 🗣️ Natural human-robot interaction
- 🧠 Complex motion planning
- 👁️ Sensor integration and perception

**Applications:**
- 🏥 Healthcare and elderly care
- 📚 Education and entertainment
- 🚨 Search and rescue
- 🏭 Industrial automation"""

    elif "ai" in q_lower or "artificial" in q_lower:
        return """**Physical AI in Robotics**

Physical AI combines:
- 🤖 Embodied intelligence
- 🧠 Machine learning
- 👁️ Computer vision
- 🎯 Real-world interaction

It enables robots to understand and interact with the physical world intelligently!"""

    else:
        return f"""**Question:** {question}

This relates to Physical AI & Humanoid Robotics!

**Try asking about:**
- ROS 2 and its features
- Humanoid robot design
- AI in robotics
- Robotics applications

**Or explore the Content tab for detailed information!** 📚"""

# Main app
st.title("🤖 Physical AI & Humanoid Robotics")
st.markdown("### AI-Powered Learning Platform")

# Tabs
tab1, tab2, tab3 = st.tabs(["🏠 Home", "💬 Chatbot", "📚 Content"])

with tab1:
    st.header("Welcome!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**🤖 AI-Powered**\n\nIntelligent chatbot for instant answers")

    with col2:
        st.info("**📚 Comprehensive**\n\nROS 2 to advanced humanoid robotics")

    with col3:
        st.info("**💡 Interactive**\n\nRAG-based Q&A system")

    st.markdown("---")
    st.subheader("What You'll Learn")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **ROS 2 Fundamentals**
        - ✓ Core concepts
        - ✓ Node communication
        - ✓ Real-time control
        - ✓ Multi-robot systems
        """)

    with col2:
        st.markdown("""
        **Humanoid Robotics**
        - ✓ Locomotion & balance
        - ✓ Human-robot interaction
        - ✓ Perception & planning
        - ✓ AI integration
        """)

with tab2:
    st.header("💬 AI Chatbot")
    st.markdown("Ask me anything about Physical AI, ROS 2, or Humanoid Robotics!")

    # Session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Chat input
    question = st.chat_input("Type your question here...")

    if question:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_demo_answer(question)
                st.markdown(answer)

        # Add assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

with tab3:
    st.header("📖 Course Content")

    with st.expander("ROS 2 - Robot Operating System"):
        st.markdown("""
        **What is ROS 2?**

        ROS 2 is a set of software libraries and tools for building robot applications.

        **Key Features:**
        - Real-time performance
        - Security features
        - Multi-robot support
        - Cross-platform

        **Core Concepts:**
        - Nodes: Independent processes
        - Topics: Message buses
        - Services: RPC calls
        - Actions: Long-running tasks
        """)

    with st.expander("Humanoid Robotics"):
        st.markdown("""
        **Overview**

        Humanoid robots are designed to resemble the human body.

        **Key Areas:**
        - Locomotion and balance
        - Human-robot interaction
        - Perception systems
        - Motion planning

        **Applications:**
        - Healthcare
        - Education
        - Search and rescue
        - Industrial automation
        """)

st.sidebar.markdown("---")
st.sidebar.info("Created for PIAIC Hackathon")
st.sidebar.markdown("[GitHub](https://github.com/NAVEED261/HACKATON-1-PIAIC)")
