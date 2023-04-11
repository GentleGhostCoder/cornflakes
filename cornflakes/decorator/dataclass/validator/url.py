from dataclasses import InitVar, fields
from typing import Any, Optional, cast
from urllib.parse import ParseResult, parse_qs, urlparse, urlunparse

import validators

from cornflakes.decorator.config.tuple import to_tuple
from cornflakes.decorator.dataclass._dataclass import dataclass as data
from cornflakes.decorator.dataclass._field import field


@data(
    slots=True,
    frozen=False,
    tuple_factory=lambda self, x: urlunparse(x[:6]),  # unparse to string
    dict_factory=lambda self, x: str(self),  # to string -> tuple -> unparse to string
)
class AnyUrl:
    """Database URL.

    :cvar url: URL to init the whole object (will be overwritten with other args).
    :cvar scheme: The scheme of the url
    :cvar netloc: user / pw / host and port of the url
    :cvar path: path of the url
    :cvar query: url query
    :cvar params: url params
    :cvar query_args: url query_args -> parsed query
    :cvar fragment: url fragment
    :cvar hostname: url hostname (overwrites the netloc)
    :cvar port: url port (overwrites the netloc)
    :cvar username: url username (overwrites the netloc)
    :cvar password: url password (overwrites the netloc)
    :cvar tld: url tld if it is valid
    :cvar valid: validators.url validation result
    """

    url: InitVar[Optional[str]] = None
    scheme: str = field(default="", init=True)
    netloc: str = field(default="", init=True)
    path: str = field(default="", init=True)
    query: str = field(default="", init=True)
    params: str = field(default="", init=True)
    query_args: dict = field(default_factory=dict, init=True)
    fragment: str = field(default="", init=True)
    hostname: Optional[str] = field(default="", init=True, repr=False)
    port: Optional[int] = field(default=None, init=True, repr=False)
    username: Optional[str] = field(default=None, init=True, repr=False)
    password: Optional[str] = field(default=None, init=True, repr=False)
    tld: Optional[str] = field(default=None, init=True, repr=False)
    valid: Optional[str] = field(default=None, init=True, repr=False)
    token: Optional[str] = field(default=None, init=True)

    def __init_parsed(self, parsed: ParseResult, overwrite=True):
        for f in fields(cast(Any, self)):
            if (overwrite or not f.default) and hasattr(parsed, f.name):
                setattr(self, f.name, getattr(parsed, f.name, None))

    def __post_init__(self, url: Optional[str] = None) -> None:
        """Post init."""
        if url:
            parsed = urlparse(url)
            if not parsed.netloc:
                parsed = urlparse(f"//{url}")
            self.query_args.update(parse_qs(parsed.query))
            self.__init_parsed(parsed, overwrite=False)
        if self.username or self.password or self.port:
            # overwrite netloc with custom user / pass
            parsed = urlparse(to_tuple(self))
            login = (
                f"{self.username or parsed.username}:{self.password or parsed.password}@"
                if (self.username or parsed.username) and (self.password or parsed.password)
                else f"{self.token or parsed.username}@"
                if self.token or parsed.username
                else ""
            )
            port = f":{self.port or parsed.port}" if self.port or parsed.port else ""
            hostname = self.hostname if self.hostname else parsed.hostname
            self.netloc = f"{login}{hostname}{port}"
        parsed = urlparse(to_tuple(self))
        self.query_args.update(parse_qs(parsed.query))
        self.__init_parsed(parsed, overwrite=True)
        tld = self.hostname[::-1].split(".", 1)[0][::-1]
        if tld in VALID_ZONES:
            self.tld = tld
        self.valid = validators.url(self.hostname)
        self.token = self.token or self.password or self.username

    def __str__(self) -> str:
        """Any url string."""
        return to_tuple(self)


