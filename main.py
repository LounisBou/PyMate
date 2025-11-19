#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import logging
import importlib
import pkgutil
from termcolor import colored

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def test_pydevmate_module(module_name):
    """
    Runs the main block of a PyDevMate module.
    """
    try:
        logging.info(colored(f"Testing {module_name}...", "yellow"))
        script_dir = os.path.join(os.path.dirname(__file__), 'pydevmate', module_name.split('.')[-1] + '.py')
        logging.info('-' * 50 + '\n')
        subprocess.run(['python', script_dir], check=True)
        print()
        logging.info('-' * 50)
    except Exception as e:
        raise Exception(f"Error testing {module_name}: {e}")

def discover_pydevmate_utilities():
    """
    Discovers available modules in the `pydevmate` package.
    Returns a list of module names.
    """
    package = importlib.import_module("pydevmate")
    return [name for _, name, is_pkg in pkgutil.iter_modules(package.__path__) if not is_pkg]

def main():
    """
    Entry point for running PyDevMate utilities.
    """
    
    # Check arguments
    parser = argparse.ArgumentParser(description='PyDevMate - A collection of Python utilities.')
    parser.add_argument('utility', type=str, nargs='?', help='Name of the utility to test.')
    args = parser.parse_args()
    
    # Log the start of the test
    logging.info(colored("PyDevMate - A collection of Python utilities.", "green"))
    logging.info(colored("Testing PyDevMate utilities...\n", "yellow"))

    # Discover utilities dynamically
    utilities = discover_pydevmate_utilities()
    if not utilities:
        logging.warning(colored("No PyDevMate utilities found.", "red"))
        return
    
    # Check if utility argument is provided and exists
    if args.utility:
        # Compare lowercase utility name
        if args.utility.lower() not in [utility.lower() for utility in utilities]:
            logging.error(colored(f"Utility '{args.utility}' not found.", "red"))
            return
        utilities = [args.utility]
    else:
        logging.info(colored(f"Found {len(utilities)} PyDevMate utilities:", "yellow"))
        for utility in utilities:
            logging.info(f" - {utility}")

    # Test each utility
    nb_errors = 0
    for utility in utilities:
        try:
            test_pydevmate_module(f"pydevmate.{utility}")
        except Exception as e:
            print("Error testing utility:", utility)
            nb_errors += 1
    
    logging.info('-' * 50)
    if nb_errors:
        logging.error(colored(f"PyDevMate utilities {len(utilities) - nb_errors}/{len(utilities)} passed.", "red"))
    else:
        logging.info(colored("All PyDevMate utilities passed successfully.", "green"))

if __name__ == '__main__':
    main()
