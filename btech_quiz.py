import streamlit as st
import random

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="B.Tech Quiz Game",
    page_icon="🎓",
    layout="centered"
)

# ==============================
# BACKGROUND IMAGE
# ==============================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.95;
    }
    .stButton button {
        background: linear-gradient(45deg, #ff6ec4, #7873f5);
        color: white;
        font-weight: bold;
        border-radius: 15px;
        padding: 12px 25px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    .stRadio button { font-weight:bold; margin: 5px; }
    .css-1d391kg { background-color: rgba(255,255,255,0.7); border-radius: 10px; padding: 15px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# HEADER
# ==============================
st.title("🎓 Programming Quiz Game")
st.markdown("Test your programming knowledge with tough questions! 💻🔥")

# ==============================
# SESSION STATE
# ==============================
if 'score' not in st.session_state: st.session_state['score'] = 0
if 'question_index' not in st.session_state: st.session_state['question_index'] = 0
if 'questions_list' not in st.session_state: st.session_state['questions_list'] = []
if 'options' not in st.session_state: st.session_state['options'] = []
if 'user_choice' not in st.session_state: st.session_state['user_choice'] = None
if 'submitted' not in st.session_state: st.session_state['submitted'] = False
if 'current_subject' not in st.session_state: st.session_state['current_subject'] = "C"

MAX_QUESTIONS = 3  # Limit quiz to 5 questions

# ==============================
# SUBJECT SELECTION
# ==============================
subject = st.selectbox(
    "Choose a subject:",
    ["C", "Java", "Python", "NLP"],
    key="subject_selectbox"
)

# Reset quiz if subject changes
if st.session_state['current_subject'] != subject:
    st.session_state['current_subject'] = subject
    st.session_state['score'] = 0
    st.session_state['question_index'] = 0
    st.session_state['questions_list'] = []
    st.session_state['options'] = []
    st.session_state['user_choice'] = None
    st.session_state['submitted'] = False

# ==============================
# QUESTIONS BANK
# ==============================
def generate_questions(subject):
    questions_bank = {
        "C": [
            ("What is the difference between malloc() and calloc()?", "Memory allocation & initialization",
             ["Only memory allocation", "Only initialization", "Allocates memory and sets to 1"]),
            ("What does the 'static' keyword do in C?", "Preserve variable value across function calls",
             ["Makes variable global", "Deletes variable after scope ends", "Prevents compilation"]),
            ("Explain pointer arithmetic in C.", "Operations on memory addresses",
             ["Operations on values", "Arithmetic not allowed", "Changes variable type"]),
            ("What is a dangling pointer?", "Pointer pointing to freed memory",
             ["Pointer pointing to NULL", "Pointer pointing to global variable", "Pointer pointing to constant"]),
            ("Difference between structure and union?", "Union shares memory, structure has separate",
             ["Both are same", "Structure shares memory", "Union has separate memory"]),
            ("How do you pass a 2D array to a function?", "Using pointers or array notation",
             ["As simple variable", "Cannot pass 2D array", "Using global variable only"]),
            ("What happens when you dereference a NULL pointer?", "Runtime error / segmentation fault",
             ["Returns 0", "Program ignores it", "Compiler error"]),
            ("Difference between call by value and call by reference?", "Value copies vs original memory reference",
             ["Both same", "Reference copies value", "Value references memory"]),
            ("What is the volatile keyword?", "Prevents compiler optimizations for variable",
             ["Makes variable constant", "Deletes variable", "Declares global variable"]),
            ("What is segmentation fault?", "Accessing invalid memory location",
             ["Compiler warning", "Program halts normally", "Memory allocation success"])
        ],
        "Java": [
            ("What is JVM and how does it work?", "Java Virtual Machine executes bytecode",
             ["Runs Java source directly", "Compiles to native code", "Handles memory only"]),
            ("Explain the difference between JDK and JRE.", "JDK includes compiler, JRE is runtime only",
             ["Both same", "JRE includes compiler", "JDK is only runtime"]),
            ("Difference between abstract class and interface?", "Abstract can have method bodies; interface mostly abstract",
             ["Interface can have variables", "Both same", "Abstract cannot have methods"]),
            ("Explain final, finally, and finalize.", "Keyword, block, garbage collection method",
             ["All keywords", "Only final works", "All are runtime methods"]),
            ("What is polymorphism in Java?", "Ability to take multiple forms",
             ["Method overloading only", "Class inheritance only", "Compile-time only"]),
            ("Difference between == and .equals()?", "Reference vs content equality",
             ["Both same", "Equals checks reference", "== checks content"]),
            ("What are checked and unchecked exceptions?", "Compile-time vs runtime exceptions",
             ["Both runtime", "Both compile-time", "Only errors"]),
            ("Explain Java memory model.", "Heap, stack, method area",
             ["Heap only", "Stack only", "Method area only"]),
            ("What is synchronization in Java?", "Thread safety mechanism",
             ["For variables only", "Prevents compilation", "Manages memory"]),
            ("Difference between StringBuilder and StringBuffer?", "StringBuffer is synchronized",
             ["StringBuilder is synchronized", "Both same", "Neither synchronized"])
        ],
        "Python": [
            ("Difference between deep copy and shallow copy?", "Deep copy duplicates objects recursively",
             ["Shallow copy duplicates recursively", "No copy happens", "Only references copied"]),
            ("Explain Python GIL.", "Global Interpreter Lock allows one thread at a time",
             ["GIL does not exist", "Allows multiple threads", "Only locks processes"]),
            ("What are Python decorators?", "Functions modifying other functions",
             ["Variables modifying functions", "Classes modifying functions", "Modules modifying functions"]),
            ("Difference between @staticmethod and @classmethod?", "Static no cls/self, Class method gets cls",
             ["Static gets cls", "Class method gets self", "Both same"]),
            ("What is monkey patching?", "Modifying classes/functions at runtime",
             ["Changing variables", "Changing modules only", "Overriding classes only"]),
            ("Difference between list and tuple?", "List mutable, tuple immutable",
             ["Tuple mutable", "List immutable", "Both same"]),
            ("Explain Python generators.", "Functions yielding values lazily",
             ["Return all values", "Store all in memory", "Do nothing"]),
            ("What is the difference between is and ==?", "Identity vs equality",
             ["Both same", "is checks content", "== checks memory"]),
            ("Explain Python context manager.", "Manage resources with 'with' statement",
             ["Manages memory only", "Manages exceptions only", "Manages loops only"]),
            ("What is metaclass in Python?", "Class of a class controlling creation",
             ["Class instance", "Object instance", "Module instance"])
        ],
        "NLP": [
            ("Explain Word2Vec.", "Word embedding representing words in vectors",
             ["Counts words only", "Transforms words to sentences", "Random number for each word"]),
            ("What is stemming vs lemmatization?", "Reduce word to root vs dictionary form",
             ["Both same", "Lemmatization removes suffix only", "Stemming checks grammar"]),
            ("Difference between Bag-of-Words and TF-IDF?", "Simple count vs weighted count",
             ["Both same", "TF counts only words", "Weighted count only"]),
            ("What is named entity recognition (NER)?", "Detect proper nouns in text",
             ["Detect verbs", "Detect adjectives", "Detect numbers only"]),
            ("Explain POS tagging.", "Part-of-speech labeling",
             ["Labels sentences", "Labels paragraphs", "Labels words randomly"]),
            ("What is sequence-to-sequence model?", "Input sequence mapped to output sequence",
             ["Single sequence only", "Unsupervised model", "Predicts single output"]),
            ("Difference between LSTM and GRU?", "Both RNNs, GRU simpler",
             ["LSTM simpler", "Both CNNs", "GRU more complex"]),
            ("Explain attention mechanism.", "Focus on important parts of sequence",
             ["Focus all equally", "Ignore sequence", "Focus first word only"]),
            ("What is sentiment analysis?", "Detect positive/negative opinion",
             ["Detect entities", "Detect frequency", "Detect syntax only"]),
            ("Difference between NLP and NLU?", "Natural language processing vs understanding",
             ["Both same", "NLU is subset", "NLP is subset"])
        ]
    }
    # Pick MAX_QUESTIONS randomly
    questions = questions_bank.get(subject, [])
    random.shuffle(questions)
    return questions[:MAX_QUESTIONS]

# ==============================
# LOAD QUESTIONS
# ==============================
if not st.session_state['questions_list']:
    st.session_state['questions_list'] = generate_questions(subject)

# ==============================
# CURRENT QUESTION
# ==============================
index = st.session_state['question_index']

if index < len(st.session_state['questions_list']):
    q, correct_ans, wrong_answers = st.session_state['questions_list'][index]
    st.subheader(f"Q{index+1}: {q}")

    if not st.session_state['options']:
        options = [correct_ans] + wrong_answers
        random.shuffle(options)
        st.session_state['options'] = options

    st.session_state['user_choice'] = st.radio(
        "Select your answer:",
        st.session_state['options'],
        key=f"options_{index}"
    )

    if st.button("Submit Answer") and not st.session_state['submitted']:
        st.session_state['submitted'] = True
        if st.session_state['user_choice'] == correct_ans:
            st.success(f"✅ Correct! Answer: {correct_ans}")
            st.session_state['score'] += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {correct_ans}")

    if st.session_state['submitted']:
        if st.button("Next Question"):
            st.session_state['question_index'] += 1
            st.session_state['options'] = []
            st.session_state['user_choice'] = None
            st.session_state['submitted'] = False

# ==============================
# QUIZ COMPLETION
# ==============================
else:
    st.balloons()
    st.success("🎉 You've completed the quiz!")
    if st.button("Restart Quiz"):
        st.session_state['score'] = 0
        st.session_state['question_index'] = 0
        st.session_state['questions_list'] = generate_questions(subject)
        st.session_state['options'] = []
        st.session_state['user_choice'] = None
        st.session_state['submitted'] = False

# ==============================
# SCORE & PROGRESS
# ==============================
st.markdown("---")
st.write(f"### Score: {st.session_state['score']} / {MAX_QUESTIONS}")
progress = st.session_state.get('question_index', 0) / max(MAX_QUESTIONS, 1)
st.progress(progress)