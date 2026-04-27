#!/usr/bin/env python3
"""
谐波计算工具

用于计算干扰源谐波是否命中受扰体频段
"""

import argparse
import sys


def calculate_harmonics(base_freq, harmonic_order, victim_start, victim_end):
    """
    计算谐波频率并判断是否命中受扰体频段

    Args:
        base_freq: 基频 (MHz)
        harmonic_order: 谐波次数
        victim_start: 受扰体频段起始频率 (MHz)
        victim_end: 受扰体频段结束频率 (MHz)

    Returns:
        dict: 计算结果
    """
    harmonic_freq = base_freq * harmonic_order

    # 判断是否命中
    is_hit = victim_start <= harmonic_freq <= victim_end

    # 计算频偏
    if is_hit:
        offset = 0
    else:
        if harmonic_freq < victim_start:
            offset = victim_start - harmonic_freq
        else:
            offset = harmonic_freq - victim_end

    return {
        'base_freq': base_freq,
        'harmonic_order': harmonic_order,
        'harmonic_freq': harmonic_freq,
        'victim_range': f"{victim_start}-{victim_end} MHz",
        'is_hit': is_hit,
        'offset': offset
    }


def main():
    parser = argparse.ArgumentParser(
        description='谐波计算工具 - 判断干扰源谐波是否命中受扰体频段'
    )
    parser.add_argument(
        'base_freq',
        type=float,
        help='干扰源基频 (MHz)'
    )
    parser.add_argument(
        'harmonic_order',
        type=int,
        help='谐波次数'
    )
    parser.add_argument(
        'victim_start',
        type=float,
        help='受扰体频段起始频率 (MHz)'
    )
    parser.add_argument(
        'victim_end',
        type=float,
        help='受扰体频段结束频率 (MHz)'
    )

    args = parser.parse_args()

    # 计算谐波
    result = calculate_harmonics(
        args.base_freq,
        args.harmonic_order,
        args.victim_start,
        args.victim_end
    )

    # 输出结果
    print("=" * 60)
    print("谐波计算结果")
    print("=" * 60)
    print(f"基频: {result['base_freq']} MHz")
    print(f"谐波次数: {result['harmonic_order']}")
    print(f"谐波频率: {result['harmonic_freq']} MHz")
    print(f"受扰体频段: {result['victim_range']}")
    print("-" * 60)

    if result['is_hit']:
        print("✓ 命中受扰体频段")
    else:
        print(f"✗ 未命中受扰体频段")
        print(f"  频偏: {result['offset']:.2f} MHz")

    print("=" * 60)


if __name__ == '__main__':
    main()
