#!/bin/python
# -*- coding:utf-8 -*-

u"""
部署工具的公共方法、公共变量
"""

import urllib
import shutil
import tarfile
import commands

from fabric.api import *
from fabric.contrib.files import *
from datetime import datetime
import time
from fabric.colors import red, green

# 年月日时分秒用作文件夹名时的格式
FULLTIME_FMT = "%Y%m%d%H%M%S"

# 相关服务器配置
NEXUS_URL = "http://--/nexus"

# 服务器相关路径配置
HOME_DIR_FORMAT = "/home/%s"
UPLOAD_DIR_FORMAT = "%s/.todeploy"
LIB_DIR_FORMAT = "%s/apphome/lib"
MODULE_LIB_DIR_FORMAT = "%s/apphome/lib/%s"
BIN_DIR_FORMAT = "%s/apphome/bin"
CATALINA_WORK_DIR_FORMAT = "%s/apphome/catalina/work/Catalina"

# 启停脚本
GROUP_LIST = ("web")
APP_BINNAMES = {"web": ["stop.sh", "start.sh"],
}


def raise_exception():
    raise Exception("部署异常终止!!!")


def read_run_result(run_result):
    lines = run_result.splitlines()
    return lines[0].strip()


def print_process(data_block, data_block_size, file_size):
    u"""
    打印下载进度的回调方法
    data_block:已经下载的数据块
    data_block_size:数据块的大小
    file_size:远程文件的大小
   """
    per = 100.0 * data_block * data_block_size / file_size
    if per > 100:
        per = 100
    print '[%-10s] %.2f%%\r' % ('=' * int(per), per),


