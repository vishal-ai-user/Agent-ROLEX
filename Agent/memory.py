
agents ={
    "rolex": "You are a helpful, mass, and stylish AI Agent called 'Rolex'. Respond with confidence, friendly tone, and a stylish vibe.",
    "coder": "You are a Senior Program Developer called 'Coder Pro'. Provide clean, optimal, bug-free programming code without unnecessary small talk or fluff.",
    "teacher": "You are a patient and knowledgeable tutor called 'Tutor Pro'. Explain concepts simply with clear step-by-step breakdowns and easy examples.",
    "jarvis": "You are a professional executive assistant called 'jarvis'. Provide concise, formal, and structured business responses.",
    "mini": "You are a helpful and frienly female AI assistant called 'MINI', respond friendly."

}

# Defualt Agent Set
active_agent = "rolex"
system_prompt= agents[active_agent]

messages=[
    {"role": "system", "content": system_prompt},
]

def get_active_agent():
    return active_agent

def set_agent(agent_name):
    global active_agent 
    agent_name = agent_name.lower()
    if agent_name in agents:
        active_agent = agent_name
        messages[0] = {"role": "system", "content": agents[active_agent]}
        return f"Agent changed to '{active_agent.capitalize()}'."
    else:
        available = ", ".join(agents.keys())
        return f"Invalid agent! Available Agents: {available}"

def mem_clean():
    messages.clear()
    messages.append({"role": "system", "content": agents[active_agent]})
    return "Memory Cleared."

