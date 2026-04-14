#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 设置页面配置
st.set_page_config(
    page_title="旅行规划助手",
    page_icon="🌍",
    layout="wide"
)

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 简化的目的地数据
destinations = {
    "亚洲": ["日本", "泰国", "中国", "韩国", "马来西亚"],
    "欧洲": ["法国", "意大利", "西班牙", "英国", "德国"],
    "北美洲": ["美国", "加拿大", "墨西哥"],
    "南美洲": ["巴西", "阿根廷", "秘鲁"],
    "大洋洲": ["澳大利亚", "新西兰"],
    "非洲": ["南非", "埃及", "摩洛哥"]
}
# 目的地详细信息
destination_details = {
    "日本": {
        "特色": "文化融合、美食、樱花/红叶季、购物",
        "最佳季节": "春季(3-4月,樱花)、秋季(10-11月,红叶)",
        "经典景点": ["东京迪士尼", "富士山", "京都金阁寺", "大阪城公园"],
        "美食": ["寿司", "拉面", "天妇罗", "怀石料理"],
        "文化注意": ["进入室内脱鞋", "公共场合保持安静", "垃圾分类严格"]
    },
    "泰国": {
        "特色": "海滩、寺庙、美食、热带气候",
        "最佳季节": "11月-次年4月(旱季)",
        "经典景点": ["曼谷大皇宫", "普吉岛", "清迈古城", "皮皮岛"],
        "美食": ["冬阴功汤", "泰式炒河粉", "芒果糯米饭", "绿咖喱鸡"],
        "文化注意": ["尊重王室和僧侣", "头部为神圣部位", "公共场合避免亲昵行为"]
    },
    "法国": {
        "特色": "浪漫、艺术、美食、时尚",
        "最佳季节": "5-6月(春季)、9-10月(秋季)",
        "经典景点": ["埃菲尔铁塔", "卢浮宫", "普罗旺斯", "凡尔赛宫"],
        "美食": ["法式面包", "奶酪", "葡萄酒", "鹅肝酱"],
        "文化注意": ["见面亲吻礼", "餐厅预约", "尊重艺术作品"]
    },
    "意大利": {
        "特色": "历史、美食、艺术、时尚",
        "最佳季节": "4-5月(春季)、9-10月(秋季)",
        "经典景点": ["罗马斗兽场", "威尼斯", "佛罗伦萨", "米兰大教堂"],
        "美食": ["披萨", "意大利面", "冰淇淋", "提拉米苏"],
        "文化注意": ["着装礼仪", "用餐时间较长", "教堂着装要求"]
    },
    "美国": {
        "特色": "多元文化、自然奇观、主题公园",
        "最佳季节": "因地区而异(西部5-10月,东部5-9月)",
        "经典景点": ["大峡谷", "纽约时代广场", "迪士尼乐园", "黄石国家公园"],
        "美食": ["汉堡", "披萨", "BBQ", "甜甜圈"],
        "文化注意": ["小费文化", "个人空间", "尊重多元文化"]
    }
}
# 旅行主题
travel_themes = {
    "休闲度假": ["放松", "SPA", "海滩", "晒太阳"],
    "美食探索": ["美食", "小吃", "餐厅", "烹饪课程"],
    "文化体验": ["文化", "艺术", "博物馆", "传统"],
    "户外探险": ["徒步", "登山", "骑行", "探险"],
    "购物血拼": ["购物", "商场", "市集", "奢侈品"],
    "亲子游玩": ["动物园", "游乐园", "互动体验", "教育"],
    "浪漫蜜月": ["浪漫", "海景", "私密", "烛光晚餐"],
    "历史考古": ["历史", "古迹", "遗址", "考古"]
}
# 预算水平
budget_levels = {
    "经济型": {"每日预算": "300-800元", "住宿": "青年旅社/经济型酒店"},
    "中等价位": {"每日预算": "800-1500元", "住宿": "三星级酒店/精品酒店"},
    "高端奢华": {"每日预算": "1500元以上", "住宿": "五星级酒店/度假村"}
}


