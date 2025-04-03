from collections import defaultdict

class Segment:
    def __init__(self, name, base, limit):
        self.name = name      # "Code", "Stack", "Heap", etc.
        self.base = base      # Logical base address
        self.limit = limit    # Segment size (in bytes)
        self.page_table = {}  # Maps page numbers to frames

class HybridMemoryManager:
    def __init__(self, total_memory, page_size):
        self.total_memory = total_memory
        self.page_size = page_size
        self.num_frames = total_memory // page_size
        self.physical_memory = [None] * self.num_frames  # None = free, else (process_id, segment_name, page_num)
        self.segments = defaultdict(list)  # process_id -> [Segment1, Segment2, ...]
    
    def allocate_segment(self, process_id, segment_name, size):
        if process_id in self.segments and segment_name in [s.name for s in self.segments[process_id]]:
            return False  # Segment already exists

        num_pages = (size + self.page_size - 1) // self.page_size  # Round up
        
        if num_pages > self.num_frames:
            return False  # Not enough memory

        free_frames = [i for i, frame in enumerate(self.physical_memory) if frame is None]
        if len(free_frames) < num_pages:
            return False  # Not enough contiguous frames (simplified)

        # Create segment and page table
        segment = Segment(segment_name, 0, size)  # Base is logical (0 for simplicity)
        for i in range(num_pages):
            frame = free_frames[i]
            segment.page_table[i] = frame
            self.physical_memory[frame] = (process_id, segment_name, i)
        
        self.segments[process_id].append(segment)
        return True
    
    def deallocate_process(self, process_id):
        if process_id not in self.segments:
            return False
        
        # Free all frames used by this process
        for segment in self.segments[process_id]:
            for page_num, frame in segment.page_table.items():
                self.physical_memory[frame] = None
        
        del self.segments[process_id]
        return True
    
    def translate_address(self, process_id, segment_name, offset):
        if process_id not in self.segments:
            return None  # Process not found
        
        segment = next((s for s in self.segments[process_id] if s.name == segment_name), None)
        if not segment:
            return None  # Segment not found
        
        if offset >= segment.limit:
            return None  # Offset out of bounds
        
        page_num = offset // self.page_size
        page_offset = offset % self.page_size
        
        if page_num not in segment.page_table:
            return None  # Page fault (page not loaded)
        
        frame = segment.page_table[page_num]
        physical_addr = frame * self.page_size + page_offset
        return physical_addr
    
    def status(self):
        print("\nMemory Status:")
        print(f"Total Memory: {self.total_memory} bytes")
        print(f"Page Size: {self.page_size} bytes")
        print(f"Available Frames: {self.physical_memory.count(None)} / {self.num_frames}")
        print("Allocated Segments:")
        for process_id, segments in self.segments.items():
            print(f"  Process {process_id}:")
            for seg in segments:
                print(f"    Segment {seg.name}: {len(seg.page_table)} pages")
        print()

# Example Usage
if __name__ == "__main__":
    hmm = HybridMemoryManager(total_memory=1024, page_size=64)  # 1KB memory, 64B pages
    
    # Allocate segments for Process P1
    hmm.allocate_segment("P1", "Code", 128)  # 2 pages
    hmm.allocate_segment("P1", "Heap", 256)  # 4 pages
    
    # Allocate segments for Process P2
    hmm.allocate_segment("P2", "Code", 192)  # 3 pages
    
    hmm.status()
    
    # Simulate address translation
    logical_addr = 80  # Offset 80 in Code segment of P1
    physical_addr = hmm.translate_address("P1", "Code", logical_addr)
    print(f"Logical Address (P1:Code+{logical_addr}) → Physical Address {physical_addr}")
    
    # Deallocate P1
    hmm.deallocate_process("P1")
    hmm.status()