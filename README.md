# binary-pattern-finder
Task for arcus team

Please provide 3 parameters:
binary_file_path, pattern_file_path, threshold

##Paramaters

binary_file_path - A binary file to search patterns in
pattern_file_path - a txt file containing patterns to find with line brakes delimiting between patterns.
patterns examples: '5f00', '00f5', '5dXXXX'(any 6 bytes that starts with 5d)
threshold - An integer. Treshold for sequence of repeating bytes.

##Output

txt file with the each pattern that was found, its location and size in case of sequence bytes