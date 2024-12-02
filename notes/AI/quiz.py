from .fill_in_the_blank import generate_fill_in_the_blank
from .multiple_choice import generate_choices_from_context
from .question_generation import generate_question
from .answer_open import generate_answer

def generate_quiz(context: str, num_choices=4) -> list[dict]:
    """
    This function generates a list of quiz questions, including fill-in-the-blank questions,
    open-ended questions, and corresponding multiple-choice options.

    Args:
    - context (str): The context from which to generate the quiz.
    - num_choices (int): The number of multiple choice options to generate (default is 4).

    Returns:
    - list[dict]: A list of dictionaries containing the generated questions, choices, and answers.
    """

    quiz = []

    # Generate a fill-in-the-blank question from the context
    fill_in_result = generate_fill_in_the_blank(context)
    if fill_in_result["answer"]:  # Ensure there is a valid answer
        quiz.append({
            "type": "fill_in_the_blank",
            "question": fill_in_result["question"],
            "answer": fill_in_result["answer"]
        })

        # Generate multiple-choice options for the fill-in-the-blank question
        choices_result = generate_choices_from_context(context, fill_in_result["question"], fill_in_result["answer"], num_choices)
        quiz[-1]["choices"] = choices_result

    # Generate an open-ended question from the context
    open_ended_question = generate_question(context)
    answer_open = generate_answer(context, open_ended_question["question"])

    quiz.append({
        "type": "open_ended",
        "question": open_ended_question["question"],
        "answer": answer_open
    })

    return quiz

# Example usage
if __name__ == "__main__":
    context = "The Great Wall of China is one of the most impressive architectural feats in history."
    quiz = generate_quiz(context)
    for q in quiz:
        print(q)
