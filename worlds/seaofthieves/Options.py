import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle
from .Configurations import Foodoptions
from .Configurations.Sealoptions import *
from .Configurations.Emoptions import *
from .Configurations import Fishoptions
from .Configurations import Fortsoptions
from .Configurations import Treasuryoptions
from .Configurations import Servantoptions
from .Configurations import Guardianoptions
from .Configurations import IllFatedoptions, Cannonsoptions, Selloptions
from .Configurations import Trapsoptions
from .Configurations import EmVoyageoptions
from .Configurations import Shipoptions, CaptainShipoptions, DaysAtSeaoptions, Rowboatoptions, Shipwreckoptions, TallTaleoptions


class ShuffleEmissaryFlags(DefaultOnToggle):
    """Adds emissary flags to item pool. If disabled, you can get credit by rasing the flag any time.
     To check chests or voyages related to a specific emissary, you must
    have the emissary flag unlocked and equiped"""
    display_name = "Shuffle Emissary Flags"

class ShuffleStandardCannons(DefaultOnToggle):
    """Adds shooting of the cannonball, firebomb, blunderbomb, and player to the item pool"""
    display_name = "Shuffle Standard Cannons"

class ShuffleCursedCannons(DefaultOnToggle):
    """Adds shooting of each cursed cannonball to the item pool"""
    display_name = "Shuffle Cursed Cannonballs"


class ShuffleVoyageBundleGh(DefaultOnToggle):
    """Adds Voyage Bundle: Gold Hoarders"""
    display_name = "Voyage Bundle: Gold Hoarders"

class ShuffleVoyageBundleMa(DefaultOnToggle):
    """Adds Voyage Bundle: Merchant Alliance"""
    display_name = "Voyage Bundle: Merchant Alliance"

class ShuffleVoyageBundleOos(DefaultOnToggle):
    """Adds Voyage Bundle: Order of Souls"""
    display_name = "Voyage Bundle: Order of Souls"

class ShuffleVoyageBundleAthena(DefaultOnToggle):
    """Adds Voyage Bundle: Athena's Fortune"""
    display_name = "Voyage Bundle: Atehna's Fortune"


class VoyQuestRorCompAny(DefaultOnToggle):
    display_name = "Location: Complete ROAR Voyage"
class VoyQuestRorCompXMark(DefaultOnToggle):
    display_name = "Location: Complete ROAR X-Marks Voyage"
class VoyQuestRorCompWay(DefaultOnToggle):
    display_name = "Location: Complete ROAR Wayfinder Voyage"
class VoyQuestRorCompRid(DefaultOnToggle):
    display_name = "Location: Complete ROAR Riddle Voyage"
class VoyQuestRorCompBounty(DefaultOnToggle):
    display_name = "Location: Complete ROAR Bounty Voyage"
class VoyQuestRorCompAthena(DefaultOnToggle):
    display_name = "Location: Complete ROAR Athena Voyage"


class HunterBurntAboard(DefaultOnToggle):
    display_name = "Enable checks on each burning food"
class HunterCookedAboard(DefaultOnToggle):
    display_name = "Enable checks on cooking each food"
class HunterTotalCooked(DefaultOnToggle):
    display_name = "Enable check on cooking 1 food"
class HunterEatenAboard(DefaultOnToggle):
    display_name = "Enable checks on eating each food"

class EmFlagRec(Range):
    """Number of emissary flags required to perform FOD"""
    display_name = "Emissary flags required for FOD"
    range_start = 0
    range_end = 5
    default = 3

class ExperimentalFeatures(Toggle):
    """Not meant for player use. Developer use only to enable WIP mechanics.
    Enabling this setting will likely brick generation and/or the client."""
    default = 0
    display_name = "Experimental Features"

@dataclass
class SOTOptions(PerGameCommonOptions):

    sealCount: SealsRequired
    voyageEmGh: EmVoyageoptions.VoyageCountSpecificGh
    voyageEmMa: EmVoyageoptions.VoyageCountSpecificMa
    voyageEmOos: EmVoyageoptions.VoyageCountSpecificOos
    voyageEmAf: EmVoyageoptions.VoyageCountSpecificAf
    voyageEmRoar: EmVoyageoptions.VoyageCountSpecificRoar

    servantSanity: Servantoptions.ServantSanity
    guardianSanity: Guardianoptions.GuardianSanity
    fortressSanity: Fortsoptions.FortressSanity
    illFated: IllFatedoptions.IllFated
    playerShip: Shipoptions.ShipSanity

    fishSanity: Fishoptions.FishSanity
    #sellSettingsGh: Selloptions.GhSellRange
    #sellSettingsMa: Selloptions.MaSellRange
    #sellSettingsOos: Selloptions.OosSellRange
    #sellSettingsAf: Selloptions.AfSellRange
    #sellSettingsRb: Selloptions.RbSellRange

    cannonSanityBalls: Cannonsoptions.CannonSanityBalls
    cannonSanityCursed: Cannonsoptions.CannonSanityCursed
    cannonSanityPhantom: Cannonsoptions.CannonSanityPhantom

    foodSanityFruit: Foodoptions.MunchSanityFruit
    foodSanityFish: Foodoptions.MunchSanityFish
    foodSanitySeamonster: Foodoptions.MunchSanitySeamonster
    foodSanityLandAnimal: Foodoptions.MunchSanityLandAnimal
    foodSanityBug: Foodoptions.MunchSanityBug

    cookSanityFish: Foodoptions.CookSanityFish
    cookSanitySeamonster: Foodoptions.CookSanitySeamonster
    cookSanityLandAnimal: Foodoptions.CookSanityLandAnimal

    burnSanityFish: Foodoptions.BurnSanityFish
    burnSanitySeamonster: Foodoptions.BurnSanitySeamonster
    burnSanityLandAnimal: Foodoptions.BurnSanityLandAnimal

    captainShipSpotted: CaptainShipoptions.CaptainShipoptions
    daysAtSea: DaysAtSeaoptions.DaysAtSeaOptions
    rowboats: Rowboatoptions.RowboatSanity
    shipwrecks: Shipwreckoptions.ShipwreckOptions
    tallTales: TallTaleoptions.TallTaleoptions

    trapsPercentage: Trapsoptions.TrapPercentage
    experimentals: ExperimentalFeatures




