#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MBTI 人格测试 - Web应用
类似16personalities的测试界面
"""

from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 测试题目数据
QUESTIONS = [
    # E vs I (外向 vs 内向) - 12题
    {"id": 1, "text": "你在社交聚会中感到精力充沛，喜欢与很多人交谈", "dimension": "EI", "direction": "E"},
    {"id": 2, "text": "你更喜欢独处或与少数亲密朋友相处", "dimension": "EI", "direction": "I"},
    {"id": 3, "text": "你倾向于先思考再说话", "dimension": "EI", "direction": "I"},
    {"id": 4, "text": "你在团队讨论中经常是主动发言的人", "dimension": "EI", "direction": "E"},
    {"id": 5, "text": "独自工作让你感到更加专注和高效", "dimension": "EI", "direction": "I"},
    {"id": 6, "text": "你很容易与陌生人展开对话", "dimension": "EI", "direction": "E"},
    {"id": 7, "text": "社交活动后你需要独处来恢复精力", "dimension": "EI", "direction": "I"},
    {"id": 8, "text": "你喜欢成为关注的焦点", "dimension": "EI", "direction": "E"},
    {"id": 9, "text": "你更喜欢通过文字而非面对面交流", "dimension": "EI", "direction": "I"},
    {"id": 10, "text": "你的朋友圈很广，认识很多人", "dimension": "EI", "direction": "E"},
    {"id": 11, "text": "你在开口前会仔细考虑要说什么", "dimension": "EI", "direction": "I"},
    {"id": 12, "text": "你享受参加大型社交活动和派对", "dimension": "EI", "direction": "E"},
    
    # S vs N (感觉 vs 直觉) - 12题
    {"id": 13, "text": "你更关注具体的事实和细节", "dimension": "SN", "direction": "S"},
    {"id": 14, "text": "你经常思考事物的深层含义和可能性", "dimension": "SN", "direction": "N"},
    {"id": 15, "text": "你更相信实践经验而非理论", "dimension": "SN", "direction": "S"},
    {"id": 16, "text": "你喜欢探索新的想法和概念", "dimension": "SN", "direction": "N"},
    {"id": 17, "text": "你倾向于按部就班地完成任务", "dimension": "SN", "direction": "S"},
    {"id": 18, "text": "你经常想象未来的各种可能性", "dimension": "SN", "direction": "N"},
    {"id": 19, "text": "你更喜欢使用已经验证过的方法", "dimension": "SN", "direction": "S"},
    {"id": 20, "text": "你善于看到事物之间隐藏的联系", "dimension": "SN", "direction": "N"},
    {"id": 21, "text": "你更关注当下而非未来", "dimension": "SN", "direction": "S"},
    {"id": 22, "text": "你经常被新奇的想法和理论吸引", "dimension": "SN", "direction": "N"},
    {"id": 23, "text": "你更注重实际应用而非抽象概念", "dimension": "SN", "direction": "S"},
    {"id": 24, "text": "你喜欢头脑风暴和创新", "dimension": "SN", "direction": "N"},
    
    # T vs F (思考 vs 情感) - 12题
    {"id": 25, "text": "做决定时，你主要依据逻辑和客观分析", "dimension": "TF", "direction": "T"},
    {"id": 26, "text": "你很容易理解和感受他人的情绪", "dimension": "TF", "direction": "F"},
    {"id": 27, "text": "你认为真相比和谐更重要", "dimension": "TF", "direction": "T"},
    {"id": 28, "text": "你在做决定时会优先考虑对他人的影响", "dimension": "TF", "direction": "F"},
    {"id": 29, "text": "你倾向于客观公正地评判事物", "dimension": "TF", "direction": "T"},
    {"id": 30, "text": "你很难对他人的请求说不", "dimension": "TF", "direction": "F"},
    {"id": 31, "text": "你更看重效率而非人际和谐", "dimension": "TF", "direction": "T"},
    {"id": 32, "text": "你经常为他人的困境感到难过", "dimension": "TF", "direction": "F"},
    {"id": 33, "text": "你喜欢辩论和理性讨论", "dimension": "TF", "direction": "T"},
    {"id": 34, "text": "维护他人的感受对你很重要", "dimension": "TF", "direction": "F"},
    {"id": 35, "text": "你更注重公平而非体谅", "dimension": "TF", "direction": "T"},
    {"id": 36, "text": "你善于提供情感支持和安慰", "dimension": "TF", "direction": "F"},
    
    # J vs P (判断 vs 感知) - 12题
    {"id": 37, "text": "你喜欢提前规划并遵守计划", "dimension": "JP", "direction": "J"},
    {"id": 38, "text": "你更喜欢保持灵活性和开放性", "dimension": "JP", "direction": "P"},
    {"id": 39, "text": "你的生活和工作空间通常井井有条", "dimension": "JP", "direction": "J"},
    {"id": 40, "text": "你倾向于在最后期限前完成任务", "dimension": "JP", "direction": "P"},
    {"id": 41, "text": "你喜欢有明确的规则和结构", "dimension": "JP", "direction": "J"},
    {"id": 42, "text": "你享受即兴发挥和随机应变", "dimension": "JP", "direction": "P"},
    {"id": 43, "text": "你会尽早完成任务以避免压力", "dimension": "JP", "direction": "J"},
    {"id": 44, "text": "你倾向于同时处理多个项目", "dimension": "JP", "direction": "P"},
    {"id": 45, "text": "你喜欢做决定并坚持执行", "dimension": "JP", "direction": "J"},
    {"id": 46, "text": "你喜欢保持选择的开放性", "dimension": "JP", "direction": "P"},
    {"id": 47, "text": "你觉得有条理的生活让你舒适", "dimension": "JP", "direction": "J"},
    {"id": 48, "text": "你在压力下工作效率更高", "dimension": "JP", "direction": "P"},
]

# MBTI类型详细描述
TYPE_DESCRIPTIONS = {
    "ISTJ": {
        "name": "物流师",
        "title": "务实可靠的实干家",
        "traits": ["责任心强", "注重细节", "逻辑清晰", "值得信赖"],
        "description": "ISTJ型人格严谨、务实，重视传统和秩序。他们是可靠的组织者，擅长制定计划并严格执行。"
    },
    "ISFJ": {
        "name": "守卫者",
        "title": "温暖体贴的保护者",
        "traits": ["忠诚可靠", "细心体贴", "乐于助人", "记忆力强"],
        "description": "ISFJ型人格温暖、负责，致力于保护和照顾他人。他们默默付出，是最可靠的支持者。"
    },
    "INFJ": {
        "name": "提倡者",
        "title": "富有洞察力的理想主义者",
        "traits": ["富有洞察力", "理想主义", "有创造力", "果断"],
        "description": "INFJ型人格神秘而富有洞察力，追求有意义的人生。他们致力于帮助他人实现潜能。"
    },
    "INTJ": {
        "name": "建筑师",
        "title": "富有想象力的战略家",
        "traits": ["战略思维", "独立", "追求完美", "富有远见"],
        "description": "INTJ型人格具有战略眼光，善于长远规划。他们独立思考，追求知识和效率。"
    },
    "ISTP": {
        "name": "鉴赏家",
        "title": "大胆灵活的实践者",
        "traits": ["实践能力强", "冷静客观", "适应力强", "善于分析"],
        "description": "ISTP型人格冷静、实际，善于用双手探索世界。他们是天生的问题解决者。"
    },
    "ISFP": {
        "name": "探险家",
        "title": "灵活友善的艺术家",
        "traits": ["艺术气质", "敏感", "热爱自由", "活在当下"],
        "description": "ISFP型人格温和、敏感，热爱生活中的美好事物。他们追求自由和真实的自我表达。"
    },
    "INFP": {
        "name": "调停者",
        "title": "充满诗意的理想主义者",
        "traits": ["理想主义", "富有同情心", "创造力强", "追求真实"],
        "description": "INFP型人格温柔、富有创造力，追求内心的真实和意义。他们是理想主义的梦想家。"
    },
    "INTP": {
        "name": "逻辑学家",
        "title": "富有创新精神的发明家",
        "traits": ["逻辑思维强", "好奇心强", "独立思考", "求知欲强"],
        "description": "INTP型人格善于思考和分析，追求知识和真理。他们是创新的思想家和问题解决者。"
    },
    "ESTP": {
        "name": "企业家",
        "title": "精明能干的实干家",
        "traits": ["行动力强", "大胆", "善于应变", "活力充沛"],
        "description": "ESTP型人格精力充沛、大胆冒险，善于抓住机会。他们是天生的谈判家和实干家。"
    },
    "ESFP": {
        "name": "表演者",
        "title": "自由奔放的娱乐者",
        "traits": ["热情", "善于社交", "乐观", "享受当下"],
        "description": "ESFP型人格热情开朗，善于社交。他们享受生活，给周围的人带来欢乐和活力。"
    },
    "ENFP": {
        "name": "竞选者",
        "title": "热情洋溢的激励者",
        "traits": ["热情", "创造力强", "社交能力强", "充满好奇"],
        "description": "ENFP型人格热情、有创造力，充满可能性。他们善于激励他人，追求有意义的联系。"
    },
    "ENTP": {
        "name": "辩论家",
        "title": "机智聪慧的思考者",
        "traits": ["机智", "好奇心强", "善于辩论", "创新"],
        "description": "ENTP型人格聪明、善于辩论，喜欢智力挑战。他们是创新的思想家和问题解决者。"
    },
    "ESTJ": {
        "name": "总经理",
        "title": "高效务实的管理者",
        "traits": ["组织能力强", "务实", "果断", "重视传统"],
        "description": "ESTJ型人格务实、高效，善于管理和组织。他们是天生的领导者和管理者。"
    },
    "ESFJ": {
        "name": "执政官",
        "title": "热心关怀的主人",
        "traits": ["热心", "善于合作", "忠诚", "注重和谐"],
        "description": "ESFJ型人格热心、负责，致力于帮助他人。他们重视传统和和谐的人际关系。"
    },
    "ENFJ": {
        "name": "主人公",
        "title": "富有魅力的领导者",
        "traits": ["富有魅力", "善于激励", "有同理心", "组织能力强"],
        "description": "ENFJ型人格富有魅力和影响力，善于激励和领导他人。他们关心他人的成长和发展。"
    },
    "ENTJ": {
        "name": "指挥官",
        "title": "大胆果断的领导者",
        "traits": ["领导力强", "果断", "战略思维", "高效"],
        "description": "ENTJ型人格果断、有远见，是天生的领导者。他们善于规划和执行，追求效率和成功。"
    },
}


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/test')
def test():
    """测试页面"""
    return render_template('test.html', questions=QUESTIONS)


@app.route('/calculate', methods=['POST'])
def calculate():
    """计算测试结果"""
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid request data"}), 400
    answers = data.get('answers', {})
    
    # 初始化分数
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    # 计算分数（1-5分对应：非常不同意到非常同意）
    for question in QUESTIONS:
        qid = str(question['id'])
        if qid in answers:
            score = int(answers[qid])
            direction = question['direction']
            
            # 将1-5的答案转换为-2到2的分数
            # 1(非常不同意)=-2, 2(不同意)=-1, 3(一般)=0, 4(同意)=1, 5(非常同意)=2
            adjusted_score = score - 3
            
            if adjusted_score > 0:
                scores[direction] += adjusted_score
            elif adjusted_score < 0:
                # 反向计分
                opposite = {'E': 'I', 'I': 'E', 'S': 'N', 'N': 'S', 
                           'T': 'F', 'F': 'T', 'J': 'P', 'P': 'J'}
                scores[opposite[direction]] += abs(adjusted_score)
    
    # 确定MBTI类型
    mbti_type = ""
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    mbti_type += "T" if scores["T"] >= scores["F"] else "F"
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"
    
    # 计算百分比
    total_ei = scores["E"] + scores["I"]
    total_sn = scores["S"] + scores["N"]
    total_tf = scores["T"] + scores["F"]
    total_jp = scores["J"] + scores["P"]
    
    percentages = {
        "E": round(scores["E"] / total_ei * 100 if total_ei > 0 else 50, 1),
        "I": round(scores["I"] / total_ei * 100 if total_ei > 0 else 50, 1),
        "S": round(scores["S"] / total_sn * 100 if total_sn > 0 else 50, 1),
        "N": round(scores["N"] / total_sn * 100 if total_sn > 0 else 50, 1),
        "T": round(scores["T"] / total_tf * 100 if total_tf > 0 else 50, 1),
        "F": round(scores["F"] / total_tf * 100 if total_tf > 0 else 50, 1),
        "J": round(scores["J"] / total_jp * 100 if total_jp > 0 else 50, 1),
        "P": round(scores["P"] / total_jp * 100 if total_jp > 0 else 50, 1),
    }
    
    result = {
        "type": mbti_type,
        "scores": scores,
        "percentages": percentages,
        "description": TYPE_DESCRIPTIONS.get(mbti_type, {})
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
