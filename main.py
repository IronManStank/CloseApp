from os import path, system, startfile
from get_config import Config


class Main(object):
    def __init__(self):
        self.closeapplist = []
        self.openapplist = []

    def check_config(self):
        if not path.exists('config.txt'):
            print('Config file not found, creating new config file')
            with open('config.txt', 'w') as f:
                pass
            return False
        else:
            print('Config file found! Phasing in config file')

    def get_config(self):
        config = Config('config.txt')
        self.closelist = list(config.get_section('closeapp', 'closeapp'))
        self.openapplist = list(config.get_section('openapp', 'openapp'))
        return self.closelist, self.openapplist

    def close_app(self):
        for item in self.closelist:
            try:
                status = system('taskkill /f /im ' + item)
            except:
                pass
            continue

    def open_app(self):
        for item in self.openapplist:
            try:
                startfile(item)
            except:
                pass
            continue


if __name__ == '__main__':
    main = Main()
    main.check_config()
    main.get_config()

    main.close_app()
    main.open_app()
