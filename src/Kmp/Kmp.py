def compute_lps(pattern):
    """
    Helper function to compute the LPS table (longest proper prefix which is also a suffix)
    """
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(pattern, text):
    """
    Main function to perform the KMP search
    """
    m = len(pattern)
    n = len(text)

    lps = compute_lps(pattern)

    i = 0  # Index to traverse the text
    j = 0  # Index to traverse the pattern
    matches = []

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

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


# Usage example

def find_matches(csv_data, pattern_to_search):
    """
    Function to find all occurrences of a pattern in a CSV file
    """
    csv_data = read_csv_file(csv_data)

    for row in csv_data:
        text = ','.join(row)  # Concatenate the elements of the row into a string
        matches = kmp_search(pattern_to_search, text)
        if matches:
            print(f'The pattern "{pattern_to_search}" was found at positions: {matches} in row: {row}')
