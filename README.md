# MBTI 人格测试系统

一个类似 16personalities 风格的 MBTI 人格测试 Web 应用。

## 功能特点

- 🎨 **现代化UI设计** - 类似16personalities的精美界面
- 📝 **60道测试题** - 全面评估四个维度，每个维度15题
- 📊 **5级量表** - 非常不同意到非常同意
- 📈 **可视化结果** - 百分比条形图展示各维度倾向
- 🎯 **16种人格类型** - 详细的类型描述
- ✨ **深度分析** - 包含优势、劣势、适合职业、人际关系和成长建议

## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 打开浏览器访问：
```
http://localhost:5000
```

## 项目结构

```
011825mbti/
├── app.py                 # Flask 应用主文件
├── requirements.txt       # 依赖包
├── templates/            # HTML 模板
│   ├── index.html       # 首页
│   └── test.html        # 测试页面
└── static/              # 静态资源
    ├── css/
    │   └── style.css    # 样式文件
    └── js/
        └── test.js      # 测试逻辑
```

## 测试维度

- **E/I** - 外向 vs 内向
- **S/N** - 感觉 vs 直觉  
- **T/F** - 思考 vs 情感
- **J/P** - 判断 vs 感知

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript
- **设计**: 响应式布局，渐变色彩

## 注意事项

- 本测试仅供参考和娱乐
- 建议诚实作答以获得准确结果
- MBTI不能完全定义一个人的性格
