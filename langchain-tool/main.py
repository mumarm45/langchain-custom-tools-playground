from core.agent import Agent

def main():
    agent = Agent("You are a helpful mathematical assistant that can perform various operations. Use the tools precisely and explain your reasoning clearly.")
    query = "What is the population of Canada? Multiply it by 0.75"

    # Test query
    # query = "add 10 and 20 and 30 then multiply the result by 2 then divide the result by 3"
    print(f"\n🤖 Query: {query}")
    print("=" * 60)
    
    result = agent.run(query)
    
    print("\n✅ Agent Response:")
    print("=" * 60)
    print("\nMessage sequence:")
    for i, msg in enumerate(result["messages"]):
        print(f"\n--- Message {i+1} ---")
        print(f"Type: {type(msg).__name__}")
        if hasattr(msg, 'content'):
            print(f"Content: {msg.content}")
        if hasattr(msg, 'name'):
            print(f"Name: {msg.name}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"Tool calls: {msg.tool_calls}")

if __name__ == "__main__":
    main()
