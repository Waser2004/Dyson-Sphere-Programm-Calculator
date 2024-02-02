# ----
# Ores
# ----
class Ore_1(object):
    def __init__(self):
        # definitions
        self.name = "Ore 1",
        self.type = "Ore"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "mining",
                "manufacturing time": 1,  # in seconds
                "input": [],
                "output": [
                    [Ore_1, 5]
                ]
            }
        ]


class Ore_2(object):
    def __init__(self):
        # definitions
        self.name = "Ore 2",
        self.type = "Ore"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "mining",
                "manufacturing time": 1,  # in seconds
                "input": [],
                "output": [
                    [Ore_2, 4]
                ]
            }
        ]

# ---------
# Materials
# ---------
class Material_1(object):
    def __init__(self):
        # definitions
        self.name = "Material 1",
        self.type = "Material"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "smelting",
                "manufacturing time": 2,  # in seconds
                "input": [
                    [Ore_1, 2]
                ],
                "output": [
                    [Material_1, 2]
                ]
            }
        ]


class Material_2(object):
    def __init__(self):
        # definitions
        self.name = "Material 2",
        self.type = "Material"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "smelting",
                "manufacturing time": 1,  # in seconds
                "input": [
                    [Ore_2, 2]
                ],
                "output": [
                    [Material_2, 1]
                ]
            }
        ]

class Material_3(object):
    def __init__(self):
        # definitions
        self.name = "Material 3",
        self.type = "Material"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "smelting",
                "manufacturing time": 5,  # in seconds
                "input": [
                    [Ore_1, 2],
                    [Ore_2, 2]
                ],
                "output": [
                    [Material_3, 1]
                ]
            }
        ]

class Material_4(object):
    def __init__(self):
        # definitions
        self.name = "Material 4",
        self.type = "Material"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "manufacturing",
                "manufacturing time": 3,  # in seconds
                "input": [
                    [Material_2, 2],
                    [Material_1, 2]
                ],
                "output": [
                    [Material_3, 1],
                    [Material_4, 2]
                ]
            }
        ]


class Material_5(object):
    def __init__(self):
        # definitions
        self.name = "Material 5",
        self.type = "Material"

        # recipes
        self.recipes = [
            # recipe 1
            {
                "manufacturing type": "smelting",
                "manufacturing time": 6,  # in seconds
                "input": [
                    [Ore_1, 1],
                    [Material_1, 2]
                ],
                "output": [
                    [Material_5, 1],
                ]
            },
            # recipe 2
            {
                "manufacturing type": "smelting",
                "manufacturing time": 1,  # in seconds
                "input": [
                    [Ore_1, 2],
                    [Ore_2, 3],
                    [Material_1, 2],
                    [Material_3, 1],
                ],
                "output": [
                    [Material_5, 4],
                ]
            }
        ]