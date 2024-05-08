import pandas as pd
import os, xmltodict
import argparse

def main(report_dir, xml_file, output_file):
    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # Iterate over all files in the report directory
    for file in os.listdir(report_dir):
        if file.endswith('.txt'):
            # Read the file
            temp_df = pd.read_csv(os.path.join(report_dir, file), sep='\t', header=None)
            # Set column names
            temp_df.columns = ['Percentage of reads covered', 'Number of reads covered', 'Number of reads', 'Rank code', 'NCBI taxonomy ID', 'Scientific name']
            # Add a new column to record the file name, named SampleID
            temp_df.insert(0, 'SampleID', file.split('.')[0])
            # Concatenate this DataFrame to the main DataFrame
            df = pd.concat([df, temp_df], ignore_index=True)

    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read())

    doc = doc['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']

    # Create a dictionary where the keys are SampleID and the values are dictionaries containing PRIMARY_ID and other attributes
    id_dict = []
    for i, item in enumerate(doc):
        sample_id = item['RUN_SET']['RUN']['IDENTIFIERS']['PRIMARY_ID']
        temp = pd.DataFrame(item['SAMPLE']['SAMPLE_ATTRIBUTES']['SAMPLE_ATTRIBUTE'])
        temp.set_index('TAG', inplace=True)
        temp = temp.transpose()
        temp.reset_index(drop=True, inplace=True)
        temp.columns.name = None
        temp_dict = temp.to_dict('records')[0]
        temp_dict['SampleID'] = sample_id
        id_dict.append(temp_dict)

    dicts = pd.DataFrame(id_dict)

    # Left join df and dicts using 'SampleID' as the key
    df = pd.merge(df, dicts, on='SampleID', how='left')

    # Save the result
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Create a parser object
    parser = argparse.ArgumentParser(description='Process some integers.')
    # Add the required arguments
    parser.add_argument('--report_dir', required=True, help='The directory of report files')
    parser.add_argument('--xml_file', required=True, help='The xml file to be processed')
    parser.add_argument('--output_file', required=True, help='The output xlsx file')

    # Parse the command line arguments
    args = parser.parse_args()

    main(args.report_dir, args.xml_file, args.output_file)
