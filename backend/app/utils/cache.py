"""缓存工具"""
from cachetools import TTLCache

# 品牌列表缓存，5 分钟过期
brand_cache: TTLCache = TTLCache(maxsize=10, ttl=300)

# 高分排行缓存，10 分钟过期
top_rated_cache: TTLCache = TTLCache(maxsize=10, ttl=600)
