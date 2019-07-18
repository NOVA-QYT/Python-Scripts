import os
import shutil
import subprocess
import zipfile
from shutil import make_archive
import time


# 新建目录
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('-----创建成功-----')

    else:
        print(path + '目录已存在')

# 删除
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)



if __name__ == "__main__":


    # 获取当前执行路径
    origin_path = os.getcwd()


    # 路径
    path = os.getcwd() + r"\temp5"
    path_build = path + r"\build"
    path_source = path + r"\source"
    path_JDSBU = path_build + r"\JDSBU"
    path_binary = path_JDSBU + r"\binary"
    path_ui = path_binary + r"\bigscreen-ui"
    path_business = path_binary + r"\jd-business"


    # 创建目录
    mkdir(path)
    mkdir(path_build)
    mkdir(path_source)
    mkdir(path_JDSBU)
    mkdir(path_binary)
    mkdir(path_ui)
    mkdir(path_business)

    # 清空source下文件
    shutil.rmtree(path_source)
    mkdir(path_source)

    print("================================================================================")


    # 获取当前系统执行路径  D:\JD\install\jdsbu_install\install\jdsbu_build 下的JD_1.py

    curPath = os.getcwd()
    # print(curPath)

    srcPath = curPath + '../../../../jdsbu_source/source'
    fileList = os.listdir(srcPath)
    # print(fileList)

    # 执行前将 目标路径  temp5\source  清空
    distPath = curPath + '/temp5/source'
    shutil.rmtree(distPath, ignore_errors=True)
    mkdir(distPath)


    for i in fileList:
        srcPath_sub = srcPath + '\\' + i
        # print(srcPath_sub)
        distPath_sub = distPath + '\\' + i
        # print(distPath_sub)
        shutil.copytree(srcPath_sub, distPath_sub)

    # 执行 mvn 语句
    # print(curPath)
    os.chdir(curPath + '/temp5/source/jd-business')
    exec_path = os.getcwd()
    # print(os.getcwd())
    subprocess.check_call('mvn -f pom.xml clean install -Dmaven.test.skip=true', shell=True,
                          cwd=exec_path)

    # 切回目录
    os.chdir(curPath)
    print(curPath)

    # 复制 jar 包
    srcPath_jar = curPath + r'/temp5/source/jd-business/target/jdbusiness-1.0-SNAPSHOT.jar'
    print(srcPath_jar)
    distPath_jar = curPath + r'/temp5/build/JDSBU/binary/jd-business/jdbusiness-1.0-SNAPSHOT.jar'
    print(distPath_jar)
    shutil.copyfile(srcPath_jar, distPath_jar)

    # 复制 .sql 语句
    srcPath_sql = curPath + r'/temp5/source/jd-business/src/main/resources/sql/jd_bu_statistics.sql'
    print(srcPath_sql)
    distPath_sql = curPath + r'/temp5/build/JDSBU/binary/jd-business/jd_bu_statistics.sql'
    print(distPath_sql)
    shutil.copyfile(srcPath_sql, distPath_sql)



    # 以下为压缩操作

    # 创建 release 目录
    release_path = curPath + '/release2'
    mkdir(release_path)

    # 压缩

    fmt = '%Y%m%d%H%M'  # 定义时间显示格式
    date = time.strftime(fmt, time.localtime(time.time()))  # 把传入的元组按照格式，输出字符串
    zipFileName = 'HUACLOUD_JDSBU_1.0.0_DEV.' + date

    archive_name = os.path.expanduser(os.path.join('~', zipFileName))
    root_dir = os.path.expanduser(os.path.join('~', curPath + '/temp5/build'))
    make_archive(archive_name, 'zip', root_dir)

    # 移动到 release2 目录下

    shutil.move(r'C:/Users/20190524/' + zipFileName + '.zip', curPath + '/release2')
