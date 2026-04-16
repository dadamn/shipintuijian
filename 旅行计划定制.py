# 完善版
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="智能旅行规划助手",
    page_icon="🌍",
    layout="wide"
)

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 扩展的目的地数据
destinations = {
    "亚洲": ["日本", "泰国", "中国", "韩国", "马来西亚", "新加坡", "越南", "印度", "马尔代夫", "印度尼西亚"],
    "欧洲": ["法国", "意大利", "西班牙", "英国", "德国", "瑞士", "希腊", "冰岛", "葡萄牙", "荷兰"],
    "北美洲": ["美国", "加拿大", "墨西哥", "古巴", "哥斯达黎加"],
    "南美洲": ["巴西", "阿根廷", "秘鲁", "智利", "哥伦比亚"],
    "大洋洲": ["澳大利亚", "新西兰", "斐济", "大溪地"],
    "非洲": ["南非", "埃及", "摩洛哥", "肯尼亚", "坦桑尼亚"]
}

# 扩展的目的地详细信息
destination_details = {
    "日本": {
        "特色": "文化融合、美食、樱花/红叶季、购物、温泉",
        "最佳季节": "春季(3-4月,樱花)、秋季(10-11月,红叶)",
        "经典景点": ["东京迪士尼", "富士山", "京都金阁寺", "大阪城公园", "奈良公园", "北海道"],
        "美食": ["寿司", "拉面", "天妇罗", "怀石料理", "和牛", "抹茶甜点"],
        "文化注意": ["进入室内脱鞋", "公共场合保持安静", "垃圾分类严格", "不给小费"],
        "签证": "需要签证，可委托旅行社办理",
        "时差": "+1小时",
        "货币": "日元(JPY)"
    },
    "泰国": {
        "特色": "海滩、寺庙、美食、热带气候、SPA",
        "最佳季节": "11月-次年4月(旱季)",
        "经典景点": ["曼谷大皇宫", "普吉岛", "清迈古城", "皮皮岛", "芭堤雅", "苏梅岛"],
        "美食": ["冬阴功汤", "泰式炒河粉", "芒果糯米饭", "绿咖喱鸡", "泰式奶茶"],
        "文化注意": ["尊重王室和僧侣", "头部为神圣部位", "公共场合避免亲昵行为", "进入寺庙要脱鞋"],
        "签证": "落地签/免签(根据政策)",
        "时差": "-1小时",
        "货币": "泰铢(THB)"
    },
    "中国": {
        "特色": "悠久历史、多元文化、美食、自然景观",
        "最佳季节": "春季(4-5月)、秋季(9-10月)",
        "经典景点": ["长城", "故宫", "兵马俑", "桂林山水", "九寨沟", "张家界"],
        "美食": ["北京烤鸭", "火锅", "小笼包", "粤菜", "川菜", "湘菜"],
        "文化注意": ["尊重传统文化", "公共场所排队", "餐桌礼仪", "文物保护"],
        "签证": "根据国籍可能需要签证",
        "时差": "0小时(北京时间)",
        "货币": "人民币(CNY)"
    },
    "韩国": {
        "特色": "K-POP、美食、购物、美容、历史",
        "最佳季节": "春季(4-6月)、秋季(9-11月)",
        "经典景点": ["首尔塔", "济州岛", "釜山海云台", "景福宫", "明洞", "东大门"],
        "美食": ["泡菜", "烤肉", "炸鸡", "部队锅", "拌饭", "韩定食"],
        "文化注意": ["长辈优先", "脱鞋进屋", "饮酒礼仪", "尊重年龄等级"],
        "签证": "需要签证(部分免签)",
        "时差": "+1小时",
        "货币": "韩元(KRW)"
    },
    "马来西亚": {
        "特色": "多元文化、海滩、雨林、美食",
        "最佳季节": "5-9月(最佳)",
        "经典景点": ["吉隆坡双子塔", "槟城", "兰卡威", "沙巴", "马六甲", "热浪岛"],
        "美食": ["椰浆饭", "沙爹", "肉骨茶", "槟城炒粿条", "榴莲"],
        "文化注意": ["尊重多元宗教", "右手进食", "礼貌待人"],
        "签证": "需要签证(电子签)",
        "时差": "0小时",
        "货币": "林吉特(MYR)"
    },
    "新加坡": {
        "特色": "花园城市、美食、购物、现代化",
        "最佳季节": "全年适宜(雨季11-1月)",
        "经典景点": ["滨海湾花园", "圣淘沙岛", "鱼尾狮公园", "环球影城", "牛车水"],
        "美食": ["海南鸡饭", "肉骨茶", "辣椒螃蟹", "叻沙", "咖椰吐司"],
        "文化注意": ["严禁 chewing gum", "公共场合禁烟", "排队文化", "垃圾分类"],
        "签证": "需要签证",
        "时差": "0小时",
        "货币": "新加坡元(SGD)"
    },
    "法国": {
        "特色": "浪漫、艺术、美食、时尚、葡萄酒",
        "最佳季节": "5-6月(春季)、9-10月(秋季)",
        "经典景点": ["埃菲尔铁塔", "卢浮宫", "普罗旺斯", "凡尔赛宫", "尼斯", "圣米歇尔山"],
        "美食": ["法式面包", "奶酪", "葡萄酒", "鹅肝酱", "马卡龙", "可颂"],
        "文化注意": ["见面亲吻礼", "餐厅预约", "尊重艺术作品", "法语问候"],
        "签证": "申根签证",
        "时差": "-7小时(夏令时-6小时)",
        "货币": "欧元(EUR)"
    },
    "意大利": {
        "特色": "历史、美食、艺术、时尚、建筑",
        "最佳季节": "4-5月(春季)、9-10月(秋季)",
        "经典景点": ["罗马斗兽场", "威尼斯", "佛罗伦萨", "米兰大教堂", "比萨斜塔", "五渔村"],
        "美食": ["披萨", "意大利面", "冰淇淋", "提拉米苏", "意式咖啡", "海鲜"],
        "文化注意": ["着装礼仪", "用餐时间较长", "教堂着装要求", "意式咖啡文化"],
        "签证": "申根签证",
        "时差": "-7小时(夏令时-6小时)",
        "货币": "欧元(EUR)"
    },
    "西班牙": {
        "特色": "热情、弗拉明戈、美食、建筑、海滩",
        "最佳季节": "5-6月、9-10月",
        "经典景点": ["圣家堂", "阿尔罕布拉宫", "马德里皇宫", "巴塞罗那", "塞维利亚", "龙达"],
        "美食": ["海鲜饭", "西班牙火腿", "塔帕斯", "西班牙油条", "桑格利亚"],
        "文化注意": ["午休时间", "晚餐较晚", "热情问候", "弗拉明戈观赏礼仪"],
        "签证": "申根签证",
        "时差": "-7小时(夏令时-6小时)",
        "货币": "欧元(EUR)"
    },
    "英国": {
        "特色": "历史、王室、文化、音乐、文学",
        "最佳季节": "5-9月",
        "经典景点": ["大本钟", "伦敦眼", "大英博物馆", "白金汉宫", "巨石阵", "爱丁堡"],
        "美食": ["英式早餐", "炸鱼薯条", "英式下午茶", "周日烤肉", "威士忌"],
        "文化注意": ["排队文化", "抱歉文化", "茶文化", "谈天气"],
        "签证": "英国签证",
        "时差": "-8小时(夏令时-7小时)",
        "货币": "英镑(GBP)"
    },
    "德国": {
        "特色": "汽车、啤酒、城堡、音乐、工业",
        "最佳季节": "5-10月",
        "经典景点": ["新天鹅堡", "勃兰登堡门", "科隆大教堂", "柏林墙", "黑森林", "国王湖"],
        "美食": ["德国香肠", "猪肘", "啤酒", "椒盐卷饼", "黑森林蛋糕"],
        "文化注意": ["守时", "直接沟通", "垃圾分类", "尊重隐私"],
        "签证": "申根签证",
        "时差": "-7小时(夏令时-6小时)",
        "货币": "欧元(EUR)"
    },
    "瑞士": {
        "特色": "雪山、手表、巧克力、湖泊、徒步",
        "最佳季节": "夏季(6-9月)、冬季(12-3月滑雪)",
        "经典景点": ["少女峰", "日内瓦湖", "卢塞恩", "马特洪峰", "因特拉肯", "苏黎世"],
        "美食": ["芝士火锅", "瑞士巧克力", "瑞士奶酪", "土豆煎饼", "瑞士葡萄酒"],
        "文化注意": ["安静环境", "准时", "垃圾分类", "小费包含"],
        "签证": "申根签证",
        "时差": "-7小时(夏令时-6小时)",
        "货币": "瑞士法郎(CHF)"
    },
    "美国": {
        "特色": "多元文化、自然奇观、主题公园、都市",
        "最佳季节": "因地区而异(西部5-10月,东部5-9月)",
        "经典景点": ["大峡谷", "纽约时代广场", "迪士尼乐园", "黄石国家公园", "拉斯维加斯", "旧金山"],
        "美食": ["汉堡", "披萨", "BBQ", "甜甜圈", "牛排", "美式早餐"],
        "文化注意": ["小费文化(15-20%)", "个人空间", "尊重多元文化", "预约文化"],
        "签证": "美国签证(B1/B2)",
        "时差": "-13至-16小时",
        "货币": "美元(USD)"
    },
    "加拿大": {
        "特色": "自然景观、枫叶、多元文化、冬季运动",
        "最佳季节": "夏季(6-8月)、秋季(9-10月赏枫)",
        "经典景点": ["班夫国家公园", "尼亚加拉大瀑布", "温哥华", "多伦多CN塔", "魁北克古城"],
        "美食": ["枫糖浆", "肉汁奶酪薯条", "加拿大培根", "纳奈莫条", "冰酒"],
        "文化注意": ["礼貌友善", "环保意识", "多元文化尊重", "冬季保暖"],
        "签证": "加拿大签证",
        "时差": "-13至-16小时",
        "货币": "加元(CAD)"
    },
    "澳大利亚": {
        "特色": "海滩、野生动物、大堡礁、户外活动",
        "最佳季节": "9-11月(春季)、3-5月(秋季)",
        "经典景点": ["悉尼歌剧院", "大堡礁", "黄金海岸", "大洋路", "乌鲁鲁", "塔斯马尼亚"],
        "美食": ["澳式BBQ", "肉派", "澳洲龙虾", "Vegemite", "澳式咖啡"],
        "文化注意": ["阳光防护", "环保意识", "土著文化尊重", "户外安全"],
        "签证": "澳大利亚签证(电子签)",
        "时差": "+2-3小时",
        "货币": "澳元(AUD)"
    },
    "新西兰": {
        "特色": "纯净自然、极限运动、电影取景地、毛利文化",
        "最佳季节": "12-2月(夏季)、6-8月(冬季滑雪)",
        "经典景点": ["皇后镇", "霍比屯", "萤火虫洞", "米尔福德峡湾", "罗托鲁瓦", "库克山"],
        "美食": ["新西兰羊肉", "海鲜", "毛利hangi", "奶制品", "葡萄酒"],
        "文化注意": ["环保意识", "尊重毛利文化", "户外安全", "自驾注意事项"],
        "签证": "新西兰签证",
        "时差": "+4-5小时",
        "货币": "新西兰元(NZD)"
    }
}

