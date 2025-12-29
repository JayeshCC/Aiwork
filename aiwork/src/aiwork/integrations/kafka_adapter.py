class KafkaAdapter:
    """
    Adapter for Apache Kafka messaging.
    Handles producing tasks to topics and consuming results.
    """
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.bootstrap_servers = bootstrap_servers
        print(f"Initialized Kafka Adapter connecting to {bootstrap_servers}")
        # self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def produce_task(self, topic: str, task_payload: dict):
        """
        Sends a task to a Kafka topic.
        """
        print(f"[Kafka] Producing task to topic '{topic}': {task_payload}")
        # self.producer.produce(topic, json.dumps(task_payload).encode('utf-8'))
        # self.producer.flush()

    def consume_tasks(self, topic: str):
        """
        Generator that yields tasks from a topic.
        """
        print(f"[Kafka] Subscribed to topic '{topic}'")
        # Mocking a stream of tasks
        mock_tasks = [
            {"task_id": "1", "name": "mock_task_1", "params": {}},
            {"task_id": "2", "name": "mock_task_2", "params": {}}
        ]
        for t in mock_tasks:
            yield t
