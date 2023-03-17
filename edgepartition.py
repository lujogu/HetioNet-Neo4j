import csv

# Define the input and output filenames
input_filename = 'edges.tsv'
output_filenames = {}

# Open the input file and read its data
with open(input_filename, 'r', newline='') as input_file:
    tsv_reader = csv.reader(input_file, delimiter='\t')
    
    # Iterate over the rows in the input file
    for row in tsv_reader:
        # Get the second field in the current row
        partition_key = row[1]
        
        # If this partition key hasn't been seen before, open a new output file
        if partition_key not in output_filenames:
            output_filenames[partition_key] = f'{partition_key}.tsv'
            output_file = open(output_filenames[partition_key], 'w', newline='')
            tsv_writer = csv.writer(output_file, delimiter='\t')
        # Otherwise, use the existing output file for this partition key
        else:
            output_file = open(output_filenames[partition_key], 'a', newline='')
            tsv_writer = csv.writer(output_file, delimiter='\t')
        
        # Write the current row to the appropriate output file
        tsv_writer.writerow(row)
        
        # Close the current output file
        output_file.close()

# Print a summary of the output filenames
print('Partitioned output:')
for partition_key, output_filename in output_filenames.items():
    print(f'{partition_key}: {output_filename}')
