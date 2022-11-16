# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: os.py
r"""OS routines for NT or Posix depending on what system we're on.

This exports:
  - all functions from posix or nt, e.g. unlink, stat, etc.
  - os.path is either posixpath or ntpath
  - os.name is either 'posix' or 'nt'
  - os.curdir is a string representing the current directory (always '.')
  - os.pardir is a string representing the parent directory (always '..')
  - os.sep is the (or a most common) pathname separator ('/' or '\\')
  - os.extsep is the extension separator (always '.')
  - os.altsep is the alternate pathname separator (None or '/')
  - os.pathsep is the component separator used in $PATH etc
  - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
  - os.defpath is the default search path for executables
  - os.devnull is the file path of the null device ('/dev/null', etc.)

Programs that import and use 'os' stand a better chance of being
portable between different platforms.  Of course, they must then
only use functions that are defined by all platforms (e.g., unlink
and opendir), and leave all pathname manipulation to os.path
(e.g., split and join).
"""
import abc, sys, errno, stat as st
_names = sys.builtin_module_names
__all__ = [
 'altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep',
 'defpath', 'name', 'path', 'devnull', 'SEEK_SET', 'SEEK_CUR',
 'SEEK_END', 'fsencode', 'fsdecode', 'get_exec_path', 'fdopen',
 'popen', 'extsep']

def _exists(name):
    return name in globals()


def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']


if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    from posix import *
    try:
        from posix import _exit
        __all__.append('_exit')
    except ImportError:
        pass

    import posixpath as path
    try:
        from posix import _have_functions
    except ImportError:
        pass

    import posix
    __all__.extend(_get_exports_list(posix))
    del posix
elif 'nt' in _names:
    name = 'nt'
    linesep = '\r\n'
    from nt import *
    try:
        from nt import _exit
        __all__.append('_exit')
    except ImportError:
        pass

    import ntpath as path, nt
    __all__.extend(_get_exports_list(nt))
    del nt
    try:
        from nt import _have_functions
    except ImportError:
        pass

else:
    raise ImportError('no os specific module found')
sys.modules['os.path'] = path
from os.path import curdir, pardir, sep, pathsep, defpath, extsep, altsep, devnull
del _names
if _exists('_have_functions'):
    _globals = globals()

    def _add(str, fn):
        if fn in _globals:
            if str in _have_functions:
                _set.add(_globals[fn])


    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHMODAT', 'chmod')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_FUTIMESAT', 'utime')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_MKDIRAT', 'mkdir')
    _add('HAVE_MKFIFOAT', 'mkfifo')
    _add('HAVE_MKNODAT', 'mknod')
    _add('HAVE_OPENAT', 'open')
    _add('HAVE_READLINKAT', 'readlink')
    _add('HAVE_RENAMEAT', 'rename')
    _add('HAVE_SYMLINKAT', 'symlink')
    _add('HAVE_UNLINKAT', 'unlink')
    _add('HAVE_UNLINKAT', 'rmdir')
    _add('HAVE_UTIMENSAT', 'utime')
    supports_dir_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    supports_effective_ids = _set
    _set = set()
    _add('HAVE_FCHDIR', 'chdir')
    _add('HAVE_FCHMOD', 'chmod')
    _add('HAVE_FCHOWN', 'chown')
    _add('HAVE_FDOPENDIR', 'listdir')
    _add('HAVE_FEXECVE', 'execve')
    _set.add(stat)
    _add('HAVE_FTRUNCATE', 'truncate')
    _add('HAVE_FUTIMENS', 'utime')
    _add('HAVE_FUTIMES', 'utime')
    _add('HAVE_FPATHCONF', 'pathconf')
    if _exists('statvfs'):
        if _exists('fstatvfs'):
            _add('HAVE_FSTATVFS', 'statvfs')
    supports_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_LCHFLAGS', 'chflags')
    _add('HAVE_LCHMOD', 'chmod')
    if _exists('lchown'):
        _add('HAVE_LCHOWN', 'chown')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_LUTIMES', 'utime')
    _add('HAVE_LSTAT', 'stat')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_UTIMENSAT', 'utime')
    _add('MS_WINDOWS', 'stat')
    supports_follow_symlinks = _set
    del _set
    del _have_functions
    del _globals
    del _add
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def makedirs(name, mode=511, exist_ok=False):
    """makedirs(name [, mode=0o777][, exist_ok=False])

    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.

    """
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    if head:
        if tail:
            if not path.exists(head):
                try:
                    makedirs(head, mode, exist_ok)
                except FileExistsError:
                    pass

                cdir = curdir
                if isinstance(tail, bytes):
                    cdir = bytes(curdir, 'ASCII')
                if tail == cdir:
                    return
    try:
        mkdir(name, mode)
    except OSError:
        if not exist_ok or not path.isdir(name):
            raise


