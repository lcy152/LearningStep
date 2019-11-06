import os
import configparser
import bson
import glob
from threading import Thread, Lock, Event
import time
import json
import datetime
import shutil
import ctypes
import platform

config_file = 'config.ini'
record_file = 'DbBackupRecord.ini'
backup_section_name = 'BackupTables'
recover_section_name = 'RecoverTables'
db_backup_position = 'DbBackupPosition'
db_backup_name = 'db_backup'
db_backup_dir = 'dir'
recent_task_name = 'RecentTask'
recent_backup_name = 'backup'
recent_backup_remarks = 'remarks'
recent_recover_name = 'recover'

json_file_name = 'detail'
mutex = Lock()
thread_list = []
force_stop_thread = False
progress_step = 0


def set_progress_step(v):
    global progress_step
    mutex.acquire()
    progress_step = v
    mutex.release()
    return


def add_to_thread_list(v):
    global thread_list
    mutex.acquire()
    thread_list.append(v)
    mutex.release()
    return


def reset_thread_list():
    global thread_list
    mutex.acquire()
    thread_list = []
    mutex.release()
    return


def set_force_stop_thread(v):
    global force_stop_thread
    mutex.acquire()
    force_stop_thread = v
    mutex.release()
    return


def get_progress_step():
    return progress_step


def get_thread_list():
    return thread_list


def get_force_stop_thread():
    return force_stop_thread


class BackUpThread(Thread):
    def __init__(self, pymongo_db, backup_name):
        super().__init__()
        self.pymongo_db = pymongo_db
        self.backup_name = backup_name
        self.singal = Event()
        self.singal.set()

    def run(self):
        # try:
        print("start:\n")
        set_force_stop_thread(False)
        config_dir = get_config_dir()
        db_path = config_dir + '\\' + self.backup_name
        mkdir(db_path)

        global record_file
        global backup_section_name
        global json_file_name

        set_option_v(recent_task_name, recent_backup_name, self.backup_name)

        # 重新开始备份
        init_section_v()

        # 获取已备份表的记录
        backup_gulp_tables = get_section_v(backup_section_name)
        backup_tables = []
        for table_gulp in backup_gulp_tables:
            backup_tables.append(table_gulp[0])
        remarks = get_option_v(recent_task_name, recent_backup_remarks)

        # 获取已备份列表
        collection_names_list = []
        try:
            collection_names_list = self.pymongo_db.collection_names(include_system_collections=True, session=None)
        except Exception as e:
            print(e)
            collection_names_list = self.pymongo_db.list_collection_names(session=None)
        if len(collection_names_list) == 0:
            return False

        # 获取未备份列表
        diff_col_names_list = list(set(collection_names_list).difference(set(backup_tables)))

        collection_names_list.sort()
        backup_tables.sort()
        diff_col_names_list.sort()

        print('备份开始: --> ')
        progress_count = len(backup_tables)
        progress_sum = len(collection_names_list)
        for collection_name in diff_col_names_list:
            item_list = self.pymongo_db[collection_name].find()
            for item in item_list:
                self.singal.wait()
                if get_force_stop_thread():
                    reset_thread_list()
                    # 备份中断,未成功
                    write_to_json(db_path, json_file_name, self.backup_name, collection_names_list, remarks)
                    print('备份中断: ')
                    return
                ref_item_id = item["_id"]
                try:
                    save_to_bson(db_path, collection_name, item, ref_item_id)
                except NotValidError as e:
                    print(e)
                    end_thread()

            progress_count = progress_count + 1
            set_progress_step(progress_count / progress_sum)
            global progress_step
            print('step: ' + str(progress_step))
            set_option_v(backup_section_name, collection_name, "True")
            print('name: ' + collection_name)
            time.sleep(2)

        # 配置文件写入相关信息
        write_to_json(db_path, json_file_name, self.backup_name, collection_names_list, remarks)
        # 备份成功,清除上次历史记录
        remove_section_v(backup_section_name)
        print('备份结束: <-- ')
        # except Exception as e:
        #     print(e)
        reset_thread_list()

    def pause(self):
        print("pause\n")
        self.singal.clear()

    def restart(self):
        print("continue\n")
        self.singal.set()


