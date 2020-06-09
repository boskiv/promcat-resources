import pypromcat
import argparse


parser = argparse.ArgumentParser(description='Parser to change a recording rule resource adding the data element into a configurations array.')
parser.add_argument('-f',
                    '--file',
                    required=True,
                    dest='file',
                    help='File to extract the alerts from')
parser.add_argument('-o',
                    '--output',
                    required=False,
                    dest='outputFile',
                    help='File to write the output')

try:
    args = parser.parse_args()
except BaseException as exception:
    # parser will print either help or syntax error details
    exit(1)


yamlFile = pypromcat.loadYamlFile(args.file)
yamlFile["configurations"] = []
configuration = {"kind": "Prometheus", "data": yamlFile["data"]}
yamlFile["configurations"].append(configuration)
del yamlFile["data"]

outputformatted = pypromcat.dict2BeautyYaml(yamlFile)
if args.outputFile is None:
    print(outputformatted)
else:
    f = open(args.outputFile, "w")
    f.write(outputformatted)
    f.close()