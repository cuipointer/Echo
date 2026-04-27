#!/usr/bin/env python3
"""
链路预算工具

用于计算干扰裕量和敏感度阈值
"""

import argparse


def calculate_link_budget(tx_power, path_loss, rx_sensitivity):
    """
    计算链路预算

    Args:
        tx_power: 发射功率 (dBm)
        path_loss: 路径损耗 (dB)
        rx_sensitivity: 接收灵敏度 (dBm)

    Returns:
        dict: 计算结果
    """
    # 接收功率 = 发射功率 - 路径损耗
    rx_power = tx_power - path_loss

    # 干扰裕量 = 接收功率 - 接收灵敏度
    interference_margin = rx_power - rx_sensitivity

    # 判断是否超标
    is_exceeded = interference_margin > 0

    return {
        'tx_power': tx_power,
        'path_loss': path_loss,
        'rx_power': rx_power,
        'rx_sensitivity': rx_sensitivity,
        'interference_margin': interference_margin,
        'is_exceeded': is_exceeded
    }


def calculate_sensitivity_threshold(tx_power, path_loss, target_margin):
    """
    计算敏感度阈值

    Args:
        tx_power: 发射功率 (dBm)
        path_loss: 路径损耗 (dB)
        target_margin: 目标干扰裕量 (dB)

    Returns:
        dict: 计算结果
    """
    # 接收功率 = 发射功率 - 路径损耗
    rx_power = tx_power - path_loss

    # 敏感度阈值 = 接收功率 - 目标干扰裕量
    sensitivity_threshold = rx_power - target_margin

    return {
        'tx_power': tx_power,
        'path_loss': path_loss,
        'rx_power': rx_power,
        'target_margin': target_margin,
        'sensitivity_threshold': sensitivity_threshold
    }


def main():
    parser = argparse.ArgumentParser(
        description='链路预算工具 - 计算干扰裕量和敏感度阈值'
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 干扰裕量计算
    margin_parser = subparsers.add_parser(
        'margin',
        help='计算干扰裕量'
    )
    margin_parser.add_argument(
        'tx_power',
        type=float,
        help='发射功率 (dBm)'
    )
    margin_parser.add_argument(
        'path_loss',
        type=float,
        help='路径损耗 (dB)'
    )
    margin_parser.add_argument(
        'rx_sensitivity',
        type=float,
        help='接收灵敏度 (dBm)'
    )

    # 敏感度阈值计算
    threshold_parser = subparsers.add_parser(
        'threshold',
        help='计算敏感度阈值'
    )
    threshold_parser.add_argument(
        'tx_power',
        type=float,
        help='发射功率 (dBm)'
    )
    threshold_parser.add_argument(
        'path_loss',
        type=float,
        help='路径损耗 (dB)'
    )
    threshold_parser.add_argument(
        'target_margin',
        type=float,
        help='目标干扰裕量 (dB)'
    )

    args = parser.parse_args()

    if args.command == 'margin':
        # 计算干扰裕量
        result = calculate_link_budget(
            args.tx_power,
            args.path_loss,
            args.rx_sensitivity
        )

        print("=" * 60)
        print("干扰裕量计算结果")
        print("=" * 60)
        print(f"发射功率: {result['tx_power']:.2f} dBm")
        print(f"路径损耗: {result['path_loss']:.2f} dB")
        print(f"接收功率: {result['rx_power']:.2f} dBm")
        print(f"接收灵敏度: {result['rx_sensitivity']:.2f} dBm")
        print("-" * 60)
        print(f"干扰裕量: {result['interference_margin']:.2f} dB")

        if result['is_exceeded']:
            print("⚠️  干扰超标！")
        else:
            print("✓ 干扰在允许范围内")

        print("=" * 60)

    elif args.command == 'threshold':
        # 计算敏感度阈值
        result = calculate_sensitivity_threshold(
            args.tx_power,
            args.path_loss,
            args.target_margin
        )

        print("=" * 60)
        print("敏感度阈值计算结果")
        print("=" * 60)
        print(f"发射功率: {result['tx_power']:.2f} dBm")
        print(f"路径损耗: {result['path_loss']:.2f} dB")
        print(f"接收功率: {result['rx_power']:.2f} dBm")
        print(f"目标干扰裕量: {result['target_margin']:.2f} dB")
        print("-" * 60)
        print(f"敏感度阈值: {result['sensitivity_threshold']:.2f} dBm")
        print(f"  (接收灵敏度需优于此值)")
        print("=" * 60)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
