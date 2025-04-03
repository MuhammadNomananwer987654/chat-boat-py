# With OpenSlide
tile = openslide.OpenSlide("COAD.svs").read_region(...)
vaddr = segment_base + tile_offset
phys_addr = mem.access(segment_id, vaddr)