<?php
class SQLiteDB extends SQLite3
{
  function __construct()
  {
	 $this->open('ai_login.db');
  }
}
$db = new SQLiteDB();
if(!$db){
  echo $db->lastErrorMsg();
} else {
  echo "Yes, Opened database successfully<br/>\n";
}

// 先删除后创建表
$sql = "DROP table user";
$ret = $db->exec($sql);

// 创建表语句

$sql =<<<EOF
      CREATE TABLE if not exists user
      (username    TEXT  PRIMARY KEY     NOT NULL,
      password     TEXT    NOT NULL);
EOF;

$ret = $db->exec($sql);
if(!$ret){
  echo $db->lastErrorMsg();
} else {
  echo "Yes, Table created successfully<br/>\n";
}

$sql =<<<EOF
      INSERT INTO user (username,password)
      VALUES ('admin', 'admin' );
      INSERT INTO user (username,password)
      VALUES ('123', '123' );
EOF;

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Yes, Some Records has Inserted successfully<br/>\n";
   }
   $db->close();