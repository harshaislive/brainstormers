import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from getpass import getpass
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from crewai import LLM

def get_timestamp():
    return datetime.now().strftime("%I:%M %p")

def authenticate_gui():
    """Check password if APP_PASSWORD is set in environment"""
    required_password = os.getenv("APP_PASSWORD")
    if not required_password:
        return True  # No password required
    
    # Simple password dialog
    password = tk.simpledialog.askstring(
        "Authentication Required", 
        "🔐 Enter password:",
        show='*'
    )
    
    if password == required_password:
        messagebox.showinfo("Access Granted", "✅ Welcome to Brainstormers!")
        return True
    else:
        messagebox.showerror("Access Denied", "❌ Incorrect password!")
        return False

# Azure OpenAI config for LiteLLM (which CrewAI uses internally)
# Set environment variables for LiteLLM to use Azure
api_key = os.getenv("AZURE_OPENAI_API_KEY")
if not api_key:
    messagebox.showerror("Configuration Error", 
                        "Please set AZURE_OPENAI_API_KEY environment variable or create a .env file")
    exit(1)
    
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

class BrainstormGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 BRAINSTORM GROUP CHAT")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Variables
        self.conversation = []
        self.agents = [alpha, beta, gamma]
        self.agent_names = ["Alpha 🔬", "Beta ⚡", "Gamma 🧠"]
        self.hypothesis = ""
        
        # Create UI
        self.create_widgets()
        
        # Start with hypothesis input
        self.get_hypothesis()
    
    def create_widgets(self):
        # Main chat display (terminal-like)
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            width=100,
            height=35,
            bg='black',
            fg='white',
            font=('Consolas', 10),
            insertbackground='white'
        )
        self.chat_display.pack(padx=10, pady=(10, 5), fill='both', expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='black')
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Input label
        tk.Label(input_frame, text="💬 You:", bg='black', fg='white', font=('Consolas', 10)).pack(side='left')
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            bg='black',
            fg='white',
            font=('Consolas', 10),
            insertbackground='white'
        )
        self.input_field.pack(side='left', fill='x', expand=True, padx=(5, 5))
        self.input_field.bind('<Return>', self.send_message)
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            bg='gray20',
            fg='white',
            font=('Consolas', 10),
            command=self.send_message
        )
        self.send_button.pack(side='right')
    
    def get_hypothesis(self):
        # Simple dialog for hypothesis
        hypothesis = tk.simpledialog.askstring(
            "Hypothesis",
            "📝 Enter the starting hypothesis/topic:",
            parent=self.root
        )
        if hypothesis:
            self.hypothesis = hypothesis
            self.conversation = [f"Hypothesis: {hypothesis}"]
            self.display_message("="*50)
            self.display_message("🧠 BRAINSTORM GROUP CHAT")
            self.display_message("="*50)
            self.display_message(f"💭 Group Chat: Brainstorming '{hypothesis}'")
            self.display_message("="*50)
            self.display_message("📝 Note: Use @Alpha, @Beta, @Gamma to mention specific agents. They can mention each other and @You too!")
            self.display_message("🔄 Flow: You message → Alpha responds → Beta responds → Gamma responds")
            self.display_message("="*50)
        else:
            self.root.quit()
    
    def display_message(self, message):
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.root.update()
    
    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message:
            return
        
        if message.lower() == "exit":
            self.display_message("👋 Left the chat")
            self.root.quit()
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Display user message
        self.display_message(f"\n💬 You: {message}")
        self.display_message(f"[{get_timestamp()}]")
        
        # Add to conversation
        self.conversation.append(f"You: {message}")
        
        # Disable input while agents respond
        self.input_field.config(state='disabled')
        self.send_button.config(state='disabled')
        
        # Start agent responses in background thread
        threading.Thread(target=self.get_agent_responses, daemon=True).start()
    
    def get_agent_responses(self):
        try:
            context = "\n".join(self.conversation)
            
            # All 3 agents respond in order
            for i, (agent, agent_name) in enumerate(zip(self.agents, self.agent_names)):
                response = self.get_agent_response(agent, agent_name, context)
                
                # Display response
                self.root.after(0, self.display_message, f"\n💬 {agent_name}")
                self.root.after(0, self.display_message, response)
                self.root.after(0, self.display_message, f"[{get_timestamp()}]")
                
                # Add to conversation
                self.conversation.append(f"{agent_name}: {response}")
                
                # Update context for next agent
                context = "\n".join(self.conversation)
            
            # Add separator
            self.root.after(0, self.display_message, "\n" + "="*50)
            
        except Exception as e:
            self.root.after(0, self.display_message, f"Error: {str(e)}")
        finally:
            # Re-enable input
            self.root.after(0, lambda: self.input_field.config(state='normal'))
            self.root.after(0, lambda: self.send_button.config(state='normal'))
            self.root.after(0, lambda: self.input_field.focus())
    
    def get_agent_response(self, agent, agent_name, context):
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

# Need to import simpledialog
import tkinter.simpledialog

def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window during authentication
    
    # Authentication check
    if not authenticate_gui():
        root.quit()
        return
    
    root.deiconify()  # Show main window after authentication
    app = BrainstormGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()