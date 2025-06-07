// script.js
document.addEventListener('DOMContentLoaded', () => {
    // 初始化编辑器配置
    const EDITOR_CONFIG = {
        mode: 'python',
        lineNumbers: true,
        theme: 'dracula',
        autofocus: true,
        indentUnit: 4,
        tabSize: 4,
        styleActiveLineGutter: true
    };

    // 示例URL映射
    const EXAMPLE_URLS = {
        Rotating_Cube: 'examples/rotating_cube.py',
        Brick_Beaking: 'examples/brick_breaking.py',
        Maze_Solver: 'examples/maze_solver.py',
        Code_Rain: 'examples/code_rain.py',
    };

    // 初始化编辑器
    const editor = CodeMirror.fromTextArea(
        document.getElementById('codeEditor'),
        EDITOR_CONFIG
    );

    // 获取DOM元素
    const statusElement = document.getElementById('status');
    const selectorElement = document.getElementById('exampleSelector');

    // 创建文件输入元素
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.py,.txt';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    // 异步加载代码函数
    async function loadCode(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP错误! 状态码: ${response.status}`);
            }
            return await response.text();
        } catch (error) {
            console.error('代码加载失败:', error);
            throw error;
        }
    }

    // 处理文件读取
    async function handleFileUpload(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            reader.readAsText(file);
        });
    }

    // 示例选择器事件处理
    selectorElement.addEventListener('change', async function () {
        const selectedValue = this.value;

        if (selectedValue === 'upLoad') {
            fileInput.click();
            return;
        }

        // 添加加载动画
        const originalText = statusElement.textContent;
        statusElement.textContent = '⏳ 加载中...';
        statusElement.style.color = '#ffcc00';

        try {
            const code = await loadCode(EXAMPLE_URLS[selectedValue]);
            editor.setValue(code);
            statusElement.textContent = `✅ [已加载] ${selectedValue}`;
            statusElement.style.color = '#a5d6a7';
        } catch (error) {
            console.error('加载失败:', error);
            editor.setValue("# 无法加载代码");
            statusElement.textContent = '❌ [加载失败]';
            statusElement.style.color = '#ff6b6b';
            // 5秒后恢复原始状态
            setTimeout(() => {
                statusElement.textContent = originalText;
                statusElement.style.color = '';
            }, 5000);
        }
    });

    // 文件选择处理
    fileInput.addEventListener('change', async (event) => {
        const [file] = event.target.files;
        if (!file) return;

        try {
            const content = await handleFileUpload(file);
            editor.setValue(content);
            statusElement.textContent = `[已加载] ${file.name}`;
        } catch (error) {
            console.error('文件读取失败:', error);
            alert('无法读取文件内容');
        } finally {
            // 重置文件输入，允许重复选择相同文件
            fileInput.value = '';
        }
    });

    // 初始加载默认示例
    selectorElement.dispatchEvent(new Event('change'));
});