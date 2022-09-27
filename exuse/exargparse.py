from ast import arg
import logging
from typing import Callable, List
from argparse import ArgumentParser, HelpFormatter
# for export
from argparse import Namespace


class BaseHandler(object):
    """
    If program has an `action` argument to handle different transactions, you 
    can realize these actions in the subclass of `BaseHandler`. Each action 
    can be defined as a static method using `@staticmethod` decorator. The 
    static method has only one parameter named `args` which is generated by 
    argument parsers, so that `action` method can access the arguments provided
    by command line. Call `set_default` or other methods of the arugment parser
    to bind the custom handler.
    """

    @classmethod
    def _run(cls, args):
        try:
            return getattr(cls, args.action)(args)
        except AttributeError as e:
            if str(e) == "'Namespace' object has no attribute 'action'":
                print(
                    "ERROR: `action` positional argument must be provided when using `BaseHandler` class")
            else:
                raise e


class SmartFormatter(HelpFormatter):
    """
    Set help message by a multi-line string quoting by `\"\"\"` or `'''`).
    """

    def _split_lines(self, text: str, width: int) -> List[str]:
        # return [*[s.strip(' \n') for s in text.strip(' \n').split('\n')], '']
        return [s.strip(' \n') for s in text.strip(' \n').split('\n')]


class ExArgumentParser(ArgumentParser):
    """
    Extend the default `ArgumentParser`. Main contents appended:
    - set our custom `SmartFormatter` as the default formatter class
    - provide `get_subparser` method to get a subparser quickly
    - provide `set_callback` method to set callback function or Callback class
      for current parser or subparser. If you use `action` argument to process
      different transactions, pass a `Callback` class inheritted from 
      `BaseHandler` is not a bad idea.
    - provide `run` method to run program by calling the given callback.
    """

    def __init__(self, formatter_class=SmartFormatter, **kwargs):
        super().__init__(formatter_class=formatter_class, **kwargs)
        self.__subparsers = None
        levels = 'DEBUG|INFO|WARNING|ERROR|CRITICAL'
        self.add_argument('--log-level', '-l', choices=levels.split('|'),
                          default='INFO', metavar=levels, help="set logging level")

    @property
    def subparsers(self):
        if self.__subparsers is None:
            self.__subparsers = self.add_subparsers()
        return self.__subparsers

    def set_callback(self, callback: Callable = None, Callback: BaseHandler = None):
        """
        set callback function or Callback class for current parser or subparser.

        Args:
            - `callback` a function to run main program
            - `Callback` a class to run different actions

        """
        if callback is not None:
            self.set_defaults(callback=callback, Callback=None)
        elif Callback is not None:
            self.set_defaults(callback=None, Callback=Callback)
        else:
            raise Exception('`Callback` and `callback` cannot be both `None`.')

    def set_callback_function(self, func: Callable):
        """
        set callback function for current parser or subparser.

        Args:
            callback (Callable): a function to run main program
        """
        self.set_callback(func, None)

    def set_callback_class(self, Handler: BaseHandler):
        """
        set callback class for current parser or subparser.

        Args:
            - `Callback` a class to run different actions

        """
        self.set_callback(None, Handler)

    def run(self):
        """
        Run callback function.
        """
        args = self.parse_args()
        log_level: str = args.log_level
        logging.getLogger().setLevel(log_level)

        if hasattr(args, 'callback') and args.callback is not None:
            callback: Callable = args.callback
            callback(args)
        elif hasattr(args, 'Callback') and args.Callback is not None:
            Callback: BaseHandler = args.Callback
            Callback._run(args)
        else:
            raise AttributeError(f'no callback or Callback provided')

    def get_subparser(self, *args, **kwargs):
        return self.subparsers.add_parser(*args, **kwargs)