# 旅行主题
travel_themes = {
    "休闲度假": ["放松", "SPA", "海滩", "晒太阳", "慢生活"],
    "美食探索": ["美食", "小吃", "餐厅", "烹饪课程", "美食节"],
    "文化体验": ["文化", "艺术", "博物馆", "传统", "历史遗迹"],
    "户外探险": ["徒步", "登山", "骑行", "探险", "极限运动"],
    "购物血拼": ["购物", "商场", "市集", "奢侈品", "奥特莱斯"],
    "亲子游玩": ["动物园", "游乐园", "互动体验", "教育", "家庭友好"],
    "浪漫蜜月": ["浪漫", "海景", "私密", "烛光晚餐", "情侣SPA"],
    "历史考古": ["历史", "古迹", "遗址", "考古", "博物馆"],
    "自然生态": ["国家公园", "观鸟", "生态", "野生动物", "森林"],
    "摄影之旅": ["摄影", "日出日落", "风景", "星空", "建筑摄影"]
}

# 预算水平
budget_levels = {
    "经济型": {"每日预算": "300-800元", "住宿": "青年旅社/经济型酒店", "餐饮": "街边小吃/快餐"},
    "中等价位": {"每日预算": "800-1500元", "住宿": "三星级酒店/精品酒店", "餐饮": "当地餐厅/中档餐厅"},
    "高端奢华": {"每日预算": "1500-3000元", "住宿": "四星级酒店/度假村", "餐饮": "高级餐厅/特色餐厅"},
    "豪华定制": {"每日预算": "3000元以上", "住宿": "五星级酒店/奢华度假村", "餐饮": "米其林餐厅/顶级餐厅"}
}

