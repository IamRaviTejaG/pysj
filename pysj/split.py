import os
import sys
import math
import hashlib
import time


AVAILABLE_ALGOS = hashlib.algorithms_guaranteed


class Split:

    @staticmethod
    def split(**kwargs):
        start_time = time.time()
        if 'filename' in kwargs.keys():
            filename = kwargs['filename']
        else:
            raise Exception('Invalid filename!')

        if 'filelocation' in kwargs.keys():
            filedir = kwargs['filelocation']
        else:
            filedir = os.getcwd()

        filepath = os.path.join(filedir, filename)

        if os.path.isfile(filepath):
            partsizeMB = kwargs['partsize']
            partsize = int(math.ceil(partsizeMB)) * 1024 * 1024  # in bytes
            blocksize = 1024 * 1024  # 1 MegaByte
            filesize = os.stat(filepath).st_size  # Gets filesize
            filesizeMB = filesize // 1048576
            fsizeMod = filesizeMB % partsizeMB

            if (partsizeMB < 1):
                raise Exception("Minimum split size is 1 MB!")

            pieces = int(math.ceil(filesize / partsize))
            times = int(math.ceil(partsize / blocksize))
            algo = 'sha256'  # Default file hashing uses sha256

            if ('algo' in kwargs.keys()):
                if (kwargs['algo'].lower() in AVAILABLE_ALGOS):
                    algo = kwargs['algo']
                else:
                    raise Exception('Invalid Algorithm!')

            sys.stdout.write(
                f'{filesizeMB} MB => {pieces-1}*{partsizeMB} + {fsizeMod} MB'
            )
            sys.stdout.write(f'\n')

            with open(filepath, 'rb') as f:
                hashtxt = open('hash.txt', 'w')
                filehash = hashlib.new(algo)
                i = 1
                while (i <= pieces):
                    hashify = hashlib.new(algo)
                    ext = str(i).zfill(len(str(pieces)))
                    partfilename = filename + ".pt" + ext
                    fw = open(partfilename, "wb")
                    # Progress bar placeholder!
                    sys.stdout.write(f'Creating part {i}: [')
                    sys.stdout.write(f'{" " * 50}')
                    sys.stdout.write('\b' * 50)
                    # Progress bar placeholder!
                    j = 1
                    while (j <= times):
                        a = (j/times) * 100  # For progress bar!
                        data_chunk = f.read(blocksize)
                        fw.write(data_chunk)
                        hashify.update(data_chunk)
                        filehash.update(data_chunk)
                        # Progress bar printing!
                        if (a % 2 == 0):
                            sys.stdout.write('=')
                            sys.stdout.flush()
                        # Progress bar printing!
                        j += 1
                    sys.stdout.write(']\n')
                    hasht = partfilename + ': ' + hashify.hexdigest() + '\n'
                    hashtxt.write(hasht)
                    fw.close()
                    i += 1
                hashtxt.write(f'{filename}: {filehash.hexdigest()}\n')
                hashtxt.close()

            time_taken = time.time() - start_time
            sys.stdout.write(
                f'Split successful! Time taken: {time_taken:.2f} s.\n'
            )
            sys.stdout.write(f'{algo} hashes stored in file \'hash.txt\'.\n')
            # sys.stdout.write(f'Total time taken: ')

        else:
            sys.stdout.write(f'Not a valid file: {filepath}')
