import random
import streamlit as st

st.set_page_config(page_title="간단한 곱셈/나눗셈 연습", layout="centered")

st.title("✳️ 간단한 곱셈 & 나눗셈 연습")
st.write("곱셈과 나눗셈 각각 5문제씩 풀고 채점해보세요. '새 문제'로 문제를 다시 생성할 수 있습니다.")

def make_mul_problems(n=5, a_min=1, a_max=12, b_min=1, b_max=12):
    return [(random.randint(a_min, a_max), random.randint(b_min, b_max)) for _ in range(n)]

def make_div_problems(n=5, divisor_min=1, divisor_max=12, quotient_min=1, quotient_max=12):
    # 나눗셈 문제는 나누어 떨어지도록 생성: dividend = divisor * quotient
    problems = []
    for _ in range(n):
        d = random.randint(divisor_min, divisor_max)
        q = random.randint(quotient_min, quotient_max)
        dividend = d * q
        problems.append((dividend, d))
    return problems

# 세션 상태 초기화
if "mul_problems" not in st.session_state:
    st.session_state.mul_problems = make_mul_problems()
if "div_problems" not in st.session_state:
    st.session_state.div_problems = make_div_problems()
if "mul_answers" not in st.session_state:
    st.session_state.mul_answers = [None] * 5
if "div_answers" not in st.session_state:
    st.session_state.div_answers = [None] * 5
if "mul_score" not in st.session_state:
    st.session_state.mul_score = None
if "div_score" not in st.session_state:
    st.session_state.div_score = None

def regen_problems():
    st.session_state.mul_problems = make_mul_problems()
    st.session_state.div_problems = make_div_problems()
    st.session_state.mul_answers = [None] * 5
    st.session_state.div_answers = [None] * 5
    st.session_state.mul_score = None
    st.session_state.div_score = None

col1, col2 = st.columns(2)

with col1:
    st.header("🔢 곱셈 (×) — 5문제")
    for i, (a, b) in enumerate(st.session_state.mul_problems):
        st.session_state.mul_answers[i] = st.number_input(f"{i+1}. {a} × {b} =", key=f"mul_{i}", value=st.session_state.mul_answers[i] if st.session_state.mul_answers[i] is not None else 0, step=1)
    if st.button("곱셈 채점"):
        correct = 0
        details = []
        for (a, b), user in zip(st.session_state.mul_problems, st.session_state.mul_answers):
            ans = a * b
            is_correct = (user == ans)
            details.append((a, b, ans, user, is_correct))
            if is_correct:
                correct += 1
        st.session_state.mul_score = (correct, details)
    if st.session_state.mul_score:
        correct, details = st.session_state.mul_score
        st.write(f"맞은 개수: {correct} / 5")
        with st.expander("정답 보기"):
            for idx, (a, b, ans, user, ok) in enumerate(details, start=1):
                mark = "✅" if ok else "❌"
                st.write(f"{idx}. {a} × {b} = {ans} — 당신: {user} {mark}")

with col2:
    st.header("➗ 나눗셈 (÷) — 5문제")
    st.write("모든 문제는 나누어떨어지는 정수입니다.")
    for i, (dividend, divisor) in enumerate(st.session_state.div_problems):
        st.session_state.div_answers[i] = st.number_input(f"{i+1}. {dividend} ÷ {divisor} =", key=f"div_{i}", value=st.session_state.div_answers[i] if st.session_state.div_answers[i] is not None else 0, step=1)
    if st.button("나눗셈 채점"):
        correct = 0
        details = []
        for (dividend, divisor), user in zip(st.session_state.div_problems, st.session_state.div_answers):
            ans = dividend // divisor
            is_correct = (user == ans)
            details.append((dividend, divisor, ans, user, is_correct))
            if is_correct:
                correct += 1
        st.session_state.div_score = (correct, details)
    if st.session_state.div_score:
        correct, details = st.session_state.div_score
        st.write(f"맞은 개수: {correct} / 5")
        with st.expander("정답 보기"):
            for idx, (dividend, divisor, ans, user, ok) in enumerate(details, start=1):
                mark = "✅" if ok else "❌"
                st.write(f"{idx}. {dividend} ÷ {divisor} = {ans} — 당신: {user} {mark}")

st.markdown("---")
st.button("새 문제 생성", on_click=regen_problems)
