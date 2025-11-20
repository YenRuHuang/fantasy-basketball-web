"""
Fantasy Basketball 分析範例 - Jupyter Notebook 用

這個檔案展示如何使用 API 進行完整的陣容分析
可以在 Jupyter Notebook 中逐步執行
"""

# %% [markdown]
# # Fantasy Basketball 完整分析範例
#
# 本範例展示如何使用 Yahoo Fantasy Basketball API 進行:
# 1. 獲取聯盟和球員數據
# 2. 分析你的陣容優劣勢
# 3. 評估交易影響
# 4. 找出交易目標球員

# %% 導入必要套件
import sys
sys.path.append('..')

from src.api.yahoo_client import YahooFantasyClient
from src.models.player import Player
from src.models.roster import Roster
from src.models.stats import PlayerStats
from src.analysis.roster_analyzer import RosterAnalyzer
from src.analysis.trade_analyzer import TradeAnalyzer
from src.analysis.category_scorer import CategoryScorer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定中文字體和圖表風格
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# %% [markdown]
# ## 步驟 1: 連接 Yahoo Fantasy API

# %% 初始化客戶端
client = YahooFantasyClient()

# 獲取聯盟資訊
league_info = client.get_league_info()
print(f"聯盟名稱: {league_info.name}")
print(f"隊伍數量: {league_info.num_teams}")
print(f"當前週次: {league_info.current_week}")

# %% [markdown]
# ## 步驟 2: 獲取你的陣容數據

# %% 獲取陣容
my_team_roster = client.get_team_roster()

print(f"\n你的陣容:")
for player in my_team_roster:
    print(f"  {player.name} ({player.display_position})")

# %% [markdown]
# ## 步驟 3: 分析陣容優劣勢

# %% 建立陣容分析器
# 注意: 這裡需要先將 Yahoo API 的數據轉換為我們的 Player 和 PlayerStats 模型
# 實際使用時需要寫一個轉換函數

def convert_yahoo_player_to_model(yahoo_player):
    """將 Yahoo API 的球員數據轉換為我們的模型"""
    # 這是示例，實際實作需要根據 Yahoo API 的數據結構調整
    stats = PlayerStats(
        player_id=yahoo_player.player_id,
        player_name=yahoo_player.name.full,
        team=yahoo_player.editorial_team_abbr,
        position=yahoo_player.display_position,
        games_played=yahoo_player.player_stats.stats.get('GP', 0),
        # ... 其他統計數據
    )

    return Player(
        player_id=yahoo_player.player_id,
        name=yahoo_player.name.full,
        team=yahoo_player.editorial_team_abbr,
        positions=yahoo_player.eligible_positions,
        stats=stats
    )

# 轉換陣容
my_roster = Roster(
    team_name="我的隊伍",
    players=[convert_yahoo_player_to_model(p) for p in my_team_roster]
)

# 分析陣容
analyzer = RosterAnalyzer(my_roster)
report = analyzer.get_roster_report()

# %% 顯示分析結果
print(f"\n陣容分析報告:")
print(f"隊伍名稱: {report['team_name']}")
print(f"活躍球員: {report['roster_size']['active']}")
print(f"受傷球員: {report['roster_size']['injured']}")

print(f"\n優勢類別: {', '.join(report['strategic_summary']['strong_categories'])}")
print(f"劣勢類別 (Punt): {', '.join(report['strategic_summary']['punt_categories'])}")

# %% [markdown]
# ## 步驟 4: 視覺化陣容強弱

# %% 繪製類別強度圖
category_data = []
for cat, data in report['category_analysis'].items():
    if data['z_score'] != 'N/A':
        category_data.append({
            'Category': cat,
            'Z-Score': data['z_score'],
            'Strength': data['strength']
        })

df_categories = pd.DataFrame(category_data)

# 繪製橫條圖
plt.figure(figsize=(12, 6))
colors = ['green' if x > 0 else 'red' for x in df_categories['Z-Score']]
plt.barh(df_categories['Category'], df_categories['Z-Score'], color=colors, alpha=0.7)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0.5, color='green', linestyle='--', linewidth=0.5, alpha=0.5, label='Strong Threshold')
plt.axvline(x=-0.5, color='red', linestyle='--', linewidth=0.5, alpha=0.5, label='Punt Threshold')
plt.xlabel('Z-Score')
plt.title('陣容各類別強度分析')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 步驟 5: 評估潛在交易

# %% 評估交易
# 假設你想送出 Mitchell，換來 Sabonis

trade_analyzer = TradeAnalyzer(my_roster)

# 定義交易
give_players = [p for p in my_roster.players if "Mitchell" in p.name]
receive_players_data = [
    # 這裡應該從 Yahoo API 獲取 Sabonis 的數據
    # 示例用模擬數據
]

# 評估交易
trade_result = trade_analyzer.evaluate_trade(give_players, receive_players_data)

print(f"\n交易評估:")
print(f"送出: {', '.join(trade_result['trade_summary']['give'])}")
print(f"換來: {', '.join(trade_result['trade_summary']['receive'])}")
print(f"\n建議: {trade_result['recommendation']['decision']}")
print(f"原因: {trade_result['recommendation']['reason']}")

# %% 繪製交易影響圖
trade_impact = []
for cat, data in trade_result['category_changes'].items():
    trade_impact.append({
        'Category': cat,
        'Before': data['before'],
        'After': data['after'],
        'Change': data['change']
    })

df_trade = pd.DataFrame(trade_impact)

fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(df_trade))
width = 0.35

ax.bar([i - width/2 for i in x], df_trade['Before'], width, label='交易前', alpha=0.7)
ax.bar([i + width/2 for i in x], df_trade['After'], width, label='交易後', alpha=0.7)

ax.set_xlabel('類別')
ax.set_ylabel('數值')
ax.set_title('交易前後類別變化')
ax.set_xticks(x)
ax.set_xticklabels(df_trade['Category'])
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 步驟 6: 找出交易目標球員

# %% 尋找補強目標
# 假設你想補強 FG% 和 REB
target_categories = ['FG%', 'REB', 'BLK']

# 獲取所有自由球員
free_agents = client.get_free_agents()

# 轉換為 PlayerStats 模型
all_players_stats = [convert_yahoo_player_to_model(p).stats for p in free_agents]

# 找出目標球員
suggestions = trade_analyzer.suggest_trade_targets(
    target_categories=target_categories,
    max_results=10
)

print(f"\n補強 {', '.join(target_categories)} 的建議球員:")
for i, player in enumerate(suggestions, 1):
    print(f"\n#{i} {player['player_name']} ({player['team']})")
    print(f"  目標分數: {player['target_score']}")
    for cat in target_categories:
        print(f"  {cat}: {player['category_scores'][cat]}")

# %% [markdown]
# ## 步驟 7: 匯出報告

# %% 匯出為 CSV
df_report = pd.DataFrame({
    'Category': list(report['category_totals'].keys()),
    'Value': list(report['category_totals'].values())
})

df_report.to_csv('../data/exports/roster_analysis.csv', index=False, encoding='utf-8-sig')
print("\n報告已匯出至 data/exports/roster_analysis.csv")

# %% [markdown]
# ## 完成！
#
# 你現在已經學會如何:
# - 連接 Yahoo Fantasy API 獲取數據
# - 分析陣容的優劣勢
# - 評估交易的影響
# - 找出交易目標球員
# - 視覺化數據和匯出報告
