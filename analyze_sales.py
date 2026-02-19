#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# 한글 폰트 설정
def setup_korean_font():
    """
    시스템에서 사용 가능한 한글 폰트를 설정합니다.
    """
    import matplotlib.font_manager as fm
    
    # 사용 가능한 한글 폰트 목록 (우선순위 순)
    korean_fonts = [
        'AppleGothic',
        'Apple SD Gothic Neo',
        'Nanum Gothic',
        'Hiragino Maru Gothic Pro',
        'Malgun Gothic'  # Windows
    ]
    
    for font_name in korean_fonts:
        try:
            # 폰트가 시스템에 있는지 확인
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            if font_name in available_fonts:
                plt.rcParams['font.family'] = font_name
                plt.rcParams['axes.unicode_minus'] = False
                # print(f"Korean font set to: {font_name}")  # JSON 파싱 방해 방지
                return font_name
        except Exception as e:
            print(f"Failed to set font {font_name}: {e}")
            continue
    
    # 한글 폰트를 찾지 못한 경우 기본 설정
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False
    # print("Warning: No Korean font found, using default font")  # JSON 파싱 방해 방지
    return 'DejaVu Sans'

# 한글 폰트 설정
setup_korean_font()

def analyze_sales_data(file_path):
    """
    판매 데이터를 분석하고 통계와 차트를 생성합니다.
    """
    try:
        # 파일 확장자에 따라 읽기
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            return {"error": "지원하지 않는 파일 형식입니다. CSV 또는 XLSX 파일을 업로드하세요."}

        # 기본 통계 계산
        stats = {}
        
        # 1. 전체 통계
        if 'Sales' in df.columns:
            stats['total_sales'] = float(df['Sales'].sum())
            stats['avg_sales'] = float(df['Sales'].mean())
            stats['median_sales'] = float(df['Sales'].median())
            stats['max_sales'] = float(df['Sales'].max())
            stats['min_sales'] = float(df['Sales'].min())
        
        if 'Profit' in df.columns:
            stats['total_profit'] = float(df['Profit'].sum())
            stats['avg_profit'] = float(df['Profit'].mean())
            stats['profit_margin'] = float(df['Profit'].sum() / df['Sales'].sum() * 100) if 'Sales' in df.columns else 0
        
        if 'Quantity' in df.columns:
            stats['total_quantity'] = int(df['Quantity'].sum())
            stats['avg_quantity'] = float(df['Quantity'].mean())
        
        stats['total_orders'] = len(df)
        
        # 2. 카테고리별 통계
        if 'Category' in df.columns:
            category_stats = df.groupby('Category').agg({
                'Sales': ['sum', 'mean', 'count'],
                'Profit': 'sum' if 'Profit' in df.columns else 'count'
            }).round(2)
            
            stats['category_sales'] = {}
            for idx, row in category_stats.iterrows():
                stats['category_sales'][idx] = {
                    'total_sales': float(row[('Sales', 'sum')]),
                    'avg_sales': float(row[('Sales', 'mean')]),
                    'count': int(row[('Sales', 'count')]),
                    'total_profit': float(row[('Profit', 'sum')]) if 'Profit' in df.columns else 0
                }
        
        # 3. 서브카테고리별 통계 (상위 10개)
        if 'Sub-Category' in df.columns:
            subcategory_stats = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
            stats['top_subcategories'] = {k: float(v) for k, v in subcategory_stats.items()}
        
        # 4. 지역별 통계
        region_column = None
        if 'State' in df.columns:
            region_column = 'State'
        elif 'Region' in df.columns:
            region_column = 'Region'
        
        if region_column:
            region_stats = df.groupby(region_column).agg({
                'Sales': 'sum',
                'Profit': 'sum' if 'Profit' in df.columns else 'count'
            }).sort_values('Sales', ascending=False).head(10)
            
            stats['top_regions'] = {}
            for idx, row in region_stats.iterrows():
                stats['top_regions'][idx] = {
                    'sales': float(row['Sales']),
                    'profit': float(row['Profit']) if 'Profit' in df.columns else 0
                }
        
        # 5. 고객 세그먼트별 통계
        if 'Segment' in df.columns:
            segment_stats = df.groupby('Segment').agg({
                'Sales': ['sum', 'mean'],
                'Profit': 'sum' if 'Profit' in df.columns else 'count'
            }).round(2)
            
            stats['segment_stats'] = {}
            for idx, row in segment_stats.iterrows():
                stats['segment_stats'][idx] = {
                    'total_sales': float(row[('Sales', 'sum')]),
                    'avg_sales': float(row[('Sales', 'mean')]),
                    'total_profit': float(row[('Profit', 'sum')]) if 'Profit' in df.columns else 0
                }
        
        # 6. 월별 추세 (날짜 컬럼이 있는 경우)
        date_column = None
        for col in ['Order Date', 'Date', 'OrderDate']:
            if col in df.columns:
                date_column = col
                break
        
        if date_column:
            try:
                df[date_column] = pd.to_datetime(df[date_column])
                df['YearMonth'] = df[date_column].dt.to_period('M')
                monthly_stats = df.groupby('YearMonth')['Sales'].sum()
                stats['monthly_trend'] = {str(k): float(v) for k, v in monthly_stats.items()}
            except:
                pass
        
        # 차트 생성
        charts = create_charts(df, stats)
        
        return {
            'success': True,
            'stats': stats,
            'charts': charts,
            'columns': list(df.columns),
            'row_count': len(df)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def create_charts(df, stats):
    """
    데이터 시각화 차트를 생성하고 파일로 저장합니다.
    """
    charts = []
    output_dir = 'temp_charts'
    os.makedirs(output_dir, exist_ok=True)
    
    # 차트 스타일 설정
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    
    try:
        # 1. 카테고리별 매출 (막대 차트)
        if 'Category' in df.columns and 'Sales' in df.columns:
            plt.figure(figsize=(10, 6))
            category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
            category_sales.plot(kind='barh', color='steelblue')
            plt.title('Sales by Category', fontsize=16, fontweight='bold')
            plt.xlabel('Sales ($)', fontsize=12)
            plt.ylabel('Category', fontsize=12)
            plt.tight_layout()
            chart_path = os.path.join(output_dir, 'category_sales.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(chart_path)
        
        # 2. 상위 10개 지역별 이익 (막대 차트)
        region_column = 'State' if 'State' in df.columns else ('Region' if 'Region' in df.columns else None)
        if region_column and 'Profit' in df.columns:
            plt.figure(figsize=(10, 6))
            region_profit = df.groupby(region_column)['Profit'].sum().sort_values(ascending=True).tail(10)
            colors = ['red' if x < 0 else 'green' for x in region_profit.values]
            region_profit.plot(kind='barh', color=colors)
            plt.title('Top 10 Regions by Profit', fontsize=16, fontweight='bold')
            plt.xlabel('Profit ($)', fontsize=12)
            plt.ylabel(region_column, fontsize=12)
            plt.tight_layout()
            chart_path = os.path.join(output_dir, 'region_profit.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(chart_path)
        
        # 3. 서브카테고리별 매출 (상위 10개)
        if 'Sub-Category' in df.columns and 'Sales' in df.columns:
            plt.figure(figsize=(10, 6))
            subcategory_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
            subcategory_sales.plot(kind='bar', color='coral')
            plt.title('Top 10 Sub-Categories by Sales', fontsize=16, fontweight='bold')
            plt.xlabel('Sub-Category', fontsize=12)
            plt.ylabel('Sales ($)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            chart_path = os.path.join(output_dir, 'subcategory_sales.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(chart_path)
        
        # 4. 세그먼트별 매출 및 이익 (그룹 막대 차트)
        if 'Segment' in df.columns and 'Sales' in df.columns and 'Profit' in df.columns:
            plt.figure(figsize=(10, 6))
            segment_data = df.groupby('Segment')[['Sales', 'Profit']].sum()
            segment_data.plot(kind='bar', color=['steelblue', 'orange'])
            plt.title('Sales and Profit by Segment', fontsize=16, fontweight='bold')
            plt.xlabel('Segment', fontsize=12)
            plt.ylabel('Amount ($)', fontsize=12)
            plt.legend(['Sales', 'Profit'])
            plt.xticks(rotation=0)
            plt.tight_layout()
            chart_path = os.path.join(output_dir, 'segment_comparison.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(chart_path)
        
        # 5. 매출과 이익의 상관관계 (산점도)
        if 'Sales' in df.columns and 'Profit' in df.columns:
            plt.figure(figsize=(10, 6))
            colors_scatter = ['red' if x < 0 else 'green' for x in df['Profit']]
            plt.scatter(df['Sales'], df['Profit'], alpha=0.5, c=colors_scatter, s=30)
            plt.title('Sales vs Profit Relationship', fontsize=16, fontweight='bold')
            plt.xlabel('Sales ($)', fontsize=12)
            plt.ylabel('Profit ($)', fontsize=12)
            plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            chart_path = os.path.join(output_dir, 'sales_profit_scatter.png')
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            charts.append(chart_path)
        
        # 6. 월별 매출 추세 (선 그래프)
        date_column = None
        for col in ['Order Date', 'Date', 'OrderDate']:
            if col in df.columns:
                date_column = col
                break
        
        if date_column:
            try:
                df_temp = df.copy()
                df_temp[date_column] = pd.to_datetime(df_temp[date_column])
                df_temp['YearMonth'] = df_temp[date_column].dt.to_period('M')
                monthly_sales = df_temp.groupby('YearMonth')['Sales'].sum()
                
                plt.figure(figsize=(12, 6))
                monthly_sales.plot(kind='line', marker='o', color='steelblue', linewidth=2, markersize=6)
                plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold')
                plt.xlabel('Month', fontsize=12)
                plt.ylabel('Sales ($)', fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                chart_path = os.path.join(output_dir, 'monthly_trend.png')
                plt.savefig(chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                charts.append(chart_path)
            except:
                pass
        
    except Exception as e:
        print(f"Chart creation error: {str(e)}", file=sys.stderr)
    
    return charts


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '파일 경로를 제공해주세요.'}))
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = analyze_sales_data(file_path)
    # JSON 출력을 한 줄로 만들어 파싱 오류 방지
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))

