from pathlib import Path


def path_log_file(file_name) -> str:
    return str(Path(__file__).parent.parent.joinpath(f'logs/{file_name}'))