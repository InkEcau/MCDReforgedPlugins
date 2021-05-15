# -*- coding: UTF-8 -*-
import json
import os
import time
from io import BytesIO

import numpy as np  
import requests
from mcdreforged.api.all import *
from nbt import nbt
from PIL import Image

PLUGIN_METADATA = {
	'id': 'mapitem',
	'version': '1.0.0',
	'name': 'mapitem',
	'description': '生成地图物品',
	'author': 'InkEcau',
	'link': 'https://github.com/InkEcau/MCDReforgedPlugins/Mapitem',
	'dependencies': {
	    'mcdreforged': '>=1.0.0',
	}
}

# !!mapitem create https://crafatar.com/avatars/e4fa59f5f34b41cca62bdd77b652fbb2?size=128&overlay -d

config_path = "./config/mapitem/"
Prefix = '!!mapitem'
help_message = '''
MCDR {1}插件: {2}
详情请见Github页面
↓ 食用方法 ↓

§7{0}§r §6<command> §7[options]

§8Commands:
    §7create§r 从URL生成地图物品，需要提供§bURL
    §7list§r 获取地图画列表
    §7get§r 从已有地图文件中获取地图物品，需要提供§bID
    §7info§r 获得地图画的详细信息，需要提供§bID

§8Options:
    §7-h --help§r 获取帮助
    §6[create]
    §7-d --details§r 显示工作细节
    §7--width §b<width>§r 指定地图画宽度
    §7--height §b<height>§r 指定地图画高度
    §7--remark §b<remark>§r 备注信息
'''.format(Prefix, PLUGIN_METADATA['name'], PLUGIN_METADATA['description'])

