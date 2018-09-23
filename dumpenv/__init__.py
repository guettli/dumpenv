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
        sys=sys_module(),
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
            for line in lines:
                fd.write('%s\n' % normalize_line(line))
    return out_dir

def normalize_line(line):
    line=normalize_line__magic(line, 'VIRTUAL_ENV')
    line=normalize_line__magic(line, 'HOME')
    return line

def normalize_line__magic(line, env_name):
    magic = os.environ.get(env_name)
    if not magic:
        return line
    if env_name in line:
        return line
    return line.replace(magic, '${%s}' % env_name)

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
    return ['%s(): %s' % (func, getattr(platform, func)()) for func in
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
            values.append('%s(): %s' % (func, getattr(os, func)()))
        except OSError as exc:
            values.append('%s: [%s]' % (func, exc))
    values.append('umask: %s' % oct(get_umask()))
    return values

def get_umask():
    current_value = os.umask(0)
    os.umask(current_value)
    return current_value

def sys_module():
    values = []
    for attr in [
        'argv', 'byteorder', 'exec_prefix', 'executable', 'flags', 'float_info',
        'maxint', 'maxsize', 'maxunicode', 'meta_path', 'py3kwarning',
    ]:
        values.append('%s: %s' % (attr, getattr(sys, attr)))
    for func in [
        'getcheckinterval', 'getdefaultencoding', 'getfilesystemencoding',
        'getrecursionlimit',
    ]:
        values.append('%s(): %s' % (func, getattr(sys, func)()))



    return values

if __name__=='__main__':
    main()