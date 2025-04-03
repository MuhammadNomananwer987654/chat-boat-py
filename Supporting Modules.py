import sys
import gc
import weakref
import tracemalloc
from pympler import tracker, muppy, summary
from memory_profiler import profile
import objgraph
import numpy as np

class MemorySupport:
    """
    A collection of supporting modules and techniques for advanced memory management in Python.
    """
    
    def __init__(self):
        self.memory_tracker = tracker.SummaryTracker()
        self.snapshots = []
        
    def enable_gc_debug(self):
        """Enable garbage collection debugging."""
        gc.set_debug(gc.DEBUG_LEAK)
        print("Garbage collection debugging enabled (DEBUG_LEAK)")
    
    def disable_gc_debug(self):
        """Disable garbage collection debugging."""
        gc.set_debug(0)
        print("Garbage collection debugging disabled")
    
    def show_gc_stats(self):
        """Show current garbage collection statistics."""
        print("\nGarbage Collection Stats:")
        print(f"Enabled: {gc.isenabled()}")
        print(f"Count: {gc.get_count()}")
        print(f"Threshold: {gc.get_threshold()}")
        print(f"Collected: {gc.collect()}")
    
    def demonstrate_weakref(self):
        """Demonstrate weak references for memory optimization."""
        print("\n=== Weak References ===")
        
        class Data:
            def __init__(self, value):
                self.value = value
            def __repr__(self):
                return f"Data({self.value})"
        
        # Regular reference
        obj = Data(42)
        regular_ref = obj
        print(f"Regular ref before del: {regular_ref}")
        
        # Weak reference
        obj = Data(99)
        weak_ref = weakref.ref(obj)
        print(f"Weak ref before del: {weak_ref()}")  # Call the ref to get object
        
        # Delete the original object
        del obj
        print(f"Regular ref after del: {regular_ref}")
        print(f"Weak ref after del: {weak_ref()}")  # Returns None
        
    def track_memory_usage(self):
        """Track memory usage using tracemalloc."""
        print("\n=== Memory Tracking with tracemalloc ===")
        tracemalloc.start()
        
        # Take snapshot before operations
        snapshot1 = tracemalloc.take_snapshot()
        
        # Perform some memory operations
        data = [np.random.rand(1000, 1000) for _ in range(5)]  # ~40MB each
        
        # Take snapshot after operations
        snapshot2 = tracemalloc.take_snapshot()
        
        # Compare snapshots
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        print("[Top 5 memory differences]")
        for stat in top_stats[:5]:
            print(stat)
        
        tracemalloc.stop()
    
    def analyze_with_pympler(self):
        """Analyze memory usage with PyMpler."""
        print("\n=== Memory Analysis with PyMpler ===")
        
        # Create some objects
        big_list = [x for x in range(100000)]
        big_dict = {x: str(x) for x in range(10000)}
        
        # Get summary of all objects in memory
        all_objects = muppy.get_objects()
        sum1 = summary.summarize(all_objects)
        summary.print_(sum1)
        
        # Track memory between operations
        self.memory_tracker.print_diff()
    
    @profile
    def memory_profiler_demo(self):
        """Demonstrate memory profiling line-by-line."""
        print("\n=== Line-by-line Memory Profiling ===")
        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        del b
        return a
    
    def detect_reference_cycles(self):
        """Detect and break reference cycles."""
        print("\n=== Reference Cycle Detection ===")
        
        class Node:
            def __init__(self, value):
                self.value = value
                self.next = None
        
        # Create a reference cycle
        node1 = Node(1)
        node2 = Node(2)
        node1.next = node2
        node2.next = node1  # Cycle created
        
        # Before collection
        print(f"Nodes before GC: {gc.get_count()}")
        
        # Force garbage collection
        collected = gc.collect()
        print(f"Collected {collected} objects")
        
        # After collection
        print(f"Nodes after GC: {gc.get_count()}")
    
    def visualize_object_graph(self):
        """Visualize object references using objgraph."""
        print("\n=== Object Reference Visualization ===")
        
        class Widget:
            def __init__(self, name):
                self.name = name
                self.children = []
        
        # Create object graph
        parent = Widget("parent")
        child1 = Widget("child1")
        child2 = Widget("child2")
        parent.children.extend([child1, child2])
        
        # Generate graph image (requires graphviz)
        try:
            objgraph.show_refs([parent], filename='object_graph.png')
            print("Object graph saved as object_graph.png")
        except ImportError:
            print("Graphviz not available - install with: pip install graphviz")
        
        # Show backreferences
        print("\nBackreferences to parent:")
        objgraph.show_backrefs([parent], max_depth=3)
    
    def numpy_memory_optimization(self):
        """Demonstrate NumPy memory optimization techniques."""
        print("\n=== NumPy Memory Optimization ===")
        
        # Create large array
        arr = np.random.rand(10000, 10000)  # ~800MB
        
        # Memory-efficient operations
        print("Original array size:", arr.nbytes / (1024**2), "MB")
        
        # Using views instead of copies
        view = arr[::2, ::2]  # No memory copied
        print("View size:", view.nbytes / (1024**2), "MB")
        
        # Memory mapping for large files
        try:
            memmap = np.memmap('temp.dat', dtype='float32', mode='w+', shape=(10000, 10000))
            print("Memory-mapped array created")
            del memmap  # Cleanup
        except Exception as e:
            print(f"Memory mapping failed: {e}")
    
    def run_all_demonstrations(self):
        """Run all memory support demonstrations."""
        self.show_gc_stats()
        self.demonstrate_weakref()
        self.track_memory_usage()
        self.analyze_with_pympler()
        self.memory_profiler_demo()
        self.detect_reference_cycles()
        self.visualize_object_graph()
        self.numpy_memory_optimization()


if __name__ == "__main__":
    # Example usage
    mem_support = MemorySupport()
    mem_support.run_all_demonstrations()
    
    # Clean up any created files
    import os
    if os.path.exists('temp.dat'):
        os.remove('temp.dat')