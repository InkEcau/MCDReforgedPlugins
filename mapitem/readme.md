# Mapitem插件
---

一个[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)(version>=1.0.0)插件

**请确保`./config/mapitem/maplist.json`不会丢失**

插件将会改变`./server/world/data/`文件夹的内容

## 安装

1.安装pip依赖`pip install -r requirements.txt`(国内速度较慢，可以试试添加`-i https://pypi.tuna.tsinghua.edu.cn/simple`)
2.将`mapitem.py`文件移动到`./plugins/`文件夹
3.如果服务器正在运行，可以在游戏内执行`!!MCDR r plugin`或重启服务端

## 指令

在游戏内执行`!!mapitem`查看帮助

## 配置

~~在游戏内执行`!!mapitem config <配置项> <配置内容>`进行配置，详情请见[可用配置项](#可用配置项)~~

### 配置文件

*插件初次加载后自动生成*
`./config/mapitem/`文件夹中:
`mapitem.json`:插件配置文件，详情请见[可用配置项](#可用配置项)
`maplist.json`:地图画列表，**如果您不知道您在做什么，请不要修改**
`temp/`:临时文件路径

### 可用配置项

`permission`:[MCDR权限等级](https://mcdreforged.readthedocs.io/zh_CN/latest/permission.html)，调用指令的最低等级，默认为`3`
`data_path`:`map_<#>.dat`文件路径，默认为`./server/world/data/`
`save_temp`:是否保存临时文件，默认为`true`
`temp_filepath`:临时文件路径，默认为`./config/mapitem/temp/`
`item_per_page`:游戏内执行`!!mapitem list`时，单页最大信息数量，默认为`8`

## 预期更新~~（咕咕咕）~~

- 完善帮助信息
- `!!mapitem config`游戏内配置，自动检测配置文件完整性
- 使用`argparse`模块解析参数，放弃硬解
- 游戏版本支持([MinecraftWiki](https://minecraft.fandom.com/wiki/Map_item_format#History))
- 多线程支持
- 允许将本地文件上传至图床以供下载
- 性能测试（？？

~~第一次认真写插件，虽然都是我自己写的，但有些地方代码风格都不太一样~~

赶时间，虽然进行了简单的测试，但应该还会有很多bug

最后，欢迎提交issue，中考临近可能要到暑假才能解决了（指立即解决