from memory_profiler import profile
import openslide

@profile
def load_and_process_slide(slide_path):
    slide = openslide.OpenSlide(slide_path)  # Load WSI
    thumbnail = slide.get_thumbnail((1024, 1024))  # Downsample
    return thumbnail

if __name__ == "__main__":
    load_and_process_slide("COAD_slide.svs")  # Profile memory
    Line #    Mem usage    Increment  Occurrences   Line Contents
Line #    Mem usage    Increment  Occurrences   Line Contents
