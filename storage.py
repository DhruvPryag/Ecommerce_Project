# import json

# def save_data(filename, data):
#     with open(filename, 'w') as f:
#         # Convert objects to dictionaries for JSON compatibility
#         json.dump(data, f, indent=4)

# def load_data(filename):
#     try:
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []