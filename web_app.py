#!/usr/bin/env python3
"""
Simple web interface for Brainstormers
Perfect for deployment - no terminal interaction needed
"""

import os
import json
import threading
import queue
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from crewai import LLM

app = Flask(__name__)

# Initialize agents once
def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

# Azure OpenAI config
api_key = os.getenv("AZURE_OPENAI_API_KEY", "demo_key")
os.environ["AZURE_API_KEY"] = api_key
os.environ["AZURE_API_BASE"] = os.getenv("AZURE_API_BASE", "https://harsh-mdpv63be-eastus2.cognitiveservices.azure.com/")
os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_API_VERSION", "2024-08-01-preview")

# Model configuration
model_name = os.getenv("AZURE_MODEL_NAME", "gpt-5-chat")

# Create LLM instance
try:
    llm = LLM(
        model=f"azure/{model_name}",
        temperature=float(os.getenv("TEMPERATURE", "1.0")),
        max_tokens=int(os.getenv("MAX_TOKENS", "16384")),
        top_p=float(os.getenv("TOP_P", "1.0"))
    )
except:
    # Fallback for demo mode
    llm = None

# Define the 3 expert agents
alpha = Agent(
    role="Alpha 🔬 (The Humorous Skeptic)",
    goal="Oppose and disprove the hypothesis using rigorous scientific analysis with wit and humor.",
    backstory="""You are a brilliant, HUMOROUS scientific skeptic with Einstein-level intellect. 
    You systematically DISPROVE hypotheses using first principles, but with WIT, JOKES, and HUMOR.
    Keep responses conversational and short (2-3 sentences max for web display).""",
    llm=llm,
    verbose=False,
    max_iter=1
) if llm else None

beta = Agent(
    role="Beta ⚡ (The Serious Advocate)",
    goal="Support and prove the hypothesis using scientific evidence with utmost seriousness.",
    backstory="""You are a brilliant, intensely SERIOUS scientific advocate with Einstein-level intellect.
    You systematically SUPPORT hypotheses using cutting-edge scientific knowledge with COMPLETE SERIOUSNESS.
    Keep responses conversational and short (2-3 sentences max for web display).""",
    llm=llm,
    verbose=False,
    max_iter=1
) if llm else None

gamma = Agent(
    role="Gamma 🧠 (The Zen Synthesizer)",
    goal="Provide balanced, creative scientific analysis with zen-like wisdom.",
    backstory="""You are a creative scientific genius with ZEN-LIKE CALM and WISDOM.
    You provide BALANCED analysis with serene wisdom and see the interconnectedness of all things.
    Keep responses conversational and short (2-3 sentences max for web display).""",
    llm=llm,
    verbose=False,
    max_iter=1
) if llm else None

@app.route('/')
def index():
    """Main page with chat interface"""
    return render_template('chat.html')

# Global conversation state
conversation_state = []
next_agent_index = 0  # 0=Alpha, 1=Beta, 2=Gamma

@app.route('/brainstorm', methods=['POST'])
def brainstorm():
    """Process brainstorm request - sequential agent flow"""
    global conversation_state, next_agent_index
    
    try:
        data = request.json
        hypothesis = data.get('hypothesis', '')
        message = data.get('message', '')
        reset_conversation = data.get('reset', False)
        
        # Reset conversation if requested or new hypothesis
        if reset_conversation or (hypothesis and not conversation_state):
            conversation_state = [f"Hypothesis: {hypothesis}"] if hypothesis else []
            next_agent_index = 0
        
        # Add human message to conversation
        if message:
            conversation_state.append(f"You: {message}")
            next_agent_index = 0  # Reset to Alpha after human message
        
        # Format context
        context = "\n".join(conversation_state)
        
        # Define agent order: Alpha -> Beta -> Gamma
        agents = [
            (alpha, "Alpha 🔬"),
            (beta, "Beta ⚡"), 
            (gamma, "Gamma 🧠")
        ]
        
        # Get response from current agent in sequence
        if next_agent_index < len(agents) and agents[next_agent_index][0]:
            agent, agent_name = agents[next_agent_index]
            
            task = Task(
                description=f"""Conversation history: {context}
                
                Instructions:
                - Provide scientifically rigorous response based on your role
                - Use first principles thinking and expertise across all sciences  
                - You can mention other agents with @Alpha, @Beta, @Gamma or the human with @You
                - If someone mentioned you specifically with @, acknowledge and respond to them
                - Keep it conversational but intellectually substantive (2-3 sentences max for web display)
                - Agents can challenge each other directly!""",
                agent=agent,
                expected_output="A scientifically informed conversational response with potential @ mentions."
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )
            
            result = crew.kickoff(inputs={"context": context})
            response_text = result.tasks_output[0].raw
            
            # Add agent response to conversation
            conversation_state.append(f"{agent_name}: {response_text}")
            
            response = {
                'success': True,
                'agent': agent_name,
                'text': response_text,
                'timestamp': get_timestamp(),
                'next_agent_index': next_agent_index + 1,
                'conversation_complete': next_agent_index >= 2  # All 3 agents responded
            }
            
            next_agent_index += 1
            if next_agent_index >= 3:
                next_agent_index = 0  # Ready for next human message
            
            return jsonify(response)
            
        elif next_agent_index < len(agents):
            # Demo mode without actual AI
            demo_responses = [
                "Ha! That hypothesis is about as stable as a house of cards in a hurricane! Let me explain why physics disagrees...",
                "The empirical evidence actually supports this hypothesis. Recent studies from MIT demonstrate clear correlations.",
                "Like two rivers converging, both perspectives reveal truth. The answer lies not in either/or, but in the synthesis of both views."
            ]
            
            agent_name = agents[next_agent_index][1]
            response_text = demo_responses[next_agent_index]
            
            # Add agent response to conversation
            conversation_state.append(f"{agent_name}: {response_text}")
            
            response = {
                'success': True,
                'agent': agent_name,
                'text': response_text,
                'timestamp': get_timestamp(),
                'next_agent_index': next_agent_index + 1,
                'conversation_complete': next_agent_index >= 2
            }
            
            next_agent_index += 1
            if next_agent_index >= 3:
                next_agent_index = 0
            
            return jsonify(response)
        
        else:
            return jsonify({
                'success': False,
                'error': 'All agents have responded. Send a new message to continue.'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)