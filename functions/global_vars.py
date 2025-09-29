db_file = "data.db"
db_accounts = "accounts.db"
reset_session = set()
json_file = "resetSession.json"
offset_gap = 25


def split_between(full_string, start_string, end_string, replace_with=None):
    start_index = full_string.upper().find(start_string.upper())
    if start_index == -1:
        return None

    end_index = full_string.upper().find(end_string, start_index + len(start_string))
    if end_index == -1:
        return None
    
    # if replace_with != None:
    #     pass
    
    return full_string[start_index + len(start_string):end_index]  

# original = "SELECT id, name, user FROM data"
# modified = split_between(original, "SELECT ", " FROM")
# print(modified)

