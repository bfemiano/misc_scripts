import subprocess
import optparse
import sys
from datetime import datetime

__author__ = 'brianfemiano'

def main():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--user', dest='user')
    parser.add_option('-d', '--date-cutoff', dest='date_arg')
    options, args = parser.parse_args()
    cmds = []
    cmds.append('hadoop')
    cmds.append('fs')
    cmds.append('-ls')
    cmds.append('/tmp')
    out = subprocess.Popen(cmds, stdout=subprocess.PIPE)
    for line in out.stdout.readlines():
        fields = line.strip('\n').split(' ')
        user = None
        group = None
        size = None
        indate = None
        time = None
        indir = None
        if not line.startswith('dr'):
            continue
        for field in fields[4:]:
            if field != '':
                if not user:
                    user = field
                    continue
                if not group:
                    group = field
                    continue
                if not size:
                    size = field
                    continue
                if not indate:
                    indate = field
                    continue
                if not time:
                    time = field
                    continue
                if not indir:
                    indir = field
                    continue
        date = datetime.strptime(indate,'%Y-%m-%d')
        cutoff_date = datetime.strptime(options.date_arg, '%Y-%m-%d')
        if (date - cutoff_date).days < 0:
            if options.user == user:
                print 'deleting {0}'.format(indir)
                cmds = []
                cmds.append('hadoop')
                cmds.append('fs')
                cmds.append('-rm')
                cmds.append('-r')
                cmds.append('-skipTrash')
                cmds.append(indir)  
                subprocess.check_call(' '.join(cmds), shell=True)   
            else:
                'owner of {0} is not {1}'.format(indir, options.user)


if __name__ == "__main__":
    main()