import yaml

def load_config(config_path: str = r"config/config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config