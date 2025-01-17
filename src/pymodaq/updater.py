import argparse
import subprocess
import sys
import time

from pymodaq_utils.logger import set_logger, get_module_name

logger = set_logger(get_module_name(__file__))

def wait_for_parent():
	'''
		A function to wait for its parent to terminate execution.

		In order to achieve that, this process has to be started with
		stdin replaced by a piped stream from its parent. When the
		parent terminates, stdin will close and either return from read
		or throw an exception. De facto creating a way to wait for its
		parent's termination.

		It then sleep for 2 seconds, to let the parent process complete
		termination.

		CAUTION: If the process was not started by piping stdin AND 
		the --wait option is set, this function will hang forever.

		We could use `psutil` or a similar lib to check for parent's process
		existance with its pid. 
	'''

	logger.info("Waiting for parent process to stop.")
	try:
		sys.stdin.read()
	except:
		pass
	logger.debug("Parent process closed stdin")
	time.sleep(2)
	logger.info("Parent process stopped.")

def process_args():
	'''
		Declare arguments for updater.py, parse them and returns them in an object.
		The arguments are:
			--file <file> to request a python program to (re)start after update if needed (optional) 
			--wait        to wait for the starting process to terminate before updating (optional, defaults to False)
			packages      the package list to install/update (they should contain the version in a pip accepted format)
	'''
	parser = argparse.ArgumentParser(description='Update pymodaq using pip.')
	parser.add_argument('--file', type=str,  help='the pymodaq script to restart after update')
	parser.add_argument("--wait", action="store_true", help="enable waiting for pymodaq to finish mode (default is disabled).")
	parser.add_argument('packages', type=str, nargs='+', help='package list')
	return parser.parse_args()

def main():
	args = process_args()
	logger.info(f"Arguments processed: {args}")

	if args.wait:
		wait_for_parent()

	logger.info(f'Updating packages: {', '.join(args.packages)}')
	
	ret_code = 0
	# with subprocess.Popen([sys.executable, '-m', 'pip', 'install'] + args.packages, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as pip:
	# 	for line in pip.stdout:
	# 		logger.info(line[:-1].decode('utf-8'))
	# ret_code = pip.wait()
	

	if ret_code == 0:
		logger.info(f'Succesfully updated {', '.join(args.packages)}')
	else:
		logger.error(f'Error while updating {', '.join(args.packages)}, pip returned {ret_code}')

	if args.file is not None:
		logger.info(f"Restarting {args.file} script after update.")
		subprocess.Popen([sys.executable, args.file])


if __name__ == "__main__":
	main()