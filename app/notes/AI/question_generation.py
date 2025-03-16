from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def generate_question(context, highlighted_text):
    """
    Generate a question based on highlighted text within a context.

    Args:
    - context (str): The full context text.
    - highlighted_text (str): The part of the text to focus on for the question.

    Returns:
    - str: The generated question.
    """
    # Load pre-trained tokenizer and model
    model_name = "valhalla/t5-base-qg-hl"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Format the input with highlighted text
    input_text = f"generate question: {context.replace(highlighted_text, f'<hl>{highlighted_text}<hl>')}"

    # Tokenize input
    inputs = tokenizer.encode(input_text, return_tensors="pt")

    # Generate output
    outputs = model.generate(inputs, max_length=64, num_beams=4, early_stopping=True)

    # Decode and return the generated question
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return question


# Example usage
if __name__ == "__main__":
    # Full context
    context = (
        "The Great Wall of China is a series of fortifications that were built across the northern borders "
        "of China to protect against invasions. The wall spans thousands of miles and is considered one of the most "
        "impressive architectural feats in history."
    )

    # Highlighted text for question generation
    highlighted_text = "The Great Wall of China is a series of fortifications"

    # Generate the question
    question = generate_question(context, highlighted_text)
    print("Generated Question:", question)
