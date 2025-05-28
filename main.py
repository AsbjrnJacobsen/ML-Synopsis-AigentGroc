"""from agent.grocery_agent import grocery_agent

def run():
    while True:
        user_input = input("🧑: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        reply = grocery_agent.generate_reply(messages=[{"role": "user", "content": user_input}])
        print(f"🤖: {reply}")

if __name__ == "__main__":
    run()
"""