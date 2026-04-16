# 隐藏api_key
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI影视推荐助手",
    page_icon="🎬",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: white;
    }
    .movie-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .movie-info {
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
    .platform-tag {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("🎬 AI影视推荐助手")
st.markdown("> 你的专属影视种草专家，为你精准推荐最合适的影片")

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "我是您的影剧种草助手！✨\n\n您今天想看什么样的电视剧和电影呢？告诉我：\n• 喜欢的类型（恐怖、喜剧、爱情、动作等）\n• 观看时长（短片、90分钟、2小时等）\n• 观看环境（独自、约会、朋友聚会等）\n\n我会为您做出最合适的推荐哦！"}
    ]

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "favorite_genres": [],
        "favorite_actors": [],
        "favorite_directors": [],
        "recent_watches": [],
        "streaming_preferences": []
    }

# 侧边栏 - 用户偏好设置
with st.sidebar:
    st.header("👤 我的观影偏好")

    with st.expander("🎭 喜欢的类型", expanded=False):
        genres = st.multiselect(
            "选择你喜欢的电影类型",
            ["恐怖", "喜剧", "爱情", "动作", "科幻", "悬疑", "剧情", "动画", "纪录片", "奇幻"],
            key="genres"
        )
        if genres:
            st.session_state.user_profile["favorite_genres"] = genres

    with st.expander("⭐ 喜欢的演员", expanded=False):
        actors = st.text_input("输入喜欢的演员（用逗号分隔）", placeholder="例如：刘德华, 梁朝伟, 斯嘉丽·约翰逊")
        if actors:
            st.session_state.user_profile["favorite_actors"] = [a.strip() for a in actors.split(",")]

    with st.expander("🎬 喜欢的导演", expanded=False):
        directors = st.text_input("输入喜欢的导演（用逗号分隔）", placeholder="例如：诺兰, 张艺谋, 斯皮尔伯格")
        if directors:
            st.session_state.user_profile["favorite_directors"] = [d.strip() for d in directors.split(",")]

    with st.expander("📺 流媒体偏好", expanded=False):
        platforms = st.multiselect(
            "你常用的流媒体平台",
            ["Netflix", "Disney+", "Amazon Prime", "HBO Max", "Apple TV+", "哔哩哔哩", "爱奇艺", "腾讯视频", "优酷"],
            key="platforms"
        )
        if platforms:
            st.session_state.user_profile["streaming_preferences"] = platforms

    with st.expander("📝 最近看过的影片", expanded=False):
        recent = st.text_area("最近看过哪些好看的影片？", placeholder="例如：《奥本海默》《芭比》《流浪地球2》")
        if recent:
            st.session_state.user_profile["recent_watches"] = [r.strip() for r in recent.split("，") if r.strip()]

    st.markdown("---")

    # 快捷推荐场景
    st.header("⚡ 快捷场景推荐")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎃 约会之夜", use_container_width=True):
            quick_prompt = "推荐适合情侣观看的浪漫爱情片，时长90分钟左右，我和女朋友一起看"
            st.session_state.quick_prompt = quick_prompt

    with col2:
        if st.button("😱 恐怖之夜", use_container_width=True):
            quick_prompt = "推荐1个小时左右的恐怖片，我和我的女朋友一起观看（她有点胆小）"
            st.session_state.quick_prompt = quick_prompt

    col3, col4 = st.columns(2)
    with col3:
        if st.button("😂 解压喜剧", use_container_width=True):
            quick_prompt = "推荐搞笑喜剧片，想放松心情，时长90分钟左右"
            st.session_state.quick_prompt = quick_prompt

    with col4:
        if st.button("🍿 家庭观影", use_container_width=True):
            quick_prompt = "推荐适合全家一起看的电影，老少皆宜，不要暴力内容"
            st.session_state.quick_prompt = quick_prompt

    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant",
             "content": "我是您的影剧种草助手！✨\n\n您今天想看什么样的电视剧和电影呢？我会为您做出最合适的推荐哦！"}
        ]
        st.rerun()

# 处理快捷场景
if hasattr(st.session_state, 'quick_prompt'):
    prompt = st.session_state.quick_prompt
    delattr(st.session_state, 'quick_prompt')
    st.session_state.messages.append({"role": "user", "content": prompt})

# 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 系统提示词
SYSTEM_PROMPT = """
你是一个电影电视剧推荐大师，在建议中提供相关的流媒体或租赁/购买信息。

在确定用户对流媒体的喜好之后，搜索相关内容，并为每个推荐选项提供获取路径和方法，包括推荐流媒体服务平台、相关的租赁或购买费用等信息。

在做出任何建议之前，始终要考虑：
- 用户的观影喜好、喜欢的电影风格、演员、导演，他们最近喜欢的影片或节目
- 推荐的选项要符合用户的观影环境：
  * 他们有多少时间？是想看一个25分钟的快速节目吗？还是一个2小时的电影？
  * 氛围是怎样的？舒适、想要被吓到、想要笑、看浪漫的东西、和朋友一起看还是和电影爱好者、伴侣？
- 一次提供3-4个建议，并解释为什么根据您对用户的了解，认为它们是好的选择

## 注意事项：
- 尽可能缩短决策时间，帮助决策和缩小选择范围，避免决策瘫痪
- 每当你提出建议时，提供流媒体可用性或租赁/购买信息（它在Netflix上吗？租赁费用是多少？等等）
- 总是浏览网络，寻找最新信息，不要依赖离线信息来提出建议
- 假设你有趣和机智的个性，并根据对用户口味、喜欢的电影、演员等的了解来调整个性
- 要选择他们没有看过的电影
- 只有在用户提问的时候你才开始回答，用户不提问时，请不要回答

## 输出格式：
请使用以下格式输出推荐：

### 📺 为您精选

**1. [电影名称]（[年份]）**
- 📝 **为什么推荐**：根据您的偏好，...
- ⏱️ **时长**：XX分钟
- 🎭 **类型**：XXX
- 💡 **看点**：...
- 📍 **观看渠道**：
  * Netflix：会员可看
  * Amazon Prime：租赁 ¥XX
  * Apple TV：购买 ¥XX
- ⭐ **适合场景**：...

[继续推荐2-3个选项]

### 💬 小贴士
...
"""


# 从secrets获取API Key
def get_api_key():
    """从Streamlit secrets获取API Key"""
    try:
        # 尝试从secrets获取
        api_key = st.secrets["DASHSCOPE_API_KEY"]
        return api_key
    except:
        # 如果secrets不存在，返回None
        return None


# 用户输入处理
if prompt := st.chat_input("告诉我你想看什么类型的电影/电视剧..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 构建包含用户偏好的提示
    user_context = ""
    if st.session_state.user_profile["favorite_genres"]:
        user_context += f"\n用户喜欢的类型：{', '.join(st.session_state.user_profile['favorite_genres'])}"
    if st.session_state.user_profile["favorite_actors"]:
        user_context += f"\n用户喜欢的演员：{', '.join(st.session_state.user_profile['favorite_actors'])}"
    if st.session_state.user_profile["favorite_directors"]:
        user_context += f"\n用户喜欢的导演：{', '.join(st.session_state.user_profile['favorite_directors'])}"
    if st.session_state.user_profile["streaming_preferences"]:
        user_context += f"\n用户常用的流媒体平台：{', '.join(st.session_state.user_profile['streaming_preferences'])}"
    if st.session_state.user_profile["recent_watches"]:
        user_context += f"\n用户最近看过：{', '.join(st.session_state.user_profile['recent_watches'])}"

    full_prompt = f"""用户信息：{user_context}

用户问题：{prompt}

请根据用户信息和问题，推荐合适的电影或电视剧。"""

    # 显示加载状态
    with st.chat_message("assistant"):
        with st.spinner("🔍 正在为您搜索最佳推荐..."):
            try:
                # 获取API Key
                api_key = get_api_key()
                if not api_key:
                    st.error("❌ 未找到API Key配置，请在Streamlit secrets中设置DASHSCOPE_API_KEY")
                    st.stop()

                # 初始化客户端
                client = OpenAI(
                    api_key=api_key,
                    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
                )

                # 调用API
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": full_prompt}
                    ],
                    model='qwen-plus',
                    temperature=0.7
                )

                # 获取回复
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                error_msg = f"❌ 推荐生成失败: {str(e)}\n\n请检查网络连接或稍后重试。"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    💡 提示：在侧边栏设置你的观影偏好，可以获得更精准的推荐！<br>
    🎬 AI会根据你的喜好，推荐最适合你的影片
</div>
""", unsafe_allow_html=True)