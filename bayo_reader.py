import os

def load_knowledge():
    knowledge_base = ""
    brain_dir = "brain"

    # Check if directory exists
    if not os.path.exists(brain_dir):
        return "System Warning: 'brain' folder not found on server."

    # Get all .txt files
    try:
        files = [f for f in os.listdir(brain_dir) if f.endswith('.txt')]
    except Exception as e:
        return f"Error accessing brain: {e}"

    if not files:
        return "No tactical manuals detected in the brain folder."

    # Read files and combine
    for filename in files:
        try:
            with open(os.path.join(brain_dir, filename), 'r', encoding='utf-8') as f:
                knowledge_base += f"\n[ SOURCE: {filename} ]\n"
                # We read only first 5000 chars per file to prevent memory overflow
                knowledge_base += f.read(5000) 
        except:
            continue

    return knowledge_base

def get_context_prompt():
    data = load_knowledge()
    # We pass this to Groq to give it "Private Context"
    return f"\n--- PRIVATE KNOWLEDGE BASE ---\n{data[:3000]}\n--- END OF PRIVATE DATA ---"
