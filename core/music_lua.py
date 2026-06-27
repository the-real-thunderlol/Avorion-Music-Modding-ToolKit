from lupa import LuaRuntime


COLLECTIONS = [
    "All", "Happy", "Neutral", "Middle", "HappyNoParticle",
    "Cold", "Desolate", "Melancholic", "HappyNeutral",
]


def read(path):
    lua = LuaRuntime(unpack_returned_tuples=True)
    with open(path, "r", encoding="utf-8") as f:
        lua.execute(f.read())
    g = lua.globals()

    track_type = g.TrackType
    tracks_table = g.Tracks
    if track_type is None or tracks_table is None:
        raise ValueError("music.lua missing TrackType or Tracks")

    id_to_name = {}
    for key in track_type:
        id_to_name[int(track_type[key])] = str(key)

    id_to_path = {}
    for k in tracks_table:
        entry = tracks_table[k]
        if entry is None:
            continue
        p = entry["path"] if entry["path"] is not None else ""
        id_to_path[int(k)] = str(p)

    collection_map = {}
    tc = g.TrackCollection
    for col in COLLECTIONS:
        ids = []
        if tc is not None:
            fn = tc[col]
            if fn is not None:
                result = fn()
                if result is not None:
                    try:
                        n = len(result)
                    except TypeError:
                        n = 0
                    for i in range(1, n + 1):
                        ids.append(int(result[i]))
        collection_map[col] = ids

    tracks_data = []
    for tid, name in id_to_name.items():
        cols = set()
        for col, ids in collection_map.items():
            if tid in ids:
                cols.add(col)
        tracks_data.append({
            "id": str(tid),
            "display_name": name,
            "path": id_to_path.get(tid, ""),
            "collections": cols,
        })
    return tracks_data


def write(tracks, target_path):
    lines = []
    lines.append('package.path = package.path .. ";data/scripts/lib/?.lua"')
    lines.append('package.path = package.path .. ";data/scripts/?.lua"')
    lines.append("")
    lines.append("TrackType =")
    lines.append("{")
    for t in tracks:
        lines.append(f'    {t["display_name"]} = {t["id"]},')
    lines.append("}")
    lines.append("")
    lines.append("Tracks = {}")
    for t in tracks:
        name = t["display_name"]
        lines.append(
            f'Tracks[TrackType.{name}] = '
            f'{{type = TrackType.{name}, '
            f'path = "data/music/background/{name}.ogg"}}'
        )
    lines.append("")
    lines.append("TrackCollection = {}")
    lines.append("")

    for col in COLLECTIONS:
        members = [t for t in tracks if col in t["collections"]]
        lines.append(f"function TrackCollection.{col}()")
        lines.append("    return")
        lines.append("    {")
        for m in members:
            lines.append(f"        TrackType.{m['display_name']},")
        lines.append("    }")
        lines.append("end")
        lines.append("")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