class RecoverThread(Thread):
    def __init__(self, pymongo_db, recover_name):
        super().__init__()
        self.pymongo_db = pymongo_db
        self.recover_name = recover_name
        self.singal = Event()
        self.singal.set()

    def run(self):
        # try:
        print("start:\n")
        set_force_stop_thread(False)
        config_dir = get_config_dir()
        db_path = config_dir + '\\' + self.recover_name

        # bson文件相关信息
        list_of_dir = []
        list_count_of_dir = []
        all_files = os.scandir(db_path)

        # 重新开始恢复
        init_section_v()

        global record_file
        global recover_section_name

        set_option_v(recent_task_name, recent_recover_name, self.recover_name)

        # 获取已恢复表的记录
        recover_gulp_tables = get_section_v(recover_section_name)
        recover_tables = []
        for table_gulp in recover_gulp_tables:
            recover_tables.append(table_gulp[0])

        # 获取已恢复列表
        collection_names_list = []
        try:
            collection_names_list = self.pymongo_db.collection_names(include_system_collections=True, session=None)
        except Exception as e:
            print(e)
            collection_names_list = self.pymongo_db.list_collection_names(session=None)

        # 获取未恢复列表
        diff_col_names_list = list(set(collection_names_list).difference(set(recover_tables)))

        print('恢复开始: --> ')
        progress_count = len(recover_tables)
        progress_sum = 0  # len(collection_names_list)

        # 恢复指定版本数据库
        # 获取目录下面所有文件夹
        for it in all_files:
            if it.is_dir():
                list_of_dir.append(it)
                list_count_of_dir.append(it)

        while list_count_of_dir:
            cur_file = list_count_of_dir.pop()
            progress_sum = progress_sum + 1
            all_files = os.scandir(cur_file.path)
            for it in all_files:
                if it.is_dir():
                    list_count_of_dir.append(it)

        # 获取文件夹下面所有bson文件
        while list_of_dir:
            cur_file = list_of_dir.pop()
            list_of_files = glob.glob(cur_file.path + '/*.bson')
            collection_name = os.path.basename(cur_file.path)
            if collection_name not in recover_tables:
                self.pymongo_db[collection_name].drop()
                for b_file in list_of_files:
                    self.singal.wait()
                    if get_force_stop_thread():
                        reset_thread_list()
                        # 恢复中断,未成功
                        print('恢复中断: ')
                        return
                    bson_file = open(b_file, 'rb')
                    bson_binary_data = bson_file.read()
                    bson_data = bson.BSON.decode(bson_binary_data)
                    # bson_data = bson.loads(bson_file.read())
                    # 插入数据
                    self.pymongo_db[collection_name].insert(bson_data)
                    bson_file.close()
                all_files = os.scandir(cur_file.path)
                for it in all_files:
                    if it.is_dir():
                        list_of_dir.append(it)
                progress_count = progress_count + 1
                set_progress_step(progress_count / progress_sum)
                global progress_step
                print('step: ' + str(progress_step))
                set_option_v(recover_section_name, collection_name, "True")
                print('name: ' + collection_name)
                time.sleep(1)

        # 恢复成功,清除上次历史记录
        remove_section_v(recover_section_name)
        print('恢复结束: <-- ')
        # except Exception as e:
        #     print(e)
        reset_thread_list()

    def pause(self):
        print("恢复暂停\n")
        self.singal.clear()

    def restart(self):
        print("恢复继续\n")
        self.singal.set()


def init_section_v():
    global record_file
    global recover_section_name
    global backup_section_name
    # 加载配置文件
    con = configparser.ConfigParser()
    con.read(record_file, encoding='utf-8')

    # 初次设置历史记录
    if not con.has_section(recover_section_name):  # 检查是否存在section
        con.add_section(recover_section_name)
    if not con.has_section(backup_section_name):  # 检查是否存在section
        con.add_section(backup_section_name)

    file_temp = open(record_file, "w", encoding="utf-8")
    con.write(file_temp)
    file_temp.close()
    return


def remove_section_v(section_name):
    global record_file
    # 加载配置文件
    con = configparser.ConfigParser()
    con.read(record_file, encoding='utf-8')
    con.remove_section(section_name)
    if not con.has_section(section_name):  # 检查是否存在section
        con.add_section(section_name)
    file_temp = open(record_file, "w", encoding="utf-8")
    con.write(file_temp)
    file_temp.close()
    return


