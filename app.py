import streamlit as st
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import streamlit.components.v1 as components
import os 
import json 
from datetime import datetime
# ============================================
# PAGE CONFIG
# ============================================
load_dotenv()
CHAT_DIR = "saved_chats" 
os.makedirs(CHAT_DIR, exist_ok=True)

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.7,
    streaming=True,
    max_tokens=900
    # other params...
)
st.set_page_config(
    page_title="Meri cutie ki Assignments 💖",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* =========================
APP ROOT
========================= */

.stApp {
    background-color: #eaf6ff;
    font-family: 'Poppins', sans-serif;
    color: #0f172a;
}

/* Main container */
.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================
SIDEBAR
========================= */

[data-testid="stSidebar"] {
    background: #dbeafe;
    border-right: 1px solid #bfdbfe;
}

[data-testid="stSidebar"] * {
    color: #0f172a;
}

/* =========================
TITLE
========================= */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: #2563eb;
    margin-top: 10px;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 1rem;
    margin-bottom: 2rem;
    font-weight: 500;
}

/* =========================
TEXT AREA
========================= */

.stTextArea textarea {
    background: white;
    color: #0f172a;

    border-radius: 18px;
    border: 2px solid #93c5fd;

    padding: 1rem;
    font-size: 16px;
    line-height: 1.6;

    box-shadow: 0 4px 12px rgba(59,130,246,0.08);
}

.stTextArea textarea::placeholder {
    color: #64748b;
}

/* =========================
BUTTONS
========================= */

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 16px;

    background: linear-gradient(90deg, #3b82f6, #60a5fa);

    color: white;

    font-size: 1rem;
    font-weight: 600;

    padding: 0.9rem;
    margin-top: 10px;

    transition: all 0.25s ease;

    box-shadow: 0 6px 18px rgba(59,130,246,0.2);
}

.stButton > button:hover {
    transform: translateY(-2px);

    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );
}

/* =========================
ANSWER BOX
========================= */

.answer-box {
    background: white;

    border-radius: 22px;

    padding: 2rem;

    margin-top: 1.5rem;

    border: 2px solid #bfdbfe;

    box-shadow: 0 8px 24px rgba(59,130,246,0.12);

    color: #0f172a;
}

/* =========================
MARKDOWN TEXT
========================= */

.stMarkdown p,
.stMarkdown li,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6 {
    color: #0f172a;
}

/* =========================
STATUS BOX
========================= */

.status-box {
    background: white;

    padding: 14px;

    border-radius: 16px;

    border: 2px solid #bfdbfe;

    color: #2563eb;

    font-weight: 600;

    text-align: center;

    margin-bottom: 15px;

    box-shadow: 0 4px 14px rgba(59,130,246,0.1);
}

/* =========================
FOOTER
========================= */

.footer {
    text-align: center;

    color: #64748b;

    margin-top: 2rem;

    font-size: 0.95rem;

    font-weight: 500;
}

