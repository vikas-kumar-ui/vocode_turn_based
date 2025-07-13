from typing import Any, List, Optional
from groq import Groq  # make sure groq is installed via: pip install groq
from vocode import getenv
from vocode.turn_based.agent.base_agent import BaseAgent

class GroqAgent(BaseAgent):
    def __init__(
        self,
        system_prompt: str,
        api_key: Optional[str] = None,
        initial_message: Optional[str] = None,
        model_name: str = "llama3-8b-8192",  # default Groq model
        temperature: float = 0.7,
        max_tokens: int = 100,
    ):
        super().__init__(initial_message=initial_message)
        api_key = getenv("GROQ_API_KEY", api_key)
        if not api_key:
            raise ValueError("Groq API key not provided")
        self.client = Groq(api_key=api_key)
        self.prompt = system_prompt
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.messages: List[Any] = [
            {"role": "system", "content": system_prompt},
        ]

        if initial_message:
            self.messages.append(
                {"role": "assistant", "content": initial_message}
            )

    def respond(self, human_input: str):
        self.messages.append({"role": "user", "content": human_input})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})

        return content
