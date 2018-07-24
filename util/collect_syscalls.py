import sys
import os
import os.path
import subprocess
import xlwt

bin_dir	= "../bin"
tests_dir = "../tests"
hase_dir = "/home/lrxiao/hase/bin"
base_dir = os.getcwd()
targets = ['base64', 
	'basename', 'cat', 'cp', 'cut', 
	'date', 'dd', 'df', 'dirname', 
	'du', 'echo', 'env', 'expand', 
	'expr', 'factor', 'fmt', 'fold', 
	'groups', 'head', 'hostid', 
	'id', 'join', 'kill', 
	'link', 'ln', 'logname', 'ls', 
	'md5sum', 'mkdir', 'mkfifo', 'mktemp', 
	'mv', 'nice', 'nl', 'nproc', 'numfmt', 
	'od', 'paste', 'pathchk', 'pinky', 
	'pr', 'printenv', 'printf', 'ptx', 
	'pwd', 'readlink', 'realpath', 'rm', 
	'rmdir', 'runcon', 'seq', 'shred', 
	'shuf', 'sleep', 'sort', 'split', 
	'stat', 'stdbuf', 'stty', 'sum', 
	'sync', 'tac', 'tail', 'tee', 
	'touch', 'tr', 'true', 'truncate', 
	'tsort', 'tty', 'uname', 'unexpand', 
	'uniq', 'unlink', 'uptime', 'users', 
	'wc', 'who', 'whoami', 'yes']


def parse_call(proc):
    func = set()
    for l in proc.stderr:
        if not l.startswith('+++'):
            fn = l.partition('(')[0]
            if fn[0].isalpha() or fn[0] == '_':
                func.add(fn)
    return func


def collect_call(target, syscall=True):
    if target not in targets:
        print("Target testcase incomplete")
        return
    if syscall:
        trace = 'strace'
    else:
        trace = 'ltrace'
    with open(os.path.join(tests_dir, "{}.test".format(target))) as f:
        cmds = ['sudo', trace, target]
        omit = False
        stdin = subprocess.PIPE
        for l in f:
            l = l.replace('$(pwd)', os.path.join(base_dir, tests_dir))
            if l.startswith('pass'):
                omit = True
            if l.startswith('stdin:'):
                stdin = open(l.split(':')[1].strip())
            if l.startswith('cmdargs:'):
                cmdargs = l.split(':')[1].strip()
                if cmdargs != '':
                    cmds.append('--')
                    cmds += cmdargs.split(' ')
        if not omit:
            print("Executing: {}".format(' '.join(cmds)))
            p = subprocess.Popen(
                cmds,
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return parse_call(p)
        else:
            print("Target testcase incomplete")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        targets = [sys.argv[1]]
    all_sys = set()
    all_lib = set()
    for t in targets:
        sys = collect_call(t, True)
        lib = collect_call(t, False)
        if sys:
            all_sys |= sys
        if lib:
            all_lib |= lib
    print(all_sys)
    print(all_lib)
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('syscalls')
    sheet2 = book.add_sheet('libraries')
    for i, f in enumerate(all_sys):
        sheet1.write(i / 5 * 2, i % 5, f)
    for i, f in enumerate(all_lib):
        sheet2.write(i / 5 * 2, i % 5, f)
    book.save('result.xls')
