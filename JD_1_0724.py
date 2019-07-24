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
        print(path, '-----创建成功-----')

    else:
        print(path, '-----目录已存在-----')


# 删除
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


# 解压文件
def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')


def toZip(startdir):

    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
    for filename in filenames:
        z.write(os.path.join(dirpath, filename), fpath + filename)
        print('压缩成功')
    z.close()
    return file_news


# 读取 Properties 传入键的值
def readPropertiesValue(propertiesPath, key):

    res = ''
    with open(propertiesPath, 'r', encoding='utf-8') as f:
        for line in f:
            a = line.split('=')[0]
            b = line.split('=')[1]
            if a == key:
                res = b
            if (b[-1] == '\n'):
                b = b[:-1]
            keyList.append(a)
            valueList.append(b)

    if (res[-1] == '\n'):
        res = res[:-1]

    return res

# 获取完整路径
def getCompletePath(propertiesPath,key):
    str = readPropertiesValue(propertiesPath,key)
    for i in range(len(str)):
        if str[i] == '$':
            begin = i
            print(i, str[i])
        if str[i] == '}':
            end = i
            print(i, str[i])
    str = str.replace(str[begin:end + 1], path)
    return str


if __name__ == "__main__":

    curPath = os.getcwd()
    propertiesPath = curPath + '/build-product.properties'

    keyList = []
    valueList = []

    with open(propertiesPath, 'r', encoding='utf-8') as f:
        for line in f:
            # if line == '\n':
            #     continue
            a = line.split('=')[0]
            b = line.split('=')[1]
            if a == 'bigscreen-ui.networksecurity.url':
                res = b
            if (b[-1] == '\n'):
                b = b[:-1]
            keyList.append(a)
            valueList.append(b)


    dic = dict(zip(keyList, valueList))
    dic2 = dict()
    for key in dic.keys():
        str = dic[key]
        if str.find('$') != -1:
            for i in range(len(str)):
                if str[i] == '$':
                    begin = i

                if str[i] == '}':
                    end = i

            character = str[begin+2:end]
            # print(character)
            str = str.replace(str[begin:end + 1], dic[character])
            dic2[key] = str
        else:
            dic2[key] = str

    print("Properties：")
    print(dic2)

    # 获取当前执行路径
    origin_path = os.getcwd()


    # 路径


    path = os.getcwd() + '/' + readPropertiesValue(propertiesPath, 'temp.dir')

    path_build = curPath + '/' + dic2['build.dir']
    path_source = curPath + '/' + dic2['temp.src.dir']
    release_path = curPath + '/' + dic2['dist.dir']

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

    srcPath = curPath + '../../../../jdsbu_source/source'
    fileList = os.listdir(srcPath)

    # 执行前将 目标路径  temp\source  清空
    distPath = curPath + '/temp/source'
    shutil.rmtree(distPath, ignore_errors=True)
    mkdir(distPath)


    for i in fileList:
        srcPath_sub = srcPath + '\\' + i
        distPath_sub = distPath + '\\' + i
        shutil.copytree(srcPath_sub, distPath_sub)

    # 执行 mvn 语句

    exec_path = curPath + '/temp/source/jd-business'
    subprocess.check_call('mvn -f pom.xml clean install -Dmaven.test.skip=true', shell=True,
                          cwd=exec_path)


    # 复制 jar 包
    srcPath_jar = curPath + r'/temp/source/jd-business/target/jdbusiness-1.0-SNAPSHOT.jar'
    print(srcPath_jar)
    distPath_jar = curPath + r'/temp/build/JDSBU/binary/jd-business/jdbusiness-1.0-SNAPSHOT.jar'
    print(distPath_jar)
    shutil.copyfile(srcPath_jar, distPath_jar)

    # 复制 .sql 语句
    srcPath_sql = curPath + r'/temp/source/jd-business/src/main/resources/sql/jd_bu_statistics.sql'
    print(srcPath_sql)
    distPath_sql = curPath + r'/temp/build/JDSBU/binary/jd-business/jd_bu_statistics.sql'
    print(distPath_sql)
    shutil.copyfile(srcPath_sql, distPath_sql)



    # 复制 bigscreen-ui_dist.zip 到



    # 压缩操作

    # 创建 release 目录
    mkdir(release_path)


    # 解压 \digitalchina_build\depends\digitalchina-ui 下的 .zip 文件到 \temp\source\bigscreen-ui
    srcZipFilePath = curPath + r'/../digitalchina_build/depends/digitalchina-ui'
    destZipFilePath = curPath + r'/temp/source/bigscreen-ui'
    zipFileList = os.listdir(srcZipFilePath)
    # print(zipFileList)

    for i in zipFileList:
        srcZipFilePath_sub = srcZipFilePath + r'/' + i
        # print(srcZipFilePath_sub)
        unzip_file(srcZipFilePath_sub, destZipFilePath)


    # # 在 /bigscreen-ui 下，执行gulp命令
    gulpPath = curPath + r'/temp/source/bigscreen-ui'
    subprocess.check_call('gulp', shell=True, cwd=gulpPath)


    # 打包操作：将dist目录下的文件打包为 /bigscreen-ui/bigscreen-ui_dist.
    zipFileName = 'bigscreen-ui_dist'
    archive_name = os.path.expanduser(os.path.join('~', zipFileName))
    root_dir = os.path.expanduser(os.path.join('~', curPath + '/temp/source/bigscreen-ui/dist'))
    make_archive(archive_name, 'zip', root_dir)

    # !每次生成的压缩包都到 C:\Users\20190524 路径下
    # 移动到 \temp\source\bigscreen-ui
    shutil.move(r'C:/Users/20190524/' + zipFileName + '.zip', curPath + '/temp/source/bigscreen-ui')
    # 再拷贝到 \temp\build\JDSBU\binary\bigscreen-ui
    srcPath_dist = curPath + '/temp/source/bigscreen-ui/bigscreen-ui_dist.zip'
    destPath_dist = curPath + '/temp/build/JDSBU/binary/bigscreen-ui/bigscreen-ui_dist.zip'
    shutil.copyfile(srcPath_dist, destPath_dist)

    # 压缩

    fmt = '%Y%m%d%H%M'  # 定义时间显示格式
    date = time.strftime(fmt, time.localtime(time.time()))  # 把传入的元组按照格式，输出字符串
    zipFileName = 'HUACLOUD_JDSBU_1.0.0_DEV.' + date

    archive_name = os.path.expanduser(os.path.join('~', zipFileName))
    root_dir = os.path.expanduser(os.path.join('~', curPath + '/temp/build'))
    make_archive(archive_name, 'zip', root_dir)

    # 移动到 release 目录下

    shutil.move(r'C:/Users/20190524/' + zipFileName + '.zip', curPath + '/release')



    # 读取 \digitalchina_build 下的 build-product.properties
    propertiesPath = curPath + '/build-product.properties'
    f = open(propertiesPath, 'r', encoding='utf-8')
    res = ''
    with open(propertiesPath, 'r', encoding='utf-8') as f:
        for line in f:
            # if line == '\n':
            #     continue
            a = line.split('=')[0]
            b = line.split('=')[1]
            if a == 'bigscreen-ui.networksecurity.url':
                res = b

    if (res[-1] == '\n'):
        res = res[:-1]

    # # 读取 dataUrl.json
    jsonPath = curPath + '/temp/source/bigscreen-ui/dist/app/scripts/data/dataUrl.json'

    f1 = open(jsonPath, "r")
    content = f1.read()
    f1.close()

    t = content.replace("https://www.baidu.com/", res)
    with open(jsonPath, "w") as f2:
        f2.write(t)