#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from openai import OpenAI

def generate_gpt_analysis(stats_data):
    """
    GPT API를 사용하여 통계 데이터를 기반으로 자연어 분석 보고서를 생성합니다.
    """
    try:
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return {
                'success': False,
                'error': 'OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.'
            }
        
        client = OpenAI(api_key=api_key)
        
        # 통계 데이터를 텍스트로 변환
        stats_text = format_stats_for_gpt(stats_data)
        
        # GPT 프롬프트 생성
        prompt = f"""당신은 전문 비즈니스 분석가입니다. 다음 판매 데이터 통계를 분석하고, 한국어로 상세한 마케팅 전략 보고서를 작성해주세요.

보고서는 다음 구조를 따라야 합니다:
1. 전체 개요 (Executive Summary)
2. 주요 발견 사항 (Key Findings)
3. 카테고리 분석
4. 지역 분석
5. 세그먼트 분석
6. 개선 제안 및 마케팅 전략
7. 결론

전문적이고 통찰력 있는 분석을 제공하되, 구체적인 수치와 함께 설명해주세요.

=== 판매 데이터 통계 ===
{stats_text}
"""

        # GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 데이터 분석과 마케팅 전략 수립에 능한 비즈니스 분석 전문가입니다. 제공된 데이터를 깊이 있게 분석하고, 실행 가능한 인사이트와 전략을 제공합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            'success': True,
            'analysis': analysis_text,
            'model': response.model,
            'tokens_used': response.usage.total_tokens
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def format_stats_for_gpt(stats):
    """
    통계 데이터를 GPT가 이해하기 쉬운 텍스트 형식으로 변환합니다.
    """
    text_parts = []
    
    # 전체 통계
    text_parts.append("## 전체 통계")
    text_parts.append(f"- 총 매출: ${stats.get('total_sales', 0):,.2f}")
    text_parts.append(f"- 평균 매출: ${stats.get('avg_sales', 0):,.2f}")
    text_parts.append(f"- 총 이익: ${stats.get('total_profit', 0):,.2f}")
    text_parts.append(f"- 평균 이익: ${stats.get('avg_profit', 0):,.2f}")
    text_parts.append(f"- 이익률: {stats.get('profit_margin', 0):.2f}%")
    text_parts.append(f"- 총 주문 수: {stats.get('total_orders', 0):,}")
    
    if 'total_quantity' in stats:
        text_parts.append(f"- 총 판매 수량: {stats.get('total_quantity', 0):,}")
    
    text_parts.append("")
    
    # 카테고리별 통계
    if 'category_sales' in stats and stats['category_sales']:
        text_parts.append("## 카테고리별 매출")
        for category, data in stats['category_sales'].items():
            text_parts.append(f"- {category}:")
            text_parts.append(f"  * 총 매출: ${data['total_sales']:,.2f}")
            text_parts.append(f"  * 평균 매출: ${data['avg_sales']:,.2f}")
            text_parts.append(f"  * 주문 수: {data['count']:,}")
            text_parts.append(f"  * 총 이익: ${data['total_profit']:,.2f}")
        text_parts.append("")
    
    # 서브카테고리 통계
    if 'top_subcategories' in stats and stats['top_subcategories']:
        text_parts.append("## 상위 서브카테고리 (매출 기준)")
        for subcategory, sales in stats['top_subcategories'].items():
            text_parts.append(f"- {subcategory}: ${sales:,.2f}")
        text_parts.append("")
    
    # 지역별 통계
    if 'top_regions' in stats and stats['top_regions']:
        text_parts.append("## 상위 지역 (매출 기준)")
        for region, data in stats['top_regions'].items():
            text_parts.append(f"- {region}:")
            text_parts.append(f"  * 매출: ${data['sales']:,.2f}")
            text_parts.append(f"  * 이익: ${data['profit']:,.2f}")
        text_parts.append("")
    
    # 세그먼트별 통계
    if 'segment_stats' in stats and stats['segment_stats']:
        text_parts.append("## 고객 세그먼트별 통계")
        for segment, data in stats['segment_stats'].items():
            text_parts.append(f"- {segment}:")
            text_parts.append(f"  * 총 매출: ${data['total_sales']:,.2f}")
            text_parts.append(f"  * 평균 매출: ${data['avg_sales']:,.2f}")
            text_parts.append(f"  * 총 이익: ${data['total_profit']:,.2f}")
        text_parts.append("")
    
    # 월별 추세
    if 'monthly_trend' in stats and stats['monthly_trend']:
        text_parts.append("## 월별 매출 추세")
        monthly_items = list(stats['monthly_trend'].items())[:6]  # 최근 6개월만
        for month, sales in monthly_items:
            text_parts.append(f"- {month}: ${sales:,.2f}")
        text_parts.append("")
    
    return "\n".join(text_parts)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '통계 데이터를 제공해주세요.'}, ensure_ascii=False))
        sys.exit(1)
    
    stats_json = sys.argv[1]
    stats_data = json.loads(stats_json)
    
    result = generate_gpt_analysis(stats_data)
    # JSON 출력을 한 줄로 만들어 파싱 오류 방지
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))

