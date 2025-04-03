import math
from typing import Dict, Optional

class BuddySystemAllocator:
    def __init__(self, total_memory_mb: int = 4096, min_block_mb: int = 64):
        """
        Buddy System allocator for COAD image processing
        
        Args:
            total_memory_mb: Total available memory in MB (default: 4GB)
            min_block_mb: Minimum allocatable block size in MB (default: 64MB)
        """
        self.total_size = total_memory_mb
        self.min_size = min_block_mb
        self.levels = int(math.log2(total_memory_mb // min_block_mb)) + 1
        self.free_blocks = [set() for _ in range(self.levels)]
        self.allocated_blocks: Dict[int, int] = {}  # {address: size}
        
        # Initialize with one free block of maximum size
        self.free_blocks[-1].add(0)
        
    def _get_level(self, size_mb: int) -> int:
        """Determine which level can satisfy this allocation request"""
        if size_mb < self.min_size:
            size_mb = self.min_size
        return max(0, math.ceil(math.log2(size_mb / self.min_size)))
    
    def allocate(self, size_mb: int) -> Optional[int]:
        """
        Allocate memory for a WSI tile or processing buffer
        
        Args:
            size_mb: Requested memory size in MB
            
        Returns:
            Starting address of allocated block, or None if allocation fails
        """
        level = self._get_level(size_mb)
        
        # Find the smallest suitable free block
        for lvl in range(level, self.levels):
            if self.free_blocks[lvl]:
                # Found a suitable block
                addr = self.free_blocks[lvl].pop()
                
                # Split block if it's larger than needed
                while lvl > level:
                    lvl -= 1
                    buddy_addr = addr + (self.min_size << lvl)
                    self.free_blocks[lvl].add(buddy_addr)
                
                self.allocated_blocks[addr] = self.min_size << level
                return addr
                
        return None  # No suitable block found
    
    def deallocate(self, addr: int) -> bool:
        """
        Free memory previously allocated for WSI processing
        
        Args:
            addr: Starting address of block to free
            
        Returns:
            True if deallocation succeeded, False if address was invalid
        """
        if addr not in self.allocated_blocks:
            return False
            
        size = self.allocated_blocks.pop(addr)
        level = self._get_level(size)
        
        # Start with the freed block
        current_addr = addr
        current_level = level
        
        # Attempt to coalesce with buddies
        while current_level < self.levels - 1:
            buddy_addr = current_addr ^ (self.min_size << current_level)
            
            if buddy_addr in self.free_blocks[current_level]:
                # Merge with buddy
                self.free_blocks[current_level].remove(buddy_addr)
                current_addr = min(current_addr, buddy_addr)
                current_level += 1
            else:
                break
                
        self.free_blocks[current_level].add(current_addr)
        return True
    
    def memory_map(self) -> str:
        """Generate a visualization of memory allocation"""
        map_str = f"Buddy System Memory Map ({self.total_size}MB total)\n"
        map_str += "-" * 60 + "\n"
        
        for addr, size in sorted(self.allocated_blocks.items()):
            map_str += f"Allocated: {addr:8d}-{addr+size-1:8d} ({size}MB)\n"
            
        for lvl in range(self.levels):
            size = self.min_size << lvl
            for addr in sorted(self.free_blocks[lvl]):
                map_str += f"Free:     {addr:8d}-{addr+size-1:8d} ({size}MB)\n"
                
        return map_str

# Example usage for COAD image processing
if __name__ == "__main__":
    # Create allocator with 8GB memory and 128MB minimum block
    allocator = BuddySystemAllocator(total_memory_mb=8192, min_block_mb=128)
    
    # Simulate allocating memory for WSI processing
    print("Allocating memory for COAD image processing...")
    tile1 = allocator.allocate(256)  # 256MB tile
    tile2 = allocator.allocate(512)  # 512MB tile
    buffer = allocator.allocate(1024) # 1GB processing buffer
    
    print("\nMemory state after allocations:")
    print(allocator.memory_map())
    
    # Free some memory
    print("\nFreeing 512MB tile...")
    allocator.deallocate(tile2)
    
    print("\nMemory state after deallocation:")
    print(allocator.memory_map())
    
    # Allocate new resources
    print("\nAllocating new 768MB buffer...")
    tile3 = allocator.allocate(768)
    
    print("\nFinal memory state:")
    print(allocator.memory_map())