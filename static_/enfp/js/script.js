let currentIndex = 0;  
  
document.querySelectorAll('.tab-btn').forEach((btn, index) => {  
    btn.addEventListener('click', function() {  
        // 移除所有按钮的active类  
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));  
        // 激活当前按钮  
        this.classList.add('active');  
        // 切换到对应的内容  
        showContent(index);  
    });  
});  
  
function showContent(index) {  
    // 移除所有内容块的active类  
    document.querySelectorAll('.content-item').forEach(item => item.classList.remove('active'));  
    // 激活对应的内容块  
    document.querySelectorAll('.content-item')[index].classList.add('active');  
    // 根据需要更新currentIndex（如果同时支持滑动）  
    currentIndex = index;  
}  
  
// 滑动逻辑（这里简化处理，具体实现取决于你的需求）  
document.querySelector('.prev').addEventListener('click', function() {  
    currentIndex = (currentIndex - 1 + document.querySelectorAll('.content-item').length) %