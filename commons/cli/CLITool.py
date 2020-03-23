import sys
import argparse
from pathlib import Path
from commons import load_user_configuration_file

CONFIG_FILE_PATH = f'{str(Path.home())}/.aws-cli-utils'


class CLITool:

    def __init__(self, name, description, config_key, key_parameters=None):
        self.parser = argparse.ArgumentParser(prog=name, description=description)
        self.subparsers = self.parser.add_subparsers(dest="subparser_name")
        self.config = load_user_configuration_file()[config_key]
        self.key_parameters = key_parameters

    def main(self):
        """
        Main function. Evaluates the CLI args and prints the help message if there are none
        :return: None
        """
        args = self.parser.parse_args()
        subcommand = args.subparser_name

        if not len(vars(args)) == 0:
            self._validate_cli_key_parameters(args, subcommand)
            args.func(args)
        else:
            self.parser.print_help()
            sys.exit(1)

    def _validate_cli_key_parameters(self, args, subcommand):
        args_dict = vars(args)
        mapped = list(map(lambda parameter: (parameter, args_dict[parameter]), self.key_parameters[subcommand]))
        for key_parameter in mapped:
            self._validate_key_parameter(key_parameter)

    def _validate_key_parameter(self, parameter_tuple):
        if not parameter_tuple[1]:
            print(f'No value was provided for CLI argument "{parameter_tuple[0]}". Consider adding a default '
                  f'value to the {CONFIG_FILE_PATH} file')
            sys.exit(1)
