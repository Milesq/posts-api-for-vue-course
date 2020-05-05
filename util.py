def have(arr, keys):
    if arr is None:
        return False

    return all([key in arr for key in keys])
