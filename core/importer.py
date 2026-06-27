from pathlib import Path
from core import mod_memory, modinfo_handler, music_lua, name_sanitizer


def open_mod(modinfo_path):
    modinfo_path = Path(modinfo_path)
    mod_root = modinfo_path.parent

    mod_memory.modinfo = modinfo_handler.read(modinfo_path)

    thumb = mod_root / "thumbnail.jpg"
    mod_memory.thumbnail_path = str(thumb) if thumb.exists() else None

    music_path = mod_root / "data" / "scripts" / "lib" / "music.lua"
    mod_memory.tracks = []
    if music_path.exists():
        tracks_data = music_lua.read(str(music_path))
        for td in tracks_data:
            source = mod_root / td["path"]
            mod_memory.tracks.append({
                "id": td["id"],
                "source_path": str(source),
                "display_name": name_sanitizer.sanitize(td["display_name"]),
                "collections": td["collections"],
            })

    mod_memory.selected = "mod_settings"
    mod_memory.notify(full_reload=True)
