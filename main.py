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
    "https://www.futureelectronics.com/c/semiconductors/discretes--transistors--general-purpose-transistors/products",
    "https://my.mouser.com/Semiconductors/Integrated-Circuits-ICs/_/N-6j73k/",
    "http://www.yageo.com/NewPortal/yageo?service=chipResistors&layer2=Thick%20Film%20Precision&lang=en",
    "https://www.murata.com/en-us/products/resistor/highvoltage/mhr",
    "https://www.avnet.com/shop/apac/c/capacitors/film-paper-capacitors/?pageNumber=1&pageSize=20",
    "https://www3.panasonic.biz/ac/spec/panasonic_ac/ae_fiber/ae_fiber/",
    "https://ds.yuden.co.jp/TYCOMPAS/or/specificationSearcher?SR2=MP&cid=L&u=M",
    "https://product.tdk.com/info/en/products/inductor/catalog.html",
    "http://www.samsungsem.com/global/support/product-search/index.jsp",
    "http://www.pdc.com.tw/product/diodege-eng.html",
    "http://www.passivecomponent.com/se-chip.asp",
    "http://www.kamaya.co.jp/detail.php?id=97",
    "http://www.koaspeer.com/products/thermal-protection/surface-mount-thermal-sensors/nt73/",
    "https://www.walmart.com/search/?query=laptop",
    "https://www.newegg.com/Laptops-Notebooks/Category/ID-223?Tpk=laptop",
    "https://www.etsy.com/c/clothing-and-shoes?ref=catnav-10923",
]

refer_url_list = [
    "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSF52334E11D475306C125707B00358DA1?OpenDocument", # 0
    "https://www.digikey.com/products/en/integrated-circuits-ics/interface-analog-switches-special-purpose/780", # 1
    "https://www.nxp.com/products/processors-and-microcontrollers/arm-based-processors-and-mcus/lpc-cortex-m-mcus/lpc54000-series-cortex-m4-mcus:MC_1414576688124", # 2
    "https://global.epson.com/products_and_drivers/semicon/products/micro_controller/8bit/", # 3
    "http://www.firmcodes.com/microcontrollers/8051-3/led-interfacing-with-8051/", # 4
    "https://www.engineersgarage.com/article/choosing-motor-robots", # 5
    "https://www.robotshop.com/en/cables-wires-connectors-en.html", # 6
    "https://www.electroncomponents.com/Mini-Components", # 7
    "https://www.jameco.com/c/ICs-Semiconductors.html", # 8
    "https://www.allelectronics.com/category/193/connectors-ac-power/1.html", # 9
    "https://www.rohm.com/new-products-listing/?nodecode=2020&period=180", # 10
    "https://www.futureelectronics.com/c/semiconductors/analog--power-switches/products", # 11
    "https://my.mouser.com/Semiconductors/Integrated-Circuits-ICs/Amplifier-ICs/_/N-6j73l/", # 12
    "http://www.yageo.com/NewPortal/yageo?service=mlcc&layer2=High%20Voltage&lang=en", # 13
    "https://www.murata.com/en-us/products/sensor/infrared/ira", # 14
    "https://www.avnet.com/shop/apac/c/discretes/diodes/rectifier-diodes/", # 15
    "https://www3.panasonic.biz/ac/spec/panasonic_ac/ae_swi_lt/ae_swi_lt/", # 16
    "https://ds.yuden.co.jp/TYCOMPAS/or/specificationSearcher?SR2=MP&cid=C&u=M", # 17
    "https://product.tdk.com/info/en/products/capacitor/catalog.html", # 18
    "http://www.samsungsem.com/global/product/passive-component/chip-resistor/general-resistor/index.jsp", # 19
    "http://www.pdc.com.tw/product/chipge-eng.html", # 20
    "http://www.passivecomponent.com/se-inductor.asp", # 21
    "http://www.kamaya.co.jp/detail.php?id=82", # 22
    "http://www.koaspeer.com/products/resistors/surface-mount-resistors/rk73b/", # 23
    "https://www.walmart.com/search/?query=phone", # 24
    "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=phone&N=-1&isNodeId=1", # 25
    "https://www.etsy.com/c/toys-and-entertainment?ref=catnav-11049", # 26
]

if __name__ == "__main__":
    index = 27

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

    threshold = 0.9
    highest_unique_count = 0
    highest_count_table = None

    while True:
        print("Running MDR with threshold = ", threshold, "...")

        mdrM = None
        mdrM = mdr.MDR(threshold=threshold)

        refer_r = requests.get(refer_url_list[index])
        refer_tree = mdrM.parse_page(refer_r.text.encode("utf8"), encoding="utf8")
        
        r = requests.get(url_list[index])
        candidates, tree = mdrM.list_candidates(r.text.encode("utf8"), encoding="utf8")

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

        str_ctrl_re = re.compile(r'[\n\r\t]')
        
        all_tables = []

        row_count_list = []
        unique_count_list = []

        for c in candidates:
            table = []

            # print(doc.getpath(c))

            seed, mappings = mdrM.extract(c)

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

            unique_count = 0
            
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
                                unique_count += 1

                            if child.tag == "a" and child.get("href") != None:
                                # text_file.write(child.get("href").encode('utf-8') + "| " + "")
                                col.append(str_ctrl_re.sub(' ', child.get("href")))                        
                                unique_count += 1

                    row.append(col)

                # text_file.write("\n")
                table.append(row)

            # text_file.write("-----------------------------")

            unique_count_list.append(unique_count)

            curr_row_count = 0

            for row in table:
                if not utils.is_list_empty(row):
                    curr_row_count += 1

            row_count_list.append(curr_row_count)

            all_tables.append(table)

        highest_index, highest_count = 0, 0

        for i, row_count in enumerate(row_count_list):
            # print(row_count, unique_count_list[i])
            if row_count > highest_count:
                highest_count = row_count
                highest_index = i

        print("Current highest: ", highest_count, unique_count_list[highest_index])

        if unique_count_list[highest_index] > highest_unique_count:
            highest_unique_count = unique_count_list[highest_index]
            highest_count_table = all_tables[highest_index][:]
        else:
            break

        threshold -= 0.1

    print("Selected: ", highest_unique_count)

    curr_url = url_list[index]

    file_url = re.sub('[\\/:*?"<>|]', "", curr_url)
    # file_url = re.sub('[^\w_.)( -]', '', curr_url)

    with open("output/" + file_url + ".json", "w") as json_file:
        json.dump(highest_count_table, json_file)        

    # seed, mappings = mdr.extract(candidates[0])

    # print(seed)
    
    # for mapping in mappings:
    #     for el in mapping:
    #         print el.text,

    #     print("\n")
