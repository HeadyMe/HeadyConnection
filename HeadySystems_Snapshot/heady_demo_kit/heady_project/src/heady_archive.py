class HeadyArchive:
    def preserve(self, manifest, context_tags=None):
        if context_tags is None:
            context_tags = []
        manifest["_heady_archive"] = {
            "status": "preserved",
            "context_tags": context_tags,
            "timestamp": "now"
        }
        return manifest
