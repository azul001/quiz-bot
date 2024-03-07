from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
    success, error = record_current_answer(message, current_question_id, session)
    if not success:
        return [error]
    next_question, next_question_id = get_next_question(current_question_id)
    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
    session["current_question_id"] = next_question_id
    session.save()
    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    question = PYTHON_QUESTION_LIST[current_question_id]
    expected_answer = question['answer']
    if answer.lower() == expected_answer.lower():
        session['user_answers'][current_question_id] = {'answer': answer, 'correct': True}
        return True, ""
    else:
        session['user_answers'][current_question_id] = {'answer': answer, 'correct': False}
        return False, "Sorry, your answer is incorrect. Please try again."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get('user_answers', {})
    total_questions = len(PYTHON_QUESTION_LIST)  # Total number of questions
    correct_answers = sum(1 for answer in user_answers.values() if answer.get('correct'))
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    final_response = f"Thank you for completing the quiz! Your score is {score:.2f}%."

    return final_response