# 安全提示
safety_tips = {
    "通用": [
        "提前了解目的地的安全状况和当地法律法规",
        "购买涵盖医疗和紧急救援的旅行保险",
        "保管好个人财物，尤其是在人多拥挤的地方",
        "随身携带紧急联系方式"
    ],
    "文化": {
        "日本": ["进入室内脱鞋", "公共场合保持安静", "垃圾分类严格"],
        "泰国": ["尊重王室和僧侣", "头部为神圣部位", "公共场合避免亲昵行为"],
        "法国": ["见面亲吻礼", "餐厅预约", "尊重艺术作品"],
        "意大利": ["着装礼仪", "用餐时间较长", "教堂着装要求"],
        "美国": ["小费文化", "个人空间", "尊重多元文化"]
    }
}
# 行李清单
packing_lists = {
    "春季": ["轻便外套", "长袖衬衫", "舒适鞋子", "雨伞"],
    "夏季": ["短袖衣物", "短裤", "凉鞋", "防晒霜", "太阳镜", "帽子"],
    "秋季": ["薄外套", "毛衣", "牛仔裤", "舒适鞋子"],
    "冬季": ["厚外套", "羽绒服", "围巾", "手套", "保暖内衣", "雪地靴"],
    "通用": ["护照和签证文件", "机票和酒店预订单", "手机充电器", "现金和信用卡"]
}

# 生成提示词
def generate_prompt(destination, theme, days, season, budget, special_requests):
    """生成发送给大模型的提示词"""
    dest_info = destination_details.get(destination, {})
    theme_keywords = travel_themes.get(theme, [])

    #季节转换
    season_mapping = {
        "春季（3-5月）": "春季",
        "夏季（6-8月）": "夏季",
        "秋季（9-11月）": "秋季",
        "冬季（12-2月）": "冬季"
    }
    season_short = season_mapping.get(season, "春季")
    
    # 构建提示词
    prompt = f"""
        你是一位专业的旅行顾问，擅长根据用户需求生成详细的旅行计划。请根据以下信息为用户生成一份到{destination}的{days}日-{theme}旅行计划：
        
        ### 用户基本信息
        - 目的地：{destination}
        - 旅行天数：{days}天
        - 旅行季节：{season_short}
        - 预算水平：{budget}（每日预算{budget_levels[budget]['每日预算']}）
        - 特殊要求：{special_requests if special_requests else "无特殊要求"}
        
        ### 目的地相关信息
        - 特色：{dest_info.get('特色', '丰富的文化和自然景观')}
        - 最佳季节：{dest_info.get('最佳季节', '全年适宜')}
        - 经典景点：{', '.join(dest_info.get('经典景点', ['当地著名景点']))}
        - 美食推荐：{', '.join(dest_info.get('美食', ['当地美食']))}
        - 文化注意事项：{', '.join(dest_info.get('文化注意', ['尊重当地习俗']))}
        
        ### 输出要求
        请生成一份详细的旅行计划，包括：
        1. 每日行程安排（按上午、下午、晚上分段，包括活动、交通、餐饮建议）
        2. 住宿推荐（符合用户预算水平）
        3. 预算估算（包括交通、住宿、餐饮、门票等分项，总预算）
        4. 实用贴士（安全提示、文化礼仪、天气准备、行李清单等）
        5. 语言风格：专业、实用、简洁，突出重点信息
    
        旅行计划：
        """
    return prompt

