import os
import logging

# '%(asctime)s |%(levelname)s| |[%(filename)s:%(lineno)d][%(funcName)s]| %(message)s'
# '%(asctime)s |%(levelname)s| %(message)s'

#
# def basic(file: str):
#     abspath = os.path.abspath(file)
#     dirname = os.path.dirname(abspath)
#     os.makedirs(dirname, exist_ok=True)
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s |%(levelname)s| %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S',
#                         filename=abspath,
#                         filemode='w')
#     logging.info(f'file     : {file}')
#     logging.info(f'abspath  : {abspath}')
#     logging.info(f'dirname  : {dirname}')


def basic(
    file: str = './log.log',
    level: int = logging.INFO,
    format: str = '%(asctime)s |%(levelname)s| |[%(filename)s:%(lineno)d][%(funcName)s]| %(message)s',
    datefmt: str = '%Y-%m-%d %H:%M:%S',
    filemode: str = 'w'
) -> None:
    """
    This function calls the logging.basicConfig() method and
    creates directories according to the file path.
    If you accept these default parameter settings,
    you can use this method to quickly set them up.

    Args:
    - file: Relative or absolute path of the file.
    - level: Same as the level parameter in basicConfig.
    - format: Same as the format parameter in basicConfig.
    - datefmt: Same as the datefmt parameter in basicConfig.
    - filemode: Same as the filemode parameter in basicConfig.
    """
    abspath = os.path.abspath(file)
    dirname = os.path.dirname(abspath)
    os.makedirs(dirname, exist_ok=True)
    logging.basicConfig(level=level, format=format, datefmt=datefmt, filename=abspath, filemode=filemode)
    logging.info(f'file    : {file}')
    logging.info(f'abspath : {abspath}')
    logging.info(f'dirname : {dirname}')