# 安全提示
safety_tips = {
    "通用": [
        "提前了解目的地的安全状况和当地法律法规",
        "购买涵盖医疗和紧急救援的旅行保险",
        "保管好个人财物，尤其是在人多拥挤的地方",
        "随身携带紧急联系方式和大使馆信息",
        "注意食品安全和饮用水安全",
        "保持与家人朋友的联系，分享行程"
    ],
    "日本": ["遵守紧急疏散指示", "注意地震预警", "防范拥挤场所踩踏"],
    "泰国": ["注意交通安全(摩托车)", "防范诈骗和宰客", "尊重皇室"],
    "美国": ["注意治安差异区域", "防范枪击事件", "妥善保管证件"],
    "欧洲": ["防范小偷和扒手", "注意示威游行", "保管好护照"]
}

# 行李清单
packing_lists = {
    "春季": ["轻便外套", "长袖衬衫", "舒适鞋子", "雨伞", "防晒霜", "薄围巾"],
    "夏季": ["短袖衣物", "短裤", "凉鞋", "防晒霜", "太阳镜", "帽子", "泳衣", "驱蚊液"],
    "秋季": ["薄外套", "毛衣", "牛仔裤", "舒适鞋子", "围巾", "保温杯"],
    "冬季": ["厚外套", "羽绒服", "围巾", "手套", "保暖内衣", "雪地靴", "帽子", "暖宝宝"],
    "通用": ["护照和签证文件", "机票和酒店预订单", "手机充电器", "现金和信用卡", "转换插头", "常用药品"]
}


# 从secrets获取API Key
def get_api_key():
    """从Streamlit secrets获取API Key"""
    try:
        api_key = st.secrets["DASHSCOPE_API_KEY"]
        return api_key
    except:
        return None


# 生成提示词
def generate_prompt(destination, theme, days, season, budget, special_requests):
    """生成发送给大模型的提示词"""
    dest_info = destination_details.get(destination, {})
    theme_keywords = travel_themes.get(theme, [])

    # 季节转换
    season_short = season.split("（")[0] if "（" in season else season

    # 构建提示词
    prompt = f"""
你是一位专业的旅行顾问，擅长根据用户需求生成详细的旅行计划。请根据以下信息为用户生成一份到{destination}的{days}日{theme}旅行计划：

### 用户基本信息
- 目的地：{destination}
- 旅行天数：{days}天
- 旅行主题：{theme}
- 旅行季节：{season_short}
- 预算水平：{budget}（{budget_levels[budget]['每日预算']}）
- 特殊要求：{special_requests if special_requests else "无特殊要求"}

### 目的地相关信息
- 特色：{dest_info.get('特色', '丰富的文化和自然景观')}
- 最佳季节：{dest_info.get('最佳季节', '全年适宜')}
- 经典景点：{', '.join(dest_info.get('经典景点', ['当地著名景点']))}
- 美食推荐：{', '.join(dest_info.get('美食', ['当地美食']))}
- 文化注意事项：{', '.join(dest_info.get('文化注意', ['尊重当地习俗']))}
- 签证要求：{dest_info.get('签证', '请提前查询')}
- 货币：{dest_info.get('货币', '当地货币')}
- 时差：{dest_info.get('时差', '请查询')}

### 输出要求
请生成一份详细的旅行计划，使用以下格式：

## 📅 每日行程安排
（按天列出，每天包括上午、下午、晚上具体安排）

## 🏨 住宿推荐
（根据预算水平推荐3-4家酒店/区域）

## 💰 预算估算
（详细列出：交通、住宿、餐饮、门票、购物等）

## 💡 实用贴士
- 签证和入境要求
- 当地交通建议
- 文化礼仪提醒
- 安全注意事项
- 行李准备清单
- 通讯和网络建议

## ⚠️ 注意事项
（根据特殊要求和目的地特点给出建议）

请确保计划实用、具体、可执行，语言专业友好。
"""
    return prompt


# 生成旅行计划
def generate_travel_plan(destination, theme, days, season, budget, special_requests):
    """调用大模型生成旅行计划"""
    prompt = generate_prompt(destination, theme, days, season, budget, special_requests)

    try:
        api_key = get_api_key()
        if not api_key:
            return "⚠️ 请配置API Key以生成个性化旅行计划。"

        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system",
                 "content": "你是一位专业、细致的旅行顾问，擅长根据用户需求生成详细的旅行计划。请使用中文回答，语言专业友好。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"生成旅行计划时出错: {str(e)}")
        return generate_fallback_plan(destination, theme, days, season, budget)


# 备用计划生成
def generate_fallback_plan(destination, theme, days, season, budget):
    """当API调用失败时生成备用计划"""
    dest_info = destination_details.get(destination, {})
    budget_info = budget_levels.get(budget, budget_levels["中等价位"])

    plan = f"""
## 📅 {days}日{theme}行程概览

### 第1天：抵达与初探
- **上午**：抵达{destination}，前往酒店办理入住
- **下午**：市区漫步，熟悉环境，参观当地地标
- **晚上**：品尝当地特色美食，体验夜生活

### 第2-{days - 1}天：深度体验
- 根据{theme}主题安排相应的景点和活动
- 推荐景点：{', '.join(dest_info.get('经典景点', ['当地著名景点'])[:3])}
- 美食体验：{', '.join(dest_info.get('美食', ['当地美食'])[:3])}

### 第{days}天：告别之旅
- 购买纪念品
- 前往机场，结束愉快的旅程

## 🏨 住宿推荐
预算水平：{budget}（{budget_info['每日预算']}）
- 推荐区域：市中心或交通便利区域
- 住宿类型：{budget_info['住宿']}

## 💰 预算估算
- 住宿：{budget_info['每日预算']} × {days}天
- 餐饮：{budget_info['餐饮']}，每日约200-500元
- 交通：根据行程安排，每日约50-200元
- 门票：根据景点选择，约500-1500元

## 💡 实用贴士
- 提前了解{destination}的签证要求
- 购买旅行保险
- 下载离线地图和翻译App
- 准备{season}季节的合适衣物
- 尊重当地文化习俗

*注：此为示例计划，建议配置API Key获取更详细的个性化推荐。*
"""
    return plan