# 所有地图色
allcolors = {
    (0, 0, 0): 0, (0, 0, 0): 1, (0, 0, 0): 2, (0, 0, 0): 3, 
    (90, 126, 40): 4, (110, 154, 48): 5, (127, 178, 56): 6, (67, 94, 30): 7, 
    (174, 164, 115): 8, (213, 201, 141): 9, (247, 233, 163): 10, (131, 123, 86): 11,
    (140, 140, 140): 12, (172, 172, 172): 13, (199, 199, 199): 14, (105, 105, 105): 15,
    (180, 0, 0): 16, (220, 0, 0): 17, (255, 0, 0): 18, (135, 0, 0): 19,
    (113, 113, 180): 20, (138, 138, 220): 21, (160, 160, 255): 22, (85, 85, 135): 23,
    (118, 118, 118): 24, (144, 144, 144): 25, (167, 167, 167): 26, (88, 88, 88): 27,
    (0, 88, 0): 28, (0, 107, 0): 29, (0, 124, 0): 30, (0, 66, 0): 31,
    (180, 180, 180): 32, (220, 220, 220): 33, (255, 255, 255): 34, (135, 135, 135): 35,
    (116, 119, 130): 36, (141, 145, 159): 37, (164, 168, 184): 38, (87, 89, 97): 39,
    (107, 77, 54): 40, (130, 94, 66): 41, (151, 109, 77): 42, (80, 58, 41): 43,
    (79, 79, 79): 44, (97, 97, 97): 45, (112, 112, 112): 46, (59, 59, 59): 47,
    (45, 45, 180): 48, (55, 55, 220): 49, (64, 64, 255): 50, (34, 34, 135): 51,
    (101, 84, 51): 52, (123, 103, 62): 53, (143, 119, 72): 54, (76, 63, 38): 55,
    (180, 178, 173): 56, (220, 217, 211): 57, (255, 252, 245): 58, (135, 133, 130): 59,
    (152, 90, 36): 60, (186, 110, 44): 61, (216, 127, 51): 62, (114, 67, 27): 63,
    (126, 54, 152): 64, (154, 66, 186): 65, (178, 76, 216): 66, (94, 40, 114): 67,
    (72, 108, 152): 68, (88, 132, 186): 69, (102, 153, 216): 70, (54, 81, 114): 71,
    (162, 162, 36): 72, (198, 198, 44): 73, (229, 229, 51): 74, (121, 121, 27): 75,
    (90, 144, 18): 76, (110, 176, 22): 77, (127, 204, 25): 78, (67, 108, 13): 79,
    (171, 90, 116): 80, (209, 110, 142): 81, (242, 127, 165): 82, (128, 67, 87): 83,
    (54, 54, 54): 84, (66, 66, 66): 85, (76, 76, 76): 86, (40, 40, 40): 87,
    (108, 108, 108): 88, (132, 132, 132): 89, (153, 153, 153): 90, (81, 81, 81): 91,
    (54, 90, 108): 92, (66, 110, 132): 93, (76, 127, 153): 94, (40, 67, 81): 95,
    (90, 44, 126): 96, (110, 54, 154): 97, (127, 63, 178): 98, (67, 33, 94): 99,
    (36, 54, 126): 100, (44, 66, 154): 101, (51, 76, 178): 102, (27, 40, 94): 103,
    (72, 54, 36): 104, (88, 66, 44): 105, (102, 76, 51): 106, (54, 40, 27): 107,
    (72, 90, 36): 108, (88, 110, 44): 109, (102, 127, 51): 110, (54, 67, 27): 111,
    (108, 36, 36): 112, (132, 44, 44): 113, (153, 51, 51): 114, (81, 27, 27): 115,
    (18, 18, 18): 116, (22, 22, 22): 117, (25, 25, 25): 118, (13, 13, 13): 119,
    (176, 168, 54): 120, (216, 205, 66): 121, (250, 238, 77): 122, (132, 126, 41): 123,
    (65, 155, 150): 124, (79, 189, 184): 125, (92, 219, 213): 126, (49, 116, 113): 127,
    (52, 90, 180): 128, (64, 110, 220): 129, (74, 128, 255): 130, (39, 68, 135): 131,
    (0, 153, 41): 132, (0, 187, 50): 133, (0, 217, 58): 134, (0, 115, 31): 135,
    (91, 61, 35): 136, (111, 74, 42): 137, (129, 86, 49): 138, (68, 46, 26): 139,
    (79, 1, 0): 140, (97, 2, 0): 141, (112, 2, 0): 142, (59, 1, 0): 143,
    (148, 125, 114): 144, (180, 153, 139): 145, (209, 177, 161): 146, (111, 94, 85): 147,
    (112, 58, 25): 148, (137, 71, 31): 149, (159, 82, 36): 150, (84, 43, 19): 151,
    (105, 61, 76): 152, (129, 75, 93): 153, (149, 87, 108): 154, (79, 46, 57): 155,
    (79, 76, 97): 156, (97, 93, 119): 157, (112, 108, 138): 158, (59, 57, 73): 159, 
    (131, 94, 25): 160, (160, 115, 31): 161, (186, 133, 36): 162, (98, 70, 19): 163,
    (73, 83, 37): 164, (89, 101, 46): 165, (103, 117, 53): 166, (55, 62, 28): 167,
    (113, 54, 55): 168, (138, 66, 67): 169, (160, 77, 78): 170, (85, 41, 41): 171,
    (40, 29, 25): 172, (49, 35, 30): 173, (57, 41, 35): 174, (30, 22, 19): 175,
    (95, 76, 69): 176, (116, 92, 85): 177, (135, 107, 98): 178, (71, 57, 52): 179,
    (61, 65, 65): 180, (75, 79, 79): 181, (87, 92, 92): 182, (46, 49, 49): 183,
    (86, 52, 62): 184, (105, 63, 76): 185, (122, 73, 88): 186, (65, 39, 47): 187,
    (54, 44, 65): 188, (66, 53, 79): 189, (76, 62, 92): 190, (40, 33, 49): 191,
    (54, 35, 25): 192, (66, 43, 30): 193, (76, 50, 35): 194, (40, 26, 19): 195,
    (54, 58, 30): 196, (66, 71, 36): 197, (76, 82, 42): 198, (40, 43, 22): 199,
    (100, 42, 32): 200, (123, 52, 40): 201, (142, 60, 46): 202, (75, 32, 24): 203,
    (26, 16, 11): 204, (32, 19, 14): 205, (37, 22, 16): 206, (20, 12, 8): 207
    #(133, 34, 35): 208, (163, 41, 42): 209, (189, 48, 49): 210, (100, 25, 26): 211,
    #(104, 44, 68): 212, (128, 54, 84): 213, (148, 63, 97): 214, (78, 33, 51): 215,
    #(65, 18, 20): 216, (79, 22, 25): 217, (92, 25, 29): 218, (49, 13, 15): 219,
    #(16, 89, 95): 220, (19, 109, 116): 221, (22, 126, 134): 222, (12, 67, 71): 223,
    #(41, 100, 99): 224, (50, 123, 121): 225, (58, 142, 140): 226, (31, 75, 74): 227,
    #(61, 31, 44): 228, (74, 38, 53): 229, (86, 44, 62): 230, (46, 23, 33): 231,
    #(14, 127, 94): 232, (17, 155, 115): 233, (20, 180, 133): 234, (11, 95, 70): 235
}

