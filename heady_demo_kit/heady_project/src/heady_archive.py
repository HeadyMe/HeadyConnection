import datetime
class HeadyArchive:
    def __init__(self):
        print("\u2690 [INIT] HeadyArchive Active")
    def preserve(self, manifest, context_tags=None):
        manifest["_heady_archive"] = {
            "status": "preserved",
            "tags": context_tags or [],
            "ts": datetime.datetime.now().isoformat(),
            "target": "Forever Vault"
        }
        return manifest
