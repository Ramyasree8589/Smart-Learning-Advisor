import streamlit as st 
import pandas as pd
import altair as alt
from fpdf import FPDF

# ---------- Backend: Learning Data ----------
learning_catalog = {
    "Mathematics": {
        "Algebra": ["Equations", "Expressions", "Factorization"],
        "Trigonometry": ["Angles", "Identities", "Heights & Distances"],
        "Geometry": ["Shapes", "Theorems", "Mensuration"]
    },
    "Science": {
        "Physics": ["Motion", "Force", "Energy"],
        "Chemistry": ["Atoms", "Reactions", "Acids & Bases"],
        "Biology": ["Cells", "Human Systems", "Environment"]
    },
    "English": {
        "Grammar": ["Tenses", "Articles", "Prepositions"],
        "Vocabulary": ["Synonyms", "Antonyms", "Word Usage"],
        "Writing": ["Essays", "Letters", "Comprehension"]
    },
    "Computer Science": {
        "Programming Basics": ["Variables", "Loops", "Functions"],
        "Data Structures": ["Lists", "Dictionaries", "Trees"],
        "Algorithms": ["Sorting", "Searching", "Recursion"]
    }
}

subject_icons = {
    "Mathematics": "📐",
    "Science": "🔬",
    "English": "📚",
    "Computer Science": "💻"
}

# ---------- Functions ----------
def evaluate_confidence(confidence_data):
    priority_map = {}
    for topic, score in confidence_data.items():
        if score <= 2:
            priority_map[topic] = "High Priority"
        elif score == 3:
            priority_map[topic] = "Moderate Priority"
        else:
            priority_map[topic] = "Low Priority"
    return priority_map

def generate_learning_plan(subject, priorities):
    plan = {}
    for topic, level in priorities.items():
        if level != "Low Priority":
            plan[topic] = {
                "priority": level,
                "concepts": learning_catalog[subject][topic]
            }
    return plan

def generate_practice_questions(topic):
    return [
        f"Explain the basic idea of {topic}.",
        f"Solve one beginner-level question from {topic}.",
        f"Mention one real-life application of {topic}."
    ]

def generate_pdf(learning_plan, subject):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Smart Learning Advisor - {subject}", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "", 12)
    for topic, details in learning_plan.items():
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"{topic} ({details['priority']})", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, "Key Concepts:", ln=True)
        for concept in details["concepts"]:
            pdf.cell(0, 6, f"- {concept}", ln=True)

        pdf.cell(0, 8, "Practice Questions:", ln=True)
        for q in generate_practice_questions(topic):
            pdf.multi_cell(0, 6, f"- {q}")

        pdf.ln(5)

    return pdf.output(dest="S").encode("latin-1", errors="replace")

# ---------- Streamlit Frontend ----------
st.set_page_config(page_title="Smart Learning Advisor", layout="wide")

# Banner
st.markdown("""
<div style='background-color:#4CAF50; padding:20px; border-radius:10px; color:white; text-align:center'>
<h1>🎓 Smart Learning Advisor</h1>
<p>AI-powered personalized learning assistant (SDG 4 – Quality Education)</p>
</div>
""", unsafe_allow_html=True)

st.write("Select your subject, rate your confidence in topics, and get a personalized study plan with charts and PDF download! 🚀")

# Sidebar
st.sidebar.header("Step 1: Select Subject")
subject_choice = st.sidebar.selectbox(
    "Your Subject:",
    [f"{subject_icons[s]} {s}" for s in learning_catalog.keys()]
)
subject = subject_choice.split(" ", 1)[1]

st.sidebar.header("Step 2: Rate Your Confidence")
confidence_data = {}
for topic in learning_catalog[subject]:
    confidence_data[topic] = st.sidebar.slider(
        topic, 1, 5, 3, help="1 = Very Weak, 5 = Very Strong"
    )

# Analyze
if st.sidebar.button("Analyze Learning Gaps"):
    priorities = evaluate_confidence(confidence_data)
    learning_plan = generate_learning_plan(subject, priorities)

    st.success("✅ Analysis Complete!")

    tabs = st.tabs(["📊 Learning Gap Analysis", "📘 Learning Plan", "📈 Visual Summary"])

    # Tab 1: Learning Gap Analysis
    with tabs[0]:
        for topic, status in priorities.items():
            st.write(f"**{topic}:** {status}")
            st.progress(confidence_data[topic] / 5)

    # Tab 2: Personalized Learning Plan with Practice Questions
    with tabs[1]:
        if not learning_plan:
            st.info("Excellent! No major learning gaps detected.")
        else:
            for topic, details in learning_plan.items():
                with st.expander(f"{topic} ({details['priority']})"):
                    st.markdown("**Key Concepts:**")
                    for concept in details["concepts"]:
                        st.write(f"• {concept}")

                    st.markdown("**Practice Questions:**")
                    for q in generate_practice_questions(topic):
                        st.write(f"• {q}")

            pdf_file = generate_pdf(learning_plan, subject)
            st.download_button(
                "📥 Download Learning Plan PDF",
                pdf_file,
                f"{subject}_LearningPlan.pdf",
                "application/pdf"
            )

    # Tab 3: Visual Summary
    with tabs[2]:
        df = pd.DataFrame({
            "Topic": confidence_data.keys(),
            "Confidence": confidence_data.values()
        })
        chart = alt.Chart(df).mark_bar().encode(
            x="Topic",
            y="Confidence",
            color=alt.Color("Confidence", scale=alt.Scale(scheme="blues")),
            tooltip=["Topic", "Confidence"]
        )
        st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.markdown("Made with ❤️ using Python & Streamlit | SDG 4 – Quality Education")
