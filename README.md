1、PHP配置  
  版本：php-8.3.9-Win32-vs16-x64（https://windows.php.net/download#php-8.2）  
  下载解压后在文件夹中将php.ini-development文件复制一份并改名为为php.ini  
  这里使用的是SQLite数据库，使用PDO库连接，因此我对php.ini的修改为去掉下面这些行的分号：  
  extension=mysqli （这行其实可以不改，但是finish login and register对应版本使用的是mysqli库连接mysql数据库所以有修改）  
  extension=pdo_sqlite   
  extension=sqlite3  
  （配置的时候参考了 https://blog.csdn.net/qq_37215621/article/details/126861680?spm=1001.2014.3001.5506 ，但是没查到对应的几行，所以是查询pdo、mysqli、sqlite然后自己改的）  
  使用的编辑器是vscode，搭配php server和php debug插件，需要将php server的PHP path设置为php.exe文件的绝对路径  
  此外，还需要将php解压后的文件夹的绝对路径和解压后的文件夹里面的ext文件夹（msqli和pdo等库）的绝对路径添加到环境变量中  
2、项目从static_\index.html页面进入  
3、ai_login.db数据库通过运行static_\init_ai_login.php创建，其包含的元组可通过运行static_\testdb_record.php查看。  
