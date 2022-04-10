import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python tournament.py FILENAME")

    # Read database file into a variable
    dnaDatabase = []
    with open(sys.argv[1], mode='r') as csvFile:
        reader = csv.DictReader(csvFile)
        strTypes = reader.fieldnames[1:]
        for row in reader:
            dnaDatabase.append(row)

    # Read DNA sequence file into a variable
    txtFile = open("./" + sys.argv[2])
    sequence = txtFile.read()
    txtFile.close()

    # Find longest match of each STR in DNA sequence
    # create a dict
    strCount = dict.fromkeys(strTypes, 0)
    # for each str type, store its longest match
    for str in strTypes:
        strCount[str] = int(longest_match(sequence, str))

    # Check database for matching profiles
    for row in dnaDatabase:
        if match(strTypes, strCount, row):
            print(f"{row['name']}")
            txtFile.close()
            return

    # if return's nothing, "no match"
    print("No match")
    txtFile.close()


# match function
def match(strTypes, strCount, row):
    for str in strTypes:
        if strCount[str] != int(row[str]):
            return False
    return True


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


if __name__ == "__main__":
    main()
