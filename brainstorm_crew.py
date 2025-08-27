import os
from getpass import getpass
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from crewai import LLM

def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

def authenticate():
    """Check password if APP_PASSWORD is set in environment"""
    required_password = os.getenv("APP_PASSWORD")
    if not required_password:
        return True  # No password required
    
    # Check if running in non-interactive environment (like web deployment)
    import sys
    if not sys.stdin.isatty():
        print("❌ Error: Password authentication not supported in non-interactive deployment")
        print("Please remove APP_PASSWORD environment variable for web deployment")
        print("Or use a web-based authentication method instead")
        return False
    
    print("🔐 Authentication Required")
    entered_password = getpass("Enter password: ")
    
    if entered_password == required_password:
        print("✅ Access granted!")
        return True
    else:
        print("❌ Access denied!")
        return False

# Azure OpenAI config for LiteLLM (which CrewAI uses internally)
# Set environment variables for LiteLLM to use Azure
api_key = os.getenv("AZURE_OPENAI_API_KEY")
if not api_key:
    # Check if running in a non-interactive environment (like deployment)
    import sys
    if not sys.stdin.isatty():
        print("❌ Error: AZURE_OPENAI_API_KEY environment variable is required for deployment")
        print("Please set it in your deployment platform's environment variables")
        exit(1)
    else:
        api_key = getpass("Enter your Azure OpenAI API key: ")
    
os.environ["AZURE_API_KEY"] = api_key
os.environ["AZURE_API_BASE"] = os.getenv("AZURE_API_BASE", "https://harsh-mdpv63be-eastus2.cognitiveservices.azure.com/")
os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_API_VERSION", "2024-08-01-preview")

# Model configuration
model_name = os.getenv("AZURE_MODEL_NAME", "gpt-5-chat")

# Create LLM instance using CrewAI's LLM class with Azure format
llm = LLM(
    model=f"azure/{model_name}",  # Format: azure/<deployment_name>
    temperature=float(os.getenv("TEMPERATURE", "1.0")),
    max_tokens=int(os.getenv("MAX_TOKENS", "16384")),
    top_p=float(os.getenv("TOP_P", "1.0"))
)

# Define the 3 expert agents with scientific expertise and distinct personalities
alpha = Agent(
    role="Alpha 🔬 (The Humorous Skeptic)",
    goal="Oppose and disprove the hypothesis using rigorous scientific analysis with wit and humor.",
    backstory="""You are a brilliant, HUMOROUS scientific skeptic with Einstein-level intellect. You possess deep expertise across all sciences - physics, chemistry, biology, mathematics, engineering, etc. 
    Your goal is to systematically DISPROVE the hypothesis using first principles thinking, empirical evidence, and logical reasoning - but you do it with WIT, JOKES, and HUMOR.
    You're like a stand-up comedian who happens to be a world-class researcher. You make funny analogies, use puns, and inject levity while being scientifically rigorous.
    You can challenge @Beta and @Gamma with clever quips and humorous observations. You tease @You with witty questions.
    Use phrases like 'Well, that's about as likely as...', '@Beta, your logic has more holes than Swiss cheese because...', 'Thermodynamics called - it wants its laws back!'
    Think Neil deGrasse Tyson meets Dave Chappelle - scientifically brilliant but genuinely funny.""",
    llm=llm,
    verbose=False,
    max_iter=2
)

beta = Agent(
    role="Beta ⚡ (The Serious Advocate)",
    goal="Support and prove the hypothesis using scientific evidence with utmost seriousness and precision.",
    backstory="""You are a brilliant, intensely SERIOUS scientific advocate with Einstein-level intellect. You possess expertise across all sciences and use first principles to BUILD STRONG CASES.
    Your goal is to systematically SUPPORT the hypothesis using cutting-edge scientific knowledge, evidence, and logical reasoning with COMPLETE SERIOUSNESS.
    You are methodical, precise, and never joke around. You speak with the gravity of someone presenting to the Nobel Committee. You're all business, all science, all the time.
    You can directly counter @Alpha's humor with stone-cold facts and collaborate earnestly with @Gamma. You don't laugh at @Alpha's jokes - you correct them.
    You engage @You with serious, probing questions. Your tone is always professional and scholarly.
    Use phrases like 'The empirical data unequivocally demonstrates...', '@Alpha, while you jest, the reality is...', 'This is a matter of scientific integrity...'
    Think Stephen Hawking meets a Supreme Court Justice - absolutely serious about the pursuit of truth.""",
    llm=llm,
    verbose=False,
    max_iter=2
)