# 生成旅行计划
# Usage
def generate_travel_plan(destination, theme, days, season, budget, special_requests):
    """调用大模型生成旅行计划"""
    # 生成提示词
    prompt = generate_prompt(destination, theme, days, season, budget, special_requests)
    print(prompt)
    try:
        response = client.chat.completions.create(
            model="qwen-plus-2025-04-28",
            messages=[
                {"role": "system", "content": "你是一位专业、细致的旅行顾问，擅长根据用户需求生成详细的旅行计划。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"生成旅行计划时出错: {str(e)}")
        # 如果出错，返回一个示例旅行计划
        return """
    # 示例旅行计划
    ### 一、行程安排
    
    #### 第一天：抵达与适应
    - **上午**：抵达目的地，前往酒店办理入住，稍作休息
    - **交通**：机场→酒店（建议使用机场大巴或出租车）
    - **餐饮**：酒店附近餐厅，品尝当地特色早餐
    - **下午**：市区漫步，参观附近景点
    - **晚上**：在夜市品尝美食，体验当地夜生活
    - **住宿**：经济型酒店
    
    #### 第二天：探索城市
    - **上午**：参观主要景点
    - **交通**：地铁/公交车
    - **餐饮**：景区附近餐厅
    - **下午**：继续游览景点，参加文化活动
    - **晚上**：享用当地美食，观看传统表演
    - **住宿**：经济型酒店
    
    ### 二、预算估算
    - 每日预算：300-800元
    - 总预算：约2000元（2天）
    - 费用包含：住宿、餐饮、交通、门票等
    
    ## 三、实用贴士
    - 安全提示：保管好个人财物，注意交通安全
    - 文化礼仪：尊重当地习俗，穿着得体
    - 行李清单：轻便衣物、舒适鞋子、必要证件
    
    希望这份示例计划能为您提供建议！
    """

def main():
    st.title("🌍 旅行规划助手")
    st.markdown("根据您的偏好，生成个性化的旅行计划")

    # 侧边栏 - 用户输入
    with st.sidebar:
        st.header("旅行偏好")

        # 目的地选择
        region = st.selectbox("选择地区", list(destinations.keys()))
        destination = st.selectbox("选择国家", destinations[region])

        # 旅行主题
        theme = st.selectbox("旅行主题", list(travel_themes.keys()))

        # 旅行天数
        days = st.slider("旅行天数", 1, 30, 7)

        # 旅行季节
        season = st.selectbox("旅行季节", ["春季（3-5月）", "夏季（6-8月）", "秋季（9-11月）", "冬季（12-2月）"])

        # 预算水平
        budget = st.selectbox("预算水平", list(budget_levels.keys()))

        # 特殊要求
        special_requests = st.text_area("特殊要求或偏好", placeholder="例如：需要无障碍设施、对花粉过敏等")

        # 生成旅行计划按钮
        if st.button("生成旅行计划"):
            with st.spinner("正在生成旅行计划..."):
                travel_plan = generate_travel_plan(destination, theme, days, season, budget, special_requests)
                st.session_state.travel_plan = travel_plan
            st.success("旅行计划生成成功！")

    # 显示旅行计划
    if "travel_plan" in st.session_state:
        st.subheader("📅 您的个性化旅行计划")
        st.markdown(st.session_state.travel_plan)
    
        # 下载按钮
        st.download_button(
            label="📥 下载旅行计划",
            data=st.session_state.travel_plan,
            file_name=f"{destination}_{days}日_{theme}之旅.txt",
            mime="text/plain"
        )
    
        # 显示一些旅行统计数据
        st.subheader("📊 旅行统计")
        col1, col2, col3 = st.columns(3)
    
        # 预算可视化
        if budget == "高端奢华":
            daily_budget = int(budget_levels[budget]['每日预算'].replace('元以上', ''))
        else:
            daily_budget = int(budget_levels[budget]['每日预算'].split('-')[1].replace('元', ''))
        total_budget = daily_budget * days
    
        col1.metric("总预算", f"{total_budget}元")
        col2.metric("每日预算", budget_levels[budget]['每日预算'])
        col3.metric("旅行天数", f"{days}天")
    
        # 预算分布饼图
        fig, ax = plt.subplots(figsize=(8, 5))
        budget_data = {
            "住宿": total_budget * 0.4,
            "餐饮": total_budget * 0.25,
            "交通": total_budget * 0.2,
            "活动": total_budget * 0.15
        }
        ax.pie(
            budget_data.values(),
            labels=budget_data.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette('pastel')
        )
        ax.set_title("预算分布")
        st.pyplot(fig)
    else:
        # 显示欢迎信息和热门目的地
        st.markdown("""
        ### 欢迎使用旅行规划助手
        请在左侧面板填写您的旅行偏好，然后点击“生成旅行计划”按钮。
    
        ### 热门目的地推荐
        """)
    
        # 随机显示几个热门目的地
        popular_destinations = ["日本", "泰国", "法国", "意大利", "美国"]
        for dest in popular_destinations:
            if dest in destination_details:
                st.markdown(f"""
                **{dest}**
                - 特色: {destination_details[dest]["特色"]}
                - 最佳季节: {destination_details[dest]["最佳季节"]}
                - 经典景点: {", ".join(destination_details[dest]["经典景点"][:3])}
                """)

if __name__ == "__main__":
    main()






