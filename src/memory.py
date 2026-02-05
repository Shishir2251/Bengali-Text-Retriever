chat_history = []

def add_to_memory(q, a):
    chat_history.append((q, a))
    return chat_history[-5:]