class DeployContext:
    def __init__(self, user, pwd, module_package_info, app_server, upload_dir_local):
        self.user = user
        self.pwd = pwd
        self.MODULE_PACKAGE_INFO = module_package_info
        self.APP_SERVER = app_server
        self.UPLOAD_DIR_LOCAL = upload_dir_local

        # 服务器相关路径配置
        self.HOME_DIR = HOME_DIR_FORMAT % user
        self.UPLOAD_DIR = UPLOAD_DIR_FORMAT % self.HOME_DIR
        self.LIB_DIR = LIB_DIR_FORMAT % self.HOME_DIR
        self.BIN_DIR = BIN_DIR_FORMAT % self.HOME_DIR
        self.CATALINA_WORK_DIR = CATALINA_WORK_DIR_FORMAT % self.HOME_DIR

    def __get_servers_address(self, module_name):
        servers_address = self.APP_SERVER[module_name]
        if servers_address is None or len(servers_address) < 1:
            raise_exception()
        return servers_address

    def upload_tar(self, module_name, tar_name):
        u"""
        从本地将tar包上传到服务器上
        :param module_name: 模块名字
        :param tar_name: tar包的名字+全路径
        :return: 上传好的路径
        """
        env.user = self.user
        env.password = self.pwd

        remote_tar_name = self.UPLOAD_DIR + "/" + os.path.basename(tar_name)
        for server_address in self.__get_servers_address(module_name):
            with settings(host_string=server_address):
                run("mkdir -p %s" % os.path.dirname(remote_tar_name))
                put(tar_name, remote_tar_name)
        return remote_tar_name

    def pull_module_tar(self, module_name, release=False):
        u"""
        1. sms的sit服务器上下载当前jenkins的jar，并打成tar包（全部）
        2. 将jar包下载到本地：/deploy/toupload/目录下
        :param module_name:
        :param release: 是否RELEASE版本
        :return: 返回下载下来的tar包名
        """
        repository = "snapshots" if not release else "releases"
        module_info = self.MODULE_PACKAGE_INFO[module_name]
        origin_dir = os.curdir

        # 创建临时文件夹，并改变当前工作路径到该文件夹  [yyyyMMddHHmmss] / [module_name]
        timestamp = datetime.now().strftime(FULLTIME_FMT)
        tmp_path = os.path.join(self.UPLOAD_DIR_LOCAL, timestamp)
        module_path = os.path.join(tmp_path, module_name)
        os.makedirs(module_path)
        os.chdir(module_path)

        # 下载远程包
        remote_file_name = "%s-%s.%s" % (module_name, module_info.version, module_info.extension)
        if repository == "snapshots":
            remote_url = "%s/service/local/artifact/maven/content?r=%s&g=%s&a=%s&v=%s&e=%s" % (NEXUS_URL, repository, module_info.group_id, module_info.artifact, module_info.version, module_info.extension)
        elif repository == "releases":
            remote_url = "%s/service/local/repositories/%s/content/com/allinfinance/%s/%s/%s/%s" % (NEXUS_URL, repository, module_info.group, module_name, module_info.version, remote_file_name)
        else:
            raise_exception()
        module_of_download = os.path.join(module_path, module_info.filename)
        print "url [%s] " % remote_url
        print "download to [%s]" % module_of_download
        urllib.urlretrieve(remote_url, filename=module_of_download, reporthook=print_process)
        print ""
        print ""

        # jar，则先下载依赖
        if module_info.extension == module_info.EXTENSION_JAR:
            # 解压pom.xml
            os.chdir(module_path)
            pom_file = "META-INF/maven/%s/%s/pom.xml" % (module_info.group_id, module_info.artifact)
            jar_cmd = "jar xf %s %s" % (module_info.filename, pom_file)
            print jar_cmd
            # output = commands.getstatusoutput(jar_cmd)
            output = os.system(jar_cmd)
            if output != 0:
                raise_exception()
            print "%s %s" % (output, type(output))

            # 下载依赖
            dependency_dir = os.path.join(module_path, "dependency")
            deps_aic_dir = os.path.join(module_path, "deps-aic")
            os.makedirs(dependency_dir)
            os.makedirs(deps_aic_dir)
            mvn_cmd = "mvn -f %s dependency:copy-dependencies -U -DoutputDirectory=%s" % (pom_file, deps_aic_dir)
            print mvn_cmd
            # output = commands.getstatusoutput(mvn_cmd)
            output = os.system(mvn_cmd)
            if output != 0:
                raise_exception()
            print "%s %s" % (output, type(output))

            # 目录分离
            os.chdir(deps_aic_dir)
            for dirpath, dirnames, filenames in os.walk(deps_aic_dir):
                for filename in filenames:
                    if not filename.startswith(GROUP_LIST):
                        print "shutil.move(%s, %s)" % (filename, dependency_dir)
                        shutil.move(filename, dependency_dir)
            os.chdir(module_path)
            shutil.move("META-INF", tmp_path)
            os.chdir(self.UPLOAD_DIR_LOCAL)

        #
        # # war则直接打包
        # else:
        #     module_war_of_download = os.path.join(module_path, module_info.filename)
        #     remote_url = NEXUS_URL + "/service/local/artifact/maven/content?r=snapshots&g=" + module_info.group_id + "&a=" + module_info.artifact + "&v=" + module_info.version + "&e=" + module_info.extension
        #     print "url %s " % remote_url
        #     print "download to [%s]" % module_war_of_download
        #     urllib.urlretrieve(remote_url, filename=module_war_of_download, reporthook=print_process)
        #     print ""
        #     print ""

        # 打包
        os.chdir(tmp_path)
        tarfile_name = os.path.join(self.UPLOAD_DIR_LOCAL, "%s.%s.tar.gz" % (module_name, timestamp))
        with tarfile.open(tarfile_name, "w:gz") as tarfile_open:
            tarfile_open.add(module_name)
            tarfile_open.close()
        print "tarfile [%s]" % tarfile_name

        os.chdir(origin_dir)
        time.sleep(10)
        shutil.rmtree(tmp_path, ignore_errors=True)
        return tarfile_name

    def backup(self, module_name):
        env.user = self.user
        env.password = self.pwd

        timestr = datetime.now().strftime(FULLTIME_FMT)
        backup_tar = "%s/.backup/%s.%s.tar.gz" % (self.HOME_DIR, module_name, timestr)
        for server_address in self.__get_servers_address(module_name):
            with settings(host_string=server_address):
                with cd(self.LIB_DIR):
                    tar_cmd = "tar -cvzf %s ./%s" % (backup_tar, module_name)
                    run("mkdir -p %s" % os.path.dirname(backup_tar))
                    run(tar_cmd)
                    print tar_cmd
        return backup_tar

    def stop_process(self, server_address, module_name):
        env.user = self.user
        env.password = self.pwd

        if not self.__check_process(server_address, module_name, 0):
            stop_bin = APP_BINNAMES[module_name][0]
            with settings(host_string=server_address):
                with cd(self.BIN_DIR):
                    out = run("./%s" % stop_bin, warn_only=True, timeout=300)
                    if out.failed:
                        run('echo "return_code = [%s]"' % str(out.return_code))
                        run('echo "停服务时未得到预期的返回，请确认服务已停止再继续执行（Y）："')
                        ctn = raw_input()
                        if ctn not in ("y", "Y"):
                            raise Exception("exit")

        # 等待5秒，再次检查服务状态
        time.sleep(5)
        if not self.__check_process(server_address, module_name, 0):
            print red("在服务器%s关闭%s进程失败" % (server_address, module_name))
            raise_exception()

    def start_process(self, server_address, app_name):
        u"""
        启动进程
        :param server_address:
        :param app_name:
        :return:
        """
        env.user = self.user
        env.password = self.pwd

        start_bin = APP_BINNAMES[app_name][1]
        with settings(host_string=server_address):
            with cd(self.BIN_DIR):
                run("./%s" % start_bin, pty=False)

        time.sleep(5)
        if not self.__check_process(server_address, app_name, 2):
            print red("在服务器%s启动%s进程失败" % (server_address, app_name))
            raise_exception()

    def __check_process(self, server_address, module_name, expect_cnt):
        u"""
        检查某台服务器的服务是否活动中
        :param server_address:
        :param module_name:
        :param expect_cnt: 查询到的进程数
        :return: 进程数等于 expect_cnt 则返回 True，否则返回False
        """
        env.user = self.user
        env.password = self.pwd

        with settings(host_string=server_address):
            myout = run("ps aux|grep %s|grep jsvc|grep -v grep|wc -l" % module_name)
            process_cnt = read_run_result(myout)
            return int(process_cnt) == expect_cnt

    def unzip_module_tar(self, server_address, module_name, module_tar):
        u"""
        删除已部署好的包，然后解压指定包。
        :param server_address:
        :param module_name: 模块名
        :param module_tar: 压缩好的tar包
        :return:
        """
        env.user = self.user
        env.password = self.pwd
        with settings(host_string=server_address):
            # 为防止误删，这里将路径写死，而非拼装方式传进来
            run("rm -rf /home/shangc/apphome/lib/%s" % module_name)
            run("tar -xvzf %s -C %s" % (module_tar, self.LIB_DIR))
        return self.LIB_DIR + module_name

    def deploy(self, module_name, release=False, confirm=True):
        u"""
        统一拉包、上传、备份，然后轮流停机、部署、启服务
        :param module_name:
        :param release:
        :return:
        """
        # 如果本地tar不存在，则执行完整流程
        tar = self.pull_module_tar(module_name, release)
        remote_tar = self.upload_tar(module_name, tar)
        backup_tar = self.backup(module_name)
        # 轮流停机、部署、启服务
        self.deploy_unzip_only(module_name, remote_tar, confirm=confirm)

    def deploy_unzip_only(self, module_name, deploy_tar, servers_address=None, confirm=True):
        u"""
        直接部署已经上传好的tar包，停服务、部署、启服务
        :param module_name:
        :param deploy_tar: jar全路径
        :param servers_address:
        :param confirm: 是否需要人工确认服务状态
        :return:
        """
        # 轮流停机、部署、启服务
        if servers_address is None:
            servers_address = self.APP_SERVER[module_name]
        for server_address in servers_address:
            self.stop_process(server_address, module_name)
            self.unzip_module_tar(server_address, module_name, deploy_tar)
            self.start_process(server_address, module_name)
            print green("在服务器%s上发布应用%s成功") % (server_address, module_name)
            if confirm:
                local('echo "请确认服务已启动成功再继续执行（Y）："')
                ctn = raw_input()
                if ctn not in ("y", "Y"):
                    raise Exception("exit")



class V:
    u"""
    打包所需要的数据集合Bean
    """
    GROUP_ID_PREFIX = "com.allinfinance"
    MODULE_TYPE = "web"
    EXTENSION_WAR = "war"
    EXTENSION_JAR = "jar"

    def __init__(self, group, module_type, version, group_name=None):
        self.group = group
        self.module_type = module_type
        self.version = version

        # 组装字段
        self.group_id = self.GROUP_ID_PREFIX + "." + ( self.group if group_name is None else group_name)
        self.artifact = self.group + "-" + self.module_type
        self.extension = self.EXTENSION_WAR if self.module_type == self.MODULE_TYPE else self.EXTENSION_JAR
        self.filename = self.artifact + "." + self.extension
