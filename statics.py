import os
# Global static variables. Determines the directory the script is in and sets the config path for the config.json
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")
