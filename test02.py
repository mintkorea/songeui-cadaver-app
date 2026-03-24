def generate_response(registered, accident, family, night):
    if not registered:
        return "❌ 사전 등록이 없어 기증 불가\n→ 장기기증 상담 안내"

    if accident:
        return "❌ 사고사로 기증 불가"

    if not family:
        return "❌ 유가족 확인 필요"

    if night:
        return "⚠ 야간: 간단 접수 후 주간 상담 유도"

    return "✅ 정상 접수 진행"