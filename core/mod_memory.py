def _default_modinfo():
    return {
        "id": "",
        "name": "",
        "title": "",
        "type": "mod",
        "description": "",
        "authors": [""],
        "version": "1.0",
        "dependencies": [],
        "serverSideOnly": False,
        "clientSideOnly": False,
        "saveGameAltering": False,
        "contact": "",
    }


modinfo = _default_modinfo()
thumbnail_path = None
tracks = []
selected = "mod_settings"

_full_token = 0
_subs = []


def subscribe(fn):
    _subs.append(fn)


def notify(full_reload=False):
    global _full_token
    if full_reload:
        _full_token += 1
    for f in list(_subs):
        f()


def select(value):
    global selected
    if selected == value:
        return
    selected = value
    notify()


def reset():
    global modinfo, thumbnail_path, tracks, selected
    modinfo = _default_modinfo()
    thumbnail_path = None
    tracks = []
    selected = "mod_settings"
    notify(full_reload=True)
