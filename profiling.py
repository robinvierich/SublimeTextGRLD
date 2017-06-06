import cProfile, pstats, io

pr = cProfile.Profile()

def start_profile(name):
    pr.enable()