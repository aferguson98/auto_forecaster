from tensorflow import keras

import auto_forecaster.io.TextForecast
from auto_forecaster.forecasting.ForecastPoint import ForecastPoint
from auto_forecaster.forecasting.ForecastRegion import ForecastRegion

east_anglia = ForecastRegion("E England", 0,
                             [ForecastPoint("Wittering", 63),
                              ForecastPoint("Marham", 65),
                              ForecastPoint("Weybourne", 66),
                              ForecastPoint("Bedford", 75),
                              ForecastPoint("Wattisham", 76),
                              ForecastPoint("Andrewsfield", 85)])

east_midlands = ForecastRegion("E Midlands", 1,
                               [ForecastPoint("Nottingham", 53),
                                ForecastPoint("Scampton", 54),
                                ForecastPoint("Waddington", 55),
                                ForecastPoint("Cranwell", 56),
                                ForecastPoint("Coningsby", 58),
                                ForecastPoint("Wainfleet", 59),
                                ForecastPoint("Fleet Haven", 64)])

london = ForecastRegion("London and SE England", 2,
                        [ForecastPoint("Benson", 82),
                         ForecastPoint("High Wycombe", 83),
                         ForecastPoint("Northolt", 84),
                         ForecastPoint("Great Wakering", 86),
                         ForecastPoint("Middle Wallop", 92),
                         ForecastPoint("Odiham", 93),
                         ForecastPoint("Farnborough", 94),
                         ForecastPoint("Gatwick", 95),
                         ForecastPoint("Heathrow", 96),
                         ForecastPoint("Manston", 98),
                         ForecastPoint("Thorney Island", 109),
                         ForecastPoint("Klin Wood", 110)])

north_east = ForecastRegion("NE England", 3,
                            [ForecastPoint("Rochester", 37),
                             ForecastPoint("Ouston", 38),
                             ForecastPoint("Boulmer", 39)])

yorks_humber = ForecastRegion("Yorks and Humber", 4,
                              [ForecastPoint("Leeming", 40),
                               ForecastPoint("Topcliffe", 41),
                               ForecastPoint("Linton-on-Ouse", 40),
                               ForecastPoint("Loftus", 43),
                               ForecastPoint("Leeds/Bradford", 51),
                               ForecastPoint("Leconfield", 57)])

north_west = ForecastRegion("NW England", 5,
                            [ForecastPoint("Whitehaven", 31),
                             ForecastPoint("Keswick", 32),
                             ForecastPoint("Spadeadam", 34),
                             ForecastPoint("Wickersgill", 35),
                             ForecastPoint("Warcop", 36),
                             ForecastPoint("Altcar", 48),
                             ForecastPoint("Manchester", 52)])

south_west = ForecastRegion("SW England", 6,
                            [ForecastPoint("Filton/Bristol", 79),
                             ForecastPoint("Little Rissington", 80),
                             ForecastPoint("Brize Norton", 81),
                             ForecastPoint("Chivenor", 87),
                             ForecastPoint("Winsford", 88),
                             ForecastPoint("Larkhill", 90),
                             ForecastPoint("Boscombe Down", 91),
                             ForecastPoint("St. Mary's/Isles of Scilly", 99),
                             ForecastPoint("Kehelland", 100),
                             ForecastPoint("Culdrose", 101),
                             ForecastPoint("Bodmin", 102),
                             ForecastPoint("Plymouth", 103),
                             ForecastPoint("Dunkeswell", 104),
                             ForecastPoint("Exeter", 105),
                             ForecastPoint("Yeovilton", 106),
                             ForecastPoint("Portland", 107),
                             ForecastPoint("Bournemouth", 108),
                             ForecastPoint("Guernsey", 111),
                             ForecastPoint("Jersey", 112)])

west_midlands = ForecastRegion("W Midlands", 7,
                               [ForecastPoint("Shawbury", 62),
                                ForecastPoint("Shobdon", 70),
                                ForecastPoint("Hereford", 71),
                                ForecastPoint("Throckmorton", 72),
                                ForecastPoint("Birmingham", 73),
                                ForecastPoint("Coventry", 74)])

