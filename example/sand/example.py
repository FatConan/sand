class Plugin:
    def configure(self, site_data, site):
        pass

    #Called during the parsing phase of the processing
    def parse(self, site_data, site):
        print("Extending Environment")
        def nl2br(value):
            return value.replace("\n", "<br />")

        site.environment.filters["nl2br"] = nl2br