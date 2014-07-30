'''Yet another Disk usage stats supporting json output'''
import os
import json


class Yadf(object):
    '''Yet another disk usage for blocks and inodes'''

    def __init__(self):

        self.mounts = self.__get_mpoints()
        self.raw_stats = self.__get_statvfs()
        self.usage_uni = self.__get_usage_universal2()
        return

    def __get_mpoints(self, mounts_f=None):
        """ Return a list of all mount points """
        mpoints = set()
        if mounts_f is None:
            mounts_f = '/proc/mounts'

        with open(mounts_f) as file_:
            for line in file_.readlines():
                mpoints.add(line.split()[1])
        return sorted(mpoints)

    def __get_statvfs(self, mpoints=None):
        """ Return a list of tuples mount point and statvfs"""
        dfs = []
        if mpoints is None:
            mpoints = self.mounts

        for i in mpoints:
            dfs.append((i, os.statvfs(i)))
        return dfs

    def refresh(self):
        """ Refresh to update the state"""

        self.mounts = self.__get_mpoints()
        self.raw_stats = self.__get_statvfs()
        self.usage_uni = self.__get_usage_universal2()
        return

    def __get_usage_universal(self):
        '''Return dict with percent usage of blocks and inodes'''
        usage_uni = []
        for fs_, stats in self.raw_stats:
            if stats.f_blocks != 0:
                p_bused_r = 100 - int(stats.f_bfree * 100 / stats.f_blocks)
                #p_bused_u = 100 - int(stats.f_bavail * 100 / stats.f_blocks)
                p_iused_r = 100 - int(stats.f_ffree * 100 / stats.f_files)
                #p_iused_u = 100 - int(stats.f_favail * 100 / stats.f_files)

                usage_uni.append({
                    'filesystem': fs_,
                    'blocks': p_bused_r,
                    'inodes': p_iused_r,
                    'unit': '%'
                })
        return usage_uni

    def __get_usage_universal2(self):
        '''Return dict with percent usage of blocks and inodes'''
        usage_uni = {}
        for fs_, stats in self.raw_stats:
            if stats.f_blocks != 0:
                p_bused_r = 100 - int(stats.f_bfree * 100 / stats.f_blocks)
                p_bused_u = 100 - int(stats.f_bavail * 100 / stats.f_blocks)
                p_iused_r = 100 - int(stats.f_ffree * 100 / stats.f_files)
                p_iused_u = 100 - int(stats.f_favail * 100 / stats.f_files)

                usage_uni.update({fs_: {
                    'blocks': p_bused_r,
                    'inodes': p_iused_r,
                    'blocks_u': p_bused_u,
                    'inodes_u': p_iused_u,
                    'unit': '%'
                }})
        return usage_uni

    def json_out(self):
        '''Return disk usage report as json'''
        json_ = json.dumps(self.usage_uni)
        return json_

    def list_out(self):
        '''Return disk usage report as list'''
        out_l = []
        for i in self.usage_uni:
            out_l.append(
                (i, self.usage_uni[i]['blocks'],
                self.usage_uni[i]['inodes'],
                self.usage_uni[i]['unit'])
            )
        return sorted(out_l)


def printout(input_):
    '''Print out formated output'''
    if type(input_) is list:
        print('{0:10} {1:2} {2:2}'.format('Filesystem', 'blocks', 'inodes'))
        for i in input_:
            print('{0:10} {1:2}% {2:2}%'.format(i[0], i[1], i[2]))
    else:
        print(input_)

def get_maxima(input_, skey_=None):
    '''Return max values, takes list of tuples as input'''

    skey_d = { 'block':(), 'inode':(), 'both':() }

    sb_ = sorted(input_, key=lambda i: i[1], reverse=True)
    si_ = sorted(input_, key=lambda i: i[2], reverse=True)

    skey_d['block'] = (sb_[0][0], sb_[0][1])
    skey_d['inode'] = (si_[0][0], si_[0][2])

    if sb_[0][1] > si_[0][2]:
        skey_d['both'] = (sb_[0][0], sb_[0][1])
    else:
        skey_d['both'] = (si_[0][0], si_[0][2])

    if skey_ is not None:
        return skey_d[skey_]
    else:
        return skey_d
    return

