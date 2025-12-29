import os
from ..core.flow import Flow

class AirflowExporter:
    """
    Exports an AIWork Flow to an Apache Airflow DAG file.
    """
    @staticmethod
    def export(flow: Flow, output_path: str):
        """
        Generates a Python file compatible with Apache Airflow.
        """
        dag_id = flow.name
        
        # Template for the Airflow DAG
        content = [
            "from airflow import DAG",
            "from airflow.operators.python import PythonOperator",
            "from datetime import datetime, timedelta",
            "",
            "default_args = {",
            "    'owner': 'aiwork',",
            "    'retries': 1,",
            "    'retry_delay': timedelta(minutes=5),",
            "}",
            "",
            f"with DAG('{dag_id}',",
            "         default_args=default_args,",
            "         description='Exported from AIWork Framework',",
            "         schedule_interval=None,",
            "         start_date=datetime(2023, 1, 1),",
            "         catchup=False) as dag:",
            ""
        ]

        # Define tasks
        # Note: We can't easily export the actual python logic of the functions 
        # unless we pickle them or assume they are importable. 
        # For this export, we will create placeholder operators or assume a generic wrapper.
        
        for task_name in flow.tasks:
            content.append(f"    t_{task_name} = PythonOperator(")
            content.append(f"        task_id='{task_name}',")
            content.append(f"        python_callable=lambda: print('Executing {task_name}'),")
            content.append("    )")
            content.append("")

        # Define dependencies
        for task_name, deps in flow.dependencies.items():
            for dep in deps:
                content.append(f"    t_{dep} >> t_{task_name}")

        # Write to file
        with open(output_path, 'w') as f:
            f.write('\n'.join(content))
        
        print(f"Successfully exported Flow '{flow.name}' to Airflow DAG at {output_path}")
