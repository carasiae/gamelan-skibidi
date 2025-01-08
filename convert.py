import sys
def convert_music_notation(notation):
    res_list = []
    result = []
    beat = []
    
    i = 0
    while i < len(notation):
        char = notation[i]

        # Convert letters A-U to integers 1-21
        if (char.isalpha() and 'A' <= char <= 'U') or char == '-' or char == ']':
            if char == '-':
                note = 0
            elif char == ']':
                res_list.append(result)
                result = []
                beat = []
                i += 1
                continue
            else:
                note = ord(char) - ord('A') + 1
            i += 1
            
            # If no underscore or equal sign, it's a whole note (just the note)
            if i < len(notation) and notation[i] != '_' and (i + 1 >= len(notation) or notation[i + 1] != '='):
                beat.append(note)
                beat.append(0)  # First part of quarter-beat
                beat.append(0)  # Second part of quarter-beat
                beat.append(0)  # Third part of quarter-beat

            # If the note is followed by underscore and equal sign (quarter-beat)
            elif i + 1 < len(notation) and notation[i] == '_' and notation[i + 1] == '=':
                beat.append(note)
                i += 2  # Skip underscore and equal sign

            # If the note is followed by an underscore (half-beat)
            elif i < len(notation) and notation[i] == '_':
                beat.append(note)
                beat.append(0)  # Half beat (note followed by underscore)
                i += 1  # Skip underscore

            # If the note is followed by nothing, it's a whole note (note followed by 3 zeros)
            else:
                beat.append(note)
                beat.append(0)
                beat.append(0)
                beat.append(0)  # Pad with 3 zeros for whole note

        else:
            # Skip any other characters
            i += 1
        
        # Once we have a full beat (with the correct number of elements), add it to the result.
        if len(beat) == 4:
            if beat[1] == 0 and beat[2] == 0 and beat[3] == 0:
                result.append((beat[0],))
            elif beat[1] == 0 and beat[3] == 0:
                result.append((beat[0], beat[2]))
            else:
                result.append(tuple(beat))
            beat = []  # Reset for the next beat
    if not len(result) == 0:
        res_list.append(result)
    
    return res_list

def process_file(filename):
    try:
        with open(filename, 'r') as file:
            notation = file.read().strip()  # Read the file content
            # Filter out any characters that are not valid (A-U, hyphen, underscore, equal sign)
            valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-_=]"
            filtered_notation = ''.join([char for char in notation if char in valid_chars])
            result = convert_music_notation(filtered_notation)
            return result
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        process_file(filename)
