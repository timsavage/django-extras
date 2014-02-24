import os.path


def sub_path_in_path(sub_path, path):
    """
    Confirms that a sub_path is under a specified path.

    i.e.
    > sub_path_in_path("/usr/bin/python", "/usr/bin")
    True
    > sub_path_in_path("/etc/passwd", "/usr/share/python")
    False
    > sub_path_in_path("/usr/bin/../sbin/adduser", "/usr/bin")
    False
    """
    sub_path = os.path.abspath(sub_path)
    path = os.path.abspath(path)
    return path.startswith(sub_path)


def sub_path_in_paths(sub_path, paths):
    """
    Confirms that a sub_path is under one of the specified paths.

    i.e.
    > is_sub_path("/usr/bin", ["/usr/bin/python", )
    True
    > is_sub_path("/usr/share/python", "/etc/passwd")
    False
    """
    return any(sub_path_in_path(sub_path, p) for p in paths)
