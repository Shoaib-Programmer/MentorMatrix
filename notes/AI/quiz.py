from .fill_in_the_blank import generate_fill_in_the_blank
# This is the code for your reference:
# from transformers import AutoTokenizer, AutoModelForMaskedLM
# import random
# import re
# from .stopwords import stopwords

# def generate_fill_in_the_blank(sentence, mask_token="[MASK]"):
#     """
#     Generate a fill-in-the-blank question by masking a capitalized word in the sentence.

#     Args:
#     - sentence (str): The full sentence to generate a blank from.
#     - mask_token (str): The token to use as the blank placeholder.

#     Returns:
#     - dict: A dictionary containing the question and the correct answer.
#     """
#     # Load pre-trained tokenizer and model
#     model_name = "bert-base-uncased"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForMaskedLM.from_pretrained(model_name)

#     # Split the sentence into words
#     words = sentence.split()
    
#     # Identify indices of capitalized words that are not stopwords
#     eligible_indices = [
#         i for i, word in enumerate(words)
#         if word[0].isupper()  # Starts with a capital letter
#         and word.isalpha()  # Ignore punctuation or non-alphabetic tokens
#         and word.lower() not in stopwords  # Exclude stopwords
#     ]
    
#     if not eligible_indices:
#         return {"question": sentence, "answer": None}  # No valid word to mask

#     # Randomly select a capitalized word to mask
#     mask_index = random.choice(eligible_indices)
#     masked_words = words[:]
#     original_word = masked_words[mask_index]
#     masked_words[mask_index] = mask_token

#     # Reconstruct the masked sentence
#     masked_sentence = " ".join(masked_words)

#     # Prepare inputs for the model
#     inputs = tokenizer.encode(masked_sentence, return_tensors="pt")
    
#     # Predict the masked token
#     outputs = model(inputs)
#     predictions = outputs.logits[0]
#     predicted_token_id = predictions.argmax(dim=-1)[mask_index].item()
#     predicted_token = tokenizer.decode([predicted_token_id]).strip()

#     # Replace the original word with a blank in the sentence
#     question = sentence.replace(original_word, "____", 1)

#     # Return the question and answer
#     return {
#         "question": question,
#         "answer": original_word
#     }

# # Example usage
# if __name__ == "__main__":
#     sentence = "The Great Wall of China is one of the most impressive architectural feats in history."
#     result = generate_fill_in_the_blank(sentence)
#     print("Fill-in-the-Blank Question:", result["question"])
#     print("Answer:", result["answer"])

from .multiple_choice import generate_choices_from_context

from .question_generation import generate_question
from .semantic_compare import evaluate_answer
from .answer_open import generate_answer

class Quiz():
  def __init__(self, context):
    if not context:
      raise ValueError('There must be some context to create a quiz.')
    self.context = context

  def generate(self, question_type, answer_type):
    '''
    question_type can be one of: fill-in-the-blank, open-ended
    answer_type can be one of: multiple-choice, open-ended
    '''