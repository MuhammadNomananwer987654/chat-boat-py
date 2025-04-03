import multiprocessing
import threading
import queue

class ResourceAllocator:
    def __init__(self, max_gpus=4, max_cpus=8):
        self.gpu_semaphore = threading.Semaphore(max_gpus)
        self.cpu_semaphore = threading.Semaphore(max_cpus)
        self.task_queue = queue.Queue()

    def allocate_gpu_task(self, task_func, *args):
        with self.gpu_semaphore:
            # Execute GPU-intensive task (e.g., inference on a WSI patch)
            return task_func(*args)

    def allocate_cpu_task(self, task_func, *args):
        with self.cpu_semaphore:
            # Execute CPU-bound task (e.g., image preprocessing)
            return task_func(*args)

    def add_task(self, task_type, task_func, *args):
        if task_type == "gpu":
            thread = threading.Thread(target=self.allocate_gpu_task, args=(task_func, *args))
        else:
            thread = threading.Thread(target=self.allocate_cpu_task, args=(task_func, *args))
        thread.start()

# Example usage:
def process_wsi_patch(patch):
    # Simulate GPU-based tumor segmentation
    return f"Processed {patch} with GPU"

allocator = ResourceAllocator(max_gpus=2)
allocator.add_task("gpu", process_wsi_patch, "COAD_patch_001.tif")