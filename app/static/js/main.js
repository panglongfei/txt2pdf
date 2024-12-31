document.addEventListener('DOMContentLoaded', function () {
    // 获取表单和相关元素
    const form = document.querySelector('form');
    const fileInput = document.getElementById('txtFile');
    const submitButton = document.querySelector('button[type="submit"]');

    // 文件选择时的处理
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            // 检查文件类型
            if (!file.name.toLowerCase().endsWith('.txt')) {
                alert('请选择TXT文件！');
                fileInput.value = '';
                return;
            }

            // 检查文件大小（最大10MB）
            if (file.size > 10 * 1024 * 1024) {
                alert('文件大小不能超过10MB！');
                fileInput.value = '';
                return;
            }
        }
    });

    // 表单提交处理
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // 检查是否选择了文件
        if (!fileInput.files[0]) {
            alert('请选择要转换的文件！');
            return;
        }

        // 创建FormData对象
        const formData = new FormData(form);

        // 禁用提交按钮，显示加载状态
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 转换中...';

        try {
            // 发送转换请求
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // 检查响应类型
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/pdf')) {
                    // 如果是PDF文件，创建下载
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = fileInput.files[0].name.replace('.txt', '.pdf');
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } else {
                    // 显示成功消息
                    const result = await response.text();
                    showAlert('success', '转换成功！' + result);
                }
            } else {
                // 显示错误消息
                const error = await response.text();
                showAlert('danger', '转换失败：' + error);
            }
        } catch (error) {
            showAlert('danger', '发生错误：' + error.message);
        } finally {
            // 恢复提交按钮状态
            submitButton.disabled = false;
            submitButton.innerHTML = '转换为PDF';
        }
    });

    // 显示提示信息的函数
    function showAlert(type, message) {
        // 移除现有的提示
        const existingAlert = document.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        // 创建新的提示
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // 插入提示到表单后面
        form.parentNode.insertBefore(alert, form.nextSibling);

        // 5秒后自动关闭提示
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    }
}); 