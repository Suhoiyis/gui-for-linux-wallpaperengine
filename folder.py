import os
from pathlib import Path
from datetime import datetime

# ================= 配置区域 =================

# 1. 忽略的文件夹名称 (目录)
# 注意：docs 已被移除，现在会被正常抓取
IGNORE_DIRS = {
    '.git', 
    '.github', 
    '.sisyphus', 
    'target',        # Rust 构建目录
    '__pycache__', 
    'node_modules', 
    'venv', 
    'env',
    '.vscode',       
    '.idea',         
    'dist',          
    'build'
}

# 2. 忽略的特定文件名 (文件)
# 注意：这里只放那些无论什么后缀都要忽略的文件，或者特定后缀的非白名单文件逻辑在下面处理
IGNORE_FILES_ALWAYS = {
    '.gitignore',
    'LICENSE',
    'PKGBUILD',
    'Makefile'      
}

# 3. Markdown 文件白名单 (只有这些 .md 文件会被保留)
MD_WHITELIST = {
    'README.md',
    'CHANGELOG.md'
}

# 输出文件名和脚本自身名称
OUTPUT_FILENAME = "project_export.md"
SCRIPT_FILENAME = "folder_to_markdown.py"
# ===========================================

def generate_ascii_tree(start_path, prefix=""):
    """
    递归生成 ASCII 树形结构字符串
    """
    tree_str = ""
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return f"{prefix}[权限拒绝]\n"
    except Exception:
        return ""

    filtered_entries = []
    for e in entries:
        # 排除输出文件和脚本本身
        if e in [OUTPUT_FILENAME, SCRIPT_FILENAME]:
            continue
        
        full_path = os.path.join(start_path, e)
        is_dir = os.path.isdir(full_path)
        is_file = os.path.isfile(full_path)
        
        # 1. 排除 IGNORE_DIRS 中的文件夹
        if is_dir and e in IGNORE_DIRS:
            continue
            
        # 2. 排除 ALWAYS_IGNORE 中的特定文件
        if is_file and e in IGNORE_FILES_ALWAYS:
            continue
            
        # 3. 特殊逻辑：如果是 .md 文件，检查是否在白名单中
        if is_file and e.lower().endswith('.md'):
            if e not in MD_WHITELIST:
                continue # 不在白名单的 .md 文件直接跳过（不显示在树中）
            
        filtered_entries.append(e)

    for i, entry in enumerate(filtered_entries):
        full_path = os.path.join(start_path, entry)
        is_last = (i == len(filtered_entries) - 1)
        
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{entry}"
        
        if os.path.isdir(full_path):
            tree_str += "/\n"
            extension = "    " if is_last else "│   "
            tree_str += generate_ascii_tree(full_path, prefix + extension)
        else:
            tree_str += "\n"
            
    return tree_str

def should_ignore_file(file_path):
    """
    综合判断文件是否应该被忽略
    """
    filename = file_path.name
    
    # 1. 检查路径中是否包含忽略的文件夹
    for part in file_path.parts:
        if part in IGNORE_DIRS:
            return True
    
    # 2. 检查是否在永久忽略列表中
    if filename in IGNORE_FILES_ALWAYS:
        return True
        
    # 3. 特殊逻辑：Markdown 文件白名单检查
    if filename.lower().endswith('.md'):
        if filename not in MD_WHITELIST:
            return True # 不在白名单的 .md 文件忽略
            
    return False

def get_file_content(file_path):
    """
    读取文件内容，处理编码问题和大文件
    """
    try:
        if os.path.getsize(file_path) > 5 * 1024 * 1024:
            return "[文件过大 (>5MB)，已跳过读取]"
    except OSError:
        pass

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception:
            return "[无法读取：可能是二进制文件或编码不支持]"
    except Exception as e:
        return f"[读取错误: {str(e)}]"

def main():
    root_dir = Path('.')
    
    print(f"🚀 开始扫描 Rust 项目: {root_dir.absolute()}")
    print(f"🚫 忽略的文件夹: {', '.join(sorted(IGNORE_DIRS))}")
    print(f"🚫 忽略的文件: {', '.join(sorted(IGNORE_FILES_ALWAYS))}")
    print(f"✅ 保留的 Markdown 文件 (白名单): {', '.join(sorted(MD_WHITELIST))}")
    print(f"⚠️  其他所有 .md 文件将被忽略")
    
    md_content = []
    
    # 1. 生成标题
    md_content.append("# 项目结构与文件内容导出 (Rust Project)\n\n")
    md_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_content.append(f"**根目录**: `{root_dir.absolute()}`\n")
    md_content.append("---\n\n")
    
    # 2. 生成 ASCII 树形图
    md_content.append("## 📂 项目结构图\n\n")
    md_content.append("```text\n")
    md_content.append(f"{root_dir.name}/\n")
    tree_art = generate_ascii_tree(str(root_dir))
    md_content.append(tree_art)
    md_content.append("```\n\n")
    md_content.append("---\n\n")
    
    # 3. 递归抓取文件内容
    md_content.append("## 📄 文件详细内容\n\n")
    
    files_to_process = []
    
    print("🔍 正在遍历文件...")
    for f in root_dir.rglob('*'):
        if not f.is_file():
            continue
            
        if f.name in [OUTPUT_FILENAME, SCRIPT_FILENAME]:
            continue
            
        if should_ignore_file(f):
            continue
            
        files_to_process.append(f)
    
    files_to_process.sort(key=lambda x: str(x))
    
    print(f"✅ 找到 {len(files_to_process)} 个有效文件，开始写入内容...")
    
    for idx, file_path in enumerate(files_to_process):
        rel_path = file_path.relative_to(root_dir)
        
        if (idx + 1) % 50 == 0:
            print(f"   处理中: {idx + 1}/{len(files_to_process)} ...")
        
        md_content.append(f"### 📄 文件: `{rel_path}`\n\n")
        
        content = get_file_content(str(file_path))
        
        suffix = file_path.suffix.lower()
        lang_map = {
            '.rs': 'rust',
            '.toml': 'toml',
            '.lock': 'toml',
            '.md': 'markdown',
            '.txt': 'text',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.sh': 'bash',
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.xml': 'xml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.env': 'bash',
        }
        lang = lang_map.get(suffix, '') 
        
        md_content.append(f"```{lang}\n{content}\n```\n\n")
        md_content.append("---\n\n")

    # 4. 写入文件
    print("💾 正在保存文件...")
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write("".join(md_content))
        print(f"🎉 完成！所有内容已保存到: {OUTPUT_FILENAME}")
        print(f"📊 总共处理了 {len(files_to_process)} 个文件。")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

if __name__ == "__main__":
    main()