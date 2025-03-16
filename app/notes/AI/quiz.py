from .fill_in_the_blank import generate_fill_in_the_blank
from .multiple_choice import generate_choices_from_context
from .question_generation import generate_question
from .semantic_compare import evaluate_answer
from .answer_open import generate_answer

# TODO: import random cuz you want to be improving the functionality


class Quiz:
    """
    A class to generate and evaluate quizzes based on a given text context.

    The Quiz class provides functionality to create open-ended and multiple-choice
    questions from a provided text and evaluate answers against the generated questions.

    Attributes:
    ----------
    context : str
        The text from which the quiz questions are generated.
    multiple_choice : list
        A list to store multiple-choice questions and their options.
    open_ended : list
        A list to store open-ended questions and their answers.

    Methods:
    -------
    generate_all_questions(ratio: float = 0.9):
        Generates open-ended and fill-in-the-blank questions from the context based on
        a specified ratio.

    evaluate(question: str, answer: str) -> bool:
        Evaluates a provided answer against the correct answer for a given question.
    """

    def __init__(self, context: str):
        """
        Initializes a Quiz instance with the given context.

        Args:
        - context (str): The text from which the quiz questions will be generated.

        Attributes:
        - context (str): The provided text to base the quiz on.
        - multiple_choice (list): A list to store multiple-choice questions and their options.
        - open_ended (list): A list to store open-ended questions and their answers.

        Raises:
        - ValueError: If the provided context is empty.
        """
        if not context:
            raise ValueError("There must be some context to create a quiz.")
        self.context = context
        self.multiple_choice = []
        self.open_ended = []

    def generate_all_questions(self, ratio: float = 0.9):
        """
        Generates all questions from the context with a specified ratio of open-ended to fill-in-the-blank.

        Args:
        - ratio (float): The proportion of open-ended questions to total questions (default is 0.9).

        Process:
        - Splits the context into sentences.
        - Randomly selects the question type for each sentence based on the ratio.
        - Generates open-ended or fill-in-the-blank questions accordingly.

        Populates:
        - self.open_ended: A list of open-ended questions and their answers.
        - self.multiple_choice: A list of multiple-choice questions and their options.

        Raises:
        - ValueError: If the ratio is not between 0 and 1.
        """
        if not (0 <= ratio <= 1):
            raise ValueError("Ratio must be between 0 and 1.")

        sentences = [s.strip() for s in self.context.split(".") if s.strip()]
        total_sentences = len(sentences)
        open_ended_count = round(total_sentences * ratio)

        for idx, sentence in enumerate(sentences):
            if idx < open_ended_count:
                # Generate an open-ended question
                question = generate_question(self.context, sentence)
                answer = generate_answer(self.context, question)
                self.open_ended.append({"question": question, "answer": answer})
            else:
                # Generate a fill-in-the-blank question
                result = generate_fill_in_the_blank(sentence)
                self.open_ended.append(
                    {"question": result["question"], "answer": result["answer"]}
                )
                choices = generate_choices_from_context(
                    self.context, result["question"], result["answer"]
                )
                self.multiple_choice.append(
                    {"question": choices["question"], "choices": choices["choices"]}
                )

    def evaluate(self, question: str, answer: str) -> bool:
        """
        Evaluates whether the provided answer is correct for a given question.

        Args:
        - question (str): The question to evaluate the answer for.
        - answer (str): The answer provided by the user.

        Returns:
        - bool: True if the answer is correct, False otherwise.

        Raises:
        - ValueError: If the question is not found in the quiz.
        """
        correct_answer = None
        for q in self.open_ended + self.multiple_choice:
            if q["question"] == question:
                correct_answer = (
                    q.get("answer") or q["choices"][0]
                )  # First choice is the correct answer
                break
        if not correct_answer:
            raise ValueError("Question not found in the quiz.")
        return evaluate_answer(answer, correct_answer)


def generate_quiz_basic(context: str, ratio: float = 0.9) -> Quiz:
    """
    Generates a basic quiz using the provided context, with open-ended and fill-in-the-blank questions
    distributed according to the specified ratio.

    Args:
    - context (str): The text from which to generate the quiz.
    - ratio (float): Proportion of open-ended questions to total questions (default is 0.9).

    Returns:
    - Quiz: A `Quiz` instance containing open-ended and multiple-choice questions.
    """
    quiz = Quiz(context)
    quiz.generate_all_questions(ratio=ratio)
    return quiz


if __name__ == "__main__":
    quiz = generate_quiz_basic(
        "The sun is a star. It provides light to Earth. Solar panels harness this light.",
        ratio=0.8,
    )
    print("Open-ended Questions:", quiz.open_ended)
    print("Multiple-choice Questions:", quiz.multiple_choice)
