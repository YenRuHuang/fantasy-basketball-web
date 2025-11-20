"""
更新版陣容分析 - 考慮多位置靈活性
"""

import json

print("=" * 80)
print(" 陣容分析 - 多位置靈活性評估")
print("=" * 80)
print()

# 載入陣容數據
with open('data/my_roster_full.json', 'r', encoding='utf-8') as f:
    roster_data = json.load(f)

players = roster_data['players']

print("📊 位置分布分析（考慮多位置）")
print("-" * 80)
print()

# 統計每個位置的球員數（含多位置）
position_coverage = {
    'PG': [],
    'SG': [],
    'SF': [],
    'PF': [],
    'C': []
}

for player in players:
    for pos in player['positions']:
        if pos in position_coverage:
            position_coverage[pos].append(player['name'])

print("各位置可用球員數量：")
print()
for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
    count = len(position_coverage[pos])
    print(f"  {pos}: {count} 人")
print()

print("詳細球員分布：")
print()
for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
    print(f"  {pos} 位置可用球員:")
    for player_name in position_coverage[pos]:
        # 找到該球員的所有位置
        player_info = next(p for p in players if p['name'] == player_name)
        all_pos = ','.join(player_info['positions'])
        status = f" ({player_info['status']})" if player_info['status'] else ""
        print(f"    • {player_name} [{all_pos}]{status}")
    print()

print("=" * 80)
print(" 🎯 多位置球員價值分析")
print("=" * 80)
print()

# 找出多位置球員
multi_pos_players = [p for p in players if len(p['positions']) > 1]

print(f"多位置球員: {len(multi_pos_players)}/{len(players)} 位")
print()

# 按彈性分類
guards = []  # PG/SG
wings = []   # SG/SF
forwards = [] # SF/PF
bigs = []    # PF/C

for player in multi_pos_players:
    pos_set = set(player['positions'])
    status = f" ({player['status']})" if player['status'] else ""

    if pos_set == {'PG', 'SG'}:
        guards.append(f"{player['name']} [PG/SG]{status}")
    elif pos_set == {'SG', 'SF'}:
        wings.append(f"{player['name']} [SG/SF]{status}")
    elif pos_set == {'SF', 'PF'}:
        forwards.append(f"{player['name']} [SF/PF]{status}")
    elif pos_set == {'PF', 'C'}:
        bigs.append(f"{player['name']} [PF/C]{status}")

if guards:
    print(f"🔵 後衛彈性 (PG/SG): {len(guards)} 人")
    for g in guards:
        print(f"  • {g}")
    print()

if wings:
    print(f"🟢 側翼彈性 (SG/SF): {len(wings)} 人")
    for w in wings:
        print(f"  • {w}")
    print()

if forwards:
    print(f"🟡 前鋒彈性 (SF/PF): {len(forwards)} 人")
    for f in forwards:
        print(f"  • {f}")
    print()

if bigs:
    print(f"🔴 大個子彈性 (PF/C): {len(bigs)} 人")
    for b in bigs:
        print(f"  • {b}")
    print()

print("=" * 80)
print(" 💡 策略建議（更新版）")
print("=" * 80)
print()

# 重新評估位置平衡
pg_count = len(position_coverage['PG'])
sg_count = len(position_coverage['SG'])
sf_count = len(position_coverage['SF'])
pf_count = len(position_coverage['PF'])
c_count = len(position_coverage['C'])

print("✅ 優勢分析:")
print()

if len(bigs) >= 3:
    print(f"1. 內線深度充足")
    print(f"   • {len(bigs)} 名 PF/C 雙位置球員 (Giannis, Chet, Filipowski)")
    print(f"   • 原本看似中鋒不足 (只有 {c_count} 名 C)")
    print(f"   • 但實際有 {c_count} 名球員可以打中鋒位置！")
    print()

if len(guards) >= 3:
    print(f"2. 後衛彈性極佳")
    print(f"   • {len(guards)} 名 PG/SG 雙位置球員")
    print(f"   • 可以靈活調整 PG 和 SG 排陣")
    print()

if len(forwards) >= 2:
    print(f"3. 前鋒位置靈活")
    print(f"   • {len(forwards)} 名 SF/PF 雙位置球員")
    print(f"   • 填補 SF 和 PF 都方便")
    print()

print("⚠️  需要注意:")
print()

# 計算單一位置球員
single_pos_players = [p for p in players if len(p['positions']) == 1]
if single_pos_players:
    print(f"1. 單一位置球員 ({len(single_pos_players)} 人)")
    print("   這些球員彈性較低，排陣時要特別注意：")
    for p in single_pos_players:
        status = f" ({p['status']})" if p['status'] else ""
        print(f"   • {p['name']} [{p['positions'][0]}]{status}")
    print()

# 檢查傷病球員
injured = [p for p in players if p['status'] in ['INJ', 'GTD']]
if injured:
    print(f"2. 傷病球員影響彈性")
    for p in injured:
        pos_str = ','.join(p['positions'])
        print(f"   • {p['name']} [{pos_str}] - {p['status']}")
    print()

print("=" * 80)
print(" 🔄 交易建議（更新版）")
print("=" * 80)
print()

print("考慮多位置後的結論：")
print()
print("✅ 不需要急著補中鋒了！")
print(f"   • 原本以為中鋒不足 (只有 Yves Missi)")
print(f"   • 但實際有 {len(bigs)} 名 PF/C 雙棲球員")
print(f"   • 可以靈活調整，不需要為了 C 而犧牲其他位置")
print()

print("🎯 新的交易優先順序：")
print()
print("1. 🔴 [高優先] 處理傷兵")
print("   • Jayson Tatum (SF/PF) - INJ")
print("   • Kyrie Irving (PG) - INJ")
print("   → 兩個都是重要球員，但 Kyrie 是單一位置，彈性較低")
print()
print("2. 🟡 [中優先] 優化單一位置球員")
if single_pos_players:
    print(f"   • 考慮交易單一位置球員換取多位置球員")
    print(f"   • 增加排陣靈活性")
print()
print("3. 🟢 [低優先] 強化數據類別")
print("   • 專注在 3PM, FT%, ST, AST 等優勢類別")
print("   • Punt FG%, REB, DD (接受這些弱項)")
print()

print("=" * 80)
print(" 總結")
print("=" * 80)
print()
print(f"✅ 你的陣容比原本分析的更平衡！")
print()
print(f"  • 多位置球員: {len(multi_pos_players)}/{len(players)} ({len(multi_pos_players)/len(players)*100:.0f}%)")
print(f"  • PF/C 雙棲: {len(bigs)} 人 → 內線不缺！")
print(f"  • PG/SG 雙棲: {len(guards)} 人 → 後衛靈活！")
print(f"  • SF/PF 雙棲: {len(forwards)} 人 → 前鋒充足！")
print()
print(f"原本的「中鋒不足」問題其實不嚴重，因為你有 {len(bigs)} 個能打 C 的球員！")
print()
