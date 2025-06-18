import streamlit as st
from quiz_logic import load_questions, submit_answer, get_leaderboard
from google_auth import get_sheet
from streamlit_autorefresh import st_autorefresh

def main():
    st.title("🎵 Music Quiz")

    if 'username' not in st.session_state or st.session_state.username == "":
        name = st.text_input("Ange ditt namn för att börja:")
        if st.button("Starta quiz") and name.strip():
            st.session_state.username = name.strip()
            st.experimental_rerun()
        return

    username = st.session_state.username

    if 'questions' not in st.session_state:
        st.session_state.questions = load_questions()

    qlist = st.session_state.questions
    idx = st.session_state.get('current_q', 0)

    if idx < len(qlist):
        q = qlist[idx]
        st.write(f"**Fråga {idx+1}:** {q['question']}")
        choice = st.radio("Välj ett alternativ:", ['A','B','C','D'])
        if st.button("Svara"):
            submit_answer(username, q['id'], choice)
            st.session_state.current_q = idx + 1
            st.experimental_rerun()
    else:
        st.header("🎉 Du har svarat på alla frågor!")
        st.subheader("Leaderboard")
        st_autorefresh(interval=5000, key="leader_auto")
        leaderboard = get_leaderboard()
        st.table(leaderboard)

if __name__ == "__main__":
    main()
