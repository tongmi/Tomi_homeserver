# Tomi_homeserver
## qq:3343977167

Tomi_homeserver Help

选项：
-h/-help/-Help      获取帮助.
-v/-version/-Version        获取版本信息
-hostname/-h/-ip <hostname>     修改使用的主机名（不修改config.json的配置）
-port/-Port/-p <port>     修改使用的端口（不修改config.json的配置）
-ssh/-s/-S      启用远程ssh连接服务器
-password/-pd   指定ssh密码
-unlog/-ul      关闭日志流(实验功能)
-unplugin/-upg   关闭插件功能(实验功能)

编译服务器核心
make compile
完整输出服务器(默认输出文件夹为./outfile)
make install
运行服务器(可以加参数)
python3 Tomi_homeserver.pyc
例如：
    获取版本信息
        python Tomi_homeserver.pyc -v
    运行服务器并关闭日志功能
        python Tomi_homeserver.pyc -ul