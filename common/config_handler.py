import pathlib

import yaml


class Config:

    config_file = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, 'config')
    print(pathlib.Path(config_file).rglob('*.yml'))
    configs = {}

    for file in pathlib.Path(config_file).rglob('*.yml'):
        print(file)
        file_key = file.stem
        if file_key in configs:
            exception = f"Duplicate config name {file_key}!"
            raise KeyError(exception)
        with open(file) as fconfig:
            configs[file_key] = yaml.safe_load(fconfig)

    @classmethod
    def get(cls, config_name='configs'):
        """Return the config file by name.

        :return: dict with config data
        """
        return cls.configs[config_name]

