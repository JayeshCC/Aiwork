"""
Example: Airflow Export Demo

To run this example, first install the aiwork package:
    pip install -e .

Then run:
    python examples/airflow_export_demo.py
"""

import os

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.integrations.airflow_exporter import AirflowExporter

def main():
    # Define a simple flow
    flow = Flow("airflow_export_demo")
    flow.add_task(Task("ingest", lambda c: None))
    flow.add_task(Task("process", lambda c: None), depends_on=["ingest"])
    flow.add_task(Task("report", lambda c: None), depends_on=["process"])

    # Export
    output_file = "airflow_dag_export.py"
    AirflowExporter.export(flow, output_file)
    
    print("\n--- Generated Airflow DAG Code ---")
    with open(output_file, 'r') as f:
        print(f.read())
        
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    main()
