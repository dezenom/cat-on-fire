from numpy import loadtxt

def levels(level):
    LEVELS = {"physics":[loadtxt(f"resources/levels/level{level}/one__physics.csv",delimiter=",",dtype=int), 16, "resources/tileset.png"],
           "playerpos":[loadtxt(f"resources/levels/level{level}/one__playerpos.csv",delimiter=",",dtype=int), 16, "resources/tileset.png"],
           "fillins":[loadtxt(f"resources/levels/level{level}/one__fillins.csv",delimiter=",",dtype=int), 16, "resources/tileset.png"],
           "GOUPS":[loadtxt(f"resources/levels/level{level}/one__GOUPS.csv",delimiter=",",dtype=int), 16, "resources/tileset.png"],
           "GODOWNS":[loadtxt(f"resources/levels/level{level}/one__GODOWNS.csv",delimiter=",",dtype=int), 16, "resources/tileset.png"]}
    return LEVELS
