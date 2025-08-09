import re

from groq import Groq

client = Groq(
    api_key="groq_api_key_here"
)

def get_llm_response(question):
  # question = "what to do in free time"
  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": question,
          }
      ],
      model="llama-3.3-70b-versatile",
  )
  answer = chat_completion.choices[0].message.content
  # Remove all non-alphanumeric characters (except for spaces)
  answer_text_num = re.sub(r'[^A-Za-z0-9 ]+', '', answer)
  print(answer_text_num)
  return answer_text_num
