import pandas as pd

# Read and preprocess TA and section data
def read_tasect(tasfile='tas.csv', sectfile='sections.csv'):
    '''Reads and cleans section and TA information'''
    # Read files
    tas = pd.read_csv(tasfile)
    sect = pd.read_csv(sectfile)

    # Clean and prepare section data
    clean_sect = sect.drop(columns=['instructor', 'location', 'students', 'topic', 'max_ta'])
    clean_sect['daytime'], time_index = pd.factorize(clean_sect['daytime'])

    # Clean and prepare TA data
    mapping = {'U': 1, 'W': 2, 'P': 3}
    clean_tas = tas.drop(columns=['name'])
    for col in clean_tas.columns[2:]:
        clean_tas[col] = clean_tas[col].map(mapping)

    return clean_tas, clean_sect
