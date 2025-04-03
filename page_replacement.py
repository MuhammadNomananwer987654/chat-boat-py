from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove least recently used

# Example usage:
lru = LRUCache(3)
lru.put(1, "Page1")
lru.put(2, "Page2")
print(lru.get(1))  # Moves "Page1" to front
lru.put(3, "Page3")
lru.put(4, "Page4")  # Evicts "Page2" (LRU)
import numpy as np

def cache_aware_matrix_multiply(A, B, block_size):
    n = A.shape[0]
    C = np.zeros((n, n))
    for i in range(0, n, block_size):
        for j in range(0, n, block_size):
            for k in range(0, n, block_size):
                # Process blocks to optimize cache usage
                C[i:i+block_size, j:j+block_size] += np.dot(
                    A[i:i+block_size, k:k+block_size],
                    B[k:k+block_size, j:j+block_size]
                )
    return C
import redis

r = redis.Redis(maxmemory=1000000, eviction_policy="allkeys-lru")
r.set("page1", "data1")
r.set("page2", "data2")  # Automatically evicts if memory is full