/* =========================
HIDE STREAMLIT UI
========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown(
    """
    <div class="main-title">💖 Meri cutie ki Assignments 💖</div>
    <div class="subtitle">
        Guddu ki assignments ke liye AI helper ✨
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================
# SIDEBAR CHAT HISTORY
# ============================================

st.sidebar.title("💙 Previous Assignments")

# ============================================
# LOAD SAVED CHATS
# ============================================

chat_files = sorted(
    os.listdir(CHAT_DIR),
    reverse=True
)

chat_display_names = []
chat_mapping = {}

for file in chat_files:

    # remove extension
    question_text = file.split("@",1)[0]

    # sidebar visible name
    display_name = question_text

    # keep duplicates unique internally
    counter = 1

    while display_name in chat_mapping:

        counter += 1

        display_name = f"{question_text} ({counter})"

    chat_display_names.append(display_name)

    # map display name -> actual file
    chat_mapping[display_name] = file

# ============================================
# SIDEBAR
# ============================================

selected_chat = st.sidebar.selectbox(
    "💙 Previous Assignments",
    ["New Chat"] + chat_display_names
)

# ============================================
# LOAD CHAT
# ============================================

if selected_chat != "New Chat":

    selected_file = chat_mapping[selected_chat]

    with open(
        os.path.join(CHAT_DIR, selected_file),
        "r",
        encoding="utf-8"
    ) as f:

        saved_data = json.load(f)

    question = saved_data["question"]

    full_response = saved_data["answer"]



# LOAD OLD CHAT
if selected_chat != "New Chat":
    selected_file = chat_mapping[selected_chat]
    with open(
        os.path.join(CHAT_DIR, selected_file),
        "r",
        encoding="utf-8"
    ) as f:

        saved_data = json.load(f)

    st.sidebar.markdown("### 📚 Question")
    st.sidebar.write(saved_data["question"])

    st.sidebar.markdown("### ✨ Saved Answer")
    st.sidebar.download_button(
        "💾 Download",
        data=saved_data["answer"],
        file_name=f"{selected_chat}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown(saved_data["answer"])


# ============================================
# USER INPUT
# ============================================

st.markdown('<div class="glass-box">', unsafe_allow_html=True)

question = st.text_area(
"💌 Enter Assignment Question",
placeholder="Example: Discuss the role of concepts and theories in sociological analysis.",
height=150
)

generate = st.button("✨ Generate Assignment Answer")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# OPENAI CLIENT
# ============================================

if generate:
    prompt = f"""
The student has asked the following assignment question:

"{question}"

Write a well-structured academic answer in approximately 500 words.

The answer must be concise yet comprehensive, ensuring that all important dimensions of the question are covered within the word limit.

Follow this structure:

1. Title
- Begin with a clear and relevant title based on the question.

2. Introduction
- Write a brief introduction explaining the topic, its relevance, and the scope of the answer.

3. Main Body
- Divide the answer into logical headings and subheadings.
- Use numbered points wherever appropriate.
- Include brief definitions or meanings of key concepts.
- Explain major arguments, features, roles, functions, or theories related to the topic.
- Use academic and sociological terminology where relevant.
- Add short examples or illustrations for clarity.
- Keep explanations concise and analytical instead of overly descriptive.

4. Relationship/Analysis Section
- If applicable, briefly explain the relationship or interconnection between major concepts, theories, or ideas.

5. Conclusion
- End with a short conclusion summarizing the overall discussion and significance of the topic.

Important Instructions:
- Strictly keep the answer close to 500 words.
- Do not exceed 520 words.
- Prioritize clarity, structure, and balanced coverage over excessive detail.
- Use formal academic language suitable for university assignments and exam answers.
- Avoid repetition, filler content, and conversational language.
- Keep paragraphs short and readable.
- Ensure the answer feels complete despite the concise length.
"""




    messages=[
        ( "system",
        "You are an expert sociology and academic assignment writer."),

        ("human",prompt),
    ]
    status = st.empty()

    status.markdown("""
    <div style="
        background:white;
        padding:12px;
        border-radius:15px;
        border:2px solid #ffd1e1;
        color:#ff4d94;
        font-weight:600;
        text-align:center;
        margin-bottom:15px;
    ">
    💖 Writing meri cutie ki assignment ...
    </div>
    """, unsafe_allow_html=True)

    stream = llm.stream(messages)

    full_response = ""

    message_placeholder = st.empty()

    for chunk in stream:

        if chunk.content:

            full_response += chunk.content

            message_placeholder.markdown(
                full_response + "▌"
            )

    message_placeholder.markdown(full_response)

    status.empty()
    
    st.session_state["last_answer"] = full_response

    # ============================================
    # SAVE CHAT
    # ============================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    chat_data = {
        "question": question,
        "answer": full_response
    }

    filename = f"{' '.join(question.split()[:5])}@{timestamp}.json"

    with open(
        os.path.join(CHAT_DIR, filename),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chat_data,
            f,
            indent=4,
            ensure_ascii=False
        )




    st.markdown(
        '<div class="answer-box">',
        unsafe_allow_html=True
    )

    # st.markdown(answer)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        label="💾 Download Answer",
        data=st.session_state["last_answer"],
        file_name="assignment_answer.txt",
        mime="text/plain"
    )

# ============================================
# FOOTER
# ============================================

st.markdown(
    """
    <div class="footer">
        Made with 💖 for you cutie
    </div>
    """,
    unsafe_allow_html=True
)