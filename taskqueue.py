import os
import time

from PIL import Image
from celery import Celery

app = Celery(
    'taskqueue',
    broker = 'redis://localhost:6379/0',    
    backend = 'redis://localhost:6379/0',    
)

@app.task
def add(a, b):
    time.sleep(10)
    return a + b


@app.task
def sum2(value):
    # assert(isinstance(value, (list, tuple)))
    print(value)
    time.sleep(10)
    return sum(value)

@app.task
def make_thumbnail(path, width, height):
    # file.png --> file_thumb.png
    filepath, ext = os.path.splitext(path)
    output_path = '{}_thumb{}'.format(filepath, ext)

    if os.path.exists(output_path):
        return output_path

    # im = Image.open(path)
    # im.thumbnail([width, height], Image.LANCZOS)
    # im.save(output_path)
    # im.close()
    with Image.open(path) as im:
        im.thumbnail([width, height], Image.LANCZOS)
        im.save(output_path)
    # Image 에 __enter__, __exit__ 가 있어야 with 문 사용 가능함 ??

    return output_path

