def save_resource(file_path, file_name):
    try:
        with open(file_path, 'wb') as file:
            file.write(file_name)
    except OSError:
        raise OSError("Can not save requested page!")
