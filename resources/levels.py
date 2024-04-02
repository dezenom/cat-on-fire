from numpy import loadtxt

tileset = "resources/tileset.png"

def levels(level):
    LEVELS = {"physics":[loadtxt(f"resources/levels/level{level}/__physics.csv",delimiter=",",dtype=int),tileset],
           "playerpos":[loadtxt(f"resources/levels/level{level}/__playerpos.csv",delimiter=",",dtype=int), tileset],
           "fillins":[loadtxt(f"resources/levels/level{level}/__fillins.csv",delimiter=",",dtype=int), tileset],
           "GOUPS":[loadtxt(f"resources/levels/level{level}/__GOUPS.csv",delimiter=",",dtype=int),tileset],
           "GODOWNS":[loadtxt(f"resources/levels/level{level}/__GODOWNS.csv",delimiter=",",dtype=int),tileset]}
    return LEVELS
