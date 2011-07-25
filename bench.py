
import cProfile
import main
cProfile.run('main.startup()', 'ffstats')
print "stilla alive"
import pstats
p = pstats.Stats('ffstats')
#p.sort_stats('file').print_stats(10)
p.sort_stats('cum','time').print_stats(10)