def removedirs(name):
    """removedirs(name)

    Super-rmdir; remove a leaf directory and all empty intermediate
    ones.  Works like rmdir except that, if the leaf directory is
    successfully removed, directories corresponding to rightmost path
    segments will be pruned away until either the whole path is
    consumed or an error occurs.  Errors during this latter phase are
    ignored -- they generally mean that a directory was not empty.

    """
    rmdir(name)
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    while head and tail:
        try:
            rmdir(head)
        except OSError:
            break

        head, tail = path.split(head)


def renames(old, new):
    """renames(old, new)

    Super-rename; create directories as necessary and delete any left
    empty.  Works like rename, except creation of any intermediate
    directories needed to make the new pathname good is attempted
    first.  After the rename, directories corresponding to rightmost
    path segments of the old name will be pruned until either the
    whole path is consumed or a nonempty directory is found.

    Note: this function can fail with the new directory structure made
    if you lack permissions needed to unlink the leaf directory or
    file.

    """
    head, tail = path.split(new)
    if head:
        if tail:
            if not path.exists(head):
                makedirs(head)
    rename(old, new)
    head, tail = path.split(old)
    if head:
        if tail:
            try:
                removedirs(head)
            except OSError:
                pass


__all__.extend(['makedirs', 'removedirs', 'renames'])

def walk(top, topdown=True, onerror=None, followlinks=False):
    """Directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 3-tuple

        dirpath, dirnames, filenames

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name).

    If optional arg 'topdown' is true or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top down).  If topdown is false, the triple
    for a directory is generated after the triples for all of its
    subdirectories (directories are generated bottom up).

    When topdown is true, the caller can modify the dirnames list in-place
    (e.g., via del or slice assignment), and walk will only recurse into the
    subdirectories whose names remain in dirnames; this can be used to prune the
    search, or to impose a specific order of visiting.  Modifying dirnames when
    topdown is false is ineffective, since the directories in dirnames have
    already been generated by the time dirnames itself is generated. No matter
    the value of topdown, the list of subdirectories is retrieved before the
    tuples for the directory and its subdirectories are generated.

    By default errors from the os.scandir() call are ignored.  If
    optional arg 'onerror' is specified, it should be a function; it
    will be called with one argument, an OSError instance.  It can
    report the error to continue with the walk, or raise the exception
    to abort the walk.  Note that the filename is available as the
    filename attribute of the exception object.

    By default, os.walk does not follow symbolic links to subdirectories on
    systems that support them.  In order to get this functionality, set the
    optional argument 'followlinks' to true.

    Caution:  if you pass a relative pathname for top, don't change the
    current working directory between resumptions of walk.  walk never
    changes the current directory, and assumes that the client doesn't
    either.

    Example:

    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/email'):
        print(root, "consumes", end="")
        print(sum([getsize(join(root, name)) for name in files]), end="")
        print("bytes in", len(files), "non-directory files")
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

    """
    top = fspath(top)
    dirs = []
    nondirs = []
    walk_dirs = []
    try:
        scandir_it = scandir(top)
    except OSError as error:
        if onerror is not None:
            onerror(error)
        return

    with scandir_it:
        while 1:
            try:
                try:
                    entry = next(scandir_it)
                except StopIteration:
                    break

            except OSError as error:
                if onerror is not None:
                    onerror(error)
                return

            try:
                is_dir = entry.is_dir()
            except OSError:
                is_dir = False

            if is_dir:
                dirs.append(entry.name)
            else:
                nondirs.append(entry.name)
            if not topdown:
                if is_dir:
                    if followlinks:
                        walk_into = True
                    else:
                        try:
                            is_symlink = entry.is_symlink()
                        except OSError:
                            is_symlink = False

                        walk_into = not is_symlink
                if walk_into:
                    walk_dirs.append(entry.path)

    if topdown:
        yield (
         top, dirs, nondirs)
        islink, join = path.islink, path.join
        for dirname in dirs:
            new_path = join(top, dirname)
            if followlinks or not islink(new_path):
                yield from walk(new_path, topdown, onerror, followlinks)

    else:
        for new_path in walk_dirs:
            yield from walk(new_path, topdown, onerror, followlinks)

        yield (top, dirs, nondirs)


