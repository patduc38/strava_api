# Parse the XML file
import xml.etree.ElementTree as ET

tree = ET.parse("Le_Mas_Julien.gpx")
#root = tree.getroot()

# Iterate through each child of the root element
#for child in root:
#    # Print the tag and attributes of each child element
#    print(child.tag, child.attrib)
#    print(child)


for node in tree.iter('trkpt'):
    name = node.attrib.get('lat')
    print(name)
    print("Pat add",node)




