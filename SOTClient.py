from __future__ import annotations
import asyncio
import ModuleUpdate
ModuleUpdate.update()

from worlds.seaofthieves.Client.SotCustomClient import main
import Utils

if __name__ == "__main__":
    Utils.init_logging("SOTClient", exception_logger="Client")
    asyncio.run(main())

