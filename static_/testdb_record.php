<?php
// 数据库文件路径
$dbfile = "ai_login.db";

try {
    // 创建PDO实例连接SQLite数据库
    $pdo = new PDO("sqlite:$dbfile");

    // 设置错误模式为异常
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 准备SQL查询语句
    $sql = "SELECT * FROM user";
    //$sql = "SELECT * FROM user WHERE username='123' AND password='123'";

    // 预处理语句
    $stmt = $pdo->prepare($sql);

    // 执行查询
    $stmt->execute();

    // 获取查询结果
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // 检查结果集中是否有数据
    if (count($result) > 0) {
        echo "存在记录：";
        print_r($result);
    } else {
        echo "没有找到匹配的记录。";
    }

} catch (PDOException $e) {
    // 输出连接或查询时发生的任何错误
    echo "Error: " . $e->getMessage();
}

// 关闭数据库连接
$pdo = null;

?>