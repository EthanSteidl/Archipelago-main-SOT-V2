import ModuleUpdate
ModuleUpdate.update()

import Utils  # noqa: E402

from worlds_disabled.zillion import launch  # noqa: E402

if __name__ == "__main__":
    Utils.init_logging("ZillionClient", exception_logger="Client")
    launch()
