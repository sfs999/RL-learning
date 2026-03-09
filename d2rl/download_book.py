#!/usr/bin/env python3
"""
下载 Hands-on RL 网页版书籍内容的脚本 - 使用 curl 方式
提取 SSR 渲染的完整内容
"""

import os
import subprocess
import re
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://hrl.boyuai.com"
OUTPUT_DIR = "book-content"

# 章节 URL 映射 - 根据实际网站结构调整
CHAPTERS = {
    "chapter/intro": "00_前言",
    "chapter/1/初探强化学习": "01_初探强化学习",
    "chapter/1/多臂老虎机": "02_多臂老虎机",
    "chapter/1/马尔可夫决策过程": "03_马尔可夫决策过程",
    "chapter/1/动态规划算法": "04_动态规划算法",
    "chapter/1/时序差分算法": "05_时序差分算法",
    "chapter/1/dyna-q 算法": "06_Dyna-Q算法",
    "chapter/2/dqn 算法": "07_DQN算法",
    "chapter/2/dqn 改进算法": "08_DQN改进算法",
    "chapter/2/策略梯度算法": "09_策略梯度算法",
    "chapter/2/actor-critic算法": "10_Actor-Critic算法",
    "chapter/2/trpo 算法": "11_TRPO算法",
    "chapter/2/ppo 算法": "12_PPO算法",
    "chapter/2/ddpg 算法": "13_DDPG算法",
    "chapter/2/sac 算法": "14_SAC算法",
    "chapter/3/模仿学习": "15_模仿学习",
    "chapter/3/模型预测控制": "16_模型预测控制",
    "chapter/3/基于模型的策略优化": "17_基于模型的策略优化",
    "chapter/3/离线强化学习": "18_离线强化学习",
    "chapter/3/目标导向的强化学习": "19_目标导向的强化学习",
    "chapter/3/多智能体强化学习入门": "20_多智能体强化学习入门",
    "chapter/3/多智能体强化学习进阶": "21_多智能体强化学习进阶",
    "chapter/ending": "22_总结与展望",
}

def download_and_extract_chapter(url_path, chapter_name):
    """下载单个章节并提取内容"""
    try:
        # URL 编码处理
        from urllib.parse import quote
        
        # 对 URL 中的中文进行编码
        encoded_url_path = quote(url_path, safe='/')
        full_url = f"{BASE_URL}/{encoded_url_path}"
        print(f"正在下载：{chapter_name}")
        
        # 创建输出文件名
        filename_html = f"{OUTPUT_DIR}/{chapter_name}.html"
        filename_md = f"{OUTPUT_DIR}/{chapter_name}.md"
        
        # 使用 curl 下载完整 HTML
        cmd = [
            "curl", "-L",
            full_url,
            "-o", filename_html,
            "--max-redirs", "50",
            "--connect-timeout", "30",
            "--retry", "3",
            "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"✗ 下载失败 {chapter_name}: {result.stderr}")
            return
        
        # 读取下载的 HTML 文件
        with open(filename_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 检查是否成功下载（文件大小应该大于一定值）
        if len(html_content) < 1000:
            print(f"⚠ 下载的文件过小，可能下载失败：{chapter_name}")
            return
        
        print(f"✓ 已下载 HTML: {filename_html} ({len(html_content)} 字符)")
        
        # 提取主要内容生成 Markdown
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找内容区域
        content_div = soup.find('div', class_='__dumi-default-layout-content')
        
        if not content_div:
            print(f"⚠ 未找到内容区域，跳过 MD 提取：{chapter_name}")
            return
        
        # 提取 markdown 内容
        markdown_div = content_div.find('div', class_='markdown')
        
        if not markdown_div:
            print(f"⚠ 未找到 markdown 内容区域：{chapter_name}")
            return
        
        # 提取所有文本内容，保留基本结构
        md_content = []
        
        # 处理标题和段落
        for element in markdown_div.children:
            if hasattr(element, 'name'):
                tag_name = element.name
                text = element.get_text().strip()
                
                if text:
                    if tag_name == 'h1':
                        md_content.append(f"# {text}\n\n")
                    elif tag_name == 'h2':
                        md_content.append(f"## {text}\n\n")
                    elif tag_name == 'h3':
                        md_content.append(f"### {text}\n\n")
                    elif tag_name == 'p':
                        md_content.append(f"{text}\n\n")
                    elif tag_name == 'pre':
                        code = element.find('code')
                        if code:
                            md_content.append(f"```\n{code.get_text()}\n```\n\n")
                    elif tag_name in ['ul', 'ol']:
                        for li in element.find_all('li'):
                            li_text = li.get_text().strip()
                            if li_text:
                                md_content.append(f"- {li_text}\n")
                        md_content.append("\n")
        
        # 保存为 Markdown 文件
        with open(filename_md, 'w', encoding='utf-8') as f:
            f.write("".join(md_content))
        
        print(f"✓ 已提取 MD: {filename_md} ({len(md_content)} 字符)")
        
    except Exception as e:
        print(f"✗ 下载失败 {chapter_name}: {str(e)}")

def main():
    """主函数"""
    print("开始下载 Hands-on RL 书籍内容...")
    print(f"保存目录：{OUTPUT_DIR}/\n")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 下载所有章节
    success_count = 0
    for url_path, chapter_name in CHAPTERS.items():
        download_and_extract_chapter(url_path, chapter_name)
        success_count += 1
    
    print(f"\n下载完成！成功下载 {success_count}/{len(CHAPTERS)} 个章节")
    print(f"\n提示：")
    print(f"- HTML 原始文件保存在 {OUTPUT_DIR}/*.html")
    print(f"- Markdown 文本内容保存在 {OUTPUT_DIR}/*.md")
    print(f"- 建议使用 Markdown 阅读器查看 .md 文件")

if __name__ == "__main__":
    main()
