def get_top_mothers(data):
    # Step 1: Identify all children (values)
    children = set(data.values())
    
    # Step 2: Identify all parents (keys)
    parents = set(data.keys())
    
    # Step 3: Top mothers are children that are not parents
    top_mothers = list(children - parents)

    return top_mothers

# Example usage
data = {
    'a': 'b',
    'b': 'c',
    'd': 'c',
    "c": "d"
}

top_mothers = get_top_mothers(data)
print(top_mothers)  # Should print ['c']
