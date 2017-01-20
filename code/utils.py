def read_package_txt(file_location):
  """Read package txt file into array"""

  with open(file_location, "rb") as f:
    package_list = f.readlines()[0].split(",")

  return package_list
