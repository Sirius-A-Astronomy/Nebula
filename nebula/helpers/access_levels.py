ACCESS_LEVELS_PROTO = {
    "guest": {"level": 0, "name": "Guest"},
    "student": {"level": 1, "name": "Student"},
    "moderator": {"level": 2, "name": "Moderator"},
    "admin": {"level": 3, "name": "Admin"},
    "maintainer": {"level": 4, "name": "Maintainer"},
}

ACCESS_LEVELS = {
    "ByLevel": {},
    "ByName": {},
}

for access_level in ACCESS_LEVELS_PROTO.values():
    ACCESS_LEVELS["ByLevel"][access_level["level"]] = access_level
    ACCESS_LEVELS["ByName"][access_level["name"].lower()] = access_level
