"""
Guardrails Demo - Input and Output Validation
==============================================

Demonstrates two-stage validation:
- Input guardrails validate data BEFORE execution
- Output guardrails validate results AFTER execution
"""

from aiwork.core.task import Task
from aiwork.core.guardrail import Guardrail
from aiwork.core.flow import Flow
from aiwork.orchestrator import Orchestrator


# Define input validation
def validate_positive_number(ctx):
    """Ensure input contains positive number."""
    value = ctx.get("value", 0)
    return isinstance(value, (int, float)) and value > 0

input_guard = Guardrail(
    name="positive_number_input",
    validator=validate_positive_number,
    description="Input must be positive number"
)


# Define output validation
def validate_result_format(result):
    """Ensure result is dict with required keys."""
    return isinstance(result, dict) and "result" in result

output_guard = Guardrail(
    name="result_format",
    validator=validate_result_format,
    description="Output must be dict with 'result' key"
)


# Task with both input and output guardrails
def calculate_square(ctx):
    """Calculate square of input value."""
    value = ctx["value"]
    return {"result": value ** 2, "input": value}


# Example 1: Valid input and output
print("=== Example 1: Valid Input/Output ===\n")

task1 = Task(
    name="square",
    handler=calculate_square,
    input_guardrails=[input_guard],
    guardrails=[output_guard],
    verbose=True
)

flow1 = Flow("valid_flow")
flow1.add_task(task1)

orchestrator = Orchestrator()
result1 = orchestrator.execute(flow1, {"value": 5})

print(f"Result: {result1['outputs']['square']}\n")


# Example 2: Invalid input (negative number)
print("=== Example 2: Invalid Input (Fails Input Guardrail) ===\n")

task2 = Task(
    name="square",
    handler=calculate_square,
    input_guardrails=[input_guard],
    guardrails=[output_guard],
    verbose=True,
    retries=0  # Don't retry, fail immediately
)

flow2 = Flow("invalid_input_flow")
flow2.add_task(task2)

try:
    result2 = orchestrator.execute(flow2, {"value": -5})
except ValueError as e:
    print(f"❌ Task failed as expected: {e}\n")


# Example 3: Invalid output
print("=== Example 3: Invalid Output (Fails Output Guardrail) ===\n")

def bad_handler(ctx):
    """
    Returns invalid format (missing 'result' key).
    
    This handler intentionally produces invalid output to demonstrate
    output guardrail validation failure.
    """
    return {"wrong_key": "value"}

task3 = Task(
    name="bad_task",
    handler=bad_handler,
    guardrails=[output_guard],
    verbose=True,
    retries=0
)

flow3 = Flow("invalid_output_flow")
flow3.add_task(task3)

try:
    result3 = orchestrator.execute(flow3, {})
except ValueError as e:
    print(f"❌ Task failed as expected: {e}\n")


print("=== Guardrails Demo Complete ===")
print("✅ Input guardrails prevent bad data from entering execution")
print("✅ Output guardrails prevent bad results from propagating")
