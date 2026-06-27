import shutil
from pathlib import Path
import soundfile


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
    if src.suffix.lower() == ".ogg":
        shutil.copy(str(src), str(dst))
        return
    with soundfile.SoundFile(str(src)) as fin:
        with soundfile.SoundFile(
            str(dst), mode="w",
            samplerate=fin.samplerate,
            channels=fin.channels,
            format="OGG", subtype="VORBIS",
        ) as fout:
            for block in fin.blocks(blocksize=8192):
                fout.write(block)
