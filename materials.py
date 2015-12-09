#!/usr/bin/python -B

defmaterials = {}
# name, color, transparency, emittance

defmaterials[(1,0)] = {'name': 'stone', 'color': (0.7,0.7,0.7),'alpha':0,'emittance':0}
defmaterials[(1,1)] = {'name': 'Granite', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(1,2)] = {'name': 'Polished Granite', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(1,3)] = {'name': 'Diorite', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(1,4)] = {'name': 'Polished Diorite', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(1,5)] = {'name': 'Andesite', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(1,6)] = {'name': 'Polished Andesite', 'color': (1,1,1),'alpha':0,'emittance':0}

defmaterials[(2,0)] = {'name': 'grass', 'color': (0,0.8,0),'alpha':0,'emittance':0}

defmaterials[(3,0)] = {'name': 'dirt', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(3,1)] = {'name': 'Coarse Dirt', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(3,2)] = {'name': 'Podzol', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(4,0)] = {'name': 'cobblestone', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(5,0)] = {'name': 'Oak Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(5,1)] = {'name': 'Spruce Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(5,2)] = {'name': 'Birch Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(5,3)] = {'name': 'Jungle Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(5,4)] = {'name': 'Acacia Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(5,5)] = {'name': 'Dark Oak Wood Plank', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}


defmaterials[(6,0)] = {'name': 'Oak Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(6,1)] = {'name': 'Spruce Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(6,2)] = {'name': 'Birch Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(6,3)] = {'name': 'Jungle Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(6,4)] = {'name': 'Acacia Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}
defmaterials[(6,5)] = {'name': 'Dark Oak Sapling', 'color': (0.9,0.7,0.6),'alpha':0,'emittance':0}

defmaterials[(7,0)] = {'name': 'Bedrock', 'color': (0.2,0.2,0.2),'alpha':0,'emittance':0}

defmaterials[(8,0)] = {'name': 'Flowing Water', 'color': (0,0,1),'alpha':0.5,'emittance':0}
defmaterials[(9,0)] = {'name': 'Still Water', 'color': (0,0,1),'alpha':0.5,'emittance':0}
defmaterials[(10,0)] = {'name': 'Flowing Lava', 'color': (0.9,0.2,0.2),'alpha':0,'emittance':5}
defmaterials[(11,0)] = {'name': 'Still Lava', 'color': (0.9,0.2,0.2),'alpha':0,'emittance':5}

defmaterials[(12,0)] = {'name': 'Sand', 'color': (1,0.8,0.7),'alpha':0,'emittance':0}
defmaterials[(12,1)] = {'name': 'Red Sand', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}


defmaterials[(13,0)] = {'name': 'Gravel', 'color': (0.5,0.5,0.5),'alpha':0,'emittance':0}
defmaterials[(14,0)] = {'name': 'Gold Ore', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(15,0)] = {'name': 'Iron Ore', 'color': (0.6,0.5,0.4),'alpha':0,'emittance':0}
defmaterials[(16,0)] = {'name': 'Coal Ore', 'color': (0.4,0.4,0.4),'alpha':0,'emittance':0}

defmaterials[(17,0)] = {'name': 'Oak Wood', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(17,1)] = {'name': 'Spruce Wood', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(17,2)] = {'name': 'Birch Wood', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(17,3)] = {'name': 'Jungle Wood', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(18,0)] = {'name': 'Oak Leaves', 'color': (0,0.8,0),'alpha':0,'emittance':0}
defmaterials[(18,1)] = {'name': 'Spruce Leaves', 'color': (0,0.8,0),'alpha':0,'emittance':0}
defmaterials[(18,2)] = {'name': 'Birch Leaves', 'color': (0,0.8,0),'alpha':0,'emittance':0}
defmaterials[(18,3)] = {'name': 'Jungle Leaves', 'color': (0,0.8,0),'alpha':0,'emittance':0}


defmaterials[(19,0)] = {'name': 'Sponge', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(19,1)] = {'name': 'Wet Sponge', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(20,0)] = {'name': 'Glass', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(21,0)] = {'name': 'Lapis Lazuli Ore', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(22,0)] = {'name': 'Lapis Lazuli Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(23,0)] = {'name': 'Dispenser', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(24,0)] = {'name': 'Sandstone', 'color': (1,0.8,0.7),'alpha':0,'emittance':0}
defmaterials[(24,1)] = {'name': 'Chiseled Sandstone', 'color': (1,0.8,0.7),'alpha':0,'emittance':0}
defmaterials[(24,2)] = {'name': 'Smooth Sandstone', 'color': (1,0.8,0.7),'alpha':0,'emittance':0}


defmaterials[(25,0)] = {'name': 'Note Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(26,0)] = {'name': 'Bed', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(27,0)] = {'name': 'Powered Rail', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(28,0)] = {'name': 'Detector Rail', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(29,0)] = {'name': 'Sticky Piston', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(30,0)] = {'name': 'Cobweb', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(31,0)] = {'name': 'Dead Shrub', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(31,1)] = {'name': 'Grass', 'color': (0,0.8,0),'alpha':0,'emittance':0}
defmaterials[(31,2)] = {'name': 'Fern', 'color': (0,0.8,0),'alpha':0,'emittance':0}

defmaterials[(32,0)] = {'name': 'Dead Bush', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(33,0)] = {'name': 'Piston', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(34,0)] = {'name': 'Piston Head', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(35,0)] = {'name': 'White Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,1)] = {'name': 'Orange Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,2)] = {'name': 'Magenta Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,3)] = {'name': 'Light Blue Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,4)] = {'name': 'Yellow Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,5)] = {'name': 'Lime Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,6)] = {'name': 'Pink Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,7)] = {'name': 'Gray Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,8)] = {'name': 'Light Gray Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,9)] = {'name': 'Cyan Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,10)] = {'name': 'Purple Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,11)] = {'name': 'Blue Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,12)] = {'name': 'Brown Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,13)] = {'name': 'Green Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,14)] = {'name': 'Red Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(35,15)] = {'name': 'Black Wool', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(37,0)] = {'name': 'Dandelion', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(38,0)] = {'name': 'Poppy', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,1)] = {'name': 'Blue Orchid', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,2)] = {'name': 'Allium', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,3)] = {'name': 'Azure Bluet', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,4)] = {'name': 'Red Tulip', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,5)] = {'name': 'Orange Tulip', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,6)] = {'name': 'White Tulip', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,7)] = {'name': 'Pink Tulip', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(38,8)] = {'name': 'Oxeye Daisy', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(39,0)] = {'name': 'Brown Mushroom', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(40,0)] = {'name': 'Red Mushroom', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(41,0)] = {'name': 'Gold Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(42,0)] = {'name': 'Iron Block', 'color': (0.7,0.7,0.7),'alpha':0,'emittance':0}

