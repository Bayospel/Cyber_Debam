import os

def load_knowledge():
    knowledge_base = ""
    brain_dir = "brain"

    if not os.path.exists(brain_dir):
        return "The brain folder is empty, Boss."

    files = [f for f in os.listdir(brain_dir) if f.endswith('.txt')]

    if not files:
        return "No text manuals found in the brain folder."

    for filename in files:
        with open(os.path.join(brain_dir, filename), 'r') as f:
            knowledge_base += f"\n--- INFO FROM {filename} ---\n"
            knowledge_base += f.read()

    return knowledge_base

def get_context_prompt():
    data = load_knowledge()
    return f"Use this private data to answer: {data[:2000]}" # Limit to 2000 chars for speed
