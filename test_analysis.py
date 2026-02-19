#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
테스트 스크립트: Sample-100-Superstore.csv 파일로 분석 테스트
"""

import sys
import json
from analyze_sales import analyze_sales_data

def main():
    print("=" * 60)
    print("Testing Sales Analysis with Sample-100-Superstore.csv")
    print("=" * 60)
    print()
    
    # 테스트 파일 경로
    test_file = "Sample-100-Superstore.csv"
    
    print(f"📊 Analyzing file: {test_file}")
    print()
    
    # 분석 실행
    result = analyze_sales_data(test_file)
    
    if not result.get('success'):
        print(f"❌ Error: {result.get('error')}")
        return 1
    
    # 결과 출력
    stats = result['stats']
    
    print("✅ Analysis completed successfully!")
    print()
    print("-" * 60)
    print("📈 OVERALL STATISTICS")
    print("-" * 60)
    print(f"Total Sales:      ${stats.get('total_sales', 0):,.2f}")
    print(f"Total Profit:     ${stats.get('total_profit', 0):,.2f}")
    print(f"Profit Margin:    {stats.get('profit_margin', 0):.2f}%")
    print(f"Average Sales:    ${stats.get('avg_sales', 0):,.2f}")
    print(f"Average Profit:   ${stats.get('avg_profit', 0):,.2f}")
    print(f"Total Orders:     {stats.get('total_orders', 0):,}")
    if 'total_quantity' in stats:
        print(f"Total Quantity:   {stats.get('total_quantity', 0):,}")
    print()
    
    # 카테고리별 통계
    if 'category_sales' in stats and stats['category_sales']:
        print("-" * 60)
        print("📊 CATEGORY PERFORMANCE")
        print("-" * 60)
        for category, data in stats['category_sales'].items():
            print(f"\n{category}:")
            print(f"  Total Sales:  ${data['total_sales']:,.2f}")
            print(f"  Total Profit: ${data['total_profit']:,.2f}")
            print(f"  Orders:       {data['count']:,}")
            print(f"  Avg Sales:    ${data['avg_sales']:,.2f}")
        print()
    
    # 상위 지역
    if 'top_regions' in stats and stats['top_regions']:
        print("-" * 60)
        print("🌍 TOP REGIONS")
        print("-" * 60)
        for i, (region, data) in enumerate(list(stats['top_regions'].items())[:5], 1):
            print(f"{i}. {region}")
            print(f"   Sales:  ${data['sales']:,.2f}")
            print(f"   Profit: ${data['profit']:,.2f}")
        print()
    
    # 차트 생성 확인
    if 'charts' in result and result['charts']:
        print("-" * 60)
        print("📉 CHARTS GENERATED")
        print("-" * 60)
        for chart in result['charts']:
            print(f"✅ {chart}")
        print()
    
    print("=" * 60)
    print("✅ Test completed successfully!")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

