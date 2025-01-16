from openai import OpenAI
client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "who is around the corner"},
            {"role": "user", "content": 'a cat around a corner'}
        ],
        max_tokens=100
    )
    print(response.choices[0].message.content)
    # return response.choices[0].message['content'].strip()
except Exception as e:
    print(f"Error generating summary: {e}")
    # return "Summary generation failed"