__all__.append('walk')
if {
 open, stat} <= supports_dir_fd:
    if {listdir, stat} <= supports_fd:

        def fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None):
            """Directory tree generator.

        This behaves exactly like walk(), except that it yields a 4-tuple

            dirpath, dirnames, filenames, dirfd

        `dirpath`, `dirnames` and `filenames` are identical to walk() output,
        and `dirfd` is a file descriptor referring to the directory `dirpath`.

        The advantage of fwalk() over walk() is that it's safe against symlink
        races (when follow_symlinks is False).

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and top should be relative; top will then be relative to that directory.
          (dir_fd is always supported for fwalk.)

        Caution:
        Since fwalk() yields file descriptors, those are only valid until the
        next iteration step, so you should dup() them if you want to keep them
        for a longer period.

        Example:

        import os
        for root, dirs, files, rootfd in os.fwalk('python/Lib/email'):
            print(root, "consumes", end="")
            print(sum([os.stat(name, dir_fd=rootfd).st_size for name in files]),
                  end="")
            print("bytes in", len(files), "non-directory files")
            if 'CVS' in dirs:
                dirs.remove('CVS')  # don't visit CVS directories
        """
            if not isinstance(top, int) or not hasattr(top, '__index__'):
                top = fspath(top)
            orig_st = stat(top, follow_symlinks=False, dir_fd=dir_fd)
            topfd = open(top, O_RDONLY, dir_fd=dir_fd)
            try:
                if follow_symlinks or st.S_ISDIR(orig_st.st_mode) and path.samestat(orig_st, stat(topfd)):
                    yield from _fwalk(topfd, top, topdown, onerror, follow_symlinks)
            finally:
                close(topfd)

            if False:
                yield None


        def _fwalk(topfd, toppath, topdown, onerror, follow_symlinks):
            names = listdir(topfd)
            dirs, nondirs = [], []
            for name in names:
                try:
                    if st.S_ISDIR(stat(name, dir_fd=topfd).st_mode):
                        dirs.append(name)
                    else:
                        nondirs.append(name)
                except OSError:
                    try:
                        if st.S_ISLNK(stat(name, dir_fd=topfd, follow_symlinks=False).st_mode):
                            nondirs.append(name)
                    except OSError:
                        continue

            if topdown:
                yield (
                 toppath, dirs, nondirs, topfd)
            for name in dirs:
                try:
                    orig_st = stat(name, dir_fd=topfd, follow_symlinks=follow_symlinks)
                    dirfd = open(name, O_RDONLY, dir_fd=topfd)
                except OSError as err:
                    if onerror is not None:
                        onerror(err)
                    continue

                try:
                    if follow_symlinks or path.samestat(orig_st, stat(dirfd)):
                        dirpath = path.join(toppath, name)
                        yield from _fwalk(dirfd, dirpath, topdown, onerror, follow_symlinks)
                finally:
                    close(dirfd)

            if not topdown:
                yield (
                 toppath, dirs, nondirs, topfd)


        __all__.append('fwalk')
try:
    environ
except NameError:
    environ = {}