defmaterials[(43,0)] = {'name': 'Double Stone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,1)] = {'name': 'Double Sandstone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,2)] = {'name': 'Double Wooden Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,3)] = {'name': 'Double Cobblestone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,4)] = {'name': 'Double Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,5)] = {'name': 'Double Stone Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,6)] = {'name': 'Double Nether Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(43,7)] = {'name': 'Double Quartz Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(44,0)] = {'name': 'Stone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,1)] = {'name': 'Sandstone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,2)] = {'name': 'Wooden Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,3)] = {'name': 'Cobblestone Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,4)] = {'name': 'Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,5)] = {'name': 'Stone Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,6)] = {'name': 'Nether Brick Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(44,7)] = {'name': 'Quartz Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(45,0)] = {'name': 'Bricks', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(46,0)] = {'name': 'TNT', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(47,0)] = {'name': 'Bookshelf', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(48,0)] = {'name': 'Moss Stone', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(49,0)] = {'name': 'Obsidian', 'color': (0,0,0.2),'alpha':0,'emittance':0}
defmaterials[(50,0)] = {'name': 'Torch', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':5}
defmaterials[(51,0)] = {'name': 'Fire', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':5}

defmaterials[(52,0)] = {'name': 'Monster Spawner', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(53,0)] = {'name': 'Oak Wood Stairs', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(54,0)] = {'name': 'Chest', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(55,0)] = {'name': 'Redstone Wire', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(56,0)] = {'name': 'Diamond Ore', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(57,0)] = {'name': 'Diamond Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(58,0)] = {'name': 'Crafting Table', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(59,0)] = {'name': 'Wheat Crops', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(60,0)] = {'name': 'Farmland', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(61,0)] = {'name': 'Furnace', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(62,0)] = {'name': 'Burning Furnace', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':4}
defmaterials[(63,0)] = {'name': 'Standing Sign Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(64,0)] = {'name': 'Oak Door Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(65,0)] = {'name': 'Ladder', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(66,0)] = {'name': 'Rail', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(67,0)] = {'name': 'Cobblestone Stairs', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(68,0)] = {'name': 'Wall-mounted Sign Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(69,0)] = {'name': 'Lever', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(70,0)] = {'name': 'Stone Pressure Plate', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(71,0)] = {'name': 'Iron Door Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(72,0)] = {'name': 'Wooden Pressure Plate', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(73,0)] = {'name': 'Redstone Ore', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(74,0)] = {'name': 'Glowing Redstone Ore', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(75,0)] = {'name': 'Redstone Torch (off)', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(76,0)] = {'name': 'Redstone Torch (on)', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(77,0)] = {'name': 'Stone Button', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(78,0)] = {'name': 'Snow', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(79,0)] = {'name': 'Ice', 'color': (0.4,0.4,1),'alpha':0.2,'emittance':0}
defmaterials[(80,0)] = {'name': 'Snow Block', 'color': (1,1,1),'alpha':0,'emittance':0}
defmaterials[(81,0)] = {'name': 'Cactus', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(82,0)] = {'name': 'Clay', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(83,0)] = {'name': 'Sugar Canes', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(84,0)] = {'name': 'Jukebox', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(85,0)] = {'name': 'Oak Fence', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(86,0)] = {'name': 'Pumpkin', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(87,0)] = {'name': 'Netherrack', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(88,0)] = {'name': 'Soul Sand', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(89,0)] = {'name': 'Glowstone', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':5}
defmaterials[(90,0)] = {'name': 'Nether Portal', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(91,0)] = {'name': 'Jack oLantern', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':5}
defmaterials[(92,0)] = {'name': 'Cake Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(93,0)] = {'name': 'Redstone Repeater Block (off)', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(94,0)] = {'name': 'Redstone Repeater Block (on)', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(95,0)] = {'name': 'White Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,1)] = {'name': 'Orange Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,2)] = {'name': 'Magenta Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,3)] = {'name': 'Light Blue Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,4)] = {'name': 'Yellow Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,5)] = {'name': 'Lime Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,6)] = {'name': 'Pink Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,7)] = {'name': 'Gray Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,8)] = {'name': 'Light Gray Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,9)] = {'name': 'Cyan Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,10)] = {'name': 'Purple Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,11)] = {'name': 'Blue Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,12)] = {'name': 'Brown Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,13)] = {'name': 'Green Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,14)] = {'name': 'Red Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}
defmaterials[(95,15)] = {'name': 'Black Stained Glass', 'color': (1, 0.627451, 0.478431),'alpha':0.5,'emittance':0}

