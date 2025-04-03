import sys
from functools import lru_cache
import numpy as np
from collections import namedtuple, defaultdict
import array
import tracemalloc
from pympler import asizeof

class MemoryOptimizer:
    """
    A class demonstrating various memory optimization techniques in Python.
    """
    
    def __init__(self):
        self.data_structures = {}
        
    def demonstrate_slot_optimization(self):
        """
        Demonstrate memory savings using __slots__ in classes.
        """
        print("\n=== Slot Optimization ===")
        
        class RegularClass:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
                
        class SlotClass:
            __slots__ = ['x', 'y', 'z']
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
                
        # Create instances
        regular = RegularClass(1, 2, 3)
        slot = SlotClass(1, 2, 3)
        
        # Compare sizes
        print(f"Regular class instance size: {asizeof.asizeof(regular)} bytes")
        print(f"Slot class instance size: {asizeof.asizeof(slot)} bytes")
        print(f"Memory savings: {asizeof.asizeof(regular) - asizeof.asizeof(slot)} bytes per instance")
        
    def demonstrate_memoryview(self):
        """
        Demonstrate memory efficiency using memoryview for large data.
        """
        print("\n=== Memoryview Optimization ===")
        
        # Create a large byte array
        large_data = bytearray(10_000_000)  # 10MB of data
        
        # Regular slicing creates copies
        slice_copy = large_data[1_000_000:2_000_000]
        
        # Memoryview creates a view without copying
        mem_view = memoryview(large_data)[1_000_000:2_000_000]
        
        print(f"Size of slice copy: {asizeof.asizeof(slice_copy) / 1024:.2f} KB")
        print(f"Size of memoryview: {asizeof.asizeof(mem_view) / 1024:.2f} KB")
        
    def demonstrate_array_module(self):
        """
        Demonstrate memory efficiency using array module instead of lists.
        """
        print("\n=== Array Module Optimization ===")
        
        # Create a large list of integers
        int_list = list(range(1_000_000))
        
        # Create an array of integers
        int_array = array.array('i', range(1_000_000))
        
        print(f"Size of list: {asizeof.asizeof(int_list) / (1024*1024):.2f} MB")
        print(f"Size of array: {asizeof.asizeof(int_array) / (1024*1024):.2f} MB")
        
    def demonstrate_namedtuple(self):
        """
        Demonstrate memory efficiency using namedtuple instead of classes.
        """
        print("\n=== Namedtuple Optimization ===")
        
        class RegularPoint:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
                
        Point = namedtuple('Point', ['x', 'y', 'z'])
        
        # Create instances
        regular = RegularPoint(1, 2, 3)
        named = Point(1, 2, 3)
        
        print(f"Regular class size: {asizeof.asizeof(regular)} bytes")
        print(f"Namedtuple size: {asizeof.asizeof(named)} bytes")
        
    def demonstrate_generators(self):
        """
        Demonstrate memory efficiency using generators.
        """
        print("\n=== Generator Optimization ===")
        
        def create_list(n):
            return [i for i in range(n)]
            
        def create_generator(n):
            return (i for i in range(n))
            
        # Create large sequences
        n = 1_000_000
        list_seq = create_list(n)
        gen_seq = create_generator(n)
        
        print(f"List memory usage: {asizeof.asizeof(list_seq) / (1024*1024):.2f} MB")
        print(f"Generator memory usage: {asizeof.asizeof(gen_seq) / 1024:.2f} KB")
        
    def demonstrate_memoization(self):
        """
        Demonstrate memory-performance tradeoff with memoization.
        """
        print("\n=== Memoization Optimization ===")
        
        @lru_cache(maxsize=None)
        def fib_cached(n):
            if n < 2:
                return n
            return fib_cached(n-1) + fib_cached(n-2)
            
        def fib_uncached(n):
            if n < 2:
                return n
            return fib_uncached(n-1) + fib_uncached(n-2)
            
        # Test performance
        import time
        n = 35
        
        start = time.time()
        result = fib_uncached(n)
        uncached_time = time.time() - start
        
        start = time.time()
        result = fib_cached(n)
        cached_time = time.time() - start
        
        print(f"Uncached fib({n}): {uncached_time:.4f} seconds")
        print(f"Cached fib({n}): {cached_time:.4f} seconds")
        print(f"Cache info: {fib_cached.cache_info()}")
        
    def demonstrate_string_interning(self):
        """
        Demonstrate memory savings with string interning.
        """
        print("\n=== String Interning ===")
        
        # Create many duplicate strings
        strings = ['hello world'] * 1000 + ['python'] * 1000 + ['optimization'] * 1000
        
        # Without interning
        tracemalloc.start()
        before = tracemalloc.get_traced_memory()
        
        list_no_intern = [s for s in strings]
        after = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Memory without interning: {(after[1] - before[1]) / 1024:.2f} KB")
        
        # With interning
        tracemalloc.start()
        before = tracemalloc.get_traced_memory()
        
        list_intern = [sys.intern(s) for s in strings]
        after = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"Memory with interning: {(after[1] - before[1]) / 1024:.2f} KB")
        
    def demonstrate_numpy_arrays(self):
        """
        Demonstrate memory efficiency with NumPy arrays.
        """
        print("\n=== NumPy Array Optimization ===")
        
        # Create large sequences
        size = 1_000_000
        
        # Python list
        py_list = list(range(size))
        
        # NumPy array
        np_array = np.arange(size)
        
        print(f"Python list size: {asizeof.asizeof(py_list) / (1024*1024):.2f} MB")
        print(f"NumPy array size: {asizeof.asizeof(np_array) / (1024*1024):.2f} MB")
        
    def demonstrate_defaultdict(self):
        """
        Demonstrate memory efficiency with defaultdict.
        """
        print("\n=== Defaultdict Optimization ===")
        
        # Create large dictionaries
        size = 100_000
        
        # Regular dict
        regular_dict = {}
        for i in range(size):
            if i not in regular_dict:
                regular_dict[i] = []
            regular_dict[i].append(i)
        
        # defaultdict
        from collections import defaultdict
        default_dict = defaultdict(list)
        for i in range(size):
            default_dict[i].append(i)
            
        print(f"Regular dict size: {asizeof.asizeof(regular_dict) / 1024:.2f} KB")
        print(f"Defaultdict size: {asizeof.asizeof(default_dict) / 1024:.2f} KB")

    def run_all_demonstrations(self):
        """
        Run all memory optimization demonstrations.
        """
        self.demonstrate_slot_optimization()
        self.demonstrate_memoryview()
        self.demonstrate_array_module()
        self.demonstrate_namedtuple()
        self.demonstrate_generators()
        self.demonstrate_memoization()
        self.demonstrate_string_interning()
        self.demonstrate_numpy_arrays()
        self.demonstrate_defaultdict()


if __name__ == "__main__":
    optimizer = MemoryOptimizer()
    optimizer.run_all_demonstrations()