from splitjoin.split import Split
from splitjoin.join import Join
import click


@click.command()
@click.argument('arg', required=True)
@click.argument('filename', type=click.Path(exists=True))
@click.argument('part', nargs=1, type=int)
@click.option('--algo', '-a', nargs=1, type=str, required=False,
              default='sha256', help='Change the file hashing algorithm')
def sj(arg, filename, part, algo):

    """
    arg: SPLIT / JOIN.

    filename: <filename>.
    
    part: Split size (in MB) / Number of parts (if JOIN).
    """


    if (arg.lower() == 'split'):
        Split.split(filename=filename, partsize=part, algo=algo)
    elif (arg.lower() == 'join'):
        Join.join(filename=filename, parts=part, algo=algo)
    else:
        click.echo('Error in argument!')


if __name__ == '__main__':
    sj()
