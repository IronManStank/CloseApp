import logging
from os import startfile, system, path, chdir
import sys
from pprint import pp
import configparser


class ConfigEmptyError(Exception):
    ...


def get_config_path() -> str:
    '''
    从命令行传入configpath，如果没传入则使用默认值
    '''
    try:
        return sys.argv[1]
    except:
        return 'config.txt'


CONFIG_PATH = get_config_path()


class Config(object):
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding='utf-8')

    def get_section(self, section, option):
        section_content = [i.strip()
                           for i in self.config.get(section, option).split(',')]
        if len(section_content[0]) == 0:
            raise ConfigEmptyError(
                "Config file is empty, please add appNames or path according to the config file!")
        else:
            return section_content


class Main(object):
    def __init__(self):
        self.closeapplist = []
        self.openapplist = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='CloseAppLog.log',
                            filemode='w',
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            encoding='utf-8')
        self.logger.setLevel(logging.DEBUG)

        # 统计
        self.openerrlist = []

        self.closeerrlist = []

    def check_config(self):
        self.logger.info('Checking config file……')
        if not path.isfile(CONFIG_PATH):
            self.logger.error(
                'Config file not found! Creating new config file……')
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                f.write('[closeapp]\n')
                f.write(
                    '# 此处为关闭应用程序的进程名，可通过任务管理器查看，\
多个进程名用逗号隔开，注意“,”为英文逗号且有空格! 示例: HuyaClient.exe\n')
                f.write('closeapp = \n')
                f.write('[openapp]\n')
                f.write('# 此处为打开应用程序的路径，多个路径用英文逗号隔开。\
注意“,”为英文逗号且有空格！\n')
                f.write('openapp = \n')
                self.logger.info('Config file created successfully!')

            return False
        else:
            self.logger.info('Config file found!')
            return True

    def get_config(self):
        self.logger.info('Phasing in config file……')
        try:
            config = Config(CONFIG_PATH)
            self.closeapplist = list(
                config.get_section('closeapp', 'closeapp'))
            self.openapplist = list(config.get_section('openapp', 'openapp'))
            self.logger.info('Config file phased in successfully!')
        except Exception as e:
            self.logger.error(e)
        return self.closeapplist, self.openapplist

    def close_app(self):
        self.logger.info('Closing apps……')
        for item in self.closeapplist:
            try:
                status = system(f'taskkill /f /im {item}')

                if status == 128:
                    self.logger.warning(f'App closed failed: {item}')
                    self.closeerrlist.append(item)
                else:
                    self.logger.info(f'App closed: {item}')
            except:
                continue

    def open_app(self):
        self.logger.info('Opening apps……')
        for item in self.openapplist:
            try:
                if path.isfile(item):
                    startfile(item)
                    self.logger.info(f'App opened: {item}')
                else:
                    self.logger.warning(
                        f'Failed to open app: {item}, not exists')

                    self.openerrlist.append(item)
            except:
                self.logger.warning(f'Failed to open app: {item}')
                self.openerrlist.append(item)
                continue

    def summary(self):
        '''
        总结
        '''
        print()
        print('#'*45)
        # 关闭失败/成功 开启失败/成功

        closeok = [i for i in self.closeapplist if i not in self.closeerrlist]
        openok = [i for i in self.openapplist if i not in self.openerrlist]
        print(f'\nClose OK: {len(closeok)}')
        pp(closeok)
        print(f'\nClose Err: {len(self.closeerrlist)}')
        pp(self.closeerrlist)
        print(f'\nOpen OK: {len(openok)}')
        pp(openok)
        print(f'\nOpen Err: {len(self.openerrlist)}')
        pp(self.openerrlist)


if __name__ == '__main__':
    chdir(path.dirname(sys.argv[0]))
    main = Main()
    main.check_config()
    main.get_config()
    main.close_app()
    main.open_app()
    main.summary()
