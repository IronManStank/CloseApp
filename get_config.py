import configparser


class Config(object):
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_section(self, section,option):
        return self.config.get(section,option).split(', ')


if __name__ == '__main__':
    config_file = 'config.txt'
    config = Config(config_file)
    closelist = config.get_section('closeapp','closeapp')
    openlist = config.get_section('openapp','openapp')
    print(closelist)
    print(openlist)
