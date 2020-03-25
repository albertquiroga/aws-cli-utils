import sys
from argparse import Namespace, ArgumentParser
from pathlib import Path

from common_utils import load_user_configuration_file

CONFIG_FILE_PATH = f'{str(Path.home())}/.aws-cli-utils'


class CLITool:
    """Superclass for all CLI tools, designed to automate common tasks

       Attributes
       ----------
       name: str
           The name of the CLI tool. This will be the 'prog' parameter of the argparse.ArgumentParser

       description: str
           Description of the CLI tool. This will be he 'description' parameter of the argparse.ArgumentParser

       config_section: str
           Name of the corresponding section in the configuration file

       key_parameters: dict
           Dictionary that defines key parameters for each subcommand of a tool. A key parameter is one for which a
           value must be provided. This is similar to positional arguments in argparse, but lets you have empty
           positional arguments as long as a default value is provided in the configuration file

        Methods
        -------
        main(None)
            Runs the CLI tool. The method will first check that CLI arguments were provided. If not, it will print
            the argparse help message and exit. Otherwise, it will validate key parameters (if any) and then
            simply call func() to run the method designated to the subcommand
     """

    def __init__(self, name: str, description: str, config_section: str, key_parameters: dict = None):
        self.parser = ArgumentParser(prog=name, description=description)
        self.subparsers = self.parser.add_subparsers(dest="subparser_name")
        self.config = load_user_configuration_file()[config_section]
        self.key_parameters = key_parameters

    def main(self):
        """
        Main function. Prints the help message if there are no CLI args, otherwise evaluates them and
        if all key_parameters are provided, runs the associated function
        :return: None
        """
        args = self.parser.parse_args()
        self._print_help_and_exit() if self._no_args_provided(args) else self._validate_and_run(args)

    @staticmethod
    def _no_args_provided(args: Namespace) -> bool:
        """
        Determines if the user didn't provide any CLI args
        :param args: Namespace object containing CLI args
        :return: True if no CLI args, False otherwise
        """
        return len(vars(args)) <= 1

    def _validate_and_run(self, args: Namespace):
        """
        Validates key parameters and runs the function associated to the provided subcommand
        :param args: Namespace object containing CLI args
        :return: None
        """
        if args.subparser_name in self.key_parameters:
            self._validate_cli_key_parameters(args, args.subparser_name)
        args.func(args)

    def _print_help_and_exit(self):
        """
        If no CLI args were provided, print the argparser help message and exit
        :return: None
        """
        self.parser.print_help()
        sys.exit(1)

    def _validate_cli_key_parameters(self, args: Namespace, subcommand: str):
        """
        For each key parameter, checks whether a value was provided for it either as a CLI arg or
        as a default value in the config file
        :param args: Namespace object containing CLI args
        :param subcommand: CLI subcommand that is currently running
        :return: None
        """
        args_dict = vars(args)
        mapped = list(map(lambda parameter: (parameter, args_dict[parameter]), self.key_parameters[subcommand]))
        for key_parameter in mapped:
            self._validate_key_parameter(key_parameter)

    @staticmethod
    def _validate_key_parameter(parameter_tuple: tuple):
        """
        Validates an individual key parameter. If no value for it was provided, inform the user and exit
        :param parameter_tuple:
        :return:
        """
        if not parameter_tuple[1]:
            print(f'No value was provided for CLI argument "{parameter_tuple[0]}". Consider adding a default '
                  f'value to the {CONFIG_FILE_PATH} file')
            sys.exit(1)
