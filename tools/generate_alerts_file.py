import pypromcat
import argparse


parser = argparse.ArgumentParser(description='Generate from an alerts.yaml with Prometheus alerts a new one with sysdig alerts and description.')
parser.add_argument('-f',
                    '--file',
                    required=True,
                    dest='file',
                    help='Original file with Prometheus alerts')
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
newConfigurations = []

prometheusAlerts = pypromcat.filterConfigurationsPerKind(yamlFile["configurations"],"Prometheus")
for prometheusAlert in prometheusAlerts:
  newConfigurations.append(prometheusAlert)

sysdigAlertsArray = pypromcat.sysdigAlerts2PromcatConfigurations(pypromcat.createArrayOfSysdigAlerts(yamlFile))
for sysdigAlert in sysdigAlertsArray:
  newConfigurations.append(sysdigAlert)

yamlFile["configurations"] = newConfigurations

newDescription = ""
newDescription += "# Alerts\n"

for prometheusAlertElement in prometheusAlerts:
  prometheusAlertsYaml = pypromcat.loadYaml(prometheusAlertElement["data"])
  for alert in prometheusAlertsYaml:
    newDescription = newDescription + "## " + alert["alert"] + "\n"
    if "annotations" in alert:
      if "summary" in alert["annotations"]:
        newDescription = newDescription + alert["annotations"]["summary"] + "\n\n"
      if "message" in alert["annotations"]:
        newDescription = newDescription + alert["annotations"]["message"] + "\n\n"
      if "runbook_url" in alert["annotations"]:
        newDescription = newDescription \
                         + "[Runbook](" \
                         + alert["annotations"]["runbook_url"] \
                        + ")\n\n"

installInstructions = """
# Installing the alerts
## In Prometheus
Copy the alerts for Prometheus and paste them inside of the configuration file in the groups section:
```yaml
[...]
groups:
- name: example
    # Insert here the alerts
    rules: 
``` 
## In Sysdig Monitor
To install these alerts in Sysdig Monitor, contact with the support service. 
"""
newDescription += installInstructions

yamlFile["description"] = newDescription

outputformatted = pypromcat.dict2BeautyYaml(yamlFile)
if args.outputFile is None:
    print(outputformatted)
else:
    f = open(args.outputFile, "w")
    f.write(outputformatted)
    f.close()