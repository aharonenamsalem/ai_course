#create a function that get file name and return its extension
def get_file_extension(file_name):
    # Split the file name by the last dot
    parts = file_name.rsplit('.', 1)
    # Check if there is an extension
    if len(parts) == 2:
        return parts[1]
    else:
        return ''  # No extension found 
# Example usage
file_name = "example.txt"
extension = get_file_extension(file_name)
print(f"The extension of the file '{file_name}' is: '{extension}'")