def main():
    st.title("🌍 智能旅行规划助手")
    st.markdown("根据您的偏好，生成个性化的深度旅行计划")

    # 侧边栏 - 用户输入
    with st.sidebar:
        st.header("✈️ 旅行偏好设置")

        # 目的地选择
        region = st.selectbox("选择地区", list(destinations.keys()))
        destination = st.selectbox("选择目的地", destinations[region])

        # 显示目的地快速信息
        if destination in destination_details:
            with st.expander("ℹ️ 目的地速览"):
                info = destination_details[destination]
                st.markdown(f"""
                **特色**：{info['特色']}
                **最佳季节**：{info['最佳季节']}
                **签证**：{info['签证']}
                **货币**：{info['货币']}
                **时差**：{info['时差']}
                """)

        st.markdown("---")

        # 旅行主题
        theme = st.selectbox("🎯 旅行主题", list(travel_themes.keys()))

        # 旅行天数
        days = st.slider("📅 旅行天数", 1, 30, 7)

        # 旅行季节
        season = st.selectbox("🌸 旅行季节", ["春季（3-5月）", "夏季（6-8月）", "秋季（9-11月）", "冬季（12-2月）"])

        # 预算水平
        budget = st.selectbox("💰 预算水平", list(budget_levels.keys()))

        # 显示预算详情
        st.caption(f"{budget_levels[budget]['住宿']} | {budget_levels[budget]['餐饮']}")

        # 特殊要求
        special_requests = st.text_area("📝 特殊要求或偏好",
                                        placeholder="例如：需要无障碍设施、素食者、对花粉过敏等",
                                        height=100)

        st.markdown("---")

        # 生成旅行计划按钮
        if st.button("✨ 生成智能旅行计划", type="primary", use_container_width=True):
            with st.spinner("🧠 AI正在为您精心规划行程..."):
                travel_plan = generate_travel_plan(destination, theme, days, season, budget, special_requests)
                st.session_state.travel_plan = travel_plan
                st.session_state.destination = destination
                st.session_state.days = days
            st.success("✅ 旅行计划生成成功！")
            st.balloons()

        # 清空按钮
        if st.button("🗑️ 清空计划", use_container_width=True):
            if "travel_plan" in st.session_state:
                del st.session_state.travel_plan
            st.rerun()

    # 主区域 - 显示旅行计划
    if "travel_plan" in st.session_state:
        st.subheader(f"📅 您的 {st.session_state.destination} {st.session_state.days}日 个性化旅行计划")

        # 使用tabs组织内容
        tab1, tab2, tab3 = st.tabs(["📋 详细行程", "📊 旅行分析", "🎒 准备清单"])

        with tab1:
            st.markdown(st.session_state.travel_plan)

        with tab2:
            # 显示旅行统计数据
            col1, col2, col3, col4 = st.columns(4)

            budget_level = st.session_state.get('budget', budget)
            daily_budget = int(
                budget_levels[budget_level]['每日预算'].split('-')[-1].replace('元', '').replace('以上', '')) if '-' in \
                                                                                                                 budget_levels[
                                                                                                                     budget_level][
                                                                                                                     '每日预算'] else 2000
            total_budget = daily_budget * st.session_state.days

            col1.metric("总预算", f"{total_budget:,}元")
            col2.metric("每日预算", budget_levels[budget_level]['每日预算'])
            col3.metric("旅行天数", f"{st.session_state.days}天")
            col4.metric("目的地", st.session_state.destination)

            # 预算分布图表
            st.subheader("💰 预算分布建议")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # 饼图
            budget_data = {
                "住宿": total_budget * 0.35,
                "餐饮": total_budget * 0.25,
                "交通": total_budget * 0.20,
                "门票活动": total_budget * 0.15,
                "购物其他": total_budget * 0.05
            }

            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            ax1.pie(budget_data.values(), labels=budget_data.keys(), autopct='%1.1f%%',
                    startangle=90, colors=colors)
            ax1.set_title("预算分配比例")

            # 柱状图
            categories = list(budget_data.keys())
            values = list(budget_data.values())
            ax2.bar(categories, values, color=colors)
            ax2.set_title("预算金额分布")
            ax2.set_ylabel("金额(元)")
            ax2.tick_params(axis='x', rotation=45)

            plt.tight_layout()
            st.pyplot(fig)

            # 每日花费趋势
            st.subheader("📈 每日花费预估")
            daily_costs = [daily_budget * (0.8 if i == 0 else 1.2 if i == st.session_state.days - 1 else 1.0)
                           for i in range(st.session_state.days)]
            fig2, ax = plt.subplots(figsize=(10, 4))
            ax.plot(range(1, st.session_state.days + 1), daily_costs, marker='o', linewidth=2, color='#FF6B6B')
            ax.fill_between(range(1, st.session_state.days + 1), daily_costs, alpha=0.3, color='#FF6B6B')
            ax.set_xlabel("天数")
            ax.set_ylabel("花费(元)")
            ax.set_title("每日预算趋势")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig2)

        with tab3:
            st.subheader("🎒 行李准备清单")

            # 根据季节显示行李清单
            season_clean = season.split("（")[0] if "（" in season else season
            items = packing_lists.get(season_clean, packing_lists["春季"])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**必备物品**")
                for item in packing_lists["通用"]:
                    st.checkbox(item, value=True, key=f"通用_{item}")
                st.markdown("**季节物品**")
                for item in items:
                    st.checkbox(item, value=True, key=f"季节_{item}")

            with col2:
                st.markdown("**目的地特定物品**")
                if st.session_state.destination in destination_details:
                    dest_items = ["转换插头", "翻译APP", "当地货币", "信用卡", "紧急联系人信息"]
                    for item in dest_items:
                        st.checkbox(item, value=True, key=f"dest_{item}")

            st.info("💡 提示：可根据实际需求调整行李清单")

        # 下载按钮
        st.download_button(
            label="📥 下载旅行计划 (TXT格式)",
            data=st.session_state.travel_plan,
            file_name=f"{st.session_state.destination}_{st.session_state.days}日_{theme}之旅_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        # 显示欢迎信息和热门推荐
        st.markdown("""
        ### ✨ 欢迎使用智能旅行规划助手

        让我帮您规划完美的旅行！请在左侧面板填写您的旅行偏好，然后点击"生成智能旅行计划"。

        ---

        ### 🌟 热门目的地推荐
        """)

        # 创建热门目的地网格
        popular_destinations = ["日本", "泰国", "法国", "意大利", "瑞士", "新西兰"]
        cols = st.columns(3)

        for idx, dest in enumerate(popular_destinations):
            if dest in destination_details:
                with cols[idx % 3]:
                    info = destination_details[dest]
                    with st.expander(f"📍 {dest}"):
                        st.markdown(f"""
                        **特色**：{info['特色']}
                        **最佳季节**：{info['最佳季节']}
                        **经典景点**：{', '.join(info['经典景点'][:2])}
                        **必尝美食**：{', '.join(info['美食'][:2])}
                        """)

        # 显示旅行提示
        st.markdown("---")
        st.info("💡 **旅行小贴士**：提前3-6个月规划国际旅行可以获得更好的机票和酒店价格！")


if __name__ == "__main__":
    main()