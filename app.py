import streamlit as st
import os
from openai import OpenAI
from qdrant_client import QdrantClient

# Page config
st.set_page_config(
    page_title="Physical AI & Humanoid Robotics",
    page_icon="🤖",
    layout="wide"
)

# Initialize clients
@st.cache_resource
def get_clients():
    openai_key = st.secrets.get("OPENAI_API_KEY", "")
    qdrant_host = st.secrets.get("QDRANT_HOST", "")
    qdrant_key = st.secrets.get("QDRANT_API_KEY", "")

    openai_client = None
    qdrant_client = None

    if openai_key:
        openai_client = OpenAI(api_key=openai_key)

    if qdrant_host and qdrant_key:
        qdrant_client = QdrantClient(host=qdrant_host, api_key=qdrant_key)

    return openai_client, qdrant_client

def get_embedding(text, client):
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-ada-002")
        return response.data[0].embedding
    except:
        return None

def search_qdrant(query, qdrant_client, openai_client):
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
    st.header("Ask Questions")

    openai_client, qdrant_client = get_clients()

    if not openai_client:
        st.error("OpenAI API not configured")
    else:
        question = st.text_input("Your question:")

        if st.button("Ask") and question:
            with st.spinner("Searching..."):
                if qdrant_client:
                    chunks = search_qdrant(question, qdrant_client, openai_client)
                    context = "\n\n".join(chunks) if chunks else "General robotics knowledge"
                else:
                    context = "Using general AI knowledge"

                answer = get_answer(question, context, openai_client)

                st.success("**Answer:**")
                st.write(answer)

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
