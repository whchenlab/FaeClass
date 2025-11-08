#!/usr/bin/env python3
"""
HMM分类器处理脚本
用于对测试文件夹中的.faa文件执行HMM搜索、分类和汇总
"""

import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from collections import defaultdict

def run_hmmsearch(test_dir, hmm_dir="hmm_classifier", output_dir="hmm_results"):
    """运行HMM搜索步骤"""
    
    # 设置目录路径
    test_path = Path(test_dir)
    hmm_path = Path(hmm_dir)
    output_path = Path(output_dir)
    details_path = output_path / "details"
    
    # 合并后的HMM模型文件
    merged_model = hmm_path / "merged.hmm"
    
    # 检查输入目录是否存在
    if not test_path.exists():
        print(f"错误: 测试序列目录 '{test_dir}' 不存在！")
        sys.exit(1)
    
    # 检查HMM模型文件是否存在
    if not merged_model.exists():
        print(f"错误: HMM模型文件 '{merged_model}' 不存在！")
        sys.exit(1)
    
    # 检查HMM模型是否已压缩
    compressed_files = [
        merged_model.with_suffix(merged_model.suffix + '.h3f'),  # merged.hmm.h3f
        merged_model.with_suffix(merged_model.suffix + '.h3i'),  # merged.hmm.h3i
        merged_model.with_suffix(merged_model.suffix + '.h3m'),  # merged.hmm.h3m
        merged_model.with_suffix(merged_model.suffix + '.h3p')   # merged.hmm.h3p
    ]
    
    # 检查所有压缩文件是否存在
    all_compressed_exist = all(f.exists() for f in compressed_files)
    
    if not all_compressed_exist:
        print(f"错误: HMM模型文件 '{merged_model}' 未压缩或压缩不完整！")
        print(f"请先运行: hmmpress {merged_model}")
        sys.exit(1)
    
    # 创建输出目录
    details_path.mkdir(parents=True, exist_ok=True)
    
    # 获取所有测试序列文件
    faa_files = list(test_path.glob("**/*.faa"))
    
    # 检查是否找到测试序列文件
    if not faa_files:
        print(f"错误: 在 '{test_dir}' 目录下未找到任何.faa文件！")
        sys.exit(1)
    
    print(f"找到 {len(faa_files)} 个.faa文件，开始处理...")
    
    # 对每个测试序列文件执行HMM搜索
    for counter, faa_file in enumerate(faa_files, 1):
        print(f"\n[{counter}/{len(faa_files)}] 处理文件: {faa_file}")
        
        # 提取文件名
        base_name = faa_file.stem
        
        # 定义输出文件路径
        results_file = details_path / f"{base_name}_hmm_results.txt"
        dom_results_file = details_path / f"{base_name}_hmm_results_dom.txt"
        
        # 运行hmmsearch并保存结果
        print("  正在运行HMM搜索...")
        try:
            cmd = [
                "hmmsearch",
                "--tblout", str(results_file),
                "--domtblout", str(dom_results_file),
                str(merged_model),
                str(faa_file)
            ]
            
            # 运行命令并丢弃标准输出
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print(f"  结果已保存至: {results_file}")
            print(f"  结构域详情已保存至: {dom_results_file}")
            
        except subprocess.CalledProcessError as e:
            print(f"  错误: 对 {faa_file} 的HMM搜索失败！")
            print(f"  错误信息: {e.stderr}")
            continue
        except FileNotFoundError:
            print("  错误: 未找到hmmsearch命令，请确保HMMER已安装并在PATH中")
            sys.exit(1)
    
    print(f"\nHMM搜索完成！")
    print(f"结果保存在: {output_path}/")
    print(f"详细结果保存在: {details_path}/")
    
    return details_path