defmaterials[(96,0)] = {'name': 'Wooden Trapdoor', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(97,0)] = {'name': 'Stone Monster Egg', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}
defmaterials[(97,1)] = {'name': 'Cobblestone Monster Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(97,2)] = {'name': 'Stone Brick Monster Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(97,3)] = {'name': 'Mossy Stone Brick Monster Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(97,4)] = {'name': 'Cracked Stone Brick Monster Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(97,5)] = {'name': 'Chiseled Stone Brick Monster Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(98,0)] = {'name': 'Stone Bricks', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}
defmaterials[(98,1)] = {'name': 'Mossy Stone Bricks', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}
defmaterials[(98,2)] = {'name': 'Cracked Stone Bricks', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}
defmaterials[(98,3)] = {'name': 'Chiseled Stone Bricks', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}

defmaterials[(99,0)] = {'name': 'Brown Mushroom Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(100,0)] = {'name': 'Red Mushroom Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(101,0)] = {'name': 'Iron Bars', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(102,0)] = {'name': 'Glass Pane', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(103,0)] = {'name': 'Melon Block', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(104,0)] = {'name': 'Pumpkin Stem', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(105,0)] = {'name': 'Melon Stem', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(106,0)] = {'name': 'Vines', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(107,0)] = {'name': 'Oak Fence Gate', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(108,0)] = {'name': 'Brick Stairs', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(109,0)] = {'name': 'Stone Brick Stairs', 'color': (0.3,0.3,0.3),'alpha':0,'emittance':0}
defmaterials[(110,0)] = {'name': 'Mycelium', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(111,0)] = {'name': 'Lily Pad', 'color': (0,0.8,0),'alpha':0,'emittance':0}
defmaterials[(112,0)] = {'name': 'Nether Brick', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(113,0)] = {'name': 'Nether Brick Fence', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(114,0)] = {'name': 'Nether Brick Stairs', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(115,0)] = {'name': 'Nether Wart', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(116,0)] = {'name': 'Enchantment Table', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(117,0)] = {'name': 'Brewing Stand', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(118,0)] = {'name': 'Cauldron', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(119,0)] = {'name': 'End Portal', 'color': (0.627451, 0.12549, 0.941176),'alpha':0,'emittance':0}
defmaterials[(120,0)] = {'name': 'End Portal Frame', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(121,0)] = {'name': 'End Stone', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(122,0)] = {'name': 'Dragon Egg', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(123,0)] = {'name': 'Redstone Lamp (inactive)', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':0}
defmaterials[(124,0)] = {'name': 'Redstone Lamp (active)', 'color': (0.9,0.9,0.2),'alpha':0,'emittance':5}

defmaterials[(125,0)] = {'name': 'Double Oak Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(125,1)] = {'name': 'Double Spruce Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(125,2)] = {'name': 'Double Birch Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(125,3)] = {'name': 'Double Jungle Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(125,4)] = {'name': 'Double Acacia Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(125,5)] = {'name': 'Double Dark Oak Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}

defmaterials[(126,0)] = {'name': 'Oak Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(126,1)] = {'name': 'Spruce Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(126,2)] = {'name': 'Birch Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(126,3)] = {'name': 'Jungle Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(126,4)] = {'name': 'Acacia Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}
defmaterials[(126,5)] = {'name': 'Dark Oak Wood Slab', 'color': (1, 0.627451, 0.478431),'alpha':0,'emittance':0}