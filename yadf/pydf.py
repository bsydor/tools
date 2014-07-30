#!/usr/bin/env python
'''df-like tool to print disk usage including blocks, inodes, and json format'''

import yadf
import sys


D = yadf.Yadf()
if '--json' in sys.argv:
    OUTPUT_ = D.json_out()
elif '--max' in sys.argv:
    maxdf = yadf.get_maxima(D.list_out(), skey_='both')
    OUTPUT_ = '{0:10} {1:3}%'.format(maxdf[0], maxdf[1])
else:
    OUTPUT_ = D.list_out()

yadf.printout(OUTPUT_)
