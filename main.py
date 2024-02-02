from items import *
from Buildings import *
from graphviz import Digraph

# items and buildings
ITEMS = {
    "Ore 1": Ore_1(),
    "Ore 2": Ore_2(),
    "Material 1": Material_1(),
    "Material 2": Material_2(),
    "Material 3": Material_3(),
    "Material 4": Material_4(),
    "Material 5": Material_5(),
}
BUILDINGS = {
    "Miner": Miner(),
    "Smelter": Smelter()
}

class Items_vector():
    def __init__(self):
        # "index" : ["Item class", "amount used", "amount open", ["prev. Building"], ["next. Building"]]
        self.item_nodes = {}
        # "index" : ["building type", "building amount", ["prev. item"], ["next. item"]]
        self.building_nodes = {}

    # add Connection to vector
    def add_connection(self, items_in, items_out, building):
        # set variables
        not_covered = 1
        item_index = len(self.item_nodes)
        building_index = len(self.building_nodes)
        skip = False

        # handle output nodes
        for i_out, item_out in enumerate(items_out):
            # only if not skip
            if skip is False:
                # handle already existing node for item
                for dict_i, dict_val in self.item_nodes.items():
                    item, _, unused, prev, _ = dict_val
                    if item == item_out[0]:
                        # handle existing recipe
                        for build_id, build_node in zip(prev, [self.building_nodes[str(x)] for x in prev]):
                            if build_node[0] == building[0]:
                                # compare eixisting and new recipe
                                exi_input = [self.item_nodes[str(x)][0] for x in build_node[2]]
                                exi_output = [self.item_nodes[str(x)][0] for x in build_node[3]]

                                new_input = [item_in[0] for item_in in items_in]
                                new_output = [item_out[0] for item_out in items_out]

                                if exi_input == new_input and exi_output == new_output:
                                    # update output amount
                                    for out_i, out_item in enumerate(build_node[3]):
                                        self.item_nodes[str(out_item)][1 if items_out[out_i][2] else 2] += items_out[out_i][1]

                                    # update building node
                                    self.building_nodes[str(build_id)][1] += building[1]
                                    skip = True
                                    break
                        # handle existing node but different recipe
                        else:
                            # sufficient unused amount to cover recipe
                            if unused >= item_out[1]:
                                self.item_nodes[dict_i][2] -= item_out[1]
                                self.item_nodes[dict_i][1] += item_out[1]

                                return 0
                            # not sufficient unused amount to cover recipe / no unused amount
                            else:
                                # calculate building amount
                                building[1] = (1 - self.item_nodes[dict_i][2] / item_out[1])  * building[1]
                                # use unused amount
                                item_out[1] -= self.item_nodes[dict_i][2]
                                self.item_nodes[dict_i][1] += self.item_nodes[dict_i][2]
                                self.item_nodes[dict_i][2] = 0

                                # building node
                                if len(self.building_nodes) == building_index:
                                    building[3].append(int(dict_i))
                                    self.building_nodes.update({f"{building_index}": building})
                                else:
                                    self.building_nodes[f"{building_index}"][3].append(int(dict_i))
                                    self.building_nodes[f"{building_index}"][1] += building[1]

                                # item node
                                self.item_nodes[dict_i][3].append(building_index)
                                self.item_nodes[dict_i][1] += item_out[1]

                            break

                        # end loop if skip
                        if skip:
                            break
                # handle create a new node
                else:
                    # building node
                    if len(self.building_nodes) == building_index:
                        building[3].append(item_index)
                        self.building_nodes.update({f"{building_index}": building})
                    else:
                        self.building_nodes[f"{building_index}"][3].append(item_index)

                    # item node
                    used_amount = item_out[1] if item_out[2] else 0
                    unused_amount = item_out[1] - used_amount
                    item_param = [item_out[0], used_amount, unused_amount, [building_index], []]
                    self.item_nodes.update({f"{item_index}": item_param})
                    item_index += 1

        # handle input items
        if skip is False:
            for i_in, item_in in enumerate(items_in):
                # handle already existing node for item
                for dict_i, dict_val in self.item_nodes.items():
                    item, _, _, _, _ = dict_val
                    if item == item_in[0]:
                        self.building_nodes[f"{building_index}"][2].append(int(dict_i))
                        self.item_nodes[dict_i][4].append(building_index)
                        break
                # handle create a new node
                else:
                    self.building_nodes[f"{building_index}"][2].append(item_index)

                    # item node
                    self.item_nodes.update({f"{item_index}": [item_in[0], 0, 0, [], [building_index]]})
                    item_index += 1

        return not_covered

    # visualise vector
    def visualise(self):
        diagraph = Digraph()

        # add building nodes
        for key, value in self.building_nodes.items():
            diagraph.node(f"b{key}", f"{value[0]}, {value[1]}")

        # add item nodes
        for key, value in self.item_nodes.items():
            diagraph.node(f"i{key}", f"{value[0]().name[0]}, {value[1]}, {value[2]}")

            # prev. Items
            for prev_i in value[3]:
                diagraph.edge(f"b{prev_i}", f"i{key}")

            # next. Items
            for next_i in value[4]:
                diagraph.edge(f"i{key}", f"b{next_i}")

        # render diagraph
        diagraph.render("diagraph.gv", view=True)


def backprop(item, amount: float, vector: Items_vector):
    # set variables
    recipe = item.recipes[0]
    multiplayer = 1
    building_amount = 0

    # calculate multiplayer and building amount
    # single output
    if len(recipe["output"]) == 1:
        multiplayer = amount / recipe["output"][0][1]
        building_amount = amount / (recipe["output"][0][1] / recipe["manufacturing time"])
    # multiple outputs
    else:
        for output in recipe["output"]:
            if output[0]().name == item.name:
                multiplayer = amount / output[1]
                building_amount = amount / (output[1] / recipe["manufacturing time"])

                break

    # add to vector
    if recipe["manufacturing type"] != "mining":
        # items_in = [[item, amount]]
        items_in = [[input[0], input[1] * multiplayer] for input in recipe["input"]]
        # items_in = [[item, amount, used]]
        items_out = [[output[0], output[1] * multiplayer, True if type(output[0]()) == type(item) else False] for output in recipe["output"]]
        building = [recipe["manufacturing type"], building_amount, [], []]

        ret = vector.add_connection(items_in, items_out, building)
    # handle ores
    else:
        for input in recipe["output"]:
            for dict_i, dict_val in vector.item_nodes.items():
                if type(input[0]()) == type(dict_val[0]()):
                    vector.item_nodes[dict_i][1] += input[1] * multiplayer
                    break

    # backprop over inputs
    if recipe["manufacturing type"] != "mining" and ret > 0:
        for input in recipe["input"]:
            backprop(input[0](), input[1] * multiplayer * ret, vector)


if __name__ == '__main__':
    # backprop
    vector = Items_vector()
    backprop(ITEMS["Material 4"], 10, vector)
    backprop(ITEMS["Material 3"], 10, vector)
    vector.visualise()

