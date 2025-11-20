"""
自動化週報告生成器

功能：
1. 每週自動分析陣容
2. 生成對戰預測
3. 提供交易建議
4. 發送通知或匯出報告
"""

import json
from datetime import datetime
from typing import Dict, List
from pathlib import Path

from ..models.roster import Roster
from ..analysis.roster_analyzer import RosterAnalyzer
from ..analysis.matchup_predictor import MatchupPredictor
from ..analysis.trade_targets import TradeTargetRecommender


class WeeklyReportGenerator:
    """週報告生成器"""

    def __init__(self, my_roster: Roster, league_players: List = None):
        """
        初始化報告生成器

        Args:
            my_roster: 你的陣容
            league_players: 聯盟所有球員數據
        """
        self.my_roster = my_roster
        self.league_players = league_players or []
        self.report_date = datetime.now()

    def generate_full_report(self, opponent_roster: Roster = None) -> Dict:
        """
        生成完整週報告

        Args:
            opponent_roster: 本週對手的陣容（可選）

        Returns:
            完整報告字典
        """
        print("正在生成週報告...")

        report = {
            'generated_at': self.report_date.strftime("%Y-%m-%d %H:%M:%S"),
            'week': self._get_current_week(),
            'roster_analysis': {},
            'matchup_prediction': {},
            'trade_recommendations': {},
            'action_items': []
        }

        # 1. 陣容分析
        print("  ├─ 分析陣容...")
        roster_analyzer = RosterAnalyzer(self.my_roster, self.league_players)
        roster_report = roster_analyzer.get_roster_report()

        report['roster_analysis'] = {
            'active_players': roster_report['roster_size']['active'],
            'injured_players': roster_report['roster_size']['injured'],
            'strong_categories': roster_report.get('strategic_summary', {}).get('strong_categories', []),
            'punt_categories': roster_report.get('strategic_summary', {}).get('punt_categories', []),
            'improvements': roster_analyzer.suggest_improvements()
        }

        # 2. 對戰預測（如果有對手資訊）
        if opponent_roster:
            print("  ├─ 預測對戰...")
            predictor = MatchupPredictor()
            matchup = predictor.predict_matchup(self.my_roster, opponent_roster)

            report['matchup_prediction'] = {
                'outcome': matchup['prediction']['outcome'],
                'win_probability': matchup['prediction']['win_probability'],
                'wins': matchup['prediction']['wins'],
                'losses': matchup['prediction']['losses'],
                'strategies': matchup['strategies']
            }

        # 3. 交易建議
        if self.league_players:
            print("  ├─ 分析交易機會...")
            recommender = TradeTargetRecommender(self.my_roster, self.league_players)

            punt_cats = report['roster_analysis']['punt_categories']
            if punt_cats:
                targets = recommender.recommend_targets(
                    target_categories=punt_cats,
                    max_results=5
                )
                report['trade_recommendations'] = {
                    'target_categories': punt_cats,
                    'top_targets': targets
                }

        # 4. 行動清單
        print("  └─ 生成行動清單...")
        report['action_items'] = self._generate_action_items(report)

        print("✅ 報告生成完成")
        return report

    def _get_current_week(self) -> int:
        """獲取當前週次"""
        # 這裡應該從 Yahoo API 獲取，這裡用假數據
        return 1

    def _generate_action_items(self, report: Dict) -> List[Dict]:
        """
        生成行動清單

        Args:
            report: 報告數據

        Returns:
            行動清單
        """
        action_items = []

        # 基於改善建議
        improvements = report.get('roster_analysis', {}).get('improvements', [])
        for imp in improvements:
            if imp.get('priority') == 'High':
                action_items.append({
                    'priority': 'High',
                    'category': '陣容改善',
                    'task': imp.get('issue', ''),
                    'action': imp.get('recommendation', '')
                })

        # 基於對戰預測
        matchup = report.get('matchup_prediction', {})
        if matchup:
            if matchup.get('win_probability', 0) < 0.5:
                action_items.append({
                    'priority': 'High',
                    'category': '對戰策略',
                    'task': '本週形勢不利',
                    'action': '仔細調整先發陣容，專注在可以贏的類別'
                })

        # 基於交易建議
        trade_recs = report.get('trade_recommendations', {})
        if trade_recs and trade_recs.get('top_targets'):
            top_target = trade_recs['top_targets'][0]
            action_items.append({
                'priority': 'Medium',
                'category': '交易機會',
                'task': f"考慮交易獲取 {top_target['player_name']}",
                'action': f"補強 {', '.join(trade_recs['target_categories'])}"
            })

        # 檢查傷兵
        injured = report.get('roster_analysis', {}).get('injured_players', 0)
        if injured > 0:
            action_items.append({
                'priority': 'Medium',
                'category': '傷病管理',
                'task': f"目前有 {injured} 名傷兵",
                'action': '關注傷兵復出時間，考慮 IL 名單調整'
            })

        return action_items

    def format_report_text(self, report: Dict) -> str:
        """
        格式化報告為文字

        Args:
            report: 報告字典

        Returns:
            格式化的文字報告
        """
        lines = []

        lines.append("╔" + "═" * 68 + "╗")
        lines.append("║" + " " * 20 + "Fantasy Basketball 週報告" + " " * 23 + "║")
        lines.append("╚" + "═" * 68 + "╝")
        lines.append("")
        lines.append(f"生成時間: {report['generated_at']}")
        lines.append(f"週次: Week {report['week']}")
        lines.append("")

        # 陣容狀態
        roster = report.get('roster_analysis', {})
        lines.append("🏀 陣容狀態")
        lines.append("─" * 70)
        lines.append(f"健康球員: {roster.get('active_players', 0)} 人")
        lines.append(f"傷兵: {roster.get('injured_players', 0)} 人")
        lines.append(f"優勢類別: {', '.join(roster.get('strong_categories', []))}")
        lines.append(f"劣勢類別: {', '.join(roster.get('punt_categories', []))}")
        lines.append("")

        # 對戰預測
        matchup = report.get('matchup_prediction', {})
        if matchup:
            lines.append("⚔️  對戰預測")
            lines.append("─" * 70)
            lines.append(f"預測結果: {matchup.get('outcome', 'N/A')}")
            lines.append(f"勝率: {matchup.get('win_probability', 0) * 100:.1f}%")
            lines.append(f"預計贏: {matchup.get('wins', 0)} 個類別")
            lines.append(f"預計輸: {matchup.get('losses', 0)} 個類別")
            lines.append("")

        # 交易建議
        trade_recs = report.get('trade_recommendations', {})
        if trade_recs and trade_recs.get('top_targets'):
            lines.append("💼 交易建議")
            lines.append("─" * 70)
            lines.append(f"建議補強: {', '.join(trade_recs.get('target_categories', []))}")
            lines.append("推薦目標:")
            for i, target in enumerate(trade_recs.get('top_targets', [])[:5], 1):
                lines.append(f"  {i}. {target['player_name']} ({target['team']}) - 分數: {target['target_score']}")
            lines.append("")

        # 行動清單
        actions = report.get('action_items', [])
        if actions:
            lines.append("📋 本週行動清單")
            lines.append("─" * 70)
            for action in actions:
                priority_icon = "🔴" if action['priority'] == 'High' else "🟡" if action['priority'] == 'Medium' else "🟢"
                lines.append(f"{priority_icon} [{action['category']}] {action['task']}")
                lines.append(f"   💡 {action['action']}")
                lines.append("")

        lines.append("═" * 70)
        lines.append("祝你本週好運！🍀")
        lines.append("═" * 70)

        return "\n".join(lines)

    def save_report(self, report: Dict, output_dir: str = None):
        """
        儲存報告到檔案

        Args:
            report: 報告字典
            output_dir: 輸出目錄
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "reports"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 儲存 JSON
        json_file = output_dir / f"report_week_{report['week']}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # 儲存文字報告
        txt_file = output_dir / f"report_week_{report['week']}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(self.format_report_text(report))

        print(f"✅ 報告已儲存:")
        print(f"   JSON: {json_file}")
        print(f"   TXT: {txt_file}")


# 自動化排程範例
def setup_weekly_automation():
    """
    設定週報告自動化

    可以使用 crontab 或 schedule 套件定期執行
    """
    print("設定週報告自動化...")
    print()
    print("方法 1: 使用 crontab (macOS/Linux)")
    print("  執行: crontab -e")
    print("  加入: 0 8 * * 1 cd /path/to/project && python3 generate_weekly_report.py")
    print("  (每週一早上 8 點執行)")
    print()
    print("方法 2: 使用 schedule 套件")
    print("  pip install schedule")
    print("  然後運行背景服務")
    print()
    print("方法 3: 手動執行")
    print("  python3 generate_weekly_report.py")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print(" 自動化週報告系統")
    print("=" * 70)
    print()
    setup_weekly_automation()
