from os import path, system, startfile
from get_config import Config
import logging


class Main(object):

    def __init__(self):
        self.closeapplist = []
        self.openapplist = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='CloseAppLog.log',
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            encoding='utf-8')
        self.logger.setLevel(logging.DEBUG)

    def check_config(self):
        self.logger.info('Checking config file……')
        if not path.exists('config.txt'):
            self.logger.info(
                'Config file not found！ Creating new config file……')
            with open('config.txt', 'w') as f:
                self.logger.info('Config file created successfully！')
                pass
            return False
        else:
            self.logger.info('Config file found! Phasing in config file')
            return True

    def get_config(self):
        self.logger.info('Phasing in config file……')
        config = Config('config.txt')
        self.closelist = list(config.get_section('closeapp', 'closeapp'))
        self.openapplist = list(config.get_section('openapp', 'openapp'))
        self.logger.info('Config file phased in successfully！')
        return self.closelist, self.openapplist

    def close_app(self):
        self.logger.info('Closing apps……')
        for item in self.closelist:
            try:
                status = system('taskkill /f /im ' + item)

                if status == 128:
                    self.logger.warning('App closed failed: ' + item)
                else:
                    self.logger.info('App closed: ' + item)
            except:

                pass
            continue

    def open_app(self):
        self.logger.info('Opening apps……')
        for item in self.openapplist:
            try:
                startfile(item)
                self.logger.info('App opened: ' + item)
            except:
                self.logger.warning('Failed to open app: ' + item)
                pass
            continue


if __name__ == '__main__':
    main = Main()
    main.check_config()
    main.get_config()

    main.close_app()
    main.open_app()
