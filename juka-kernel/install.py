import argparse
import json
import os
import sys
from io import BytesIO
from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {
    "argv": [sys.executable, "-m", "juka-kernel", "-f", "{connection_file}"],
    "display_name": "Juka",
    "language": "text",
}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        # TODO: Copy any resources

        print("Checking path for Juka...")
        if which("Juka"):
            print("Juka is installed...")
        else:
            print("Juka is not installed...")
            print("Installing Juka....")
            import urllib.request
            with urllib.request.urlopen('https://api.github.com/repos/JukaLang/juka/releases/latest') as f:
                html = f.read().decode('utf-8')
            tag = json.loads(html)['tag_name']
            import platform
            system = platform.system()
            from zipfile import ZipFile
            if system == "Windows":
                print("Downloading Windows version of Juka...")
                file = urllib.request.urlopen("https://github.com/jukaLang/Juka/releases/download/"+tag+"/Juka_WindowsX64_"+tag+".zip")
                zipfile = ZipFile(BytesIO(file.read()))
                zipfile.extractall()
                sys.path.append(os.getcwd())
                #os.system('setx path "%PATH%";'+os.getcwd()+'') -- NOT SAFE
            elif system == "Darwin":
                print("Downloading Macintosh version of Juka...")
                file = urllib.request.urlopen("https://github.com/jukaLang/Juka/releases/download/"+tag+"/Juka_MacOS_"+tag+".zip")
                zipfile = ZipFile(BytesIO(file.read()))
                zipfile.extractall()
                sys.path.append(os.getcwd())
            elif system == "Unix":
                import tarfile
                print("Downloading Unix version of Juka...")
                file = urllib.request.urlopen("https://github.com/jukaLang/Juka/releases/download/"+tag+"/Juka_FreeBSD_"+tag+".tar.gz")
                thetarfile = tarfile.open(fileobj=file, mode="r|gz")
                thetarfile.extractall()
                sys.path.append(os.getcwd())
            else:
                print("Downloading Linux version of Juka...")
                file = urllib.request.urlopen("https://github.com/jukaLang/Juka/releases/download/"+tag+"/Juka_Linux_"+tag+".zip")
                zipfile = ZipFile(BytesIO(file.read()))
                zipfile.extractall()
                sys.path.append(os.getcwd())


        print('Installing Jupyter kernel spec')
        KernelSpecManager().install_kernel_spec(td, 'juka', user=user, prefix=prefix)


def which(program):
    path_ext = [""]
    ext_list = None

    if sys.platform == "win32":
        ext_list = [ext.lower() for ext in os.environ["PATHEXT"].split(";")]

    def is_exe(fpath):
        exe = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        # search for executable under windows
        if not exe:
            if ext_list:
                for ext in ext_list:
                    exe_path = "%s%s" % (fpath,ext)
                    if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
                        path_ext[0] = ext
                        return True
                return False
        return exe

    fpath, fname = os.path.split(program)

    if fpath:
        if is_exe(program):
            return "%s%s" % (program, path_ext[0])
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return "%s%s" % (exe_file, path_ext[0])
    return None

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', action='store_true',
        help="Install to the per-user kernels registry. Default if not root.")
    ap.add_argument('--sys-prefix', action='store_true',
        help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    ap.add_argument('--prefix',
        help="Install to the given prefix. "
             "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    install_my_kernel_spec(user=args.user, prefix=args.prefix)

if __name__ == '__main__':
    main()
