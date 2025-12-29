class StateManager:
    """
    Manages state persistence for workflows.
    """
    def __init__(self, use_redis=False):
        self.use_redis = use_redis
        self.local_store = {}
        if use_redis:
            print("Initializing Redis connection for state management...")
            # self.redis = redis.Redis(...)

    def save_state(self, flow_id: str, state: dict):
        if self.use_redis:
            # self.redis.set(flow_id, json.dumps(state))
            pass
        else:
            self.local_store[flow_id] = state

    def get_state(self, flow_id: str):
        if self.use_redis:
            # return json.loads(self.redis.get(flow_id))
            return {}
        return self.local_store.get(flow_id, {})
