from transformers import AutoTokenizer, AutoModelForMaskedLM
import random
import re
from .stopwords import stopwords


def generate_choices_from_context(context, question, correct_answer, num_choices=4):
    """
    Generate a list of multiple-choice options (including the correct answer)
    for a given question and context.

    Args:
    - context (str): The context or passage related to the question.
    - question (str): The question being asked.
    - correct_answer (str): The correct answer to the question.
    - num_choices (int): Number of choices (default 4).

    Returns:
    - dict: A dictionary containing the question, choices, and the correct answer.
    """
    # Load pre-trained model and tokenizer
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)

    # Tokenize the context and predict possible distractors
    inputs = tokenizer(context, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = outputs.logits[0]

    # Generate distractors from context
    distractors = []
    top_predictions = predictions.topk(50).indices.flatten().tolist()
    for idx in top_predictions:
        word = tokenizer.decode([idx]).strip()
        if (
            re.match(r"^[A-Za-z]+$", word)  # Alphanumeric check
            and len(word) > 1  # Minimum word length
            and word.lower() not in stopwords  # Exclude stopwords
            and word.lower() != correct_answer.lower()  # Exclude correct answer
            and word not in distractors  # No duplicates
        ):
            distractors.append(word)
        if (
            len(distractors) >= num_choices - 1
        ):  # Stop when enough distractors are found
            break

    # If insufficient distractors are found, add random words from context
    context_words = set(re.findall(r"\b[A-Za-z]+\b", context))
    additional_distractors = [
        word for word in context_words if word.lower() != correct_answer.lower()
    ]
    distractors.extend(additional_distractors[: num_choices - 1 - len(distractors)])

    # Combine correct answer with distractors and shuffle
    choices = [correct_answer] + distractors[: num_choices - 1]
    random.shuffle(choices)

    return {"question": question, "choices": choices, "answer": correct_answer}


if __name__ == "__main__":
    context = (
        "The Great Wall of China is one of the most impressive architectural feats in history. "
        "It was built to protect the northern borders of the Chinese Empire from invading forces. "
        "The wall spans thousands of miles and was constructed over several centuries. "
        "Emperor Qin Shi Huang is often credited for its initial construction."
    )
    question = "The Great Wall of ____ is one of the most impressive architectural feats in history."
    correct_answer = "China"

    result = generate_choices_from_context(
        context, question, correct_answer, num_choices=4
    )
    print("Question:", result["question"])
    print("Choices:", result["choices"])
    print("Correct Answer:", result["answer"])
