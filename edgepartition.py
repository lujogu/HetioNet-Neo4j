import csv
# Define the input and output filenames
input_filename = 'edges.tsv'
output_filenames = {}

def partition(partition_key_param):
    if partition_key_param not in output_filenames:
        output_filenames[partition_key_param] = f'{partition_key_param}.tsv'
        output_file = open(output_filenames[partition_key_param], 'w', newline='')
        tsv_writer = csv.writer(output_file, delimiter='\t')
    # Otherwise, use the existing output file for this partition key
    else:
        output_file = open(output_filenames[partition_key_param], 'a', newline='')
        tsv_writer = csv.writer(output_file, delimiter='\t')
    
    # Write the current row to the appropriate output file
    tsv_writer.writerow(row)
    
    # Close the current output file
    output_file.close()

# Open the input file and read its data
with open(input_filename, 'r', newline='') as input_file:
    tsv_reader = csv.reader(input_file, delimiter='\t')
    
    # Iterate over the rows in the input file
    for row in tsv_reader:
        # Get the second field in the current row
        partition_key = row[1]

        # exception case for GrG
        if partition_key == 'Gr>G':
            partition('GrG')
        else:
            partition(partition_key)