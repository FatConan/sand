from config.config_loader import ConfigLoader
import sys
import os

def main(args):
    if len(args) <= 1:
        print("Error: No path to site root")
        return 1

    site_root = args[1] if os.path.isdir(args[1]) else None

    sites = ConfigLoader().load(site_root)

    for site in sites:
        site.render()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
