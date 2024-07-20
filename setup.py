import paramiko
from scp import SCPClient
import os, sys


if __name__ == '__main__':
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('localhost', username='cs246')
    scpclient = SCPClient(client.get_transport())

    # get the submission folder directory of the student specified by watiam
    # scp the folder to the current directory, as a subdirectory, named 'submission'
    scpclient.get('~/handin/a4/graphics_tests', 'graphics_tests', recursive=True)

    # cd to the graphics_tests directory
    os.chdir('graphics_tests')

    NUM_TEST = 7
    for i in range(1, NUM_TEST + 1):
        # cat testX/input.txt - | ./canonical_exec
        os.system(f'cat test{i}/input.txt - | ./canonical_exec')

    # cd into the submission directory
    os.chdir('submission')
    # run make to compile the code
    os.system('make')

    scpclient.close()
    client.close()