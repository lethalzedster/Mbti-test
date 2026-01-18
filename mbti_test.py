#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MBTI 人格测试程序
测试四个维度：E/I, S/N, T/F, J/P
"""

class MBTITest:
    def __init__(self):
        # 测试题目，格式：(问题, 维度, A选项倾向, B选项倾向)
        self.questions = [
            # E vs I (外向 vs 内向)
            ("在社交聚会中，你通常：", "EI", "E", "I",
             "A. 主动与很多人交谈，感到精力充沛",
             "B. 更愿意与少数几个人深入交谈"),
            
            ("周末休息时，你更喜欢：", "EI", "E", "I",
             "A. 出去和朋友们一起活动",
             "B. 在家独处或做自己喜欢的事"),
            
            ("工作或学习时，你更喜欢：", "EI", "E", "I",
             "A. 在团队中协作，边讨论边思考",
             "B. 独立工作，有自己的思考空间"),
            
            ("当遇到问题时，你倾向于：", "EI", "E", "I",
             "A. 立即找人讨论，说出来帮助理清思路",
             "B. 先自己思考，想清楚了再和别人交流"),
            
            ("认识新朋友后，你通常：", "EI", "E", "I",
             "A. 很快就能熟络起来，主动分享",
             "B. 需要时间慢慢了解，比较谨慎"),
            
            # S vs N (感觉 vs 直觉)
            ("在处理任务时，你更注重：", "SN", "S", "N",
             "A. 具体的事实、细节和实际经验",
             "B. 整体的概念、含义和未来可能性"),
            
            ("学习新知识时，你更喜欢：", "SN", "S", "N",
             "A. 从具体例子开始，循序渐进",
             "B. 先理解整体框架和原理"),
            
            ("描述事情时，你倾向于：", "SN", "S", "N",
             "A. 具体、详细、按步骤描述",
             "B. 概括性描述，强调要点和意义"),
            
            ("你更相信：", "SN", "S", "N",
             "A. 实际经验和已被证明的方法",
             "B. 直觉、灵感和创新的想法"),
            
            ("在日常生活中，你更关注：", "SN", "S", "N",
             "A. 现在和眼前的事情",
             "B. 未来和各种可能性"),
            
            # T vs F (思考 vs 情感)
            ("做决定时，你主要依据：", "TF", "T", "F",
             "A. 逻辑分析和客观标准",
             "B. 个人价值观和对他人的影响"),
            
            ("当朋友向你倾诉烦恼时，你会：", "TF", "T", "F",
             "A. 帮助分析问题，提供解决方案",
             "B. 首先给予情感支持和理解"),
            
            ("评价一件事时，你更看重：", "TF", "T", "F",
             "A. 是否合理、有效、公平",
             "B. 是否和谐、是否考虑了大家的感受"),
            
            ("在团队中，你更倾向于：", "TF", "T", "F",
             "A. 直接指出问题和不足",
             "B. 先肯定优点，委婉提出建议"),
            
            ("别人认为你是一个：", "TF", "T", "F",
             "A. 理性、客观的人",
             "B. 热情、体贴的人"),
            
            # J vs P (判断 vs 感知)
            ("对待计划，你的态度是：", "JP", "J", "P",
             "A. 喜欢提前规划，按计划执行",
             "B. 更喜欢灵活应变，保持开放性"),
            
            ("工作方式上，你更喜欢：", "JP", "J", "P",
             "A. 有明确的截止日期和时间表",
             "B. 时间充裕，可以随时调整"),
            
            ("你的生活状态通常是：", "JP", "J", "P",
             "A. 有条理，物品摆放整齐",
             "B. 比较随性，觉得舒适就好"),
            
            ("面对任务时，你倾向于：", "JP", "J", "P",
             "A. 尽早开始，避免最后赶工",
             "B. 在截止日期前完成即可，有压力更有动力"),
            
            ("做决定时，你更倾向于：", "JP", "J", "P",
             "A. 快速做出决定，然后执行",
             "B. 保持选择的开放性，看情况再定"),
        ]
        
        # 分数统计
        self.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        
        # MBTI类型描述
        self.type_descriptions = {
            "ISTJ": "检查员 - 认真负责，注重细节，遵守承诺",
            "ISFJ": "守卫者 - 温暖体贴，关心他人，忠诚可靠",
            "INFJ": "提倡者 - 富有洞察力，理想主义，追求意义",
            "INTJ": "建筑师 - 独立思考，战略眼光，追求完美",
            "ISTP": "鉴赏家 - 冷静理性，善于分析，动手能力强",
            "ISFP": "探险家 - 温和友善，热爱生活，追求自由",
            "INFP": "调停者 - 理想主义，富有创造力，追求真实",
            "INTP": "逻辑学家 - 善于思考，创新求知，追求真理",
            "ESTP": "企业家 - 精力充沛，大胆冒险，善于行动",
            "ESFP": "表演者 - 热情开朗，享受当下，充满活力",
            "ENFP": "竞选者 - 热情创新，充满可能性，善于激励他人",
            "ENTP": "辩论家 - 聪明机智，喜欢挑战，善于创新",
            "ESTJ": "总经理 - 务实高效，善于管理，注重秩序",
            "ESFJ": "执政官 - 热心助人，善于社交，注重和谐",
            "ENFJ": "主人公 - 富有魅力，善于领导，关心他人",
            "ENTJ": "指挥官 - 果断坚定，善于规划，天生领导者",
        }
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print(" " * 20 + "MBTI 人格测试")
        print("=" * 60)
        print("\n欢迎参加MBTI人格测试！")
        print("\n本测试将通过20道题目，帮助你了解自己的人格类型。")
        print("MBTI测试评估四个维度：")
        print("  · E (外向) vs I (内向)")
        print("  · S (感觉) vs N (直觉)")
        print("  · T (思考) vs F (情感)")
        print("  · J (判断) vs P (感知)")
        print("\n请根据你的真实感受选择最符合你的选项。")
        print("=" * 60)
        input("\n按回车键开始测试...")
    
    def conduct_test(self):
        """进行测试"""
        print("\n开始测试！\n")
        
        for i, question_data in enumerate(self.questions, 1):
            question, dimension, a_type, b_type, option_a, option_b = question_data
            
            print(f"\n问题 {i}/20")
            print("-" * 60)
            print(question)
            print(option_a)
            print(option_b)
            
            while True:
                choice = input("\n请选择 A 或 B: ").strip().upper()
                if choice in ['A', 'B']:
                    if choice == 'A':
                        self.scores[a_type] += 1
                    else:
                        self.scores[b_type] += 1
                    break
                else:
                    print("无效输入，请输入 A 或 B")
    
    def calculate_result(self):
        """计算结果"""
        result = ""
        result += "E" if self.scores["E"] >= self.scores["I"] else "I"
        result += "S" if self.scores["S"] >= self.scores["N"] else "N"
        result += "T" if self.scores["T"] >= self.scores["F"] else "F"
        result += "J" if self.scores["J"] >= self.scores["P"] else "P"
        return result
    
    def display_result(self, mbti_type):
        """显示结果"""
        print("\n" + "=" * 60)
        print(" " * 20 + "测试结果")
        print("=" * 60)
        
        print(f"\n你的MBTI类型是: {mbti_type}")
        print(f"\n{self.type_descriptions.get(mbti_type, '未知类型')}")
        
        print("\n各维度得分：")
        print(f"  外向(E) {self.scores['E']} : {self.scores['I']} 内向(I)")
        print(f"  感觉(S) {self.scores['S']} : {self.scores['N']} 直觉(N)")
        print(f"  思考(T) {self.scores['T']} : {self.scores['F']} 情感(F)")
        print(f"  判断(J) {self.scores['J']} : {self.scores['P']} 感知(P)")
        
        print("\n" + "=" * 60)
        print("\n感谢参与测试！")
        print("注意：MBTI测试仅供参考，不能完全定义一个人。")
        print("=" * 60)
    
    def run(self):
        """运行测试"""
        self.display_welcome()
        self.conduct_test()
        result = self.calculate_result()
        self.display_result(result)


def main():
    """主函数"""
    test = MBTITest()
    test.run()


if __name__ == "__main__":
    main()
