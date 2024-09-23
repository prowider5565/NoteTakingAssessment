import openai

# Set up your OpenAI API key
openai.api_key = ''

# Define a function to get a response from GPT-3.5
def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Example usage
user_question = "What is the capital of France?"
response = get_gpt_response(user_question)
print("Response:", response)
