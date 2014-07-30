#!/usr/bin/env python
'''Return as IP in reversed order'''

import sys


try:
    print('.'.join(reversed(sys.argv[1].split('.'))))
except Exception:
    print('Usage: {0} 1.2.3.4'.format(sys.argv[0]))
