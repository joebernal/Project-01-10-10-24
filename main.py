import re
import keyword

# Read data from input file
def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data

# Remove excess space, single-line comments, and multi-line comments from data
def remove_comments_and_spaces(data):
    processed_code = []
    comments = []
    inside_multiline_comment = False

    for line in data:
        # Remove leading and trailing spaces
        stripped_line = line.strip()

        # Check for start or end of multi-line comment (triple quotes)
        if '"""' in stripped_line:
            if not inside_multiline_comment:
                # Starting a multi-line comment
                inside_multiline_comment = True
                comment_start_index = stripped_line.index('"""')
                comment = stripped_line[comment_start_index:]
                comments.append(comment.strip())
            else:
                # Ending a multi-line comment
                inside_multiline_comment = False
                comment_end_index = stripped_line.index('"""') + 3
                comment = stripped_line[:comment_end_index]
                comments[-1] += " " + stripped_line[:comment_end_index].strip()
            continue

        # Capture lines inside a multi-line comment block
        if inside_multiline_comment:
            comments[-1] += " " + stripped_line
            continue

        #Capture and remove single-line comment from processed code
        if '#' in stripped_line:
            comment_start_index = stripped_line.index('#')
            comment = stripped_line[comment_start_index:]
            comments.append(comment.strip())

            # Remove the part of the line after the comment
            stripped_line = stripped_line[:comment_start_index].strip()


        # Skip empty lines
        if stripped_line != "":
            processed_code.append(stripped_line)

    return processed_code, comments

# Tokenize cleaned-up code
def tokenize_code(processed_code, comments):
    tokens = {
        'Keywords': [],
        'Identifiers': [],
        'Operators': [],
        'Delimiters': [],
        'Literals': [],
        'Comments': comments
    }

    operators = ['=', '+', '-', '*', '/', '%', ':']
    delimiters = ['(', ')', ':', ',', '[', ']', '{', '}']
    token_pattern = r"[\w']+|\"[^\"]*\"|'[^']*'|[" + re.escape("".join(operators + delimiters)) + "]"

    # Count total number of tokens
    total_tokens = 0;

    for line in processed_code:
        line_tokens = re.findall(token_pattern, line)
        for token in line_tokens:
            if token in keyword.kwlist:
                tokens['Keywords'].append(token)
            elif token in operators:
                tokens['Operators'].append(token)
            elif token in delimiters:
                tokens['Delimiters'].append(token)
            elif re.match(r'^\d+$', token) or token.startswith('"') or token.startswith("'"):
                tokens['Literals'].append(token)
            else:
                tokens['Identifiers'].append(token)
            total_tokens += 1


    return tokens, total_tokens

# Print code after removing excess space and comments
def print_processed_code(processed_code):
    print("Output 1 - Code after removing excess space and comments:")
    for line in processed_code:
        print(line)

# Print tokenized code, comments and total count of tokens
def print_tokenized_code(tokens, total_tokens):
    print("\nOutput 2 - Tokens:")
    print("-" * 30)
    for category, token_list in tokens.items():
        print(f"{category}: {', '.join(set(token_list))}")  # Using set to avoid duplicates
    print(f"\nTotal tokens: {total_tokens}")

# Main function to run program
def main():
    file_path = 'example2.txt'
    data = read_file(file_path)

    processed_code, comments = remove_comments_and_spaces(data)
    print_processed_code(processed_code)

    tokens, total_tokens = tokenize_code(processed_code, comments)
    print_tokenized_code(tokens, total_tokens)

# Run program
if __name__ == "__main__":
    main()