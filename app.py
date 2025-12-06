import streamlit as st

# Page config
st.set_page_config(
    page_title="Physical AI & Humanoid Robotics",
    page_icon="🤖",
    layout="wide"
)

# Try to import optional dependencies
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

try:
    from qdrant_client import QdrantClient
    QDRANT_AVAILABLE = True
except:
    QDRANT_AVAILABLE = False

# Initialize clients
@st.cache_resource
def get_clients():
    openai_client = None
    qdrant_client = None

    # Try to get from secrets, then environment
    try:
        openai_key = st.secrets.get("OPENAI_API_KEY", "")
    except:
        openai_key = ""

    try:
        qdrant_host = st.secrets.get("QDRANT_HOST", "")
        qdrant_key = st.secrets.get("QDRANT_API_KEY", "")
    except:
        qdrant_host = ""
        qdrant_key = ""

    if OPENAI_AVAILABLE and openai_key:
        openai_client = OpenAI(api_key=openai_key)

    if QDRANT_AVAILABLE and qdrant_host and qdrant_key:
        qdrant_client = QdrantClient(host=qdrant_host, api_key=qdrant_key)

    return openai_client, qdrant_client

def get_embedding(text, client):
    if not client:
        return None
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
        return response.data[0].embedding
    except:
        return None

def search_qdrant(query, qdrant_client, openai_client):
    if not qdrant_client or not openai_client:
        return []
    try:
        embedding = get_embedding(query, openai_client)
        if not embedding:
            return []
        results = qdrant_client.search(
            collection_name="book_chunks",
            query_vector=embedding,
            limit=3
        )
        return [hit.payload.get("chunk_text", "") for hit in results]
    except:
        return []

def get_answer(question, context, client):
    if not client:
        return get_demo_answer(question)

    try:
        prompt = f"""Based on this context about Physical AI & Humanoid Robotics:

{context}

Question: {question}

Answer:"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a robotics expert assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_demo_answer(question):
    """Demo answers when API is not configured"""
    q_lower = question.lower()

    if "ros" in q_lower or "robot operating system" in q_lower:
        return """ROS 2 (Robot Operating System 2) is an open-source framework for building robot applications.

Key features include:
- Real-time performance for critical tasks
- Enhanced security features
- Better support for multi-robot systems
- Cross-platform compatibility (Linux, Windows, macOS)

It uses a distributed architecture with nodes communicating via topics, services, and actions."""

    elif "humanoid" in q_lower:
        return """Humanoid robots are designed to resemble the human body, typically featuring:

- A torso and head
- Two arms for manipulation
- Two legs for bipedal locomotion

Key challenges include:
- Balance and dynamic walking
- Natural human-robot interaction
- Complex motion planning
- Sensor integration and perception

Applications range from healthcare to industrial automation."""

    else:
        return f"""This is a demo mode response. The question "{question}" relates to Physical AI and Humanoid Robotics.

To get AI-powered answers, please configure the OpenAI API key in Streamlit secrets.

For now, explore the Content tab to learn more about ROS 2 and Humanoid Robotics!"""

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
    st.header("💬 Ask Questions")

    openai_client, qdrant_client = get_clients()

    if not openai_client:
        st.info("ℹ️ **Demo Mode** - AI-powered answers require OpenAI API configuration")

    question = st.text_input("Your question about robotics:")

    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            if qdrant_client and openai_client:
                chunks = search_qdrant(question, qdrant_client, openai_client)
                context = "\n\n".join(chunks) if chunks else "General robotics knowledge"
            else:
                context = "Using general robotics knowledge"

            answer = get_answer(question, context, openai_client)

            st.success("**Answer:**")
            st.write(answer)

            if not openai_client:
                st.info("💡 This is a demo answer. Configure OpenAI API for intelligent responses.")

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
