import json
import xmltodict

file_path = "sample.xml"

with open(file_path) as xml_file:
    data_dict = xmltodict.parse(xml_file.read(), encoding="utf-8")
    xml_file.close()

    # generate the object using json.dumps()
    # corresponding to json data, but as a string, to be stored in a file

    json_data = json.dumps(data_dict)
    print(json.loads(json_data)["doc"]["plot"])

    # # Write the json data to output
    # # json file
    # with open("sample.json", "w") as json_file:
    #     json_file.write(json_data)
    #     json_file.close()
