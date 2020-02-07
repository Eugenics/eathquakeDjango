import json
import requests


def get_json_data(date_from, date_till):
    #date_from = "2020-01-13"
    #date_till = "2020-01-14"

    response = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime="
                            + date_from + "&endtime="
                            + date_till + "&minmagnitude=2")

    #eathquakes_list = json.loads(response.text)
    

    return json.loads(response.text)

    # for eathquake_feature in eathquake_features:
    #        eathquake_properties = eathquake_feature["properties"]

    #       print(eathquake_properties["place"])

    # with open("data_file.json", "w") as write_file:
    #    json.dump(eathquakes_list, write_file)
# if __name__ == "__main__":
#    get_json_data()
