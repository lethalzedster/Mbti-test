let currentQuestion = 1;
const totalQuestions = 60;
let answers = {};

// 显示第一个问题
document.addEventListener('DOMContentLoaded', function() {
    showQuestion(1);
    
    // 为所有选项添加事件监听
    const allInputs = document.querySelectorAll('.option-input');
    allInputs.forEach(input => {
        input.addEventListener('change', function() {
            const questionId = this.name.replace('q', '');
            answers[questionId] = this.value;
            
            // 启用下一题按钮
            const card = this.closest('.question-card');
            const nextButton = card.querySelector('.next-button');
            nextButton.disabled = false;
            
            updateProgress();
        });
    });
});

function showQuestion(questionNumber) {
    // 隐藏所有问题
    const allCards = document.querySelectorAll('.question-card');
    allCards.forEach(card => {
        card.style.display = 'none';
    });
    
    // 显示当前问题
    const currentCard = document.querySelector(`[data-question-id="${questionNumber}"]`);
    if (currentCard) {
        currentCard.style.display = 'block';
        
        // 更新按钮显示
        const prevButton = currentCard.querySelector('.prev-button');
        const nextButton = currentCard.querySelector('.next-button');
        
        if (prevButton) {
            prevButton.style.display = questionNumber > 1 ? 'block' : 'none';
        }
        
        // 检查是否已回答
        if (answers[questionNumber]) {
            nextButton.disabled = false;
        }
        
        // 最后一题改变按钮文字
        if (questionNumber === totalQuestions) {
            nextButton.textContent = '查看结果';
        } else {
            nextButton.textContent = '下一题';
        }
    }
    
    currentQuestion = questionNumber;
    updateProgress();
}

function nextQuestion() {
    if (currentQuestion < totalQuestions) {
        showQuestion(currentQuestion + 1);
    } else {
        // 提交答案
        submitTest();
    }
}

function prevQuestion() {
    if (currentQuestion > 1) {
        showQuestion(currentQuestion - 1);
    }
}

function updateProgress() {
    const answeredCount = Object.keys(answers).length;
    const progress = (answeredCount / totalQuestions) * 100;
    
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    progressBar.style.width = progress + '%';
    progressText.textContent = `${answeredCount} / ${totalQuestions}`;
}

function submitTest() {
    // 检查是否所有问题都已回答
    if (Object.keys(answers).length < totalQuestions) {
        alert('请回答所有问题后再提交！');
        return;
    }
    
    // 显示加载状态
    const questionContainer = document.getElementById('questionContainer');
    questionContainer.innerHTML = '<div style="text-align: center; padding: 60px; color: white; font-size: 1.5rem;">正在分析你的人格类型...</div>';
    
    // 发送答案到服务器
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers: answers })
    })
    .then(response => response.json())
    .then(data => {
        displayResult(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('计算结果时出错，请重试！');
    });
}

function displayResult(result) {
    // 隐藏问题容器
    document.getElementById('questionContainer').style.display = 'none';
    document.querySelector('.progress-bar-container').style.display = 'none';
    
    // 显示结果容器
    const resultContainer = document.getElementById('resultContainer');
    resultContainer.style.display = 'block';
    
    // 填充结果数据
    document.getElementById('resultType').textContent = result.type;
    document.getElementById('resultName').textContent = result.description.name;
    document.getElementById('resultTitle').textContent = result.description.title;
    
    // 显示特质标签
    const traitsContainer = document.getElementById('resultTraits');
    traitsContainer.innerHTML = '';
    result.description.traits.forEach(trait => {
        const tag = document.createElement('div');
        tag.className = 'trait-tag';
        tag.textContent = trait;
        traitsContainer.appendChild(tag);
    });
    
    // 显示描述
    document.getElementById('resultDescription').textContent = result.description.description;
    
    // 显示优势
    const strengthsList = document.getElementById('strengthsList');
    strengthsList.innerHTML = '';
    result.description.strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });
    
    // 显示劣势/成长空间
    const weaknessesList = document.getElementById('weaknessesList');
    weaknessesList.innerHTML = '';
    result.description.weaknesses.forEach(weakness => {
        const li = document.createElement('li');
        li.textContent = weakness;
        weaknessesList.appendChild(li);
    });
    
    // 显示适合职业
    const careersList = document.getElementById('careersList');
    careersList.textContent = result.description.careers.join('、');
    
    // 显示人际关系说明
    document.getElementById('relationshipsText').textContent = result.description.relationships;
    
    // 显示成长建议
    document.getElementById('growthText').textContent = result.description.growth;
    
    // 更新百分比条
    setTimeout(() => {
        updatePercentageBar('E', 'I', result.percentages);
        updatePercentageBar('S', 'N', result.percentages);
        updatePercentageBar('T', 'F', result.percentages);
        updatePercentageBar('J', 'P', result.percentages);
    }, 300);
}

function updatePercentageBar(left, right, percentages) {
    const leftPercent = percentages[left];
    const rightPercent = percentages[right];
    
    document.getElementById('percent' + left).textContent = leftPercent + '%';
    document.getElementById('percent' + right).textContent = rightPercent + '%';
    
    document.getElementById('bar' + left).style.width = (leftPercent / 2) + '%';
    document.getElementById('bar' + right).style.width = (rightPercent / 2) + '%';
    
    // 高亮显示主导倾向
    if (leftPercent > rightPercent) {
        document.getElementById('label' + left).style.color = '#667eea';
        document.getElementById('label' + left).style.fontWeight = 'bold';
    } else {
        document.getElementById('label' + right).style.color = '#f5576c';
        document.getElementById('label' + right).style.fontWeight = 'bold';
    }
}
