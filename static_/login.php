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

// 处理登录请求
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    $sql = "SELECT * FROM user WHERE username='$username' AND password='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
    	$_SESSION['username'] = $username;
        //echo "登录成功！";
        header('Location: test.html');
        exit;
    } else {
        // 登录失败，输出JavaScript代码
        echo '<script>';
        echo 'alert("用户名或密码错误！");';
        echo 'window.location.href = "index.html";';
        echo '</script>';
        exit; // 防止进一步的输出
    }
}

// 关闭数据库连接
$conn->close();
?>