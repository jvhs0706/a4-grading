import paramiko
from scp import SCPClient
import os, sys


if __name__ == '__main__':
    watiam = sys.argv[1]
    if not watiam:
        print('Please provide a valid watiam')
        sys.exit(1)

    if os.path.isdir('submission'):
        os.system('rm -rf submission')
    elif os.path.isfile('submission'):
        os.system('rm submission')

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('localhost', username='cs246')
    scpclient = SCPClient(client.get_transport())

    # get the submission folder directory of the student specified by watiam
    # scp the folder to the current directory, as a subdirectory, named 'submission'
    scpclient.get(os.path.join('~/handin/a4/a4q3b', watiam), 'submission', recursive=True)

    # cd into the submission directory
    os.chdir('submission')
    # run make to compile the code
    os.system('make')

    NUM_TEST = 7
    for i in range(1, NUM_TEST + 1):
        # cat testX/input.txt - | ./canonical_exec
        os.system(f'cat ../graphics_tests/test{i}/input.txt - | ./a4q3')

    scpclient.close()
    client.close()