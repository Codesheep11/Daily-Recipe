import random
from datetime import datetime
from core.memory_store import MemoryManager
from tools.mock_search import RestaurantRetriever

class DiningAgent:
    def __init__(self, api_key):
        self.memory_manager = MemoryManager(api_key)
        self.retriever = RestaurantRetriever()
        
    def decide_what_to_eat(self, user_id, user_query):
        """
        执行完整的 IR + RAG 流程
        """
        logs = [] # 用于在前端展示思维链
        
        # 1. [Query Analysis] 获取当前上下文
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 2. [Retrieval - Internal] 从 mem0 获取历史记忆
        recent_memories = self.memory_manager.retrieve_recent_history(user_id)
        memory_str = "; ".join(recent_memories) if recent_memories else "无"
        logs.append(f"🧠 [Memory Retrieval] 检索到近期记忆: {memory_str}")

        # 3. [Logic/Ranking] 简单的规则引擎 (Rule-based Reranking)
        # 实际项目中这里应该调用 LLM 来分析，但为了代码演示清晰，我们写一段 Python 逻辑
        target_flavor = "随机"
        reasoning = ""
        
        if "辛辣" in memory_str or "火锅" in memory_str:
            target_flavor = "清淡"
            reasoning = "检测到近期吃过辛辣食物，触发健康规则 -> 推荐清淡。"
        elif "清淡" in memory_str or "沙拉" in memory_str:
            target_flavor = "辛辣" 
            reasoning = "检测到近期饮食清淡，触发补偿规则 -> 推荐重口味。"
        else:
            target_flavor = random.choice(["辛辣", "清淡", "咸香"])
            reasoning = "无特殊冲突，随机探索口味。"
            
        logs.append(f"🤔 [Reasoning] 决策逻辑: {reasoning} (目标口味: {target_flavor})")

        # 4. [Retrieval - External] 从文档库召回餐厅
        candidates = self.retriever.search(flavor_preference=target_flavor)
        # 按评分排序 (Ranking)
        candidates.sort(key=lambda x: x['rating'], reverse=True)
        top_choice = candidates[0]
        
        logs.append(f"📚 [External Search] 在知识库中召回了 {len(candidates)} 个结果，Top 1 是: {top_choice['name']}")

        # 5. [Generation] 生成最终回复 (此处简化，直接返回结构化文本)
        response_text = (
            f"根据你的历史记录（{memory_str}），"
            f"{reasoning} \n\n"
            f"🚀 **推荐结果**：{top_choice['name']} ({top_choice['category']})\n"
            f"⭐ 评分：{top_choice['rating']} | 口味：{top_choice['flavor']}"
        )

        return response_text, top_choice['name'], logs

    def commit_choice(self, user_id, food_name):
        """用户确认后，更新记忆索引"""
        today = datetime.now().strftime("%Y-%m-%d")
        memory_text = f"On {today}, user chose to eat {food_name}."
        self.memory_manager.add_memory(user_id, memory_text)