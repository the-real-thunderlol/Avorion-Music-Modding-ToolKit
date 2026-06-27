from pathlib import Path
from core import mod_memory, modinfo_handler, music_lua, audio_converter, thumbnail_converter


def export_mod(base_dir):
    name = (mod_memory.modinfo.get("name") or "").strip()
    if not name:
        raise ValueError("Mod name is required before exporting.")

    target = Path(base_dir) / name
    target.mkdir(parents=True, exist_ok=True)

    music_dir = target / "data" / "music" / "background"
    scripts_dir = target / "data" / "scripts" / "lib"
    music_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    if mod_memory.thumbnail_path:
        thumbnail_converter.convert(mod_memory.thumbnail_path, target / "thumbnail.jpg")

    for t in mod_memory.tracks:
        dst = music_dir / f"{t['display_name']}.ogg"
        try:
            audio_converter.convert(t["source_path"], dst)
        except Exception as e:
            raise RuntimeError(
                f"Failed converting '{t['source_path']}' -> '{dst}': {e}"
            ) from e

    modinfo_handler.write(mod_memory.modinfo, target / "modinfo.lua")
    music_lua.write(mod_memory.tracks, scripts_dir / "music.lua")

    return target
