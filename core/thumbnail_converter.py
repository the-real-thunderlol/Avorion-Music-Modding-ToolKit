import shutil
from pathlib import Path
from PIL import Image


def convert(src, dst):
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        if src.resolve() == dst.resolve():
            # file was unchanged, thus no copy needed
            return
    except OSError:
        pass
    if src.suffix.lower() in (".jpg", ".jpeg"):
        shutil.copy(str(src), str(dst))
        return
    img = Image.open(str(src)).convert("RGB")
    img.save(str(dst), "JPEG")
