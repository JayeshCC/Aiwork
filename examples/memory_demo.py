"""
AIWork Memory Demo
==================

This example demonstrates agent memory and observability features:
- VectorMemory for context storage
- Agent memory recall capabilities
- Metrics collection and reporting

Learn more: https://github.com/JayeshCC/Aiwork/blob/main/docs/USER_GUIDE.md
"""

from aiwork.core.agent import Agent
from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.core.memory import VectorMemory
from aiwork.orchestrator import Orchestrator
from aiwork.core.observability import metrics


def main():
    """Main execution function demonstrating memory and observability."""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         AIWork Memory & Observability Demo                ║")
    print("║         Learn how agents remember context                 ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    try:
        # ═══════════════════════════════════════════════════════════
        # STEP 1: Setup Memory with Context
        # ═══════════════════════════════════════════════════════════
        
        print("📝 Step 1: Initializing Vector Memory...")
        print("   Adding context to memory store:\n")
        
        memory = VectorMemory()
        
        # Add various pieces of information
        contexts = [
            "The secret code is 42.",
            "Project deadline is Dec 31st.",
            "The sky is blue."
        ]
        
        for idx, context in enumerate(contexts, 1):
            memory.add(context)
            print(f"   {idx}. ✅ Added: '{context}'")
        
        print(f"\n   💾 Memory initialized with {len(contexts)} entries\n")

        # ═══════════════════════════════════════════════════════════
        # STEP 2: Create Agent with Memory
        # ═══════════════════════════════════════════════════════════
        
        print("🤖 Step 2: Creating agent with memory capabilities...")
        
        agent = Agent(
            role="Detective",
            goal="Find the secret code from memory",
            backstory="An AI detective who never forgets a clue.",
            memory=memory  # Attach memory to agent
        )
        
        print("   ✅ Agent 'Detective' created with memory access\n")

        # ═══════════════════════════════════════════════════════════
        # STEP 3: Define and Execute Task
        # ═══════════════════════════════════════════════════════════
        
        print("📋 Step 3: Creating task to search memory...\n")
        
        def find_secret(ctx):
            """
            Task handler that uses agent's memory.
            
            Note: When no handler is provided, Task.execute calls
            agent.execute_task automatically, which queries memory.
            """
            return {"result": "Secret Found", "status": "success"}

        task = Task(
            name="search_memory",
            description="What is the secret code?",
            agent=agent
            # No handler means agent.execute_task is used (queries memory)
        )

        # ═══════════════════════════════════════════════════════════
        # STEP 4: Execute Flow
        # ═══════════════════════════════════════════════════════════
        
        print("▶️  Step 4: Executing flow...\n")
        
        flow = Flow("memory_demo_flow")
        flow.add_task(task)

        orchestrator = Orchestrator()
        result = orchestrator.execute(flow, {})

        # ═══════════════════════════════════════════════════════════
        # STEP 5: Display Observability Metrics
        # ═══════════════════════════════════════════════════════════
        
        print("\n" + "═" * 60)
        print("📊 OBSERVABILITY METRICS")
        print("═" * 60)
        
        summary = metrics.get_summary()
        
        if summary:
            print("\nCollected metrics during execution:\n")
            for idx, metric in enumerate(summary, 1):
                print(f"  {idx}. {metric['name']}: {metric['value']}")
                if metric.get('tags'):
                    print(f"     Tags: {metric['tags']}")
        else:
            print("\n   ℹ️  No metrics collected in this run")
        
        # ═══════════════════════════════════════════════════════════
        # STEP 6: Summary
        # ═══════════════════════════════════════════════════════════
        
        print("\n" + "═" * 60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("═" * 60)
        
        print("\n💡 Key Takeaways:")
        print("   • VectorMemory stores and retrieves context efficiently")
        print("   • Agents can query memory to make informed decisions")
        print("   • Observability metrics track execution performance")
        
        print("\n" + "─" * 60)
        print("📚 Next Steps:")
        print("   1. Run: python examples/agents/document_processor/run.py")
        print("   2. Explore: Agent memory with custom embeddings")
        print("   3. Read: docs/USER_GUIDE.md for advanced memory features")
        print("─" * 60 + "\n")
        
        return result
        
    except Exception as e:
        print("\n" + "═" * 60)
        print("❌ DEMO EXECUTION FAILED")
        print("═" * 60)
        print(f"\nError: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Ensure VectorMemory is properly initialized")
        print("   2. Check that agent has memory attached")
        print("   3. Verify AIWork is installed: pip install -e .")
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
