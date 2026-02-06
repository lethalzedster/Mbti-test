#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MBTI 人格测试 - Web应用
类似16personalities的测试界面
"""

from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 测试题目数据 - 60题，每个维度15题
QUESTIONS = [
    # E vs I (外向 vs 内向) - 15题
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
    {"id": 13, "text": "你更倾向于在安静的环境中思考和工作", "dimension": "EI", "direction": "I"},
    {"id": 14, "text": "你喜欢通过交流来整理自己的想法", "dimension": "EI", "direction": "E"},
    {"id": 15, "text": "长时间独处让你感到舒适和充实", "dimension": "EI", "direction": "I"},
    
    # S vs N (感觉 vs 直觉) - 15题
    {"id": 16, "text": "你更关注具体的事实和细节", "dimension": "SN", "direction": "S"},
    {"id": 17, "text": "你经常思考事物的深层含义和可能性", "dimension": "SN", "direction": "N"},
    {"id": 18, "text": "你更相信实践经验而非理论", "dimension": "SN", "direction": "S"},
    {"id": 19, "text": "你喜欢探索新的想法和概念", "dimension": "SN", "direction": "N"},
    {"id": 20, "text": "你倾向于按部就班地完成任务", "dimension": "SN", "direction": "S"},
    {"id": 21, "text": "你经常想象未来的各种可能性", "dimension": "SN", "direction": "N"},
    {"id": 22, "text": "你更喜欢使用已经验证过的方法", "dimension": "SN", "direction": "S"},
    {"id": 23, "text": "你善于看到事物之间隐藏的联系", "dimension": "SN", "direction": "N"},
    {"id": 24, "text": "你更关注当下而非未来", "dimension": "SN", "direction": "S"},
    {"id": 25, "text": "你经常被新奇的想法和理论吸引", "dimension": "SN", "direction": "N"},
    {"id": 26, "text": "你更注重实际应用而非抽象概念", "dimension": "SN", "direction": "S"},
    {"id": 27, "text": "你喜欢头脑风暴和创新", "dimension": "SN", "direction": "N"},
    {"id": 28, "text": "你倾向于记住具体的细节而非整体印象", "dimension": "SN", "direction": "S"},
    {"id": 29, "text": "你经常思考'为什么'而不只是'是什么'", "dimension": "SN", "direction": "N"},
    {"id": 30, "text": "你更喜欢处理实际问题而非理论问题", "dimension": "SN", "direction": "S"},
    
    # T vs F (思考 vs 情感) - 15题
    {"id": 31, "text": "做决定时，你主要依据逻辑和客观分析", "dimension": "TF", "direction": "T"},
    {"id": 32, "text": "你很容易理解和感受他人的情绪", "dimension": "TF", "direction": "F"},
    {"id": 33, "text": "你认为真相比和谐更重要", "dimension": "TF", "direction": "T"},
    {"id": 34, "text": "你在做决定时会优先考虑对他人的影响", "dimension": "TF", "direction": "F"},
    {"id": 35, "text": "你倾向于客观公正地评判事物", "dimension": "TF", "direction": "T"},
    {"id": 36, "text": "你很难对他人的请求说不", "dimension": "TF", "direction": "F"},
    {"id": 37, "text": "你更看重效率而非人际和谐", "dimension": "TF", "direction": "T"},
    {"id": 38, "text": "你经常为他人的困境感到难过", "dimension": "TF", "direction": "F"},
    {"id": 39, "text": "你喜欢辩论和理性讨论", "dimension": "TF", "direction": "T"},
    {"id": 40, "text": "维护他人的感受对你很重要", "dimension": "TF", "direction": "F"},
    {"id": 41, "text": "你更注重公平而非体谅", "dimension": "TF", "direction": "T"},
    {"id": 42, "text": "你善于提供情感支持和安慰", "dimension": "TF", "direction": "F"},
    {"id": 43, "text": "批评他人时你倾向于直接指出问题", "dimension": "TF", "direction": "T"},
    {"id": 44, "text": "你在冲突中更关注人际关系而非谁对谁错", "dimension": "TF", "direction": "F"},
    {"id": 45, "text": "你认为原则比特殊情况更重要", "dimension": "TF", "direction": "T"},
    
    # J vs P (判断 vs 感知) - 15题
    {"id": 46, "text": "你喜欢提前规划并遵守计划", "dimension": "JP", "direction": "J"},
    {"id": 47, "text": "你更喜欢保持灵活性和开放性", "dimension": "JP", "direction": "P"},
    {"id": 48, "text": "你的生活和工作空间通常井井有条", "dimension": "JP", "direction": "J"},
    {"id": 49, "text": "你倾向于在最后期限前完成任务", "dimension": "JP", "direction": "P"},
    {"id": 50, "text": "你喜欢有明确的规则和结构", "dimension": "JP", "direction": "J"},
    {"id": 51, "text": "你享受即兴发挥和随机应变", "dimension": "JP", "direction": "P"},
    {"id": 52, "text": "你会尽早完成任务以避免压力", "dimension": "JP", "direction": "J"},
    {"id": 53, "text": "你倾向于同时处理多个项目", "dimension": "JP", "direction": "P"},
    {"id": 54, "text": "你喜欢做决定并坚持执行", "dimension": "JP", "direction": "J"},
    {"id": 55, "text": "你喜欢保持选择的开放性", "dimension": "JP", "direction": "P"},
    {"id": 56, "text": "你觉得有条理的生活让你舒适", "dimension": "JP", "direction": "J"},
    {"id": 57, "text": "你在压力下工作效率更高", "dimension": "JP", "direction": "P"},
    {"id": 58, "text": "未完成的任务会让你感到不安", "dimension": "JP", "direction": "J"},
    {"id": 59, "text": "你喜欢探索多种可能性而不急于做决定", "dimension": "JP", "direction": "P"},
    {"id": 60, "text": "你倾向于制定详细的待办清单", "dimension": "JP", "direction": "J"},
]

# MBTI类型详细描述
TYPE_DESCRIPTIONS = {
    "ISTJ": {
        "name": "物流师",
        "title": "务实可靠的实干家",
        "traits": ["责任心强", "注重细节", "逻辑清晰", "值得信赖", "有条不紊"],
        "description": "ISTJ型人格严谨、务实，重视传统和秩序。他们是可靠的组织者，擅长制定计划并严格执行。对承诺极为认真，总是言出必行。",
        "strengths": ["高度责任感和可靠性", "出色的组织和计划能力", "注重细节，工作精确", "逻辑思维清晰", "遵守规则和程序"],
        "weaknesses": ["可能过于刻板和固执", "难以适应突发变化", "不善于表达情感", "可能忽视创新可能性"],
        "careers": ["会计师", "审计师", "项目管理", "法律工作", "工程师", "军人", "医疗管理"],
        "relationships": "ISTJ在人际关系中忠诚可靠，重视长期稳定的关系。虽然不善于表达情感，但会通过实际行动来表达关心。",
        "growth": "尝试更灵活地看待问题，学习接受变化。多关注他人的情感需求，练习表达自己的感受。"
    },
    "ISFJ": {
        "name": "守卫者",
        "title": "温暖体贴的保护者",
        "traits": ["忠诚可靠", "细心体贴", "乐于助人", "记忆力强", "富有同理心"],
        "description": "ISFJ型人格温暖、负责，致力于保护和照顾他人。他们默默付出，是最可靠的支持者。具有出色的观察力和记忆力，能记住他人的重要细节。",
        "strengths": ["极强的责任感", "细致体贴，善于照顾他人", "忠诚可靠", "实践能力强", "记忆力出色"],
        "weaknesses": ["过度承担责任", "难以拒绝他人", "不善于应对冲突", "可能忽视自己的需求"],
        "careers": ["护士", "教师", "社工", "行政助理", "人力资源", "图书管理员", "咨询顾问"],
        "relationships": "ISFJ是忠诚而专注的伴侣，善于营造温暖和谐的氛围。他们记得每个特殊的日子，会用实际行动表达爱意。",
        "growth": "学会设定界限，适当拒绝不合理要求。多关注自己的需求，不要总是把他人放在第一位。"
    },
    "INFJ": {
        "name": "提倡者",
        "title": "富有洞察力的理想主义者",
        "traits": ["富有洞察力", "理想主义", "有创造力", "果断", "神秘"],
        "description": "INFJ型人格神秘而富有洞察力，追求有意义的人生。他们致力于帮助他人实现潜能，是天生的咨询者和导师。具有独特的直觉，能够深刻理解他人。",
        "strengths": ["深刻的洞察力和直觉", "富有同理心", "理想主义和使命感", "创造力强", "善于激励他人"],
        "weaknesses": ["过于理想化", "容易感到疲惫", "难以处理批评", "可能过度关注他人而忽视自己"],
        "careers": ["心理咨询师", "作家", "教师", "人力资源", "社会工作者", "艺术家", "非营利组织"],
        "relationships": "INFJ寻求深刻而有意义的关系，重视精神层面的连接。他们是理解和支持的伴侣，但需要独处时间来充电。",
        "growth": "学会接受现实的不完美，不要对自己和他人要求过高。适当表达自己的需求，避免过度付出导致倦怠。"
    },
    "INTJ": {
        "name": "建筑师",
        "title": "富有想象力的战略家",
        "traits": ["战略思维", "独立", "追求完美", "富有远见", "自信"],
        "description": "INTJ型人格具有战略眼光，善于长远规划。他们独立思考，追求知识和效率，是天生的系统设计师。对自己的想法充满信心，执行力强。",
        "strengths": ["出色的战略规划能力", "独立思考和创新", "追求卓越和完美", "逻辑思维严密", "学习能力强"],
        "weaknesses": ["可能显得傲慢", "缺乏耐心", "不善于处理情感", "过于追求完美"],
        "careers": ["软件工程师", "科学家", "战略顾问", "投资分析师", "建筑师", "教授", "系统分析师"],
        "relationships": "INTJ在关系中重视智力契合，寻找能够进行深度交流的伴侣。虽然不善于表达情感，但一旦承诺就会非常忠诚。",
        "growth": "学会更好地理解和表达情感，多倾听他人的观点。不要过于追求完美，接受事物的不完美性。"
    },
    "ISTP": {
        "name": "鉴赏家",
        "title": "大胆灵活的实践者",
        "traits": ["实践能力强", "冷静客观", "适应力强", "善于分析", "独立"],
        "description": "ISTP型人格冷静、实际，善于用双手探索世界。他们是天生的问题解决者，喜欢拆解和理解事物的运作原理。行动力强，能够快速应对突发情况。",
        "strengths": ["出色的动手能力", "冷静理性的问题解决", "适应能力强", "独立自主", "善于危机处理"],
        "weaknesses": ["不善于长期规划", "可能显得冷漠", "难以表达情感", "容易感到无聊"],
        "careers": ["机械师", "工程师", "飞行员", "外科医生", "运动员", "技术人员", "侦探"],
        "relationships": "ISTP需要个人空间和自由，不喜欢过于亲密的关系。他们通过行动而非言语来表达关心，喜欢与伴侣一起进行活动。",
        "growth": "学会更好地规划未来，不要只活在当下。多关注他人的情感需求，练习表达自己的感受。"
    },
    "ISFP": {
        "name": "探险家",
        "title": "灵活友善的艺术家",
        "traits": ["艺术气质", "敏感", "热爱自由", "活在当下", "温和友善"],
        "description": "ISFP型人格温和、敏感，热爱生活中的美好事物。他们追求自由和真实的自我表达，具有独特的审美眼光。善于用行动表达情感，重视个人价值观。",
        "strengths": ["艺术天赋和审美能力", "温和友善", "灵活适应", "忠于内心价值观", "善于观察细节"],
        "weaknesses": ["难以面对冲突", "过于敏感", "缺乏长期规划", "可能过度追求完美"],
        "careers": ["艺术家", "设计师", "摄影师", "音乐家", "厨师", "美容师", "兽医"],
        "relationships": "ISFP是温柔体贴的伴侣，擅长用行动表达爱意。他们重视和谐的关系，需要伴侣尊重他们的个人空间和价值观。",
        "growth": "学会更好地规划未来，不要只关注眼前。练习面对冲突，勇敢表达自己的需求和观点。"
    },
    "INFP": {
        "name": "调停者",
        "title": "充满诗意的理想主义者",
        "traits": ["理想主义", "富有同情心", "创造力强", "追求真实", "深思熟虑"],
        "description": "INFP型人格温柔、富有创造力，追求内心的真实和意义。他们是理想主义的梦想家，致力于让世界变得更美好。具有深刻的情感和丰富的内心世界。",
        "strengths": ["深刻的同理心", "创造力和想象力丰富", "忠于价值观", "善于写作和表达", "开放包容"],
        "weaknesses": ["过于理想化", "容易情绪化", "难以面对批评", "可能拖延"],
        "careers": ["作家", "心理咨询师", "艺术家", "教师", "社会工作者", "翻译", "非营利工作"],
        "relationships": "INFP寻求深刻而真挚的关系，重视情感的共鸣。他们是理解和支持的伴侣，但需要伴侣理解他们的敏感和理想主义。",
        "growth": "学会接受现实，不要过于理想化。提高执行力，将梦想转化为实际行动。学会处理批评和冲突。"
    },
    "INTP": {
        "name": "逻辑学家",
        "title": "富有创新精神的发明家",
        "traits": ["逻辑思维强", "好奇心强", "独立思考", "求知欲强", "创新"],
        "description": "INTP型人格善于思考和分析，追求知识和真理。他们是创新的思想家和问题解决者，喜欢探索复杂的理论和概念。具有出色的分析能力和创造性思维。",
        "strengths": ["出色的逻辑分析能力", "创新思维", "开放的心态", "独立思考", "善于发现模式"],
        "weaknesses": ["可能显得冷漠", "难以表达情感", "容易陷入分析瘫痪", "不善于实际执行"],
        "careers": ["研究员", "程序员", "数学家", "哲学家", "分析师", "发明家", "大学教授"],
        "relationships": "INTP在关系中需要智力刺激和个人空间。他们不善于表达情感，但会用独特的方式表达关心。寻找能够理解他们思考方式的伴侣。",
        "growth": "学会更好地表达情感和关心他人。提高执行力，不要只停留在思考阶段。多关注现实生活的实际需求。"
    },
    "ESTP": {
        "name": "企业家",
        "title": "精明能干的实干家",
        "traits": ["行动力强", "大胆", "善于应变", "活力充沛", "务实"],
        "description": "ESTP型人格精力充沛、大胆冒险，善于抓住机会。他们是天生的谈判家和实干家，喜欢在行动中学习。具有出色的观察力和应变能力，擅长处理危机。",
        "strengths": ["行动力强", "适应能力出色", "善于谈判", "务实理性", "精力充沛"],
        "weaknesses": ["可能冲动", "缺乏长期规划", "不善于处理情感", "容易感到无聊"],
        "careers": ["企业家", "销售", "消防员", "警察", "运动员", "投资者", "急救人员"],
        "relationships": "ESTP是充满活力和趣味的伴侣，喜欢与伴侣一起冒险和尝试新事物。他们重视行动胜于言语，用实际方式表达爱意。",
        "growth": "学会更好地规划未来，不要只关注眼前。多考虑行动的长远后果，培养耐心。更多关注他人的情感需求。"
    },
    "ESFP": {
        "name": "表演者",
        "title": "自由奔放的娱乐者",
        "traits": ["热情", "善于社交", "乐观", "享受当下", "富有同情心"],
        "description": "ESFP型人格热情开朗，善于社交。他们享受生活，给周围的人带来欢乐和活力。具有强烈的感染力，能够营造轻松愉快的氛围。活在当下，珍惜每一刻。",
        "strengths": ["社交能力强", "乐观开朗", "实践能力强", "善于观察", "富有同情心"],
        "weaknesses": ["缺乏长期规划", "可能过于冲动", "难以面对批评", "容易分心"],
        "careers": ["演员", "活动策划", "销售", "导游", "美容师", "健身教练", "儿童工作者"],
        "relationships": "ESFP是热情而有趣的伴侣，擅长营造浪漫和惊喜。他们重视当下的快乐，喜欢与伴侣分享生活的美好时刻。",
        "growth": "学会更好地规划未来，培养财务管理能力。多思考行动的后果，不要过于冲动。学会接受建设性批评。"
    },
    "ENFP": {
        "name": "竞选者",
        "title": "热情洋溢的激励者",
        "traits": ["热情", "创造力强", "社交能力强", "充满好奇", "富有洞察力"],
        "description": "ENFP型人格热情、有创造力，充满可能性。他们善于激励他人，追求有意义的联系。具有丰富的想象力和感染力，能够看到事物的多种可能性。",
        "strengths": ["创造力和想象力丰富", "社交能力出色", "热情洋溢", "善于激励他人", "开放灵活"],
        "weaknesses": ["可能过于理想化", "容易分心", "难以坚持", "可能忽视细节"],
        "careers": ["作家", "记者", "咨询顾问", "营销", "教师", "演讲家", "心理学家"],
        "relationships": "ENFP是热情而富有创意的伴侣，重视情感连接和精神交流。他们为关系带来活力和新鲜感，但需要伴侣理解他们对自由的需求。",
        "growth": "学会坚持和专注，不要总是追逐新的可能性。提高执行力，将创意转化为实际成果。多关注细节和实际问题。"
    },
    "ENTP": {
        "name": "辩论家",
        "title": "机智聪慧的思考者",
        "traits": ["机智", "好奇心强", "善于辩论", "创新", "魅力四射"],
        "description": "ENTP型人格聪明、善于辩论，喜欢智力挑战。他们是创新的思想家和问题解决者，享受探索新想法和可能性。具有出色的口才和说服力。",
        "strengths": ["创新思维", "辩论能力强", "适应能力出色", "机智幽默", "善于发现机会"],
        "weaknesses": ["可能显得好辩", "难以坚持", "不善于处理情感", "可能忽视细节"],
        "careers": ["企业家", "律师", "顾问", "发明家", "营销", "工程师", "投资者"],
        "relationships": "ENTP是机智而有趣的伴侣，喜欢智力交锋和深度讨论。他们需要伴侣能够跟上他们的思维节奏，接受他们的挑战性格。",
        "growth": "学会坚持完成项目，不要总是追逐新想法。多关注他人的情感需求，不要过于好辩。提高对细节的关注。"
    },
    "ESTJ": {
        "name": "总经理",
        "title": "高效务实的管理者",
        "traits": ["组织能力强", "务实", "果断", "重视传统", "责任感强"],
        "description": "ESTJ型人格务实、高效，善于管理和组织。他们是天生的领导者和管理者，重视秩序和效率。具有出色的执行力，能够将计划付诸实践。",
        "strengths": ["出色的组织管理能力", "执行力强", "务实高效", "责任感强", "果断决策"],
        "weaknesses": ["可能过于刻板", "难以接受变化", "不善于处理情感", "可能显得专制"],
        "careers": ["管理者", "军官", "法官", "银行家", "项目经理", "警察", "企业高管"],
        "relationships": "ESTJ是可靠而忠诚的伴侣，重视传统和稳定。他们用实际行动表达关心，为家庭提供稳定和安全感。",
        "growth": "学会更灵活地看待问题，接受不同的观点。多关注他人的情感需求，不要过于强硬。尝试接受创新和变化。"
    },
    "ESFJ": {
        "name": "执政官",
        "title": "热心关怀的主人",
        "traits": ["热心", "善于合作", "忠诚", "注重和谐", "组织能力强"],
        "description": "ESFJ型人格热心、负责，致力于帮助他人。他们重视传统和和谐的人际关系，是优秀的组织者和协调者。善于营造温暖的氛围，关心他人的需求。",
        "strengths": ["善于照顾他人", "组织协调能力强", "忠诚可靠", "社交能力出色", "实践能力强"],
        "weaknesses": ["过于在意他人评价", "难以面对批评", "可能过度关注细节", "不善于处理冲突"],
        "careers": ["护士", "教师", "活动策划", "人力资源", "客户服务", "社区工作者", "行政管理"],
        "relationships": "ESFJ是体贴而忠诚的伴侣，擅长营造温馨的家庭氛围。他们重视传统和稳定的关系，喜欢照顾和支持伴侣。",
        "growth": "学会设定界限，不要过度关注他人评价。培养独立性，关注自己的需求。学会接受建设性批评。"
    },
    "ENFJ": {
        "name": "主人公",
        "title": "富有魅力的领导者",
        "traits": ["富有魅力", "善于激励", "有同理心", "组织能力强", "理想主义"],
        "description": "ENFJ型人格富有魅力和影响力，善于激励和领导他人。他们关心他人的成长和发展，是天生的导师和领袖。具有出色的沟通能力和组织能力。",
        "strengths": ["出色的领导能力", "善于激励他人", "同理心强", "沟通能力出色", "组织协调能力强"],
        "weaknesses": ["过于理想化", "可能忽视自己的需求", "难以处理批评", "可能过度干预"],
        "careers": ["教师", "人力资源", "咨询顾问", "政治家", "培训师", "心理学家", "公关"],
        "relationships": "ENFJ是充满爱心和支持的伴侣，致力于帮助伴侣成长。他们重视深刻的情感连接，擅长营造和谐的关系氛围。",
        "growth": "学会关注自己的需求，不要总是优先考虑他人。接受他人的不完美，不要过度干预。学会处理批评和拒绝。"
    },
    "ENTJ": {
        "name": "指挥官",
        "title": "大胆果断的领导者",
        "traits": ["领导力强", "果断", "战略思维", "高效", "自信"],
        "description": "ENTJ型人格果断、有远见，是天生的领导者。他们善于规划和执行，追求效率和成功。具有强大的组织能力和战略眼光，能够带领团队实现目标。",
        "strengths": ["出色的领导和战略能力", "果断高效", "逻辑思维强", "自信有魅力", "执行力强"],
        "weaknesses": ["可能显得强势", "缺乏耐心", "不善于处理情感", "可能忽视细节"],
        "careers": ["企业高管", "律师", "管理咨询", "企业家", "投资银行家", "政治家", "军官"],
        "relationships": "ENTJ是强大而忠诚的伴侣，重视效率和成长。他们寻找智力上的契合，需要伴侣能够理解他们的雄心壮志。",
        "growth": "学会更好地倾听和理解他人，不要过于强势。多关注情感层面，提高同理心。学会放慢节奏，欣赏过程。"
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
    app.run(host='0.0.0.0', debug=True, port=5000)
