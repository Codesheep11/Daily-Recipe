from mem0 import Memory
from configs.settings import MEM0_CONFIG
import os

class MemoryManager:
    def __init__(self, api_key):
        os.environ["OPENAI_API_KEY"] = api_key
        self.memory = Memory.from_config(MEM0_CONFIG)

    def retrieve_recent_history(self, user_id, limit=3):
        """
        检索最近的记忆
        IR 概念: Context Retrieval
        """
        results = self.memory.search(query="recent meals", user_id=user_id, limit=limit)
        return [res['memory'] for res in results]

    def add_memory(self, user_id, text):
        """
        写入记忆
        IR 概念: Index Update / Feedback Loop
        """
        self.memory.add(text, user_id=user_id)
        
    def get_all(self, user_id):
        """Debug 用：获取所有记忆"""
        return self.memory.get_all(user_id=user_id)