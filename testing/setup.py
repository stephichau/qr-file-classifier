from __future__ import absolute_import
from utils.log import cool_print_decoration
import subprocess
import sys


def installed_packages() -> set:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    return set(r.decode().split('==')[0] for r in reqs.split()) 

def read_requirements(req_path: str) -> None:
    _installed = installed_packages()
    _req = ''
    with open(req_path, 'r') as f:
        _req = set([mod_name.strip().split('==')[0] for mod_name in f])
    _filered_modules = set(filter(lambda mod_name: mod_name in _req, _installed))
    if _filered_modules.difference(_req):
        txt = ''
        for name in _filered_modules.difference(_req):
            txt += 'Missing: {} module.\n'.format(name)
        cool_print_decoration(txt, 'danger')
    else: cool_print_decoration('Requirements check!', 'result')