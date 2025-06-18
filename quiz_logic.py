import pandas as pd
from google_auth import get_sheet
from datetime import datetime

def load_questions():
    sheet = get_sheet("questions")
    df = pd.DataFrame(sheet.get_all_records())
    return df.to_dict(orient='records')

def submit_answer(user, question_id, answer):
    q_sheet = get_sheet("questions")
    questions = pd.DataFrame(q_sheet.get_all_records())
    correct = questions.loc[questions.id == question_id, 'correct_answer'].values[0]
    is_correct = (answer == correct)

    ans_sheet = get_sheet("answers")
    ans_sheet.append_row([user, question_id, answer, is_correct, datetime.now().isoformat()])

    score_sheet = get_sheet("scores")
    scores = pd.DataFrame(score_sheet.get_all_records())
    if user in scores['user'].values:
        scores.loc[scores.user == user, 'score'] += int(is_correct)
        score_sheet.clear()
        score_sheet.append_row(["user", "score"])
        for _, r in scores.iterrows():
            score_sheet.append_row([r.user, r.score])
    else:
        score_sheet.append_row([user, int(is_correct)])

def get_leaderboard():
    sheet = get_sheet("scores")
    df = pd.DataFrame(sheet.get_all_records())
    return df.sort_values("score", ascending=False).reset_index(drop=True)
