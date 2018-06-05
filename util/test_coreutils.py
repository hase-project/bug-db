import sys
import os
import os.path
import subprocess

bin_dir	= "../bin"
tests_dir = "../tests"
hase_dir = "/home/lrxiao/hase/bin"
base_dir = os.getcwd()
targets = ['base64', 
	'basename', 'cat', 'cp', 'cut', 
	'date', 'dd', 'df', 'dirname', 
	'du', 'echo', 'env', 'expand', 
	'expr', 'factor', 'fmt', 'fold', 
	'getlimits', 'groups', 'head', 'hostid', 
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


def do_test(target):
	if target not in targets:
		print("Target testcase incomplete")
		return
	with open(os.path.join(tests_dir, "{}.test".format(target))) as f:
		cmds = [
				'sudo',
				os.path.join(hase_dir, 'hase'),
				'record',
				os.path.join(bin_dir, target),
			]
		stdin = subprocess.PIPE
		# FIXME: Lack of a valid testcase
		omit = False
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
			subprocess.check_call(
				cmds, stdin=stdin
			)
		else:
			print("Target testcase incomplete")

if __name__ == "__main__":
	do_test(sys.argv[1])
