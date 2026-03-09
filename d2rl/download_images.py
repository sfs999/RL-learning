#!/usr/bin/env python3
"""
下载网页中的图片并修复 HTML 链接
"""

import os
import re
import subprocess
from pathlib import Path

BASE_URL = "https://hrl.boyuai.com"
OUTPUT_DIR = "book-content"
STATIC_DIR = os.path.join(OUTPUT_DIR, "static")

def extract_image_sources():
    """从所有 HTML 文件中提取图片链接"""
    image_sources = set()
    
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取 /static/ 开头的图片链接
                matches = re.findall(r'src="(/static/[^"]+)"', content)
                image_sources.update(matches)
    
    return sorted(image_sources)

def download_images(image_sources):
    """下载所有图片"""
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    print(f"开始下载 {len(image_sources)} 个图片...")
    
    success_count = 0
    for img_path in image_sources:
        img_name = os.path.basename(img_path)
        local_path = os.path.join(STATIC_DIR, img_name)
        
        # 如果图片已存在，跳过
        if os.path.exists(local_path):
            print(f"✓ 已存在：{img_name}")
            success_count += 1
            continue
        
        # 下载图片
        full_url = f"{BASE_URL}{img_path}"
        cmd = [
            "curl", "-L",
            full_url,
            "-o", local_path,
            "--max-redirs", "50",
            "--connect-timeout", "30",
            "--user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and os.path.getsize(local_path) > 0:
                print(f"✓ 已下载：{img_name}")
                success_count += 1
            else:
                print(f"✗ 下载失败：{img_name}")
                if os.path.exists(local_path):
                    os.remove(local_path)
        except Exception as e:
            print(f"✗ 下载失败 {img_name}: {str(e)}")
    
    return success_count

def fix_html_links():
    """修复 HTML 文件中的图片链接"""
    print("\n正在修复 HTML 文件中的图片链接...")
    
    fixed_count = 0
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换相对路径为本地相对路径
            # 将 src="/static/xxx.png" 替换为 src="./static/xxx.png"
            new_content = re.sub(
                r'src="/static/',
                r'src="./static/',
                content
            )
            
            # 替换 CSS 和 JS 文件链接（如果需要）
            new_content = re.sub(
                r'href="/umi\.css"',
                r'href="./umi.css"',
                new_content
            )
            new_content = re.sub(
                r'href="/umi\.js"',
                r'href="./umi.js"',
                new_content
            )
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ 已修复：{filename}")
                fixed_count += 1
    
    return fixed_count

def main():
    """主函数"""
    print("=" * 60)
    print("下载图片并修复 HTML 链接")
    print("=" * 60)
    print()
    
    # 提取图片链接
    print("正在从 HTML 文件中提取图片链接...")
    image_sources = extract_image_sources()
    print(f"找到 {len(image_sources)} 个独特的图片\n")
    
    # 下载图片
    success_count = download_images(image_sources)
    print(f"\n下载完成！成功下载 {success_count}/{len(image_sources)} 个图片")
    
    # 修复 HTML 链接
    fixed_count = fix_html_links()
    print(f"修复了 {fixed_count} 个 HTML 文件")
    
    print("\n" + "=" * 60)
    print("完成！")
    print(f"图片保存在：{STATIC_DIR}/")
    print("现在可以在本地浏览器中打开 HTML 文件，图片应该能正常显示了")
    print("=" * 60)

if __name__ == "__main__":
    main()
