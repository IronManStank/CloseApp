import configparser

class ConfigEmptyError(Exception):
    pass

class Config(object):
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file,encoding='utf-8')

    def get_section(self, section,option):
        section_content = self.config.get(section,option).split(', ')
        if len(section_content[0]) == 0:
            raise ConfigEmptyError("Config file is empty, please add appNames or path according to the config file!")
        else:
            return section_content


if __name__ == '__main__':
    config_file = 'config.txt'
    config = Config(config_file)
    closelist = config.get_section('closeapp','closeapp')
    openlist = config.get_section('openapp','openapp')
    print(closelist)
    print(openlist)