config = {}
maplist = {}


'''
配置 - start
'''
def config():
    global config, maplist
    default_config = {
        "permission": 3,
        "data_path": "./server/world/data/",
        "save_temp": True,
        "temp_filepath": "./config/mapitem/temp/",
        "item_per_page": 8
    }
    default_map_list = {
        "next_mapid": 2147483646,
        "next_id": 0,
        "map_list":[]
    }
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.exists(config_path + "temp/"):
        os.makedirs(config_path + "temp/")

    config = read_config(config_path + "mapitem.json")
    if config == None:
        update_config(config_path + "mapitem.json", default_config)
        config = default_config
    
    maplist = read_config(config_path + "maplist.json")
    if maplist == None:
        update_config(config_path + "maplist.json", default_map_list)
        maplist = default_map_list
    
# 读取json配置文件
def read_config(path):
    try:
        with open(path) as json_file:
            config = json.load(json_file)
        return config
    except:
        open(path, 'w')
        return None

# 更新json配置文件
def update_config(path, config):
    with open(path, 'w') as json_file:
        json.dump(config, json_file, indent=4)

'''
配置 - end
'''

'''
图片处理 - start
'''
# 下载图片
def download_image(server, info, url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            server.reply(info, "网络错误(状态码:{}). §7若无法自行解决，请报告管理员".format(r.status_code)) 
            return None
        return r.content
    except:
        server.reply(info, "URL错误")
        return None

# 切图 
def cut_image(image, line, column):
    pw = image.size[0] / column
    ph = image.size[1] / line
    box_list=[]
    for i in range(line):
        for j in range(column):
            box_list.append((i*ph, j*pw, (i+1)*ph, (j+1)*pw))
        image_list = [image.crop(box) for box in box_list]
    return image_list

# 保存image_list中的图片
def save_images(path, image_list):
    index = 1
    file_list = []
    for image in image_list:
        image.save(path.format(index), 'PNG')
        file_list.append(path.format(index))
        index += 1
    return file_list

# 寻找最近颜色
def nearest_color_id(color):
    return allcolors.get(min( allcolors, key = lambda allcolors: sum( (s - q) ** 2 for s, q in zip( allcolors, color ) ) ))

# 将图片数据转化为bytearray
def to_barray(image):
    img=np.array(image.resize((128, 128)))
    ba = bytearray(16384)
    i = 0
    for cs in img:
        for c in cs:
            ba[i] = nearest_color_id(tuple(c))
            i += 1
    return ba

# 将数据保存至文件
def save_to_nbtfile(barray, map_id):
    nbtfile = nbt.NBTFile()
    colors = nbt.TAG_Byte_Array(name="colors")
    colors.value = barray
    data = nbt.TAG_Compound()
    data.name = "data"
    data.tags = [
        nbt.TAG_Byte(value=1, name="scale"),#地图缩放
        nbt.TAG_Byte(value=0, name="dimension"),#维度
        nbt.TAG_Byte(value=0, name="trackingPosition"),#箭头永不显示
        nbt.TAG_Byte(value=1, name="locked"),#被锁定
        nbt.TAG_Int(value=0, name="xCenter"),
        nbt.TAG_Int(value=0, name="zCenter"),
        nbt.TAG_Short(value=128, name="width"),
        nbt.TAG_Short(value=128, name="height"),
        colors
    ]
    nbtfile.tags.append(data)
    nbtfile.write_file("server/world/data/map_{}.dat".format(map_id))
'''
图片处理 - end
'''

'''
文字处理 - start
'''
# 格式化单行文本
def format_text(id, remark, gen_time, creator):
    return RTextList(
        RText(str(id) + "."), 
        RText(remark + " ", color=RColor.aqua), 
        RText(gen_time + " ", color=RColor.white), 
        RText(creator, color=RColor.gray),
        RText(" [i]", color=RColor.blue).h("详细信息").c(RAction.run_command, "{0} info {1}".format(Prefix, id)),
        RText(" [√]", color=RColor.green).h("获取").c(RAction.run_command, "{0} get {1}".format(Prefix, id)),
        RText(" [×]", color=RColor.red).h("删除").c(RAction.run_command, "{0} delete {1}".format(Prefix, id))
    )

# 获得一页列表
def get_list(page):
    global maplist,config
    max_page = len(maplist["map_list"]) // config["item_per_page"] + 1
    l = []
    l.append(RText("=====第{0}页/共{1}页=====".format(page, max_page), color=RColor.gray))
    show_list = maplist["map_list"][(page-1)*config["item_per_page"]:page*config["item_per_page"]]
    for i in show_list:
        l.append(format_text(
            i["id"],
            i["remark"] if i["remark"] != "" else "<NULL>", 
            i["time"], 
            i["creator"]))
    
    l.append(RTextList(
        RText("[←]", color=RColor.dark_gray).h("上一页").c(RAction.run_command, "{0} list {1}".format(Prefix, page-1)) if page != 1 else "",
        RText("[→]", color=RColor.dark_gray).h("下一页").c(RAction.run_command, "{0} list {1}".format(Prefix, page+1)) if page != max_page else ""
    ))
    return l

# 获得数据
def get_map(id):
    fid = -1
    try:
        fid = int(id)
    except:
        return None
    for i in maplist["map_list"]:
        if i["id"] == fid: 
            return i
    return None

# 格式化详细信息    
def format_detail(map):
    def f(key,value,is_url=False):
        v = RTextList()
        if type(value) == list:
            v.append(RText("[\n", color=RColor.white))
            count = 1
            length = len(value)
            for i in value:
                v.append(RText(str(i), color=RColor.gold))
                if count < length:
                    v.append(RText(",", color=RColor.white))
                v.append('\n')
                count += 1
            v.append(RTextList(RText("]\n", color=RColor.white)))
        elif is_url:
            v.append(RText(value + '\n', color=RColor.gold).c(RAction.open_url, value))
        else:
            v.append(RText(str(value) + '\n', color=RColor.gold))
        return RTextList(RText(key, color=RColor.aqua), RText(": ", color=RColor.white), v)
    
    text = RTextList(f("地图画ID", map["id"]))
    text.append(f("作者", map["creator"]))
    text.append(f("生成时间", map["time"]))
    text.append(f("耗时", map["time_used"]))
    text.append(f("原画URL", map["url"], is_url=True))
    text.append(f("备注", map["remark"]))
    text.append(f("大小", str(map["size"][0]) + '×' + str(map["size"][1])))
    text.append(f("MapID列表", map["id_list"]))
    if config["save_temp"]:
        text.append(f("缓存文件列表", map["temp_file_list"]))
    return text
'''
文字处理 - end
'''

@new_thread(PLUGIN_METADATA['id'])
def on_user_info(server, info):
    global config, maplist
    command = info.content.split()
    length = len(command)
    if length == 0 or command[0] != Prefix:
        return

    # 解析参数
    if length == 1 or info.content.find(' -h') >= 0 or info.content.find(' --help') >= 0:
        server.reply(info, help_message)
        return
    
    if command[1] == 'create' and length > 2:
        time_start = time.time()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 解析参数
        is_show_details = True if info.content.find('-d') >= 0 or info.content.find('--details') >= 0 else False
        height = command[command.index('--height') + 1] if info.content.find('--height') != -1 else 1
        width = command[command.index('--width') + 1] if info.content.find('--width') != -1 else 1
        remark = command[command.index('--remark') + 1] if info.content.find('--remark') != -1 else ""
        try:
            height = int(height)
            width = int(width)
        except:
            server.reply(info, "§c参数错误")
            return

        map_id = maplist["next_mapid"]
        id_list = []
        temp_file_list = []

        # 下载图片
        content = download_image(server, info, command[2])
        if content == None: return
        image = Image.open(BytesIO(content))
        if is_show_details: server.reply(info, "图片下载完成")
        if config["save_temp"]: 
            image.save(config_path + "temp/{0}_main.png".format(time.time()), "png")
            temp_file_list.append(config_path + "temp/{}_main".format(time.time()))

        # 分割图片
        image_list = cut_image(image, width, height)
        if config["save_temp"]: 
            temp_file_list = save_images(config_path + "temp/" + str(time.time()) + "_split_{}.png", image_list)
        if is_show_details: server.reply(info, "图片分割完成({0}×{1})".format(width, height))

        count = 0
        for i in image_list:
            ba = to_barray(i)
            save_to_nbtfile(ba, map_id)
            if is_show_details: server.reply(info, str(image_list.index(i)) + "转换完成")
            # 给予物品
            item_name = remark + "_" + str(t) + "_" + str(count)
            # give @p filled_map{map:1,display:{Name: '{"text":"123"}', Lore:['{"text":"123"}']}}
            server.execute("/give {0} filled_map{{map:{1},display:{{Name:'{{\"text\":\"{2}\"}}', Lore:['{{\"text\":\"{3}\"}}']}}}}".format(info.player, map_id, item_name, "该物品由" + PLUGIN_METADATA["name"] + "插件生成"))
            id_list.append(map_id)
            map_id -= 1
            count += 1
        maplist["next_mapid"] = map_id
        if is_show_details: server.reply(info, "已给予物品")

        time_end = time.time()

        server.reply(info, "完成!{}".format("(用时{}秒)".format(time_end - time_start) if is_show_details else ""))

        data = {}
        data["id"] = maplist["next_id"]
        maplist["next_id"] = maplist["next_id"] + 1
        data["creator"] = info.player
        data["time"] = t
        data["time_used"] = time_end - time_start
        data["url"] = command[2]
        data["size"] = [width, height]
        data["remark"] = remark
        data["id_list"] = id_list
        data["temp_file_list"] = temp_file_list
        maplist["map_list"].append(data)
        update_config(config_path + "maplist.json", maplist)
    elif command[1] == 'list':
        page = 1
        try:
            if length > 2:
                page = int(command[2])
        except:
            server.reply(info, "§c参数错误")
            return
        for i in get_list(page):
            server.reply(info, i)
    elif command[1] == 'get' and length > 2:
        m = get_map(command[2])
        if m == None:
            server.reply(info, "§c错误的ID")
            return
        count = 0
        for i in m["id_list"]:
            item_name = m["remark"] + "_" + str(m["time"]) + "_" + str(count)
            server.execute("/give {0} filled_map{{map:{1},display:{{Name:'{{\"text\":\"{2}\"}}', Lore:['{{\"text\":\"{3}\"}}']}}}}".format(info.player, i, item_name, "该物品由" + PLUGIN_METADATA["name"] + "插件生成"))
            count += 1
    elif command[1] == 'info' and length > 2:
        m = get_map(command[2])
        if m == None:
            server.reply(info, "§c错误的ID")
            return
        print(config)
        server.reply(info, format_detail(m))
    else:
        server.reply(info, "§c发生错误，请使用§7{0}§c查看帮助".format(Prefix))

def on_load(server, old_module):
    server.register_help_message('!!mapitem', PLUGIN_METADATA['description'])
    config()
