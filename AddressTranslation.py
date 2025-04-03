class MMU:
    """
    Memory Management Unit (MMU) that handles address translation
    between virtual and physical addresses using paging.
    """
    
    def __init__(self, page_size_kb=4, physical_memory_mb=64):
        """
        Initialize the MMU with page size and physical memory size.
        
        Args:
            page_size_kb: Size of each page in KB (default: 4KB)
            physical_memory_mb: Total physical memory in MB (default: 64MB)
        """
        self.page_size = page_size_kb * 1024  # Convert KB to bytes
        self.physical_memory_size = physical_memory_mb * 1024 * 1024  # Convert MB to bytes
        
        # Calculate number of physical frames
        self.num_frames = self.physical_memory_size // self.page_size
        
        # Data structures
        self.page_table = {}  # Maps virtual page numbers to frame numbers
        self.free_frames = set(range(self.num_frames))  # Tracks available frames
        self.used_frames = set()  # Tracks used frames
        
        # Statistics
        self.page_faults = 0
        self.memory_accesses = 0
    
    def translate_address(self, virtual_address, process_id):
        """
        Translate a virtual address to a physical address.
        
        Args:
            virtual_address: The virtual address to translate
            process_id: ID of the process making the request
            
        Returns:
            Tuple of (physical_address, page_fault_occurred)
        """
        self.memory_accesses += 1
        
        # Calculate page number and offset
        page_number = virtual_address // self.page_size
        offset = virtual_address % self.page_size
        
        # Create process-specific page table if it doesn't exist
        if process_id not in self.page_table:
            self.page_table[process_id] = {}
        
        # Check if page is in page table
        if page_number in self.page_table[process_id]:
            frame_number = self.page_table[process_id][page_number]
            physical_address = frame_number * self.page_size + offset
            return (physical_address, False)
        else:
            # Page fault - need to allocate a frame
            self.page_faults += 1
            frame_number = self._allocate_frame()
            
            if frame_number is None:
                # No free frames available (in real system, would page out)
                raise MemoryError("No free frames available")
            
            # Update page table
            self.page_table[process_id][page_number] = frame_number
            physical_address = frame_number * self.page_size + offset
            return (physical_address, True)
    
    def _allocate_frame(self):
        """
        Allocate a free physical frame.
        
        Returns:
            Frame number if available, None otherwise
        """
        if not self.free_frames:
            return None
            
        frame_number = self.free_frames.pop()
        self.used_frames.add(frame_number)
        return frame_number
    
    def free_process_memory(self, process_id):
        """
        Free all memory allocated to a process.
        
        Args:
            process_id: ID of the process to free
        """
        if process_id in self.page_table:
            # Return all frames to free list
            for frame in self.page_table[process_id].values():
                if frame in self.used_frames:
                    self.used_frames.remove(frame)
                    self.free_frames.add(frame)
            
            # Remove process from page table
            del self.page_table[process_id]
    
    def get_stats(self):
        """
        Get MMU statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'page_faults': self.page_faults,
            'memory_accesses': self.memory_accesses,
            'page_fault_rate': self.page_faults / self.memory_accesses if self.memory_accesses > 0 else 0,
            'free_frames': len(self.free_frames),
            'used_frames': len(self.used_frames)
        }
    
    def print_memory_status(self):
        """
        Print current memory status.
        """
        print("\nMemory Status:")
        print(f"Total frames: {self.num_frames}")
        print(f"Free frames: {len(self.free_frames)}")
        print(f"Used frames: {len(self.used_frames)}")
        print(f"Page faults: {self.page_faults}")
        print(f"Memory accesses: {self.memory_accesses}")
        print(f"Page fault rate: {self.get_stats()['page_fault_rate']:.2%}")


# Example usage
if __name__ == "__main__":
    # Create MMU with 4KB pages and 64MB physical memory
    mmu = MMU(page_size_kb=4, physical_memory_mb=64)
    
    # Process 1 memory accesses
    print("Process 1 accessing memory:")
    virtual_addresses = [0, 4096, 8192, 5000, 12000]
    for addr in virtual_addresses:
        physical_addr, page_fault = mmu.translate_address(addr, 1)
        print(f"Virtual: {addr:6d} -> Physical: {physical_addr:6d} | Page fault: {page_fault}")
    
    # Process 2 memory accesses
    print("\nProcess 2 accessing memory:")
    virtual_addresses = [0, 4096, 20000, 25000]
    for addr in virtual_addresses:
        physical_addr, page_fault = mmu.translate_address(addr, 2)
        print(f"Virtual: {addr:6d} -> Physical: {physical_addr:6d} | Page fault: {page_fault}")
    
    # Free Process 1 memory
    mmu.free_process_memory(1)
    print("\nAfter freeing Process 1 memory:")
    mmu.print_memory_status()
    
    # Process 3 memory accesses
    print("\nProcess 3 accessing memory:")
    virtual_addresses = [0, 4096, 8192, 16384]
    for addr in virtual_addresses:
        physical_addr, page_fault = mmu.translate_address(addr, 3)
        print(f"Virtual: {addr:6d} -> Physical: {physical_addr:6d} | Page fault: {page_fault}")
    
    # Final statistics
    print("\nFinal statistics:")
    mmu.print_memory_status()