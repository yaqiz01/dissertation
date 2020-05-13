
stanford_colors = {
    "Cardinal Red":"#8c1515",
    "Sandstone":"#d2c295",
    "White":"#ffffff",
    "Black":"#2e2d29",
    "Warm Grey":"#3f3c30",
    "Cool Grey":"#4d4f53",
    "Beige":"#9d9573",
    "Light Sage":"#c7d1c5",
    "Clay":"#5f574f",
    "Cloud":"#dad7cb",
    "Driftwood":"#b6b1a9",
    "Stone":"#928b81",
    "Sandhill":"#b3995d",
    "Palo Alto":"#175e54",
    "Teal":"#00505c",
    "Purple":"#53284f",
    "Redwood":"#8d3c1e",
    "Brown":"#5e3032",
    "Sky":"#0098db",
    "Lagunita":"#007c92",
    "Mint":"#009b76",
    "Gold":"#b26f16",
    "Sun":"#eaab00",
    "Poppy":"#e98300",
    "Bright Red": "#B1040E"
}
def get_stanford_colors(*names):
    return [stanford_colors[n] for n in names]
