import sys
import weakref
from typing import Dict, List, Set
import gc
import psutil
import numpy as np

class WSITile:
    """Represents a tile from a Whole Slide Image"""
    def __init__(self, tile_data: np.ndarray, x: int, y: int):
        self.data = tile_data  # Image pixel data
        self.x = x            # Tile X coordinate
        self.y = y            # Tile Y coordinate
        self.processed = False

class COADGarbageCollector:
    def __init__(self, memory_limit_mb: int = 4096):
        """
        Garbage collector for COAD image processing
        
        Args:
            memory_limit_mb: Memory threshold in MB when GC should trigger
        """
        self.memory_limit = memory_limit_mb * 1024 * 1024  # Convert to bytes
        self.tile_registry: Dict[int, WSITile] = {}  # Strong references
        self.weak_tiles = weakref.WeakValueDictionary()  # Weak references
        self.circular_refs: Set[int] = set()  # Track potential circular refs
        
    def register_tile(self, tile: WSITile) -> int:
        """Register a WSI tile for memory management"""
        tile_id = id(tile)
        self.tile_registry[tile_id] = tile
        self.weak_tiles[tile_id] = tile
        return tile_id
    
    def mark_processed(self, tile_id: int):
        """Mark a tile as processed (eligible for collection)"""
        if tile_id in self.tile_registry:
            self.tile_registry[tile_id].processed = True
    
    def check_memory_pressure(self) -> bool:
        """Check if memory usage exceeds threshold"""
        return psutil.virtual_memory().used > self.memory_limit
    
    def collect(self, aggressive: bool = False):
        """
        Run garbage collection
        
        Args:
            aggressive: If True, force full collection and clear processed tiles
        """
        # Standard Python GC
        collected = gc.collect()
        print(f"GC collected {collected} objects")
        
        # Our specialized cleanup
        if aggressive or self.check_memory_pressure():
            self._clean_processed_tiles()
            
    def _clean_processed_tiles(self):
        """Remove processed tiles from registry"""
        to_delete = [
            tile_id for tile_id, tile in self.tile_registry.items() 
            if tile.processed
        ]
        
        for tile_id in to_delete:
            del self.tile_registry[tile_id]
            
        print(f"Cleaned {len(to_delete)} processed tiles")
    
    def detect_circular_refs(self):
        """Identify potential circular references in tile objects"""
        self.circular_refs.clear()
        for tile_id, tile in self.tile_registry.items():
            referrers = gc.get_referrers(tile)
            if any(isinstance(x, WSITile) for x in referrers):
                self.circular_refs.add(tile_id)
        
        print(f"Found {len(self.circular_refs)} potential circular references")

# Example usage for COAD processing
if __name__ == "__main__":
    # Initialize with 8GB memory limit
    gc_manager = COADGarbageCollector(memory_limit_mb=8192)
    
    # Simulate processing WSI tiles
    print("Processing COAD slide tiles...")
    active_tiles = []
    
    for i in range(10):
        # Simulate loading a 512x512 RGB tile (~0.75MB)
        tile_data = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
        tile = WSITile(tile_data, x=i*512, y=0)
        
        # Register tile with garbage collector
        tile_id = gc_manager.register_tile(tile)
        active_tiles.append(tile_id)
        
        # Process every other tile
        if i % 2 == 0:
            gc_manager.mark_processed(tile_id)
        
        # Simulate memory pressure after 5 tiles
        if i == 5:
            print("\nMemory pressure detected...")
            gc_manager.collect(aggressive=True)
    
    # Final cleanup
    print("\nFinal cleanup...")
    for tile_id in active_tiles:
        gc_manager.mark_processed(tile_id)
    gc_manager.collect(aggressive=True)
    
    # Diagnostic information
    print("\nMemory diagnostics:")
    gc_manager.detect_circular_refs()
    print(f"Active tiles in registry: {len(gc_manager.tile_registry)}")
    print(f"Memory used: {psutil.virtual_memory().used / 1024 / 1024:.2f} MB")