def process_hmm_results(input_dir, output_dir):
    """处理HMM结果并生成分类报告"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 处理每个HMM结果文件
    for hmm_result_file in input_path.glob("*hmm_results.txt"):
        print(f"Processing: {hmm_result_file}")
        
        # 生成输出文件名
        output_filename = hmm_result_file.stem.replace('_hmm_results', '') + '.classification.txt'
        output_file = output_path / output_filename
        
        # 解析HMM结果文件
        classification_results = parse_hmm_results(hmm_result_file)
        
        # 写入分类结果
        with open(output_file, 'w') as f:
            # 写入各类型统计
            for type_name in ["Fp", "Fd", "Fl", "Other"]:
                count = classification_results['counts'][type_name]
                total_score = classification_results['totals'][type_name]
                f.write(f"Type {type_name}: matches={count}, total_score={total_score:.2f}\n")
            
            # 写入总结
            max_type = classification_results['max_type']
            max_total = classification_results['max_total']
            f.write(f"\nSummary: The highest score type is {max_type} with a total score of {max_total:.2f}.\n")
        
        print(f"  -> {output_file}")
    
    return output_path

def parse_hmm_results(hmm_file):
    """解析HMM结果文件并返回分类统计"""
    
    # 初始化数据结构
    max_scores = defaultdict(float)
    query_types = {}
    type_patterns = {
        'Fp': r'_Fp_alignment$',
        'Fd': r'_Fd_alignment$', 
        'Fl': r'_Fl_alignment$',
        'Other': r'_Other_alignment$'
    }
    
    with open(hmm_file, 'r') as f:
        for line in f:
            # 跳过注释行和空行
            if line.startswith('#') or not line.strip():
                continue
            
            # 解析行数据
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            
            query = parts[2]  # 第三列：query name
            try:
                score = float(parts[5])  # 第六列：full sequence score
            except ValueError:
                continue
            
            # 仅处理score > 0的情况
            if score <= 0:
                continue
            
            # 确定类型
            query_type = "Other"
            for type_name, pattern in type_patterns.items():
                if re.search(pattern, query):
                    query_type = type_name
                    break
            
            # 存储每个查询的最高得分及其类型
            if query not in max_scores or score > max_scores[query]:
                max_scores[query] = score
                query_types[query] = query_type
    
    # 按类型汇总统计
    counts = defaultdict(int)
    totals = defaultdict(float)
    
    for query, score in max_scores.items():
        query_type = query_types[query]
        counts[query_type] += 1
        totals[query_type] += score
    
    # 计算最高得分类型
    max_total = -1
    max_type = "Other"
    for type_name, total_score in totals.items():
        if total_score > max_total:
            max_total = total_score
            max_type = type_name
    
    return {
        'counts': counts,
        'totals': totals,
        'max_type': max_type,
        'max_total': max_total
    }

def generate_summary(classification_dir, output_dir):
    """生成汇总文件"""
    
    classification_path = Path(classification_dir)
    output_path = Path(output_dir)
    
    summary_file = output_path / "summary.txt"
    
    with open(summary_file, 'w') as f:
        f.write("Genome\tType\tMax_Score\n")  # 写入表头
    
    # 处理每个分类文件
    for classification_file in classification_path.glob("*.classification.txt"):
        filename = classification_file.name
        
        # 提取基因组名称
        genome_name = re.sub(r'_hmm_results\.txt\.classification\.txt$', '', filename)
        
        # 读取分类文件内容
        with open(classification_file, 'r') as f:
            content = f.read()
        
        # 提取Summary行
        summary_match = re.search(r'Summary: The highest score type is (\w+) with a total score of ([\d.]+)', content)
        
        if summary_match:
            raw_type = summary_match.group(1)
            raw_score = summary_match.group(2)
            
            # 清洗得分
            cleaned_score = re.sub(r'\.+$', '', raw_score)
            try:
                score_value = float(cleaned_score)
            except ValueError:
                print(f"Warning: 无效得分格式 '{raw_score}'，已修正为0 (文件: {filename})")
                score_value = 0
            
            # 阈值判断
            if score_value < 50000:
                final_type = "Outgroup"
            elif score_value < 70000:
                final_type = "Other"
            else:
                final_type = raw_type
            
            # 写入汇总文件
            with open(summary_file, 'a') as f:
                f.write(f"{genome_name}\t{final_type}\t{score_value}\n")
            
            print(f"Added: {genome_name} -> {final_type} (Score: {score_value})")
        else:
            print(f"Warning: 无法解析summary行 (文件: {filename})")
    
    print(f"最终汇总文件已生成：{summary_file}")

def main():
    parser = argparse.ArgumentParser(description='HMM分类器处理脚本')
    parser.add_argument('TEST_DIR', help='测试序列所在目录')
    parser.add_argument('--hmm-dir', default='hmm_classifier', help='HMM模型所在目录 (默认: hmm_classifier)')
    parser.add_argument('--output-dir', default='hmm_results', help='结果输出目录 (默认: hmm_results)')
    
    args = parser.parse_args()
    
    print("=== HMM搜索阶段 ===")
    details_dir = run_hmmsearch(args.TEST_DIR, args.hmm_dir, args.output_dir)
    
    print("\n=== 结果处理阶段 ===")
    classification_dir = process_hmm_results(details_dir, args.output_dir)
    
    print("\n=== 汇总生成阶段 ===")
    generate_summary(classification_dir, args.output_dir)
    
    print("\n所有处理完成！")

if __name__ == "__main__":
    main()