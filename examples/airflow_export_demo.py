"""
AIWork Airflow Export Demo
===========================

This example demonstrates how to export AIWork flows to Apache Airflow DAG format:
- Convert Flow to Airflow DAG Python code
- Generate Airflow-compatible task definitions
- Integrate with existing Airflow infrastructure

Learn more: https://github.com/JayeshCC/Aiwork/blob/main/docs/USER_GUIDE.md
"""

import os

from aiwork.core.task import Task
from aiwork.core.flow import Flow
from aiwork.integrations.airflow_exporter import AirflowExporter


def main():
    """Main execution function demonstrating Airflow export."""
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         AIWork Airflow Export Demo                        ║")
    print("║         Convert Flows to Airflow DAGs                     ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    try:
        # ═══════════════════════════════════════════════════════════
        # STEP 1: Define a Simple Flow
        # ═══════════════════════════════════════════════════════════
        
        print("📋 Step 1: Creating AIWork flow...")
        print("   Building a data pipeline with 3 tasks:\n")
        
        flow = Flow("airflow_export_demo")
        
        # Define tasks with descriptions
        print("   1. ✅ Task 'ingest' - Data ingestion")
        flow.add_task(Task("ingest", lambda c: None))
        
        print("   2. ✅ Task 'process' - Data processing (depends on: ingest)")
        flow.add_task(Task("process", lambda c: None), depends_on=["ingest"])
        
        print("   3. ✅ Task 'report' - Report generation (depends on: process)")
        flow.add_task(Task("report", lambda c: None), depends_on=["process"])
        
        print("\n   Flow structure: ingest → process → report\n")

        # ═══════════════════════════════════════════════════════════
        # STEP 2: Export to Airflow DAG
        # ═══════════════════════════════════════════════════════════
        
        print("🔄 Step 2: Exporting to Airflow DAG format...")
        
        output_file = "airflow_dag_export.py"
        AirflowExporter.export(flow, output_file)
        
        print(f"   ✅ Exported to: {output_file}\n")

        # ═══════════════════════════════════════════════════════════
        # STEP 3: Display Generated DAG Code
        # ═══════════════════════════════════════════════════════════
        
        print("═" * 60)
        print("📄 GENERATED AIRFLOW DAG CODE")
        print("═" * 60 + "\n")
        
        with open(output_file, 'r') as f:
            dag_code = f.read()
            print(dag_code)
        
        print("═" * 60)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 4: Cleanup and Summary
        # ═══════════════════════════════════════════════════════════
        
        print("\n🧹 Cleaning up temporary file...")
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"   ✅ Removed: {output_file}")
        
        print("\n" + "═" * 60)
        print("✅ EXPORT COMPLETED SUCCESSFULLY")
        print("═" * 60)
        
        print("\n💡 Usage Instructions:")
        print("   1. Copy generated code to your Airflow dags/ folder")
        print("   2. Update task implementations with actual logic")
        print("   3. Configure Airflow connections and variables")
        print("   4. Deploy and schedule in Airflow UI")
        
        print("\n" + "─" * 60)
        print("📚 Next Steps:")
        print("   1. Learn about Airflow: https://airflow.apache.org")
        print("   2. Customize DAG parameters (schedule, retries, etc.)")
        print("   3. Add Airflow operators (PythonOperator, BashOperator)")
        print("─" * 60 + "\n")
        
    except Exception as e:
        print("\n" + "═" * 60)
        print("❌ EXPORT FAILED")
        print("═" * 60)
        print(f"\nError: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        print("   1. Ensure flow has valid task dependencies")
        print("   2. Check write permissions for output file")
        print("   3. Verify AirflowExporter is available")
        print("═" * 60 + "\n")
        raise


if __name__ == "__main__":
    main()
