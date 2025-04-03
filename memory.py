class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.available_memory = total_memory
        self.allocated_blocks = []
    
    def allocate(self, process_id, size):
        if size > self.available_memory:
            print(f"Error: Not enough memory to allocate {size} for process {process_id}")
            return False
        
        # Simple first-fit allocation
        self.available_memory -= size
        self.allocated_blocks.append((process_id, size))
        print(f"Allocated {size} to process {process_id}")
        return True
    
    def deallocate(self, process_id):
        for i, (pid, size) in enumerate(self.allocated_blocks):
            if pid == process_id:
                self.available_memory += size
                del self.allocated_blocks[i]
                print(f"Deallocated {size} from process {process_id}")
                return True
        print(f"Error: Process {process_id} not found")
        return False
    
    def status(self):
        print("\nMemory Status:")
        print(f"Total Memory: {self.total_memory}")
        print(f"Available Memory: {self.available_memory}")
        print("Allocated Blocks:")
        for pid, size in self.allocated_blocks:
            print(f"  Process {pid}: {size}")
        print()

# Example usage
if __name__ == "__main__":
    mm = MemoryManager(1024)  # 1KB total memory
    
    mm.allocate("P1", 256)
    mm.allocate("P2", 512)
    mm.status()
    
    mm.deallocate("P1")
    mm.status()
    
    mm.allocate("P3", 768)
    mm.status()