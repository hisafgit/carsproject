import logging


logging.basicConfig(filename='downloader.log',
                    filemode='a',
                    format='%(asctime)s, [%(filename)s:%(lineno)s - %(funcName)s()] --- %(levelname)s --- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# format='%(asctime)s, [%(filename)s:%(lineno)s - %(funcName)s()] %(name)s -- %(levelname)s -- %(message)s'