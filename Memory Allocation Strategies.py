import sys
from collections import defaultdict

class MemoryAllocator:
    """
    A class to demonstrate different memory allocation strategies.
    """
    
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.available_memory = total_memory
        self.allocated_blocks = defaultdict(dict)
        self.next_block_id = 1
        
    def first_fit(self, process_id, size):
        """
        Allocate memory using First Fit strategy.
        Finds the first available block that's large enough.
        """
        # Sort blocks by their starting address
        sorted_blocks = sorted(self.allocated_blocks.values(), key=lambda x: x['start'])
        
        # Check space before first block
        if len(sorted_blocks) == 0:
            if size <= self.available_memory:
                block_id = self.next_block_id
                self.allocated_blocks[block_id] = {
                    'process_id': process_id,
                    'start': 0,
                    'end': size - 1,
                    'size': size
                }
                self.next_block_id += 1
                self.available_memory -= size
                return block_id
            else:
                return None
        
        prev_end = -1
        for block in sorted_blocks:
            gap = block['start'] - (prev_end + 1)
            if gap >= size:
                block_id = self.next_block_id
                self.allocated_blocks[block_id] = {
                    'process_id': process_id,
                    'start': prev_end + 1,
                    'end': prev_end + size,
                    'size': size
                }
                self.next_block_id += 1
                self.available_memory -= size
                return block_id
            prev_end = block['end']
        
        # Check space after last block
        gap = self.total_memory - (prev_end + 1)
        if gap >= size:
            block_id = self.next_block_id
            self.allocated_blocks[block_id] = {
                'process_id': process_id,
                'start': prev_end + 1,
                'end': prev_end + size,
                'size': size
            }
            self.next_block_id += 1
            self.available_memory -= size
            return block_id
        
        return None
    
    def best_fit(self, process_id, size):
        """
        Allocate memory using Best Fit strategy.
        Finds the smallest available block that's large enough.
        """
        # Get all free blocks (gaps between allocated blocks)
        free_blocks = self._get_free_blocks()
        
        # Find the smallest free block that can accommodate the request
        best_block = None
        min_waste = sys.maxsize
        
        for block in free_blocks:
            if block['size'] >= size:
                waste = block['size'] - size
                if waste < min_waste:
                    min_waste = waste
                    best_block = block
        
        if best_block:
            block_id = self.next_block_id
            self.allocated_blocks[block_id] = {
                'process_id': process_id,
                'start': best_block['start'],
                'end': best_block['start'] + size - 1,
                'size': size
            }
            self.next_block_id += 1
            self.available_memory -= size
            return block_id
        
        return None
    
    def worst_fit(self, process_id, size):
        """
        Allocate memory using Worst Fit strategy.
        Finds the largest available block to place the request.
        """
        # Get all free blocks (gaps between allocated blocks)
        free_blocks = self._get_free_blocks()
        
        # Find the largest free block
        worst_block = None
        max_size = -1
        
        for block in free_blocks:
            if block['size'] >= size and block['size'] > max_size:
                max_size = block['size']
                worst_block = block
        
        if worst_block:
            block_id = self.next_block_id
            self.allocated_blocks[block_id] = {
                'process_id': process_id,
                'start': worst_block['start'],
                'end': worst_block['start'] + size - 1,
                'size': size
            }
            self.next_block_id += 1
            self.available_memory -= size
            return block_id
        
        return None
    
    def _get_free_blocks(self):
        """
        Helper method to find all free memory blocks (gaps between allocations).
        """
        free_blocks = []
        sorted_blocks = sorted(self.allocated_blocks.values(), key=lambda x: x['start'])
        
        # Check space before first block
        if len(sorted_blocks) == 0:
            if self.available_memory > 0:
                return [{'start': 0, 'end': self.total_memory - 1, 'size': self.total_memory}]
            else:
                return []
        
        prev_end = -1
        for block in sorted_blocks:
            gap = block['start'] - (prev_end + 1)
            if gap > 0:
                free_blocks.append({
                    'start': prev_end + 1,
                    'end': block['start'] - 1,
                    'size': gap
                })
            prev_end = block['end']
        
        # Check space after last block
        gap = self.total_memory - (prev_end + 1)
        if gap > 0:
            free_blocks.append({
                'start': prev_end + 1,
                'end': self.total_memory - 1,
                'size': gap
            })
        
        return free_blocks
    
    def deallocate(self, block_id):
        """
        Deallocate a memory block.
        """
        if block_id in self.allocated_blocks:
            block = self.allocated_blocks.pop(block_id)
            self.available_memory += block['size']
            return True
        return False
    
    def display_memory_map(self):
        """
        Display the current memory allocation map.
        """
        print("\nMemory Map:")
        print(f"Total Memory: {self.total_memory}")
        print(f"Available Memory: {self.available_memory}")
        
        if not self.allocated_blocks:
            print("No allocated blocks.")
            return
        
        sorted_blocks = sorted(self.allocated_blocks.values(), key=lambda x: x['start'])
        
        # Print memory before first block
        if sorted_blocks[0]['start'] > 0:
            print(f"0 - {sorted_blocks[0]['start'] - 1}: Free")
        
        # Print allocated blocks and gaps between them
        for i in range(len(sorted_blocks)):
            block = sorted_blocks[i]
            print(f"{block['start']} - {block['end']}: Process {block['process_id']} (Block {block_id})")
            
            if i < len(sorted_blocks) - 1:
                next_block = sorted_blocks[i + 1]
                if block['end'] + 1 < next_block['start']:
                    print(f"{block['end'] + 1} - {next_block['start'] - 1}: Free")
        
        # Print memory after last block
        last_block = sorted_blocks[-1]
        if last_block['end'] < self.total_memory - 1:
            print(f"{last_block['end'] + 1} - {self.total_memory - 1}: Free")


# Example usage
if __name__ == "__main__":
    allocator = MemoryAllocator(1024)  # 1024 units of memory
    
    print("First Fit Allocation:")
    block1 = allocator.first_fit("P1", 200)
    block2 = allocator.first_fit("P2", 150)
    block3 = allocator.first_fit("P3", 300)
    allocator.display_memory_map()
    
    print("\nBest Fit Allocation:")
    allocator = MemoryAllocator(1024)  # Reset
    block1 = allocator.best_fit("P1", 200)
    block2 = allocator.best_fit("P2", 150)
    block3 = allocator.best_fit("P3", 300)
    allocator.display_memory_map()
    
    print("\nWorst Fit Allocation:")
    allocator = MemoryAllocator(1024)  # Reset
    block1 = allocator.worst_fit("P1", 200)
    block2 = allocator.worst_fit("P2", 150)
    block3 = allocator.worst_fit("P3", 300)
    allocator.display_memory_map()