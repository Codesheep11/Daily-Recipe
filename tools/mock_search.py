import json
import os

class RestaurantRetriever:
    def __init__(self, data_path="data/restaurants.json"):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)
        else:
            self.corpus = []

    def search(self, flavor_preference=None):
        """
        模拟基于 Metadata 的检索 (Boolean Retrieval)
        如果用户想要'清淡'，只召回 flavor='清淡' 的文档
        """
        if not flavor_preference:
            return self.corpus
        
        # 简单的倒排索引逻辑模拟
        results = [r for r in self.corpus if r['flavor'] == flavor_preference]
        
        # 如果没找到，为了鲁棒性返回全部
        return results if results else self.corpus