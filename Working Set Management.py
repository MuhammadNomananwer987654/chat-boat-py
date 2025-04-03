# Prioritize critical segments
def prioritize_segment(segment_id: int):
    if segment_id in mem.segments:
        mem.segments[segment_id].access_count = float('inf')