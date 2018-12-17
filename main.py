from splitjoin.split import Split
from splitjoin.join import Join

Split.split(
    filename='audio.flac',
    partsize=2,
    algo='md5'
)

Join.join(
    filename='audio.flac.pt01',
    parts=48,
    algo='md5'
)
