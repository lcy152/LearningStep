# Learning and talking

* mongo数据库备份

## Chapter 1

#### 1. 读取数据库bson数据

备份数据库与保存为bson文件
~~~~
def backup_test(pymongo_db, backup_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + backup_name
    mkdir(db_path)
    collection_names_list = []
    try:
        collection_names_list = pymongo_db.collection_names(include_system_collections=True, session=None)
    except Exception as e:
        print(e)
        collection_names_list = pymongo_db.list_collection_names(session=None)

    for collection_name in collection_names_list:
        item_list = pymongo_db[collection_name].find()
        for item in item_list:
            ref_item_id = item["_id"]
            save_to_bson(db_path, collection_name, item, ref_item_id)
    return True

def save_to_bson(db_path, collection_name, file_data, file_id):
    backup_valid_check()
    path = db_path + '\\' + collection_name
    if not os.path.exists(path):
        os.mkdir(path)
    data = bson.BSON.encode(file_data)
    cur_path = path + '\\' + str(file_id) + '.bson'
    file_bson = open(cur_path, 'wb')
    file_bson.write(bson.binary.Binary(data))
    file_bson.close()
    return
~~~~


恢复指定版本数据库
~~~~
def recover_from_bson_test(pymongo_db, bak_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + bak_name
    list_of_dir = []
    all_files = os.scandir(db_path)

    # 恢复指定版本数据库
    # 获取目录下面所有文件夹
    for it in all_files:
        if it.is_dir():
            list_of_dir.append(it)
    # 获取文件夹下面所有bson文件
    while list_of_dir:
        cur_file = list_of_dir.pop()
        list_of_files = glob.glob(cur_file.path + '/*.bson')
        for file in list_of_files:
            bson_file = open(file, 'rb')
            data = bson_file.read()
            collection_name = os.path.basename(cur_file.path)
            bson_data = bson.decode_all(data)
            # 插入数据
            pymongo_db[collection_name].drop()
            pymongo_db[collection_name].insert(bson_data)
            bson_file.close()
        all_files = os.scandir(cur_file.path)
        for it in all_files:
            if it.is_dir():
                list_of_dir.append(it)
    return
~~~~


