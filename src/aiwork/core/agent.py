from typing import List, Any, Dict, Optional, Callable

class Agent:
    """
    Represents an autonomous agent with a specific role and set of tools.
    
    Args:
        role: Agent's role/name
        goal: Agent's primary objective
        backstory: Agent's background/context
        tools: List of tools available to agent
        memory: Memory instance for context retrieval
        llm: LLM instance (BaseLLM) for reasoning. If None, agent uses deterministic logic.
        verbose: Enable verbose output
    """
    def __init__(
        self, 
        role: str, 
        goal: str, 
        backstory: str,
        tools: List[Any] = None,
        memory: Any = None,
        llm: Any = None,
        verbose: bool = True
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.memory = memory
        self.llm = llm
        self.verbose = verbose

    def execute_task(self, task_description: str, context: Dict[str, Any]) -> Any:
        """
        Simulates the Agent 'thinking' and executing a task.
        """
        if self.verbose:
            print(f"\n🤖 [Agent: {self.role}]")
            print(f"   Goal: {self.goal}")
            print(f"   Working on: {task_description}")

        # 1. Retrieve Context from Memory
        memory_context = ""
        if self.memory:
            relevant_docs = self.memory.search(task_description)
            if relevant_docs:
                print(f"    [Agent: {self.role}] Recalled {len(relevant_docs)} memories.")
                memory_context = "\nRelevant Context:\n" + "\n".join([f"- {d['text']}" for d in relevant_docs])

        # 2. Formulate Prompt (Simulation)
        # In a real LLM scenario, this prompt would be sent to the model.
        full_prompt = f"{self.backstory}\nGoal: {self.goal}\nTask: {task_description}\n{memory_context}"
        
        # 3. Generate Response
        if self.llm:
            # Agent has LLM - use it for reasoning
            try:
                response = self.llm.generate(full_prompt)
                
                # Store interaction in memory if available
                if self.memory:
                    self.memory.add(
                        f"Task: {task_description}\nResponse: {response}",
                        metadata={"role": self.role, "type": "task_execution"}
                    )
                
                return response
            except Exception as e:
                if self.verbose:
                    print(f"    [Agent: {self.role}] LLM call failed: {e}")
                # Fallback to deterministic response
                return f"[Agent {self.role}] Task: {task_description} (LLM unavailable)"
        else:
            # No LLM configured - deterministic behavior
            if self.verbose:
                print(f"    [Agent: {self.role}] No LLM configured, using deterministic mode")
            return f"[Agent {self.role} Result] Processed: {task_description}"
