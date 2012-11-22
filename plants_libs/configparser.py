import ConfigParser

from plants_libs import tuple_list_to_dict

def config_parser_dict(config_file):
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config_file)
    
    config_parser_dict = {}
    for section in config_parser.sections():
        config_parser_dict[section] = tuple_list_to_dict(config_parser.items(section))
    
    return config_parser_dict