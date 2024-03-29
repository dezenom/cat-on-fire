from globals import change_level

def run(screen,state_runs):
    while change_level:
        state_runs["game"](screen,state_runs)