def execl(file, *args):
    """execl(file, *args)

    Execute the executable file with argument list args, replacing the
    current process. """
    execv(file, args)


def execle(file, *args):
    """execle(file, *args, env)

    Execute the executable file with argument list args and
    environment env, replacing the current process. """
    env = args[(-1)]
    execve(file, args[:-1], env)


def execlp(file, *args):
    """execlp(file, *args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process. """
    execvp(file, args)


def execlpe(file, *args):
    """execlpe(file, *args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env, replacing the current
    process. """
    env = args[(-1)]
    execvpe(file, args[:-1], env)


def execvp(file, args):
    """execvp(file, args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args)


def execvpe(file, args, env):
    """execvpe(file, args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env , replacing the
    current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args, env)


__all__.extend(['execl', 'execle', 'execlp', 'execlpe', 'execvp', 'execvpe'])

def _execvpe(file, args, env=None):
    if env is not None:
        exec_func = execve
        argrest = (args, env)
    else:
        exec_func = execv
        argrest = (args,)
        env = environ
    head, tail = path.split(file)
    if head:
        exec_func(file, *argrest)
        return
    last_exc = saved_exc = None
    saved_tb = None
    path_list = get_exec_path(env)
    if name != 'nt':
        file = fsencode(file)
        path_list = map(fsencode, path_list)
    for dir in path_list:
        fullname = path.join(dir, file)
        try:
            exec_func(fullname, *argrest)
        except OSError as e:
            last_exc = e
            tb = sys.exc_info()[2]
            if e.errno != errno.ENOENT:
                if e.errno != errno.ENOTDIR:
                    if saved_exc is None:
                        saved_exc = e
                        saved_tb = tb

    if saved_exc:
        raise saved_exc.with_traceback(saved_tb)
    raise last_exc.with_traceback(tb)


def get_exec_path(env=None):
    """Returns the sequence of directories that will be searched for the
    named executable (similar to a shell) when launching a process.

    *env* must be an environment variable dict or None.  If *env* is None,
    os.environ will be used.
    """
    import warnings
    if env is None:
        env = environ
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', BytesWarning)
        try:
            path_list = env.get('PATH')
        except TypeError:
            path_list = None

        if supports_bytes_environ:
            try:
                path_listb = env[b'PATH']
            except (KeyError, TypeError):
                pass
            else:
                if path_list is not None:
                    raise ValueError("env cannot contain 'PATH' and b'PATH' keys")
                path_list = path_listb
            if path_list is not None:
                if isinstance(path_list, bytes):
                    path_list = fsdecode(path_list)
    if path_list is None:
        path_list = defpath
    return path_list.split(pathsep)


from _collections_abc import MutableMapping

class _Environ(MutableMapping):

    def __init__(self, data, encodekey, decodekey, encodevalue, decodevalue, putenv, unsetenv):
        self.encodekey = encodekey
        self.decodekey = decodekey
        self.encodevalue = encodevalue
        self.decodevalue = decodevalue
        self.putenv = putenv
        self.unsetenv = unsetenv
        self._data = data

    def __getitem__(self, key):
        try:
            value = self._data[self.encodekey(key)]
        except KeyError:
            raise KeyError(key) from None

        return self.decodevalue(value)

    def __setitem__(self, key, value):
        key = self.encodekey(key)
        value = self.encodevalue(value)
        self.putenv(key, value)
        self._data[key] = value

    def __delitem__(self, key):
        encodedkey = self.encodekey(key)
        self.unsetenv(encodedkey)
        try:
            del self._data[encodedkey]
        except KeyError:
            raise KeyError(key) from None

    def __iter__(self):
        keys = list(self._data)
        for key in keys:
            yield self.decodekey(key)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return 'environ({{{}}})'.format(', '.join('{!r}: {!r}'.format(self.decodekey(key), self.decodevalue(value)) for key, value in self._data.items()))

    def copy(self):
        return dict(self)

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
        return self[key]


try:
    _putenv = putenv
except NameError:
    _putenv = lambda key, value: None
