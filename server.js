/**
 * 蛇星刁手 Fantasy Basketball Data Center - Static Server
 * 提供 JSON 數據和靜態網頁服務
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8080;

// 中間件
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// 健康檢查
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'snakestar-basketball-data-center',
        league: '蛇星刁手',
        timestamp: new Date().toISOString()
    });
});

// API 端點：獲取聯盟數據
app.get('/api/league-data', (req, res) => {
    try {
        const dataPath = path.join(__dirname, 'data', 'full_league_data.json');

        if (!fs.existsSync(dataPath)) {
            return res.status(404).json({
                error: 'League data not found',
                message: '數據檔案不存在，請先執行數據同步'
            });
        }

        const data = fs.readFileSync(dataPath, 'utf8');
        const leagueData = JSON.parse(data);

        res.json({
            success: true,
            data: leagueData,
            last_updated: leagueData.last_updated
        });
    } catch (error) {
        console.error('Error loading league data:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// API 端點：獲取特定隊伍的陣容
app.get('/api/roster/:teamId', (req, res) => {
    try {
        const { teamId } = req.params;
        const dataPath = path.join(__dirname, 'data', 'full_league_data.json');

        const data = fs.readFileSync(dataPath, 'utf8');
        const leagueData = JSON.parse(data);

        const roster = leagueData.rosters[teamId];
        const team = leagueData.teams.find(t => t.team_id == teamId);

        if (!roster || !team) {
            return res.status(404).json({
                error: 'Team not found',
                message: `找不到 Team ID: ${teamId}`
            });
        }

        res.json({
            success: true,
            team: team,
            roster: roster
        });
    } catch (error) {
        console.error('Error loading roster:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// 主頁面
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 404 處理
app.use((req, res) => {
    res.status(404).json({
        error: 'Not Found',
        message: '端點不存在'
    });
});

// 錯誤處理
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({
        error: 'Internal Server Error',
        message: err.message
    });
});

// 啟動服務器
app.listen(PORT, () => {
    console.log('='.repeat(80));
    console.log(' 蛇星刁手 Fantasy Basketball Data Center - Server Started');
    console.log('='.repeat(80));
    console.log(`\n🚀 Server running on port ${PORT}`);
    console.log(`📊 Main page: http://localhost:${PORT}`);
    console.log(`🔍 Health check: http://localhost:${PORT}/health`);
    console.log(`📡 API endpoint: http://localhost:${PORT}/api/league-data`);
    console.log('\n' + '='.repeat(80) + '\n');
});

module.exports = app;
