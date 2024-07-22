<?php
// 数据库文件路径
$dbfile = "ai_login.db";

// 连接到数据库
try {
    $pdo = new PDO("sqlite:$dbfile");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 处理注册请求
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];

        // 检查用户名是否已存在
        $checkSql = "SELECT username FROM user WHERE username = :username";
        $checkStmt = $pdo->prepare($checkSql);
        $checkStmt->bindParam(':username', $username);
        $checkStmt->execute();
        if ($checkStmt->fetchColumn() !== false) {
            // 用户名已存在，输出JavaScript代码
            echo '<script>';
            echo 'alert("用户名已存在，请尝试其他用户名！");';
            echo 'window.location.href = "index.html";';
            echo '</script>';
            exit; // 防止进一步的输出
        }

        // 准备SQL插入语句，使用占位符
        $sql = "INSERT INTO user (username, password) VALUES (:username, :password)";

        // 预处理语句
        $stmt = $pdo->prepare($sql);

        // 绑定参数
        $stmt->bindParam(':username', $username);
        $stmt->bindParam(':password', $password);

        // 执行插入操作
        if ($stmt->execute()) {
            //echo "注册成功！";
            // 注册成功，输出JavaScript代码
            echo '<script>';
            echo 'alert("注册成功！");';
            echo 'window.location.href = "index.html";';
            echo '</script>';
            exit; // 防止进一步的输出
        } else {
            //echo "注册失败: " . $conn->error;
            // 注册失败，输出JavaScript代码
            echo '<script>';
            echo 'alert("注册失败，请检查输入或数据库连接！");';
            echo 'window.location.href = "index.html";';
            echo '</script>';
            exit; // 防止进一步的输出
        }
    }

} catch (PDOException $e) {
    // 输出连接或查询时发生的任何错误
    echo "Error: " . $e->getMessage();
}

// 关闭数据库连接
$pdo = null;
?>