def get_section_v(section_name):
    global record_file
    # 加载配置文件
    con = configparser.ConfigParser()
    con.read(record_file, encoding='utf-8')
    if not con.has_section(section_name):  # 检查是否存在section
        con.add_section(section_name)
    return con.items(section_name)


def set_option_v(section_name, option_name, option_value):
    global record_file
    # 加载配置文件
    con = configparser.ConfigParser()
    con.read(record_file, encoding='utf-8')
    if not con.has_section(section_name):  # 检查是否存在section
        con.add_section(section_name)
    con.set(section_name, option_name, option_value)
    file_temp = open(record_file, "w", encoding="utf-8")
    con.write(file_temp)
    file_temp.close()
    return


def get_option_v(section_name, option_name):
    global record_file
    # 加载配置文件
    con = configparser.ConfigParser()
    con.read(record_file, encoding='utf-8')
    if not con.has_section(section_name):  # 检查是否存在section
        con.add_section(section_name)
    if not con.has_option(section_name, option_name):  # 检查是否存在section
        con.set(section_name, option_name, '')
    v = con.get(section_name, option_name)
    file_temp = open(record_file, "w", encoding="utf-8")
    con.write(file_temp)
    file_temp.close()
    return v


def backup_service(pymongo_db, backup_name):
    if len(get_thread_list()) != 0:
        if not get_thread_list()[0].is_alive():
            reset_thread_list()
    if len(get_thread_list()) == 0:
        thread = BackUpThread(pymongo_db, backup_name)
        add_to_thread_list(thread)
        thread.start()
        return True
    else:
        return False


