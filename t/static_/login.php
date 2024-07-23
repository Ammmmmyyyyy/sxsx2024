
<?php
// 数据库文件路径
$dbfile = "ai_login.db";

try {
    // 创建PDO实例连接SQLite数据库
    $pdo = new PDO("sqlite:$dbfile");

    // 设置错误模式为异常
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 准备SQL查询语句，使用占位符
    $sql = "SELECT * FROM user WHERE username=:username AND password=:password";

    // 预处理语句
    $stmt = $pdo->prepare($sql);

    // 绑定参数
    $stmt->bindParam(':username', $username);
    $stmt->bindParam(':password', $password);

    // 设置参数值
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];
    }

    // 执行查询
    $stmt->execute();

    // 获取查询结果
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // 检查结果集中是否有数据
    if (count($result) > 0) {
        $_SESSION['username'] = $username;
        //echo "登录成功！";
        header('Location: test.html');
    } else {
        // 登录失败，输出JavaScript代码
        echo '<script>';
        echo 'alert("用户名或密码错误！");';
        echo 'window.location.href = "index.html";';
        echo '</script>';
        exit; // 防止进一步的输出
    }

} catch (PDOException $e) {
    // 输出连接或查询时发生的任何错误
    echo "Error: " . $e->getMessage();
}

// 关闭数据库连接
$pdo = null;

?>