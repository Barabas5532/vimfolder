#based on https://github.com/JDevlieghere/dotfiles
import os
import os.path
import fnmatch
import logging
import ycm_core
import re

compilation_db_path = None
compilation_db_dir  = None

C_BASE_FLAGS = [
        '-Wall',
        '-Wextra',
        '-Werror',
        '-Wno-long-long',
        '-Wno-variadic-macros',
        '-fexceptions',
        '-ferror-limit=10000',
        '-DNDEBUG',
        '-std=c11',
        ]

CPP_BASE_FLAGS = [
        '-Wall',
        '-Wextra',
        '-Wno-long-long',
        '-Wno-variadic-macros',
        '-fexceptions',
        '-ferror-limit=10000',
        '-DNDEBUG',
        '-std=c++1z',
        '-xc++',
        '-I/usr/lib/',
        '-I/usr/include/'
        ]

C_SOURCE_EXTENSIONS = [
        '.c'
        ]

CPP_SOURCE_EXTENSIONS = [
        '.cpp',
        '.cxx',
        '.cc',
        '.m',
        '.mm'
        ]

SOURCE_DIRECTORIES = [
        'src',
        'lib'
        ]

HEADER_EXTENSIONS = [
        '.h',
        '.hxx',
        '.hpp',
        '.hh'
        ]

HEADER_DIRECTORIES = [
        'include'
        ]

BUILD_DIRECTORY = 'build';

def IsSourceFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in C_SOURCE_EXTENSIONS + CPP_SOURCE_EXTENSIONS

def IsHeaderFile(filename):
    extension = os.path.splitext(filename)[1]
    return extension in HEADER_EXTENSIONS

def GetCompilationInfoForFile(database, filename):
    if IsHeaderFile(filename):
        basename = os.path.splitext(filename)[0]
        for extension in C_SOURCE_EXTENSIONS + CPP_SOURCE_EXTENSIONS:
            # Get info from the source files by replacing the extension.
            replacement_file = basename + extension
            if os.path.exists(replacement_file):
                compilation_info = database.GetCompilationInfoForFile(replacement_file)
                if compilation_info.compiler_flags_:
                    return compilation_info
            # If that wasn't successful, try replacing possible header directory with possible source directories.
            for header_dir in HEADER_DIRECTORIES:
                for source_dir in SOURCE_DIRECTORIES:
                    src_file = replacement_file.replace(header_dir, source_dir)
                    if os.path.exists(src_file):
                        compilation_info = database.GetCompilationInfoForFile(src_file)
                        if compilation_info.compiler_flags_:
                            return compilation_info
        return None
    return database.GetCompilationInfoForFile(filename)

def FindNearest(path, target, build_folder=None):
    candidate = os.path.join(path, target)
    if(os.path.isfile(candidate) or os.path.isdir(candidate)):
        logging.info("Found nearest " + target + " at " + candidate)
        return candidate;

    parent = os.path.dirname(os.path.abspath(path));
    if(parent == path):
        raise RuntimeError("Could not find " + target);

    if(build_folder):
        candidate = os.path.join(parent, build_folder, target)
        if(os.path.isfile(candidate) or os.path.isdir(candidate)):
            logging.info("Found nearest " + target + " in build folder at " + candidate)
            return candidate;

    return FindNearest(parent, target, build_folder)

def MakeRelativePathsInFlagsAbsolute(flags, working_directory):
    if not working_directory:
        return list(flags)
    new_flags = []
    make_next_absolute = False
    path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
    for flag in flags:
        new_flag = flag

        if make_next_absolute:
            make_next_absolute = False
            if not flag.startswith('/'):
                new_flag = os.path.join(working_directory, flag)

        for path_flag in path_flags:
            if flag == path_flag:
                make_next_absolute = True
                break

            if flag.startswith(path_flag):
                path = flag[ len(path_flag): ]
                new_flag = path_flag + os.path.join(working_directory, path)
                break

        if new_flag:
            new_flags.append(new_flag)
    return new_flags


def CleanUpFlags(flags):
    """
    Removes anything that might create false errors.

    These include gcc specific options, and embedded standard libraries.
    """

    logging.debug(f"cleaning up: {flags}")

    flags_to_remove = ["-mlongcalls", "-fstrict-volatile-bitfields"]
    for flag in flags_to_remove:
        if flag in flags:
            flags.remove(flag)

    # prevent false errors from assert
    flags.append("-DNDEBUG")

    # ESP_IDF use GCC extension for variadic macro in ESP_LOGI
    flags.append("-Wno-gnu-zero-variadic-macro-arguments")

    # False positives. GCC actually accepts NULL as a nullptr
    flags.append("-Wno-zero-as-null-pointer-constant")

    logging.debug(f"cleaned up: {flags}")
    return flags


def FlagsForClangComplete(root):
    try:
        clang_complete_path = FindNearest(root, '.clang_complete')
        clang_complete_flags = open(clang_complete_path, 'r').read().splitlines()
        return clang_complete_flags
    except:
        return None

def FlagsForInclude(root):
    try:
        include_path = FindNearest(root, 'include')
        flags = []
        for dirroot, dirnames, filenames in os.walk(include_path):
            for dir_path in dirnames:
                real_path = os.path.join(dirroot, dir_path)
                flags = flags + ["-I" + real_path]
        return flags
    except:
        return None

def FlagsForCompilationDatabase(root, filename):
    logging.info(f"root: {root}, filename: {filename}")
    try:
        # always use the first compilation database
        # The build info for all of the esp-idf components is contained in the
        # project's compilation database. If we open a project file first, and
        # keep using the first db, then all the info for any esp-idf files is
        # going to be present.
        global compilation_db_path
        global compilation_db_dir
        if(not compilation_db_path or not compilation_db_dir):
            compilation_db_path = FindNearest(root, 'compile_commands.json', BUILD_DIRECTORY)
            compilation_db_dir = os.path.dirname(compilation_db_path)
            logging.info("Set compilation database directory to " + compilation_db_dir)
        else:
            logging.info("Using exisiting compilation database at " + compilation_db_dir)

        compilation_db =  ycm_core.CompilationDatabase(compilation_db_dir)
        if not compilation_db:
            logging.info("Compilation database file found but unable to load")
            return None
        compilation_info = GetCompilationInfoForFile(compilation_db, filename)
        if not compilation_info:
            logging.info("No compilation info for " + filename + " in compilation database")
            return None
        return CleanUpFlags(MakeRelativePathsInFlagsAbsolute(
                compilation_info.compiler_flags_,
                compilation_info.compiler_working_dir_))
    except Exception as e:
        logging.error(f"FlagsForCompilationDatabase raised exception: {e}")
        return None

def Settings(filename, **kwargs):
    final_flags = ""
    root = os.path.realpath(filename);
    compilation_db_flags = FlagsForCompilationDatabase(root, filename)
    if compilation_db_flags:
        logging.info("returning flags from compilation db")
        final_flags = compilation_db_flags
    else:
        if IsSourceFile(filename):
            extension = os.path.splitext(filename)[1]
            if extension in C_SOURCE_EXTENSIONS:
                logging.info("returning flags for c files")
                final_flags = C_BASE_FLAGS
            else:
                logging.info("returning flags for c++ files")
                final_flags = CPP_BASE_FLAGS

        clang_flags = FlagsForClangComplete(root)
        if clang_flags:
            logging.info("adding clang flags")
            final_flags = final_flags + clang_flags
        include_flags = FlagsForInclude(root)
        if include_flags:
            logging.info("adding include flags")
            final_flags = final_flags + include_flags
    return {
            'flags': final_flags,
            'do_cache': True
            }
