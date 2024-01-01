def convert_to_json(data):
    result = {}

    if "json.object" in data:
        result = convert_json_object(data["json.object"])
    if "json.array" in data:
        result = convert_json_array(data["json.array"])

    return result


def convert_json_array(data):
    arr = []
    if "json.object" in data:
        for json_object in data["json.object"]:
            arr.append(convert_json_object(json_object))
    else:
        return get_member_tree_value(data)

    return arr


def convert_json_object(data):
    result = {}
    if data == "":
        return {}
    elif isinstance(data["json.member_tree"], list):
        for member in data["json.member_tree"]:
            key = member["json.key"]

            if "json.path_with_value" in member:
                result[key] = get_member_tree_value(member)
            else:
                result[key] = convert_to_json(member)
    else:
        key = data["json.member_tree"]["json.key"]
        if "json.path_with_value" in data["json.member_tree"]:
            result[key] = get_member_tree_value(data["json.member_tree"])
        else:
            result[key] = convert_to_json(data["json.member_tree"])

    return result


def get_member_tree_value(member):
    if "json.value.number" in member:
        if isinstance(member["json.value.number"], list):
            arr = []
            for value in member["json.value.number"]:
                arr.append(get_member_tree_value_number(value))
            return arr
        else:
            return get_member_tree_value_number(member["json.value.number"])
    elif "json.value.string" in member:
        if isinstance(member["json.value.string"], list):
            arr = []
            for value in member["json.value.string"]:
                arr.append(value)
            return arr
        else:
            return member["json.value.string"]
    elif "json.value.false" in member:
        return False
    elif "json.value.true" in member:
        return True
    elif "json.value.null" in member:
        return None
    else:
        print("MEMBER: ", member)
        raise Exception("Unknown value on member")


def get_member_tree_value_number(value):
    if "." in value:
        return float(value)
    else:
        return int(value)
