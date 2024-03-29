from numpy import loadtxt
level_0 = loadtxt("resources/levels/l_0.csv",delimiter=",",dtype=int)
level_1 = loadtxt("resources/levels/l_1.csv",delimiter=",",dtype=int)
level_2 = loadtxt("resources/levels/l_2.csv",delimiter=",",dtype=int)
all_levels = [level_0,level_1,level_2]