wales = ForecastRegion("Wales", 8,
                       [ForecastPoint("Mona", 44),
                        ForecastPoint("Valley/Anglesey", 45),
                        ForecastPoint("Snowdonia", 46),
                        ForecastPoint("Bodelwyddan", 47),
                        ForecastPoint("Uwchmynydd", 60),
                        ForecastPoint("Llanwyddyn", 61),
                        ForecastPoint("Aberporth", 67),
                        ForecastPoint("Llanafan", 68),
                        ForecastPoint("Tirabad", 69),
                        ForecastPoint("Milford Haven", 77),
                        ForecastPoint("Pembrey", 78),
                        ForecastPoint("St. Athan", 89)])

tayside = ForecastRegion("Tayside Central and Fife", 9,
                         [ForecastPoint("Strathallan", 23),
                          ForecastPoint("Leuchars", 29)])

strathclyde = ForecastRegion("Strathclyde", 10,
                             [ForecastPoint("Tiree", 17),
                              ForecastPoint("Islay", 18),
                              ForecastPoint("Campbeltown", 19),
                              ForecastPoint("Bishopton", 21),
                              ForecastPoint("Prestwick/Glasgow", 22),
                              ForecastPoint("Lanark", 25)])

orkney_shetland = ForecastRegion("Orkney and Shetland", 11,
                                 [ForecastPoint("Baltasound", 0),
                                  ForecastPoint("Tingwall", 1),
                                  ForecastPoint("Kirkwall", 2)])

northern_ireland = ForecastRegion("N Ireland", 12,
                                  [ForecastPoint("Killyhevlin", 113),
                                   ForecastPoint("Castlederg", 114),
                                   ForecastPoint("Magilligan", 115),
                                   ForecastPoint("Lough Fea", 116),
                                   ForecastPoint("Portglenone", 117),
                                   ForecastPoint("Ballypatrick", 118),
                                   ForecastPoint("Aldergrove/Belfast", 119),
                                   ForecastPoint("Glenanne", 120)])

highland = ForecastRegion("Highland and Eilean Siar", 13,
                          [ForecastPoint("Geirinis", 3),
                           ForecastPoint("Stornoway", 4),
                           ForecastPoint("Lochdrum", 5),
                           ForecastPoint("Mellon Charles", 6),
                           ForecastPoint("Altnaharra", 7),
                           ForecastPoint("Fersit", 8),
                           ForecastPoint("Balnagall", 9),
                           ForecastPoint("Aviemore", 10),
                           ForecastPoint("Wick", 13)])

grampian = ForecastRegion("Grampian", 14,
                          [ForecastPoint("Kinloss", 11),
                           ForecastPoint("Lossiemouth", 12),
                           ForecastPoint("Aboyne", 14),
                           ForecastPoint("Inverbervie", 15),
                           ForecastPoint("Aberdeen", 16)])

dumfries = ForecastRegion("Dumfries Galloway Lothian Borders", 15,
                          [ForecastPoint("West Freugh", 20),
                           ForecastPoint("Kirkcudbright", 24),
                           ForecastPoint("Charterhall", 26),
                           ForecastPoint("Fingland", 27),
                           ForecastPoint("Edinburgh", 28)])

regions = [east_anglia, east_midlands, london, north_east, yorks_humber,
           north_west, south_west, west_midlands, wales, tayside, strathclyde,
           orkney_shetland, northern_ireland, highland, grampian, dumfries]


def get_regions_with_tokeniser(region_to_tokenise=regions):
    tokeniser = keras.preprocessing.text.Tokenizer(
        filters='!"#$%&()*+,-/:;<=>?@[\\]^_`{|}~\t\n', lower=False)
    text_to_fit = [
        auto_forecaster.io.TextForecast.open_files_from_glob_as_str()
    ]
    tokeniser.fit_on_texts(text_to_fit)
    for region in regions:
        region.tokeniser = tokeniser
    return regions
