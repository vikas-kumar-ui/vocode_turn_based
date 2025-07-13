from vocode.turn_based.agent.groq_agent import GroqAgent

# Create the agent
agent = GroqAgent(
    system_prompt="You are a helpful assistant.",
    initial_message="Hello! How can I help you?",
    api_key="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",
    model_name="llama3-8b-8192"
)

# Interact with it
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = agent.respond(user_input)
    print("GroqBot:", response)
