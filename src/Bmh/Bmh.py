def compute_bad_match_table(pattern):
    """
    Helper function to compute the bad match table (last occurrence of each character in the pattern)
    """
    table = {}

    for i in range(len(pattern) - 1):
        table[pattern[i]] = len(pattern) - 1 - i

    return table


def bmh_search(pattern, text):
    """
    Main function to perform the BMH search
    """
    m = len(pattern)
    n = len(text)

    table = compute_bad_match_table(pattern)

    i = m - 1
    j = m - 1
    matches = []

    while i < n:
        if pattern[j] == text[i]:
            if j == 0:
                matches.append(i)
                i += m
                j = m - 1
            else:
                i -= 1
                j -= 1
        else:
            if text[i] in table:
                i += table[text[i]]
            else:
                i += m
            j = m - 1

    return matches


def read_csv_file(filename):
    """
    Function to read a CSV file and return a list of lines
    """
    data = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                data.append(line.split(','))

    return data


def find_matches(csv_file, pattern_to_search):
    """
    Function to find all occurrences of a pattern in a CSV file
    """
    csv_data = read_csv_file(csv_file)
    for row in csv_data:
        text = ','.join(row)  # Concatenate the elements of the row into a string
        matches = bmh_search(pattern_to_search, text)
        if matches:
            print(f'The pattern "{pattern_to_search}" was found at positions: {matches} in row: {row}')