# TODO: generic get ZONES from zonefiles.io at build time
VALID_ZONES = [
    "aaa",
    "aarp",
    "abarth",
    "abb",
    "abbott",
    "abbvie",
    "abc",
    "able",
    "abogado",
    "abudhabi",
    "ac",
    "academy",
    "accenture",
    "accountant",
    "accountants",
    "aco",
    "actor",
    "ad",
    "adac",
    "ads",
    "adult",
    "ae",
    "aeg",
    "aero",
    "aetna",
    "af",
    "afamilycompany",
    "afl",
    "africa",
    "ag",
    "agakhan",
    "agency",
    "ai",
    "aig",
    "airbus",
    "airforce",
    "airtel",
    "akdn",
    "al",
    "alfaromeo",
    "alibaba",
    "alipay",
    "allfinanz",
    "allstate",
    "ally",
    "alsace",
    "am",
    "amazon",
    "americanexpress",
    "americanfamily",
    "amex",
    "amfam",
    "amica",
    "amsterdam",
    "analytics",
    "android",
    "anquan",
    "anz",
    "ao",
    "aol",
    "apartments",
    "app",
    "apple",
    "aq",
    "aquarelle",
    "ar",
    "arab",
    "aramco",
    "archi",
    "army",
    "art",
    "arte",
    "as",
    "asda",
    "asia",
    "associates",
    "at",
    "athleta",
    "attorney",
    "au",
    "auction",
    "audi",
    "audible",
    "audio",
    "auspost",
    "author",
    "auto",
    "autos",
    "avianca",
    "aw",
    "aws",
    "ax",
    "axa",
    "az",
    "azure",
    "ba",
    "baby",
    "baidu",
    "banamex",
    "bananarepublic",
    "band",
    "bank",
    "bar",
    "barcelona",
    "barclaycard",
    "barclays",
    "barefoot",
    "bargains",
    "baseball",
    "basketball",
    "bauhaus",
    "bayern",
    "bb",
    "bbc",
    "bbt",
    "bbva",
    "bcg",
    "bcn",
    "bd",
    "be",
    "beats",
    "beauty",
    "beer",
    "bentley",
    "berlin",
    "best",
    "bestbuy",
    "bet",
    "bf",
    "bg",
    "bh",
    "bharti",
    "bi",
    "bible",
    "bid",
    "bike",
    "bing",
    "bingo",
    "bio",
    "biz",
    "bj",
    "black",
    "blackfriday",
    "blockbuster",
    "blog",
    "bloomberg",
    "blue",
    "bm",
    "bms",
    "bmw",
    "bn",
    "bnl",
    "bo",
    "boats",
    "boehringer",
    "bofa",
    "bom",
    "bond",
    "boo",
    "book",
    "booking",
    "bosch",
    "bostik",
    "boston",
    "bot",
    "boutique",
    "box",
    "br",
    "bradesco",
    "bridgestone",
    "broadway",
    "broker",
    "brother",
    "brussels",
    "bs",
    "bt",
    "budapest",
    "bugatti",
    "build",
    "builders",
    "business",
    "buy",
    "buzz",
    "bv",
    "bw",
    "by",
    "bz",
    "bzh",
    "ca",
    "cab",
    "cafe",
    "cal",
    "call",
    "calvinklein",
    "cam",
    "camera",
    "camp",
    "cancerresearch",
    "canon",
    "capetown",
    "capital",
    "capitalone",
    "car",
    "caravan",
    "cards",
    "care",
    "career",
    "careers",
    "cars",
    "cartier",
    "casa",
    "case",
    "caseih",
    "cash",
    "casino",
    "cat",
    "catering",
    "catholic",
    "cba",
    "cbn",
    "cbre",
    "cbs",
    "cc",
    "cd",
    "ceb",
    "center",
    "ceo",
    "cern",
    "cf",
    "cfa",
    "cfd",
    "cg",
    "ch",
    "chanel",
    "channel",
    "charity",
    "chase",
    "chat",
    "cheap",
    "chintai",
    "christmas",
    "chrome",
    "chrysler",
    "church",
    "ci",
    "cipriani",
    "circle",
    "cisco",
    "citadel",
    "citi",
    "citic",
    "city",
    "cityeats",
    "ck",
    "cl",
    "claims",
    "cleaning",
    "click",
    "clinic",
    "clinique",
    "clothing",
    "cloud",
    "club",
    "clubmed",
    "cm",
    "cn",
    "co",
    "coach",
    "codes",
    "coffee",
    "college",
    "cologne",
    "com",
    "comcast",
    "commbank",
    "community",
    "company",
    "compare",
    "computer",
    "comsec",
    "condos",
    "construction",
    "consulting",
    "contact",
    "contractors",
    "cooking",
    "cookingchannel",
    "cool",
    "coop",
    "corsica",
    "country",
    "coupon",
    "coupons",
    "courses",
    "cpa",
    "cr",
    "credit",
    "creditcard",
    "creditunion",
    "cricket",
    "crown",
    "crs",
    "cruise",
    "cruises",
    "csc",
    "cu",
    "cuisinella",
    "cv",
    "cw",
    "cx",
    "cy",
    "cymru",
    "cyou",
    "cz",
    "dabur",
    "dad",
    "dance",
    "data",
    "date",
    "dating",
    "datsun",
    "day",
    "dclk",
    "dds",
    "de",
    "deal",
    "dealer",
    "deals",
    "degree",
    "delivery",
    "dell",
    "deloitte",
    "delta",
    "democrat",
    "dental",
    "dentist",
    "desi",
    "design",
    "dev",
    "dhl",
    "diamonds",
    "diet",
    "digital",
    "direct",
    "directory",
    "discount",
    "discover",
    "dish",
    "diy",
    "dj",
    "dk",
    "dm",
    "dnp",
    "do",
    "docs",
    "doctor",
    "dodge",
    "dog",
    "domains",
    "dot",
    "download",
    "drive",
    "dtv",
    "dubai",
    "duck",
    "dunlop",
    "dupont",
    "durban",
    "dvag",
    "dvr",
    "dz",
    "earth",
    "eat",
    "ec",
    "eco",
    "edeka",
    "edu",
    "education",
    "ee",
    "eg",
    "email",
    "emerck",
    "energy",
    "engineer",
    "engineering",
    "enterprises",
    "epson",
    "equipment",
    "er",
    "ericsson",
    "erni",
    "es",
    "esq",
    "estate",
    "esurance",
    "et",
    "etisalat",
    "eu",
    "eurovision",
    "eus",
    "events",
    "everbank",
    "exchange",
    "expert",
    "exposed",
    "express",
    "extraspace",
    "fage",
    "fail",
    "fairwinds",
    "faith",
    "family",
    "fan",
    "fans",
    "farm",
    "farmers",
    "fashion",
    "fast",
    "fedex",
    "feedback",
    "ferrari",
    "ferrero",
    "fi",
    "fiat",
    "fidelity",
    "fido",
    "film",
    "final",
    "finance",
    "financial",
    "fire",
    "firestone",
    "firmdale",
    "fish",
    "fishing",
    "fit",
    "fitness",
    "fj",
    "fk",
    "flickr",
    "flights",
    "flir",
    "florist",
    "flowers",
    "fly",
    "fm",
    "fo",
    "foo",
    "food",
    "foodnetwork",
    "football",
    "ford",
    "forex",
    "forsale",
    "forum",
    "foundation",
    "fox",
    "fr",
    "free",
    "fresenius",
    "frl",
    "frogans",
    "frontdoor",
    "frontier",
    "ftr",
    "fujitsu",
    "fujixerox",
    "fun",
    "fund",
    "furniture",
    "futbol",
    "fyi",
    "ga",
    "gal",
    "gallery",
    "gallo",
    "gallup",
    "game",
    "games",
    "gap",
    "garden",
    "gay",
    "gb",
    "gbiz",
    "gd",
    "ge",
    "gea",
    "gent",
    "genting",
    "george",
    "gf",
    "gg",
    "ggee",
    "gh",
    "gi",
    "gift",
    "gifts",
    "gives",
    "giving",
    "gl",
    "glade",
    "glass",
    "gle",
    "global",
    "globo",
    "gm",
    "gmail",
    "gmbh",
    "gmo",
    "gmx",
    "gn",
    "godaddy",
    "gold",
    "goldpoint",
    "golf",
    "goo",
    "goodyear",
    "goog",
    "google",
    "gop",
    "got",
    "gov",
    "gp",
    "gq",
    "gr",
    "grainger",
    "graphics",
    "gratis",
    "green",
    "gripe",
    "grocery",
    "group",
    "gs",
    "gt",
    "gu",
    "guardian",
    "gucci",
    "guge",
    "guide",
    "guitars",
    "guru",
    "gw",
    "gy",
    "hair",
    "hamburg",
    "hangout",
    "haus",
    "hbo",
    "hdfc",
    "hdfcbank",
    "health",
    "healthcare",
    "help",
    "helsinki",
    "here",
    "hermes",
    "hgtv",
    "hiphop",
    "hisamitsu",
    "hitachi",
    "hiv",
    "hk",
    "hkt",
    "hm",
    "hn",
    "hockey",
    "holdings",
    "holiday",
    "homedepot",
    "homegoods",
    "homes",
    "homesense",
    "honda",
    "horse",
    "hospital",
    "host",
    "hosting",
    "hot",
    "hoteles",
    "hotels",
    "hotmail",
    "house",
    "how",
    "hr",
    "hsbc",
    "ht",
    "hu",
    "hughes",
    "hyatt",
    "hyundai",
    "ibm",
    "icbc",
    "ice",
    "icu",
    "id",
    "ie",
    "ieee",
    "ifm",
    "ikano",
    "il",
    "im",
    "imamat",
    "imdb",
    "immo",
    "immobilien",
    "in",
    "inc",
    "industries",
    "infiniti",
    "info",
    "ing",
    "ink",
    "institute",
    "insurance",
    "insure",
    "int",
    "intel",
    "international",
    "intuit",
    "investments",
    "io",
    "ipiranga",
    "iq",
    "ir",
    "irish",
    "is",
    "iselect",
    "ismaili",
    "ist",
    "istanbul",
    "it",
    "itau",
    "itv",
    "iveco",
    "jaguar",
    "java",
    "jcb",
    "jcp",
    "je",
    "jeep",
    "jetzt",
    "jewelry",
    "jio",
    "jll",
    "jm",
    "jmp",
    "jnj",
    "jo",
    "jobs",
    "joburg",
    "jot",
    "joy",
    "jp",
    "jpmorgan",
    "jprs",
    "juegos",
    "juniper",
    "kaufen",
    "kddi",
    "ke",
    "kerryhotels",
    "kerrylogistics",
    "kerryproperties",
    "kfh",
    "kg",
    "kh",
    "ki",
    "kia",
    "kids",
    "kim",
    "kinder",
    "kindle",
    "kitchen",
    "kiwi",
    "km",
    "kn",
    "koeln",
    "komatsu",
    "kosher",
    "kp",
    "kpmg",
    "kpn",
    "kr",
    "krd",
    "kred",
    "kuokgroup",
    "kw",
    "ky",
    "kyoto",
    "kz",
    "la",
    "lacaixa",
    "ladbrokes",
    "lamborghini",
    "lamer",
    "lancaster",
    "lancia",
    "lancome",
    "land",
    "landrover",
    "lanxess",
    "lasalle",
    "lat",
    "latino",
    "latrobe",
    "law",
    "lawyer",
    "lb",
    "lc",
    "lds",
    "lease",
    "leclerc",
    "lefrak",
    "legal",
    "lego",
    "lexus",
    "lgbt",
    "li",
    "liaison",
    "lidl",
    "life",
    "lifeinsurance",
    "lifestyle",
    "lighting",
    "like",
    "lilly",
    "limited",
    "limo",
    "lincoln",
    "linde",
    "link",
    "lipsy",
    "live",
    "living",
    "lixil",
    "lk",
    "llc",
    "llp",
    "loan",
    "loans",
    "locker",
    "locus",
    "loft",
    "lol",
    "london",
    "lotte",
    "lotto",
    "love",
    "lpl",
    "lplfinancial",
    "lr",
    "ls",
    "lt",
    "ltd",
    "ltda",
    "lu",
    "lundbeck",
    "lupin",
    "luxe",
    "luxury",
    "lv",
    "ly",
    "ma",
    "macys",
    "madrid",
    "maif",
    "maison",
    "makeup",
    "man",
    "management",
    "mango",
    "map",
    "market",
    "marketing",
    "markets",
    "marriott",
    "marshalls",
    "maserati",
    "mattel",
    "mba",
    "mc",
    "mckinsey",
    "md",
    "me",
    "med",
    "media",
    "meet",
    "melbourne",
    "meme",
    "memorial",
    "men",
    "menu",
    "merckmsd",
    "metlife",
    "mg",
    "mh",
    "miami",
    "microsoft",
    "mil",
    "mini",
    "mint",
    "mit",
    "mitsubishi",
    "mk",
    "ml",
    "mlb",
    "mls",
    "mm",
    "mma",
    "mn",
    "mo",
    "mobi",
    "mobile",
    "mobily",
    "moda",
    "moe",
    "moi",
    "mom",
    "monash",
    "money",
    "monster",
    "mopar",
    "mormon",
    "mortgage",
    "moscow",
    "moto",
    "motorcycles",
    "mov",
    "movie",
    "movistar",
    "mp",
    "mq",
    "mr",
    "ms",
    "msd",
    "mt",
    "mtn",
    "mtr",
    "mu",
    "museum",
    "music",
    "mutual",
    "mv",
    "mw",
    "mx",
    "my",
    "mz",
    "na",
    "nab",
    "nadex",
    "nagoya",
    "name",
    "nationwide",
    "natura",
    "navy",
    "nba",
    "nc",
    "ne",
    "nec",
    "net",
    "netbank",
    "netflix",
    "network",
    "neustar",
    "new",
    "newholland",
    "news",
    "next",
    "nextdirect",
    "nexus",
    "nf",
    "nfl",
    "ng",
    "ngo",
    "nhk",
    "ni",
    "nico",
    "nike",
    "nikon",
    "ninja",
    "nissan",
    "nissay",
    "nl",
    "no",
    "nokia",
    "northwesternmutual",
    "norton",
    "now",
    "nowruz",
    "nowtv",
    "np",
    "nr",
    "nra",
    "nrw",
    "ntt",
    "nu",
    "nyc",
    "nz",
    "obi",
    "observer",
    "off",
    "office",
    "okinawa",
    "olayan",
    "olayangroup",
    "oldnavy",
    "ollo",
    "om",
    "omega",
    "one",
    "ong",
    "onl",
    "online",
    "onyourside",
    "ooo",
    "open",
    "oracle",
    "orange",
    "org",
    "organic",
    "origins",
    "osaka",
    "otsuka",
    "ott",
    "ovh",
    "pa",
    "page",
    "panasonic",
    "paris",
    "pars",
    "partners",
    "parts",
    "party",
    "passagens",
    "pay",
    "pccw",
    "pe",
    "pet",
    "pf",
    "pfizer",
    "pg",
    "ph",
    "pharmacy",
    "phd",
    "philips",
    "phone",
    "photo",
    "photography",
    "photos",
    "physio",
    "piaget",
    "pics",
    "pictet",
    "pictures",
    "pid",
    "pin",
    "ping",
    "pink",
    "pioneer",
    "pizza",
    "pk",
    "pl",
    "place",
    "play",
    "playstation",
    "plumbing",
    "plus",
    "pm",
    "pn",
    "pnc",
    "pohl",
    "poker",
    "politie",
    "porn",
    "pr",
    "pramerica",
    "praxi",
    "press",
    "prime",
    "pro",
    "prod",
    "productions",
    "prof",
    "progressive",
    "promo",
    "properties",
    "property",
    "protection",
    "pru",
    "prudential",
    "ps",
    "pt",
    "pub",
    "pw",
    "pwc",
    "py",
    "qa",
    "qpon",
    "quebec",
    "quest",
    "qvc",
    "racing",
    "radio",
    "raid",
    "re",
    "read",
    "realestate",
    "realtor",
    "realty",
    "recipes",
    "red",
    "redstone",
    "redumbrella",
    "rehab",
    "reise",
    "reisen",
    "reit",
    "reliance",
    "ren",
    "rent",
    "rentals",
    "repair",
    "report",
    "republican",
    "rest",
    "restaurant",
    "review",
    "reviews",
    "rexroth",
    "rich",
    "richardli",
    "ricoh",
    "rightathome",
    "ril",
    "rio",
    "rip",
    "rmit",
    "ro",
    "rocher",
    "rocks",
    "rodeo",
    "rogers",
    "room",
    "rs",
    "rsvp",
    "ru",
    "rugby",
    "ruhr",
    "run",
    "rw",
    "rwe",
    "ryukyu",
    "sa",
    "saarland",
    "safe",
    "safety",
    "sakura",
    "sale",
    "salon",
    "samsclub",
    "samsung",
    "sandvik",
    "sandvikcoromant",
    "sanofi",
    "sap",
    "sarl",
    "sas",
    "save",
    "saxo",
    "sb",
    "sbi",
    "sbs",
    "sc",
    "sca",
    "scb",
    "schaeffler",
    "schmidt",
    "scholarships",
    "school",
    "schule",
    "schwarz",
    "science",
    "scjohnson",
    "scor",
    "scot",
    "sd",
    "se",
    "search",
    "seat",
    "secure",
    "security",
    "seek",
    "select",
    "sener",
    "services",
    "ses",
    "seven",
    "sew",
    "sex",
    "sexy",
    "sfr",
    "sg",
    "sh",
    "shangrila",
    "sharp",
    "shell",
    "shia",
    "shiksha",
    "shoes",
    "shop",
    "shopping",
    "shouji",
    "show",
    "showtime",
    "shriram",
    "si",
    "silk",
    "sina",
    "singles",
    "site",
    "sj",
    "sk",
    "ski",
    "skin",
    "sky",
    "skype",
    "sl",
    "sling",
    "sm",
    "smart",
    "smile",
    "sn",
    "sncf",
    "so",
    "soccer",
    "social",
    "softbank",
    "software",
    "sohu",
    "solar",
    "solutions",
    "song",
    "sony",
    "soy",
    "space",
    "sport",
    "spot",
    "spreadbetting",
    "sr",
    "srl",
    "srt",
    "ss",
    "st",
    "stada",
    "staples",
    "star",
    "starhub",
    "statebank",
    "statefarm",
    "stc",
    "stcgroup",
    "stockholm",
    "storage",
    "store",
    "stream",
    "studio",
    "study",
    "style",
    "su",
    "sucks",
    "supplies",
    "supply",
    "support",
    "surf",
    "surgery",
    "suzuki",
    "sv",
    "swatch",
    "swiftcover",
    "swiss",
    "sx",
    "sy",
    "sydney",
    "symantec",
    "systems",
    "sz",
    "tab",
    "taipei",
    "talk",
    "taobao",
    "target",
    "tatamotors",
    "tatar",
    "tattoo",
    "tax",
    "taxi",
    "tc",
    "tci",
    "td",
    "tdk",
    "team",
    "tech",
    "technology",
    "tel",
    "telefonica",
    "temasek",
    "tennis",
    "teva",
    "tf",
    "tg",
    "th",
    "thd",
    "theater",
    "theatre",
    "tiaa",
    "tickets",
    "tienda",
    "tiffany",
    "tips",
    "tires",
    "tirol",
    "tj",
    "tjmaxx",
    "tjx",
    "tk",
    "tkmaxx",
    "tl",
    "tm",
    "tmall",
    "tn",
    "to",
    "today",
    "tokyo",
    "tools",
    "top",
    "toray",
    "toshiba",
    "total",
    "tours",
    "town",
    "toyota",
    "toys",
    "tr",
    "trade",
    "trading",
    "training",
    "travel",
    "travelchannel",
    "travelers",
    "travelersinsurance",
    "trust",
    "trv",
    "tt",
    "tube",
    "tui",
    "tunes",
    "tushu",
    "tv",
    "tvs",
    "tw",
    "tz",
    "ua",
    "ubank",
    "ubs",
    "uconnect",
    "ug",
    "uk",
    "unicom",
    "university",
    "uno",
    "uol",
    "ups",
    "us",
    "uy",
    "uz",
    "va",
    "vacations",
    "vana",
    "vanguard",
    "vc",
    "ve",
    "vegas",
    "ventures",
    "verisign",
    "versicherung",
    "vet",
    "vg",
    "vi",
    "viajes",
    "video",
    "vig",
    "viking",
    "villas",
    "vin",
    "vip",
    "virgin",
    "visa",
    "vision",
    "vistaprint",
    "viva",
    "vivo",
    "vlaanderen",
    "vn",
    "vodka",
    "volkswagen",
    "volvo",
    "vote",
    "voto",
    "voyage",
    "vu",
    "vuelos",
    "wales",
    "walmart",
    "walter",
    "wang",
    "wanggou",
    "warman",
    "watch",
    "watches",
    "weather",
    "weatherchannel",
    "webcam",
    "weber",
    "website",
    "wed",
    "wedding",
    "weibo",
    "weir",
    "wf",
    "whoswho",
    "wien",
    "wiki",
    "williamhill",
    "win",
    "windows",
    "wine",
    "winners",
    "wme",
    "wolterskluwer",
    "woodside",
    "work",
    "works",
    "world",
    "wow",
    "ws",
    "wtc",
    "wtf",
    "xbox",
    "xerox",
    "xfinity",
    "xihuan",
    "xin",
    "xn--11b4c3d",
    "xn--1ck2e1b",
    "xn--1qqw23a",
    "xn--2scrj9c",
    "xn--30rr7y",
    "xn--3bst00m",
    "xn--3ds443g",
    "xn--3e0b707e",
    "xn--3hcrj9c",
    "xn--3oq18vl8pn36a",
    "xn--3pxu8k",
    "xn--42c2d9a",
    "xn--45brj9c",
    "xn--45q11c",
    "xn--4gbrim",
    "xn--54b7fta0cc",
    "xn--55qw42g",
    "xn--55qx5d",
    "xn--5su34j936bgsg",
    "xn--5tzm5g",
    "xn--6frz82g",
    "xn--6qq986b3xl",
    "xn--80adxhks",
    "xn--80ao21a",
    "xn--80aqecdr1a",
    "xn--80asehdb",
    "xn--80aswg",
    "xn--8y0a063a",
    "xn--90a3ac",
    "xn--90ae",
    "xn--90ais",
    "xn--9dbq2a",
    "xn--9et52u",
    "xn--9krt00a",
    "xn--b4w605ferd",
    "xn--bck1b9a5dre4c",
    "xn--c1avg",
    "xn--c2br7g",
    "xn--cck2b3b",
    "xn--cckwcxetd",
    "xn--cg4bki",
    "xn--clchc0ea0b2g2a9gcd",
    "xn--czr694b",
    "xn--czrs0t",
    "xn--czru2d",
    "xn--d1acj3b",
    "xn--d1alf",
    "xn--e1a4c",
    "xn--eckvdtc9d",
    "xn--efvy88h",
    "xn--estv75g",
    "xn--fct429k",
    "xn--fhbei",
    "xn--fiq228c5hs",
    "xn--fiq64b",
    "xn--fiqs8s",
    "xn--fiqz9s",
    "xn--fjq720a",
    "xn--flw351e",
    "xn--fpcrj9c3d",
    "xn--fzc2c9e2c",
    "xn--fzys8d69uvgm",
    "xn--g2xx48c",
    "xn--gckr3f0f",
    "xn--gecrj9c",
    "xn--gk3at1e",
    "xn--h2brj9c",
    "xn--hxt814e",
    "xn--i1b6b1a6a2e",
    "xn--imr513n",
    "xn--io0a7i",
    "xn--j1aef",
    "xn--j1amh",
    "xn--j6w193g",
    "xn--jlq480n2rg",
    "xn--jlq61u9w7b",
    "xn--jvr189m",
    "xn--kcrx77d1x4a",
    "xn--kprw13d",
    "xn--kpry57d",
    "xn--kpu716f",
    "xn--l1acc",
    "xn--lgbbat1ad8j",
    "xn--mgba3a3ejt",
    "xn--mgba3a4f16a",
    "xn--mgba7c0bbn0a",
    "xn--mgbaakc7dvf",
    "xn--mgbaam7a8h",
    "xn--mgbab2bd",
    "xn--mgbah1a3hjkrd",
    "xn--mgbayh7gpa",
    "xn--mgbb9fbpob",
    "xn--mgbbh1a",
    "xn--mgbbh1a71e",
    "xn--mgbca7dzdo",
    "xn--mgberp4a5d4ar",
    "xn--mgbi4ecexp",
    "xn--mgbt3dhd",
    "xn--mk1bu44c",
    "xn--mxtq1m",
    "xn--ngbc5azd",
    "xn--ngbe9e0a",
    "xn--ngbrx",
    "xn--node",
    "xn--nqv7f",
    "xn--nqv7fs00ema",
    "xn--nyqy26a",
    "xn--o3cw4h",
    "xn--ogbpf8fl",
    "xn--otu796d",
    "xn--p1acf",
    "xn--p1ai",
    "xn--pbt977c",
    "xn--pgbs0dh",
    "xn--pssy2u",
    "xn--q9jyb4c",
    "xn--qcka1pmc",
    "xn--qxam",
    "xn--rhqv96g",
    "xn--rovu88b",
    "xn--rvc1e0am3e",
    "xn--s9brj9c",
    "xn--ses554g",
    "xn--t60b56a",
    "xn--tckwe",
    "xn--tiq49xqyj",
    "xn--unup4y",
    "xn--vermgensberater-ctb",
    "xn--vermgensberatung-pwb",
    "xn--vhquv",
    "xn--vuq861b",
    "xn--w4r85el8fhu5dnra",
    "xn--w4rs40l",
    "xn--wgbh1c",
    "xn--wgbl6a",
    "xn--xhq521b",
    "xn--xkc2dl3a5ee0h",
    "xn--y9a3aq",
    "xn--yfro4i67o",
    "xn--zfr164b",
    "xxx",
    "xyz",
    "yachts",
    "yahoo",
    "yamaxun",
    "yandex",
    "ye",
    "yodobashi",
    "yoga",
    "yokohama",
    "you",
    "youtube",
    "yt",
    "yun",
    "za",
    "zappos",
    "zara",
    "zero",
    "zip",
    "zm",
    "zone",
    "zuerich",
    "zw",
]