import streamlit as st
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

# ============================================
# PAGE CONFIG
# ============================================
load_dotenv()


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
    layout="centered"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #ffe6f2, #fff0f7, #ffeef8);
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: #ff4d94;
    margin-top: 10px;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #7d4c61;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* Cute glass container */
.glass-box {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(12px);
    padding: 1.5rem;
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.5);
    box-shadow: 0 8px 32px rgba(255, 105, 180, 0.15);
}

/* Text area */
.stTextArea textarea {
    border-radius: 18px !important;
    border: 2px solid #ffb6d5 !important;
    background-color: #fff9fc !important;
    color: #5a3b47 !important;
    font-size: 16px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 16px;
    background: linear-gradient(90deg, #ff66a3, #ff85b3);
    color: white;
    border: none;
    padding: 0.8rem;
    font-size: 1rem;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #ff4d94, #ff75ab);
}

/* Output box */
.answer-box {
    background: white;
    padding: 1.5rem;
    border-radius: 20px;
    border: 2px solid #ffd1e6;
    margin-top: 1.5rem;
    box-shadow: 0 8px 25px rgba(255, 105, 180, 0.12);
}

/* Footer */
.footer {
    text-align: center;
    color: #9a6b82;
    margin-top: 2rem;
    font-size: 0.9rem;
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
# USER INPUT
# ============================================

# st.markdown('<div class="glass-box">', unsafe_allow_html=True)

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



    st.markdown(
        '<div class="answer-box">',
        unsafe_allow_html=True
    )

    # st.markdown(answer)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # st.download_button(
    #     label="💾 Download Answer",
    #     data=st.session_state["last_answer"],
    #     file_name="assignment_answer.txt",
    #     mime="text/plain"
    # )

# ============================================
# FOOTER
# ============================================

st.markdown(
    """
    <div class="footer">
        Made with 💖 for your cutie
    </div>
    """,
    unsafe_allow_html=True
)