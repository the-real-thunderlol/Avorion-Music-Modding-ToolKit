import re


def sanitize(name):
    s = re.sub(r"[^A-Za-z0-9_]", "_", name)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        return "track"
    if s[0].isdigit():
        s = "_" + s
    return s