def recover_service(pymongo_db, recover_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + recover_name
    is_exists = os.path.exists(db_path)
    if not is_exists:
        return "path not exist"
    if len(get_thread_list()) != 0:
        if not get_thread_list()[0].is_alive():
            reset_thread_list()
    if len(get_thread_list()) == 0:
        thread = RecoverThread(pymongo_db, recover_name)
        add_to_thread_list(thread)
        thread.start()
        return True
    else:
        return False


def end_thread():
    if len(get_thread_list()) != 0:
        set_force_stop_thread(True)
        return True
    else:
        return False


def restart_thread():
    if len(get_thread_list()) != 0:
        get_thread_list()[0].restart()
        return True
    else:
        return False


def pause_thread():
    if len(get_thread_list()) != 0:
        get_thread_list()[0].pause()
        return True
    else:
        return False


def get_thread_status():
    if len(get_thread_list()) != 0:
        return True
    else:
        return False


def delete_section():
    if len(get_thread_list()) != 0:
        return True
    else:
        return False


# 备份数据库
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
    print(collection_names_list)
    if len(collection_names_list) == 0:
        return False
    for collection_name in collection_names_list:
        item_list = pymongo_db[collection_name].find()
        for item in item_list:
            ref_item_id = item["_id"]
            save_to_bson(db_path, collection_name, item, ref_item_id)
    return True


# 保存为bson文件
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


# 恢复指定版本数据库
def recover_from_bson_test(pymongo_db, bak_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + bak_name
    list_of_dir = []
    all_files = os.scandir(db_path)

    # 删除数据库
    drop_all_collection(pymongo_db)

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
            pymongo_db[collection_name].insert(bson_data)
            bson_file.close()
        all_files = os.scandir(cur_file.path)
        for it in all_files:
            if it.is_dir():
                list_of_dir.append(it)
    return


# 删除数据库
def drop_all_collection(pymongo_db):
    col_names_list = []
    try:
        col_names_list = pymongo_db.collection_names(include_system_collections=True, session=None)
    except Exception as e:
        print(e)
        col_names_list = pymongo_db.list_collection_names(session=None)
    print(col_names_list)
    if len(col_names_list) == 0:
        return False
    for col_name in col_names_list:
        pymongo_db[col_name].drop()
    return


# 初始化配置文件夹路径
def init_dir():
    global config_file
    file = config_file
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8')
    if not con.has_section(db_backup_position):  # 检查是否存在section
        con.add_section(db_backup_position)
    v = ''
    if con.has_option(db_backup_position, db_backup_dir):
        v = con.get(db_backup_position, db_backup_dir)
    if not con.has_option(db_backup_position, db_backup_dir) or not os.path.exists(v):
        path = os.getcwd() + '\\' + db_backup_name
        con.set(db_backup_position, db_backup_dir, path)
        print('初始化数据库备份地址: ' + path)
        con.write(open(file, "r+", encoding="utf-8"))
    else:
        print('数据库备份地址: ' + v)
    return


# 创建文件夹
def mkdir(path):
    path = path.strip()
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False


# 获取配置文件的目录
def get_config_dir():
    global config_file
    file = config_file
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8')
    # sections = con.sections()
    # 初次设置历史记录
    if not con.has_section(db_backup_position):  # 检查是否存在section
        con.add_section(db_backup_position)
    if not con.has_option(db_backup_position, db_backup_dir):
        init_dir()
    return con.get(db_backup_position, db_backup_dir)


# 写入详情配置文件
def write_to_json(path, file_name, backup_name, table_list, remarks):
    global config_file
    # 获取已备份数据
    backup_gulp_tables = get_section_v(backup_section_name)
    backup_list = []
    for table_gulp in backup_gulp_tables:
        backup_list.append(table_gulp[0])

    new_dict = {}
    diff_list = list(set(table_list).difference(set(backup_list)))
    status = False
    if len(diff_list) == 0:
        status = True
    new_dict['backup_name'] = backup_name
    new_dict['description'] = remarks
    new_dict['backup_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dict['status'] = status
    new_dict['backup_list'] = backup_list
    new_dict['not_backup_list'] = diff_list
    new_dict['all_list'] = table_list
    with open(path + "\\" + file_name + ".json", "w", encoding='utf-8') as f:
        json.dump(new_dict, f)
        print("写入json文件完成...")
        f.close()


# 读取详情配置文件
def read_json_to_dict(dir_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + dir_name
    global json_file_name
    json_str = ''
    json_path = db_path + "\\" + json_file_name + ".json"
    if os.path.exists(json_path):
        with open(db_path + "\\" + json_file_name + ".json", encoding='utf-8') as f:
            try:
                while True:
                    line = f.readline()
                    if line:
                        json_str = json_str + line
                        # print(r)
                    else:
                        break
            except Exception as e:
                print(e)
                f.close()
    json_str = json_str.replace("\n", "").replace("\t", "").strip()
    d = json.loads(json_str)
    print(d)
    f.close()
    return d


# 读取详情配置文件
def read_backup_database_json_list():
    db_path = get_config_dir()
    if not os.path.exists(db_path):
        raise NotValidError('1', '备份地址不存在,请修改服务器配置config.ini文件!')
    list_of_dir = []
    all_files = os.scandir(db_path)
    global json_file_name
    db_list = []

    # 获取目录下面所有文件夹
    for it in all_files:
        if it.is_dir():
            list_of_dir.append(it)
    # 获取文件夹下面所有bson文件
    while list_of_dir:
        cur_file = list_of_dir.pop()
        json_str = ''
        json_path = cur_file.path + "\\" + json_file_name + ".json"
        if os.path.exists(json_path):
            with open(json_path, encoding='utf-8') as f:
                try:
                    while True:
                        line = f.readline()
                        if line:
                            json_str = json_str + line
                            # print(r)
                        else:
                            break
                except Exception as e:
                    print(e)
                    f.close()
            json_str = json_str.replace("\n", "").replace("\t", "").strip()
            d = json.loads(json_str)
            db_list.append(d)
            f.close()
        # else:

    return db_list


# 恢复指定版本数据库
def delete_backup_file(bak_name):
    config_dir = get_config_dir()
    db_path = config_dir + '\\' + bak_name
    is_exists = os.path.exists(db_path)
    if is_exists:
        shutil.rmtree(db_path, True)
    return


# 恢复指定版本数据库
def backup_valid_check():
    config_dir = get_config_dir()
    room = get_free_space_mb() / 1024 / 1024
    if not os.path.exists(config_dir):
        raise NotValidError('1', '备份地址不存在,请修改服务器配置config.ini文件!')
    if room < 50:
        raise NotValidError('1', '内存不足,请清理内存或者更换备份磁盘路径!')
    return


# 恢复指定版本数据库
def get_free_space_mb():
    config_dir = get_config_dir()
    if not os.path.exists(config_dir):
        raise NotValidError('1', '备份地址不存在,请修改服务器配置config.ini文件!')
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(config_dir), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(config_dir)
        return st.f_bavail * st.f_frsize


class NotValidError(RuntimeError):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg



