def find_longest_substring(s):
    start = 0
    max_length = 0
    max_substring = ""
    char_index = {}

    for end in range(len(s)):
        if s[end] in char_index:
            start = max(start, char_index[s[end]] + 1)
        if end - start + 1 > max_length:
            max_length = end - start + 1
            max_substring = s[start:end + 1]
        char_index[s[end]] = end

    return max_substring, max_length

if __name__ == "__main__":
    input_string = input("input: ")
    longest_substring, length = find_longest_substring(input_string)
    print(f"output: {longest_substring} length: {length}")