from mdrModule import mdr
from mdrModule import utils
import re
import requests
from lxml import etree
import json

url_list = [
    "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSDF15D356B046D53BC1256D550038A9E0?OpenDocument&wg=U1232&refDoc=CMS322921A477B31844C125707B0034EB15",
    "https://www.digikey.com/products/en/integrated-circuits-ics/embedded-fpgas-field-programmable-gate-array-with-microcontrollers/767",
    "https://www.nxp.com/products/processors-and-microcontrollers/arm-based-processors-and-mcus/lpc-cortex-m-mcus/lpc800-series-cortex-m0-plus-mcus:MC_71785",
    "https://global.epson.com/products_and_drivers/semicon/products/micro_controller/16bit/#ac01",
    "http://www.firmcodes.com/microcontrollers/8051-3/features-of-8051-microcontroller/",
    "https://www.engineersgarage.com/8051-microcontroller",
    "https://www.robotshop.com/en/microcontrollers.html",
    "https://www.electroncomponents.com/Integrated-Circuits/Microcontroller",
    "https://www.jameco.com/shop/keyword=Buy-Transistors",
    "https://www.allelectronics.com/category/793/transistors/1.html",
    "https://www.rohm.com/new-products-listing/?nodecode=2020&period=180",
    "https://www.futureelectronics.com/c/semiconductors/discretes--transistors--general-purpose-transistors/products"
]

refer_url_list = [
    "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSF52334E11D475306C125707B00358DA1?OpenDocument",
    "https://www.digikey.com/products/en/integrated-circuits-ics/interface-analog-switches-special-purpose/780",
    "https://www.nxp.com/products/processors-and-microcontrollers/arm-based-processors-and-mcus/lpc-cortex-m-mcus/lpc54000-series-cortex-m4-mcus:MC_1414576688124",
    "https://global.epson.com/products_and_drivers/semicon/products/micro_controller/8bit/",
    "http://www.firmcodes.com/microcontrollers/8051-3/led-interfacing-with-8051/",
    "https://www.engineersgarage.com/article/choosing-motor-robots",
    "https://www.robotshop.com/en/cables-wires-connectors-en.html",
    "https://www.electroncomponents.com/Mini-Components",
    "https://www.jameco.com/c/ICs-Semiconductors.html",
    "https://www.allelectronics.com/category/193/connectors-ac-power/1.html",
    "https://www.rohm.com/new-products-listing/?nodecode=2020&period=180",
    "https://www.futureelectronics.com/c/semiconductors/analog--power-switches/products"

]

if __name__ == "__main__":
    index = 11

    mdr = mdr.MDR()

    # tree = mdr.parse_page(url_list[index])

    # refer_tree = mdr.parse_page(refer_url_list[index])

    # print("Different page running...")

    # for child in tree.getroot().iter():
    #     has_found = False

    #     for refer_child in refer_tree.getroot().iter():
    #         if utils.cmp_elements(child, refer_child):
    #             has_found = True
    #             break

    #     if not has_found:
    #         child.set("is_unique_node", "true")
    
    # print("MDR running...")

    # candidates, doc = mdr.list_candidates(tree)

    print("MDR running...")

    refer_r = requests.get(refer_url_list[index])
    refer_tree = mdr.parse_page(refer_r.text.encode("utf8"), encoding="utf8")
    
    r = requests.get(url_list[index])
    candidates, tree = mdr.list_candidates(r.text.encode("utf8"), encoding="utf8")

    print("Different page running...")

    unique_el_dict = {}

    for child in tree.getroot().iter():
        has_found = False

        for refer_child in refer_tree.getroot().iter():
            if utils.cmp_elements(child, refer_child):
                has_found = True
                break

        if not has_found:
            # child.set("is_unique_node", "true")
            # unique_el_list.append(child)
            # if child.keys(len(child.keys - 1))
            
            # if "is_unique_node" not in child.keys():
            #     identifier = etree.SubElement(child, "div")
            #     identifier.set("is_unique_node","true")

            #     for c in child.iterchildren():
            #         print(c.keys())

            #     print("------------------")

            unique_el_dict[tree.getpath(child)] = "true"

    print("Partial tree alignment running...")

    curr_url = url_list[index]

    file_url = re.sub('[\\/:*?"<>|]', "", curr_url)

    str_ctrl_re = re.compile(r'[\n\r\t]')

    with open("output/" + file_url + ".json", "w") as json_file:
        all_tables = []

        for c in candidates:
            table = []

            # print(doc.getpath(c))

            seed, mappings = mdr.extract(c)

            # print(seed)

            if seed != None:
                row = []

                for el in seed:
                    col = []

                    for child in el.iter():
                        if child.tag != "script" and child.text != None:                            
                            # text_file.write(child.text.encode('utf-8') + "| " + "")
                            col.append(str_ctrl_re.sub(' ', child.text))

                    row.append(col)

                # text_file.write("\n")
                table.append(row)
            
            for mapping in mappings:
                row = []

                for el in mapping:
                    col = []

                    child_list = el.iter()

                    # has_unique_found = False

                    # for child in child_list:
                    #     if tree.getpath(child) in unique_el_dict:
                    #         has_unique_found = True
                    #         break

                    # if has_unique_found:
                    #     for child in child_list:
                    #         if child.tag != "script" and child.text != None:                                
                    #             # text_file.write(child.text.encode('utf-8') + "| " + "")
                    #             col.append(str_ctrl_re.sub(' ', child.text))

                    #         if child.tag == "a" and child.get("href") != None:
                    #             # text_file.write(child.get("href").encode('utf-8') + "| " + "")
                    #             col.append(str_ctrl_re.sub(' ', child.get("href")))

                    for child in child_list:
                        if tree.getpath(child) in unique_el_dict:
                            if child.tag != "script" and child.text != None:                                
                                # text_file.write(child.text.encode('utf-8') + "| " + "")
                                col.append(str_ctrl_re.sub(' ', child.text))

                            if child.tag == "a" and child.get("href") != None:
                                # text_file.write(child.get("href").encode('utf-8') + "| " + "")
                                col.append(str_ctrl_re.sub(' ', child.get("href")))                        

                    row.append(col)

                # text_file.write("\n")
                table.append(row)

            # text_file.write("-----------------------------")

            all_tables.append(table)

        json.dump(all_tables, json_file)

    # seed, mappings = mdr.extract(candidates[0])

    # print(seed)
    
    # for mapping in mappings:
    #     for el in mapping:
    #         print el.text,

    #     print("\n")
