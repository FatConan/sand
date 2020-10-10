class SiteExt:
    def _extend_environment(self, environment):
        print("Extending Environment")
        def nl2br(value):
            return value.replace("\n", "<br />")

        environment.filters["nl2br"] = nl2br