else:
    if 'putenv' not in __all__:
        __all__.append('putenv')
    try:
        _unsetenv = unsetenv
    except NameError:
        _unsetenv = lambda key: _putenv(key, '')
    else:
        if 'unsetenv' not in __all__:
            __all__.append('unsetenv')
        else:

            def _createenviron():
                if name == 'nt':

                    def check_str(value):
                        if not isinstance(value, str):
                            raise TypeError('str expected, not %s' % type(value).__name__)
                        return value

                    encode = check_str
                    decode = str

                    def encodekey(key):
                        return encode(key).upper()

                    data = {}
                    for key, value in environ.items():
                        data[encodekey(key)] = value

                else:
                    encoding = sys.getfilesystemencoding()

                    def encode(value):
                        if not isinstance(value, str):
                            raise TypeError('str expected, not %s' % type(value).__name__)
                        return value.encode(encoding, 'surrogateescape')

                    def decode(value):
                        return value.decode(encoding, 'surrogateescape')

                    encodekey = encode
                    data = environ
                return _Environ(data, encodekey, decode, encode, decode, _putenv, _unsetenv)


            environ = _createenviron()
            del _createenviron

            def getenv(key, default=None):
                """Get an environment variable, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    key, default and the result are str."""
                return environ.get(key, default)


            supports_bytes_environ = name != 'nt'
            __all__.extend(('getenv', 'supports_bytes_environ'))
            if supports_bytes_environ:

                def _check_bytes(value):
                    if not isinstance(value, bytes):
                        raise TypeError('bytes expected, not %s' % type(value).__name__)
                    return value


                environb = _Environ(environ._data, _check_bytes, bytes, _check_bytes, bytes, _putenv, _unsetenv)
                del _check_bytes

                def getenvb(key, default=None):
                    """Get an environment variable, return None if it doesn't exist.
        The optional second argument can specify an alternate default.
        key, default and the result are bytes."""
                    return environb.get(key, default)


                __all__.extend(('environb', 'getenvb'))

            def _fscodec():
                encoding = sys.getfilesystemencoding()
                errors = sys.getfilesystemencodeerrors()

                def fsencode(filename):
                    filename = fspath(filename)
                    if isinstance(filename, str):
                        return filename.encode(encoding, errors)
                    else:
                        return filename

                def fsdecode(filename):
                    filename = fspath(filename)
                    if isinstance(filename, bytes):
                        return filename.decode(encoding, errors)
                    else:
                        return filename

                return (fsencode, fsdecode)


            fsencode, fsdecode = _fscodec()
            del _fscodec
            if _exists('fork'):
                if not _exists('spawnv'):
                    if _exists('execv'):
                        P_WAIT = 0
                        P_NOWAIT = P_NOWAITO = 1
                        __all__.extend(['P_WAIT', 'P_NOWAIT', 'P_NOWAITO'])

                        def _spawnvef(mode, file, args, env, func):
                            if not isinstance(args, (tuple, list)):
                                raise TypeError('argv must be a tuple or a list')
                            if not args or not args[0]:
                                raise ValueError('argv first element cannot be empty')
                            pid = fork()
                            if not pid:
                                try:
                                    if env is None:
                                        func(file, args)
                                    else:
                                        func(file, args, env)
                                except:
                                    _exit(127)

                            else:
                                if mode == P_NOWAIT:
                                    return pid
                                while True:
                                    wpid, sts = waitpid(pid, 0)
                                    if WIFSTOPPED(sts):
                                        continue
                                    else:
                                        if WIFSIGNALED(sts):
                                            return -WTERMSIG(sts)
                                        if WIFEXITED(sts):
                                            return WEXITSTATUS(sts)
                                        raise OSError('Not stopped, signaled or exited???')


                        def spawnv(mode, file, args):
                            """spawnv(mode, file, args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                            return _spawnvef(mode, file, args, None, execv)


                        def spawnve(mode, file, args, env):
                            """spawnve(mode, file, args, env) -> integer

