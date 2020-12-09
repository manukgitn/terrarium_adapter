"""Main module."""

import sys
import os
import subprocess
import shutil    

original_open = subprocess.Popen

def  our_popen(scmd):
    print('Fake!!!')
    pass


class TerraPopen(subprocess.Popen):
    """ Execute a child program in a new process.

    For a complete description of the arguments see the Python documentation.

    Arguments:
      args: A string, or a sequence of program arguments.

      bufsize: supplied as the buffering argument to the open() function when
          creating the stdin/stdout/stderr pipe file objects

      executable: A replacement program to execute.

      stdin, stdout and stderr: These specify the executed programs' standard
          input, standard output and standard error file handles, respectively.

      preexec_fn: (POSIX only) An object to be called in the child process
          just before the child is executed.

      close_fds: Controls closing or inheriting of file descriptors.

      shell: If true, the command will be executed through the shell.

      cwd: Sets the current directory before the child is executed.

      env: Defines the environment variables for the new process.

      text: If true, decode stdin, stdout and stderr using the given encoding
          (if set) or the system default otherwise.

      universal_newlines: Alias of text, provided for backwards compatibility.

      startupinfo and creationflags (Windows only)

      restore_signals (POSIX only)

      start_new_session (POSIX only)

      pass_fds (POSIX only)

      encoding and errors: Text mode encoding and error handling to use for
          file objects stdin, stdout and stderr.

    Attributes:
        stdin, stdout, stderr, pid, returncode
    """
    _child_created = False  # Set here since __del__ checks it

    def __init__(self, args, **kwargs):
        args_ = list(args)
        # print("+"*10, args_)

        root_dir = None
        if 'ebin' in sys.executable:
            root_dir = sys.executable.split('ebin')[0]

        if 'ebin' in sys.argv[0]:
            root_dir = sys.argv[0].split('ebin')[0]

        if root_dir:
            ldso = os.path.join(root_dir, 'pbin', 'ld.so')
            utterms_ = os.path.split(args[0])
            # print(utterms_)
            utname = utterms_[-1]
            pbin_path = os.path.join(root_dir, 'pbin', utname)
            os.environ['LD_PRELOAD'] = ''
            if os.path.exists(pbin_path):
                args_[0] = pbin_path
            else:
                # Here we should 
                if utterms_[0] == '':
                    args_[0] = shutil.which(utname)
                for p_ in ['/lib64/ld-linux-x86-64.so.2']:
                    if os.path.exists(p_):
                        ldso = p_     
                        break

                for p_ in ['/lib/x86_64-linux-gnu/libc.so.6']:
                    if os.path.exists(p_):
                        os.environ['LD_PRELOAD']=p_
                        break
                # print('*****')
            args_.insert(0, ldso)    

        # print("!"*10, args_)
        super().__init__(args_, **kwargs)
        pass


subprocess.Popen=TerraPopen