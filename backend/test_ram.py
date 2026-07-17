import psutil
import os
process = psutil.Process(os.getpid())
print(f"RAM sebelum load model: {process.memory_info().rss / 1024 / 1024:.2f} MB")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

print(f"RAM setelah load model: {process.memory_info().rss / 1024 / 1024:.2f} MB")