import os
import sys
import math
import hashlib
import time


AVAILABLE_ALGOS = hashlib.algorithms_guaranteed


class Join:

    @staticmethod
    def join(**kwargs):
        start_time = time.time()
        if 'filename' in kwargs.keys():
            filename = kwargs['filename']
        else:
            raise Exception('Invalid filename!')

        if 'parts' not in kwargs.keys():
            raise Exception('Number of parts is mandatory!')

        if 'filelocation' in kwargs.keys():
            filedir = kwargs['filelocation']
        else:
            filedir = os.getcwd()

        filepath = os.path.join(filedir, filename)
        parts = kwargs['parts']
        plen = len(str(parts))
        blocksize = 1024 * 1024
        fdesthash = hashlib.new(kwargs['algo'])

        if os.path.isfile(filepath):
            fext = os.path.splitext(filename)[1]
            if (fext[1:3] == "pt" and fext[-1*plen:] == str(1).zfill(plen)):
                fdname = os.path.splitext(filename)[0]
                with open(fdname, "wb") as fdest:
                    i = 1
                    while (i <= parts):
                        filepath = fdname + ".pt" + str(i).zfill(plen)
                        sys.stdout.write(f'Processing file: {filepath}\n')
                        fs = open(filepath, 'rb')

                        filesize = os.stat(filepath).st_size
                        times = int(math.ceil(filesize / blocksize))

                        j = 1
                        while (j <= times):
                            data_chunk = fs.read(blocksize)
                            fdest.write(data_chunk)
                            fdesthash.update(data_chunk)
                            j += 1

                        fs.close()
                        i += 1

                fhash = ""
                if os.path.exists('hash.txt'):
                    with open('hash.txt', 'r') as f:
                        lines = f.read().splitlines()
                        fhash = lines[-1].split(':')[1][1:]

                    if (fhash == fdesthash.hexdigest()):
                        time_taken = time.time() - start_time
                        sys.stdout.write(
                            f'Joint success! Time taken: {time_taken:.2f} s.\n'
                        )
                    else:
                        sys.stdout.write(
                            f'Hash mismatch! Joint operation failed!\n'
                        )
                else:
                    sys.stdout.write(
                        f'hash.txt not found! Final file hashes unverified!\n'
                    )

            else:
                sys.stdout.write(f'Invalid starting filename!\n')

        else:
            sys.stdout.write(f'Not a valid file: {filepath}')
