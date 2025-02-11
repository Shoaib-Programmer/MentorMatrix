from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

def generate_answer(context, question):
    """
    Generate an answer to an open-ended question based on the given context.

    Args:
    - context (str): The passage or context from which to derive the answer.
    - question (str): The open-ended question to answer.

    Returns:
    - str: The generated answer.
    """
    # Load pre-trained QA model and tokenizer
    model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    
    # Initialize QA pipeline
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    
    # Generate the answer
    result = qa_pipeline(question=question, context=context)
    
    return result["answer"]

if __name__ == "__main__":
    # Example context and question
    context = (
        "The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, "
        "wood, and other materials, generally built along an east-to-west line across the historical northern borders "
        "of China to protect the Chinese states and empires against raids and invasions. Several walls were being built "
        "as early as the 7th century BC. Emperor Qin Shi Huang connected and expanded several walls during his reign."
    )
    question = "Who expanded and connected several walls during his reign?"

    # Generate the answer
    answer = generate_answer(context, question)
    print("Generated Answer:", answer)
