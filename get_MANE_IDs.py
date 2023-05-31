import os
import urllib.request

# Function to download the MANE transcript summary file if it is not present in the current directory
def get_MANE_transcripts(file_name, url):
	if not os.path.isfile(file_name):
		print(f"'{file_name}' is not present. Downloading it now.")
		urllib.request.urlretrieve(url, file_name)
		print(f"'{file_name}' has been downloaded successfully, continuing.")
	else:
		print(f"'{file_name}' is present in the current directory.")

# Run the function
file_name = "MANE.GRCh38.v1.1.summary.txt"
url = "https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/release_1.1/MANE.GRCh38.v1.1.summary.txt.gz"
get_MANE_transcripts(file_name, url)

# Get gene names from the ROI file
def get_gene_names(roi_file):
	gene_names = []
	with open(roi_file, "r") as file:
		for line in file:
			if line.startswith("#"):
				continue
			else:
				line = line.strip().split("\t")
				if len(line) >= 4:
					gene_names.append(line[3])
	return gene_names

# Define the ROI file and get the gene names
roi_file = "llgp4_coding_only_target.bed"
gene_names = get_gene_names(roi_file)

# Remove any text after an underscore in the gene names (e.g. "NOTCH2_Pseudo" becomes "NOTCH2")
for i in range(len(gene_names)):
	if "_" in gene_names[i]:
		gene_names[i] = gene_names[i].split("_")[0]

# Remove duplicates from the list
gene_names = list(dict.fromkeys(gene_names))

# Function to match the MANE transcript ID to the gene name

# Find matches between gene_names and MANE.GRCh38.v1.1.summary.txt. If a match is found save the entire line to a new file.
def find_matching_lines(MANE_IDs_file, gene_names):
	MANE_ID_matches = []
	with open(MANE_IDs_file, 'r') as MANE_IDs:
		values = set(gene_names)
		for line in MANE_IDs:
			if any(value in line for value in values):
				MANE_ID_matches.append(line)
		return MANE_ID_matches

# Run the function
MANE_IDs_file = 'MANE.GRCh38.v1.1.summary.txt'
gene_names = gene_names
MANE_IDs_matches = find_matching_lines(MANE_IDs_file, gene_names)

# Write column 4, 6 and 10 of MANE_IDs_matches to a new file
with open("MANE_IDs_matches.txt", "w") as file:
	for line in MANE_IDs_matches:
		file.write(
			line.split("\t")[3] + "\t" + line.split("\t")[5] + "\t" + line.split("\t")[9] + "\n")
		
# Load MANE_IDs_matches.txt. Where duplicates exist in column 1 keep the line with the value "MANE Plus Clinical" in column 3 and delete the other lines.
def remove_duplicates(file_name):
    unique_lines = []
    with open(file_name, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            if columns[2] == 'MANE Plus Clinical':
                for unique_line in unique_lines:
                    if columns[0] == unique_line[0]:
                        break
                else:
                    unique_lines.append(columns)
    
    with open(file_name, 'w') as file:
        for line in unique_lines:
            file.write('\t'.join(line) + '\n')

file_name = 'MANE_IDs_matches.txt'
remove_duplicates(file_name)


