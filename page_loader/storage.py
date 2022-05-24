import os


def save_resource(file_path, file_name):
    try:
        output_dir = os.path.dirname(file_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(file_name)
    except OSError:
        raise OSError('Can not save requested page!')
