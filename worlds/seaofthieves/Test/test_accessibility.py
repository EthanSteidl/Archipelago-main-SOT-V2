from Options import Toggle

#from .. import Locations

from test.TestBase import WorldTestBase


class SOTTestBase(WorldTestBase):
    game = "Sea of Thieves"


class TestBasic(SOTTestBase):
    def test_always_accessible(self) -> None:
        self.assertFalse(self.can_reach_location("Legend of the Vale"))

class TestReachEnd(SOTTestBase):
    def test_reaching_end(self) -> None:
        self.collect_by_name("Voyages of Athena")
        self.assertTrue(self.can_reach_location("Legend of the Vale"))



