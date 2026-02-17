import logging
import sys
from py_GUI.ui.app import main

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def application_main():
    try:
        # Main application logic
        main()
    except Exception as e:
        logging.error(f"An unhandled exception occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    application_main()