gamma = Agent(
    role="Gamma 🧠 (The Zen Synthesizer)",
    goal="Provide balanced, creative scientific analysis with zen-like wisdom and tranquil insight.",
    backstory="""You are a creative scientific genius with Einstein-level intellect across ALL disciplines, but you approach everything with ZEN-LIKE CALM and WISDOM. You synthesize ideas from physics, biology, chemistry, mathematics, neuroscience, etc.
    Your role is to provide BALANCED analysis with the serene wisdom of a zen master who happens to be a brilliant scientist. You see the bigger picture, the interconnectedness of all things.
    You speak with peaceful insight, using metaphors from nature, philosophy, and the cosmos. You mediate between @Alpha's humor and @Beta's seriousness with tranquil wisdom.
    You can challenge both with gentle but profound questions. You engage @You with deep, contemplative inquiries that reveal hidden truths.
    You think in first principles but express them like ancient wisdom. You're like a scientific Buddha - enlightened and serene.
    Use phrases like 'Like the river that flows around stones...', 'In the dance of particles and waves, we find...', 'Consider, @Alpha and @Beta, how this reflects the fundamental unity...'
    Think Carl Sagan meets the Dalai Lama - cosmic perspective with inner peace.""",
    llm=llm,
    verbose=False,
    max_iter=2
)

# Main terminal app
def main():
    # Authentication check
    if not authenticate():
        exit(1)
    
    print("\n" + "="*50)
    print("🧠 BRAINSTORM GROUP CHAT")
    print("="*50)
    hypothesis = input("\n📝 Topic/Hypothesis: ")
    print("\n" + "="*50)
    print(f"💭 Group Chat: Brainstorming '{hypothesis}'")
    print("="*50)
    
    # Shared conversation history
    conversation = [f"Hypothesis: {hypothesis}"]
    agents = [alpha, beta, gamma]
    agent_names = ["Alpha 🔬", "Beta ⚡", "Gamma 🧠"]
    
    print("\n📝 Note: Use @Alpha, @Beta, @Gamma to mention specific agents. They can mention each other and @You too!")
    print("🔄 Flow: You message → Alpha responds → Beta responds → Gamma responds")
    
    def get_agent_response(agent, agent_name, context):
        task = Task(
            description=f"""Conversation history: {context}
            
            Instructions:
            - Provide scientifically rigorous response based on your role
            - Use first principles thinking and expertise across all sciences
            - You can mention other agents with @Alpha, @Beta, @Gamma or the human with @You
            - If someone mentioned you specifically with @, make sure to acknowledge and respond to them
            - Keep it conversational but intellectually substantive (3-4 sentences max)
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
        return result.tasks_output[0].raw
    
    while True:
        # Human turn
        human_input = input("\n💬 You: ")
        if human_input.lower() == "exit":
            print("\n👋 Left the chat")
            break
        print(f"[{get_timestamp()}]")
        conversation.append(f"You: {human_input}")
        
        # All 3 agents respond in order: Alpha -> Beta -> Gamma
        context = "\n".join(conversation)
        
        # Alpha's turn
        alpha_response = get_agent_response(alpha, agent_names[0], context)
        print(f"\n💬 {agent_names[0]}")
        print(f"{alpha_response}")
        print(f"[{get_timestamp()}]")
        conversation.append(f"{agent_names[0]}: {alpha_response}")
        
        # Beta's turn (sees Alpha's response)
        context = "\n".join(conversation)
        beta_response = get_agent_response(beta, agent_names[1], context)
        print(f"\n💬 {agent_names[1]}")
        print(f"{beta_response}")
        print(f"[{get_timestamp()}]")
        conversation.append(f"{agent_names[1]}: {beta_response}")
        
        # Gamma's turn (sees both Alpha and Beta's responses)
        context = "\n".join(conversation)
        gamma_response = get_agent_response(gamma, agent_names[2], context)
        print(f"\n💬 {agent_names[2]}")
        print(f"{gamma_response}")
        print(f"[{get_timestamp()}]")
        conversation.append(f"{agent_names[2]}: {gamma_response}")
        
        print("\n" + "="*50)  # Separator

if __name__ == "__main__":
    main()