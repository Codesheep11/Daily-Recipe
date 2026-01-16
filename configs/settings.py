import os

# 这里建议从环境变量读取，或者直接为了演示填入
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "") 

# Mem0 向量数据库配置 (使用本地 Qdrant 存储，无需联网)
MEM0_CONFIG = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": "./local_vector_db", 
        }
    }
}

# 模拟用户ID
DEFAULT_USER_ID = "student_ir_001"