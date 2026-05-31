import streamlit as st
from langchain_mistralai import ChatMistralAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 


from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
# ============================================
# PAGE CONFIG
# ============================================
load_dotenv()
CHAT_DIR = "saved_chats" 
os.makedirs(CHAT_DIR, exist_ok=True)

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    streaming=True,
    max_tokens=1000,
    # other params...
)

# gemini = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", 
#                                         temperature=2)
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

saved_chats = (
    supabase.table("assignments")
    .select("*")
    .order("created_at", desc=True)
    .execute()
).data

chat_mapping = {}

for row in saved_chats:

    title = row["title"] or "Untitled Assignment"

    display_name = title

    counter = 1

    while display_name in chat_mapping:
        counter += 1
        display_name = f"{title} ({counter})"

    chat_mapping[display_name] = row


# ============================================
# SIDEBAR
# ============================================


selected_chat = st.sidebar.selectbox(
    "💙 Previous Assignments",
    ["New Chat"] + list(chat_mapping.keys())
)

# ============================================
# LOAD CHAT
# ============================================

if selected_chat != "New Chat":
    chat = chat_mapping[selected_chat]

    question = chat["question"]

    full_response = chat["answer"]

    st.markdown(full_response)

    st.sidebar.markdown("### 📚 Question")
    st.sidebar.write(question)

    st.sidebar.markdown("### ✨ Saved Answer")
    st.sidebar.download_button(
        "💾 Download",
        data=full_response,
        file_name=f"{question}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown(full_response)


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
You are an academic assignment writer.

Question:
"{question}"

TASK:
Write a complete university-level answer between 480 and 520 words.
The final answer MUST NOT be below 480 words and MUST NOT exceed 520 words.

Before generating the answer:
- Plan the structure.
- Allocate words proportionally across sections.
- Ensure all major dimensions of the question are covered.
- Verify that the final answer is within the required word range.

STRUCTURE

# Title
Provide a clear, relevant title based on the question.

# Introduction (60–80 words)
- Introduce the topic.
- Explain its significance.
- State the scope of the discussion.

# Main Body (300–340 words)
Organize the discussion using logical headings and subheadings.

Requirements:
- Use numbered points wherever appropriate.
- Define important concepts briefly.
- Explain key theories, functions, characteristics, arguments, or perspectives relevant to the question.
- Use academic and sociological terminology where applicable.
- Include short examples or illustrations.
- Focus on analysis rather than lengthy description.
- Avoid unnecessary details.

# Relationship / Analytical Discussion (60–80 words)
- Explain relationships, interconnections, comparisons, or theoretical linkages among the major concepts discussed.
- Highlight significance or implications.

# Conclusion (40–60 words)
- Summarize the main arguments.
- Reinforce the overall significance of the topic.

WRITING GUIDELINES
- Maintain a formal academic tone.
- Use concise and precise language.
- Keep paragraphs short and readable.
- Avoid repetition, filler content, and conversational expressions.
- Ensure smooth transitions between sections.
- Do not include bullet points unless they improve clarity.
- Cover all important dimensions of the question within the word limit.

FINAL CHECK BEFORE OUTPUT
1. Is the answer between 480 and 520 words?
2. Does it contain all required sections?
3. Are headings clearly marked?
4. Is the discussion balanced and complete?
5. If any condition is not met, revise before producing the final answer.

Output only the final answer.
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
    title = question[:80].strip()
    supabase.table("assignments").insert(
    {   "title": title,
        "question": question,
        "answer": full_response
    }
    ).execute()




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
        file_name=f"{question}.txt",
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