import numpy as np
from collections import OrderedDict, deque
import psutil
import matplotlib.pyplot as plt

class VirtualMemoryManager:
    def __init__(self, total_memory_gb=8, page_size_mb=256):
        """
        Simulates virtual memory for COAD WSI processing
        
        Args:
            total_memory_gb: Total available RAM in GB
            page_size_mb: Size of each memory page in MB
        """
        self.total_memory = total_memory_gb * 1024  # Convert to MB
        self.page_size = page_size_mb
        self.physical_memory = OrderedDict()  # Active pages in RAM
        self.disk = {}  # Simulated disk storage
        self.page_faults = 0
        self.hits = 0
        
    def load_page(self, page_id, data):
        """Load a page into memory using LRU replacement"""
        if page_id in self.physical_memory:
            self.hits += 1
            self.physical_memory.move_to_end(page_id)
            return True
        
        # Handle page fault
        self.page_faults += 1
        
        if len(self.physical_memory) * self.page_size >= self.total_memory:
            # Remove LRU page
            evicted_page, _ = self.physical_memory.popitem(last=False)
            self.disk[evicted_page] = self.physical_memory.get(evicted_page)
        
        # Load new page
        self.physical_memory[page_id] = data
        return False

    def process_slide(self, slide_path, tile_size=512):
        """
        Simulate processing a WSI with virtual memory management
        """
        print(f"Processing {slide_path} with virtual memory...")
        
        # Simulate loading tiles from a WSI
        for i in range(0, 20000, tile_size):
            for j in range(0, 20000, tile_size):
                page_id = f"{i}_{j}"
                tile_data = np.random.rand(tile_size, tile_size, 3)  # Simulate image tile
                
                # Load tile with virtual memory management
                self.load_page(page_id, tile_data)
                
        print(f"Page faults: {self.page_faults} | Hits: {self.hits}")

def monitor_memory_usage():
    """Track memory usage during execution"""
    mem = psutil.virtual_memory()
    print(f"Available: {mem.available/1024**3:.2f}GB | Used: {mem.used/1024**3:.2f}GB")

if __name__ == "__main__":
    # Initialize with 16GB RAM and 512MB pages
    vmm = VirtualMemoryManager(total_memory_gb=16, page_size_mb=512)
    
    # Monitor initial memory
    monitor_memory_usage()
    
    # Process a simulated WSI
    vmm.process_slide("COAD_slide.svs")
    
    # Check final memory status
    monitor_memory_usage()