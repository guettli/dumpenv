from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import pwd
import sys
import tempfile

import site
import subx

def main():
    out_dir = create_data_and_dump_it()
    print('Dumped environment to directory %s' % out_dir)

def create_data_and_dump_it():
    env_data = dict(
        os=os_module(),
        os_environ=os_environ(),
        sys_path=sys.path,
        PATH=os.environ.get('PATH', '').split(os.pathsep),
        pip_freeze=pip_freeze(),
        site=site_module(),
        platform=platform_module(),
    )
    return dump_data(env_data)

def name_of_environment():
    return '%s@%s--%s' % (pwd.getpwuid(os.geteuid()).pw_name, platform.node(),
                          os.path.basename(os.environ.get('VIRTUAL_ENV', '')))
def dump_data(env_data):
    out_dir = tempfile.mkdtemp(prefix='dumpenv_%s_' % name_of_environment())
    for key, lines in env_data.items():
        with open(os.path.join(out_dir, key), 'wt') as fd:
            fd.write('\n'.join(lines))
    return out_dir

def dict_to_lines(my_dict):
    return ['%s: %r' % (key, value) for key, value in sorted(my_dict.items())]

def os_environ():
    return dict_to_lines(os.environ)

def pip_freeze():
    return subx.call(['pip', 'freeze']).stdout.splitlines()

def site_module():
    return ['%s: %s' % (attr, getattr(site, attr))
            for attr in ['PREFIXES', 'ENABLE_USER_SITE', 'USER_SITE', 'USER_BASE']]

def platform_module():
    return ['%s: %s' % (func, getattr(platform, func)()) for func in
                        ['architecture', 'machine', 'node', 'platform', 'processor',
                         'python_build',
                 'python_compiler', 'python_branch', 'python_implementation',
                 'python_version', 'system']]


def os_module():
    values = []
    for func in [
        'getcwd', 'getegid', 'geteuid', 'getgid', 'getgroups', 'getlogin',
        'getpgrp', 'getresuid', 'getresgid', 'getuid',
    ]:
        try:
            values.append('%s: %s' % (func, getattr(os, func)()))
        except OSError as exc:
            values.append('%s: [%s]' % (func, exc))
    values.append('umask: %s' % get_umask())
    return values

def get_umask():
    current_value = os.umask(0)
    os.umask(current_value)
    return current_value

if __name__=='__main__':
    main()