<?php
// 连接到数据库
$servername = "localhost";
$username = "root";
$password = "666";
$dbname = "ai_login";
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 处理注册请求
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    $sql = "INSERT INTO user (username, password) VALUES ('$username', '$password')";

    if ($conn->query($sql) === TRUE) {
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
        echo 'alert("注册失败，请检查数据库连接！");';
        echo 'window.location.href = "index.html";';
        echo '</script>';
        exit; // 防止进一步的输出
    }
}

// 关闭数据库连接
$conn->close();
?>
