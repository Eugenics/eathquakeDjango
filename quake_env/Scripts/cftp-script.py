#!l:\django\eathquakes\quake_env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Twisted==19.10.0','console_scripts','cftp'
__requires__ = 'Twisted==19.10.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Twisted==19.10.0', 'console_scripts', 'cftp')()
    )