Execute file with arguments from args in a subprocess with the
specified environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                            return _spawnvef(mode, file, args, env, execve)


                        def spawnvp(mode, file, args):
                            """spawnvp(mode, file, args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                            return _spawnvef(mode, file, args, None, execvp)


                        def spawnvpe(mode, file, args, env):
                            """spawnvpe(mode, file, args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                            return _spawnvef(mode, file, args, env, execvpe)


                        __all__.extend(['spawnv', 'spawnve', 'spawnvp', 'spawnvpe'])
            if _exists('spawnv'):

                def spawnl(mode, file, *args):
                    """spawnl(mode, file, *args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    return spawnv(mode, file, args)


                def spawnle(mode, file, *args):
                    """spawnle(mode, file, *args, env) -> integer

Execute file with arguments from args in a subprocess with the
supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    env = args[(-1)]
                    return spawnve(mode, file, args[:-1], env)


                __all__.extend(['spawnl', 'spawnle'])
            if _exists('spawnvp'):

                def spawnlp(mode, file, *args):
                    """spawnlp(mode, file, *args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    return spawnvp(mode, file, args)


                def spawnlpe(mode, file, *args):
                    """spawnlpe(mode, file, *args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
                    env = args[(-1)]
                    return spawnvpe(mode, file, args[:-1], env)


                __all__.extend(['spawnlp', 'spawnlpe'])

            def popen(cmd, mode='r', buffering=-1):
                if not isinstance(cmd, str):
                    raise TypeError('invalid cmd type (%s, expected string)' % type(cmd))
                else:
                    if mode not in ('r', 'w'):
                        raise ValueError('invalid mode %r' % mode)
                    if buffering == 0 or buffering is None:
                        raise ValueError('popen() does not support unbuffered streams')
                import subprocess, io
                if mode == 'r':
                    proc = subprocess.Popen(cmd, shell=True,
                      stdout=(subprocess.PIPE),
                      bufsize=buffering)
                    return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
                else:
                    proc = subprocess.Popen(cmd, shell=True,
                      stdin=(subprocess.PIPE),
                      bufsize=buffering)
                    return _wrap_close(io.TextIOWrapper(proc.stdin), proc)


            class _wrap_close:

                def __init__(self, stream, proc):
                    self._stream = stream
                    self._proc = proc

                def close(self):
                    self._stream.close()
                    returncode = self._proc.wait()
                    if returncode == 0:
                        return
                    else:
                        if name == 'nt':
                            return returncode
                        return returncode << 8

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    self.close()

                def __getattr__(self, name):
                    return getattr(self._stream, name)

                def __iter__(self):
                    return iter(self._stream)


            def fdopen(fd, *args, **kwargs):
                if not isinstance(fd, int):
                    raise TypeError('invalid fd type (%s, expected integer)' % type(fd))
                import io
                return (io.open)(fd, *args, **kwargs)


            def _fspath(path):
                """Return the path representation of a path-like object.

    If str or bytes is passed in, it is returned unchanged. Otherwise the
    os.PathLike interface is used to get the path representation. If the
    path representation is not str or bytes, TypeError is raised. If the
    provided path is not str, bytes, or os.PathLike, TypeError is raised.
    """
                if isinstance(path, (str, bytes)):
                    return path
                path_type = type(path)
                try:
                    path_repr = path_type.__fspath__(path)
                except AttributeError:
                    if hasattr(path_type, '__fspath__'):
                        raise
                    else:
                        raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__)

                if isinstance(path_repr, (str, bytes)):
                    return path_repr
                raise TypeError('expected {}.__fspath__() to return str or bytes, not {}'.format(path_type.__name__, type(path_repr).__name__))


            fspath = _exists('fspath') or _fspath
            fspath.__name__ = 'fspath'

        class PathLike(abc.ABC):
            __doc__ = 'Abstract base class for implementing the file system path protocol.'

            @abc.abstractmethod
            def __fspath__(self):
                """Return the file system path representation of the object."""
                raise NotImplementedError

            @classmethod
            def __subclasshook__(cls, subclass):
                return hasattr(subclass, '__fspath__')