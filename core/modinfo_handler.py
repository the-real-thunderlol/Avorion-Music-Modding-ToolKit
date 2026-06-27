from lupa import LuaRuntime


def _esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def read(path):
    lua = LuaRuntime(unpack_returned_tuples=True)
    with open(path, "r", encoding="utf-8") as f:
        lua.execute(f.read())
    meta = lua.globals().meta
    if meta is None:
        raise ValueError("modinfo.lua does not define 'meta'")

    authors = []
    if meta.authors is not None:
        try:
            n = len(meta.authors)
        except TypeError:
            n = 0
        for i in range(1, n + 1):
            v = meta.authors[i]
            if v is not None:
                authors.append(str(v))

    def g(field, default=""):
        v = meta[field]
        return str(v) if v is not None else default

    def gb(field):
        v = meta[field]
        return bool(v) if v is not None else False

    return {
        "id": g("id"),
        "name": g("name"),
        "title": g("title"),
        "type": g("type", "mod") or "mod",
        "description": g("description"),
        "authors": authors if authors else [""],
        "version": g("version", "1.0") or "1.0",
        "dependencies": [],
        "serverSideOnly": gb("serverSideOnly"),
        "clientSideOnly": gb("clientSideOnly"),
        "saveGameAltering": gb("saveGameAltering"),
        "contact": g("contact"),
    }


def write(modinfo, target_path):
    authors_list = [a for a in modinfo.get("authors", []) if a]
    if not authors_list:
        authors_list = [""]
    authors_str = ", ".join(f'"{_esc(a)}"' for a in authors_list)

    text = f'''
meta =
{{
    id = "{_esc(modinfo.get("id", ""))}",
    name = "{_esc(modinfo.get("name", ""))}",
    title = "{_esc(modinfo.get("title", ""))}",
    type = "mod",
    description = "{_esc(modinfo.get("description", ""))}",
    authors = {{{authors_str}}},
    version = "{_esc(modinfo.get("version", "1.0"))}",
    dependencies = {{

    }},
    serverSideOnly = {str(bool(modinfo.get("serverSideOnly", False))).lower()},
    clientSideOnly = {str(bool(modinfo.get("clientSideOnly", False))).lower()},
    saveGameAltering = {str(bool(modinfo.get("saveGameAltering", False))).lower()},
    contact = "{_esc(modinfo.get("contact", ""))}",
}}
'''
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(text)
