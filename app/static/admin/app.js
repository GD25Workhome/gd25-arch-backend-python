// 管理后台应用主逻辑

// API 基础 URL
const API_BASE = '/api/v1';

// 当前页面状态
let currentPage = 'overview';
let currentUserPage = 1;
let currentUserPageSize = 10;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadOverview();
});

// 初始化导航
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const page = btn.dataset.page;
            switchPage(page);
        });
    });
}

// 切换页面
function switchPage(page) {
    // 更新导航按钮状态
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.page === page);
    });

    // 更新页面显示
    document.querySelectorAll('.page').forEach(p => {
        p.classList.toggle('active', p.id === `page-${page}`);
    });

    currentPage = page;

    // 加载对应页面数据
    switch (page) {
        case 'overview':
            loadOverview();
            break;
        case 'users':
            loadUsers();
            break;
        case 'system':
            loadSystemInfo();
            break;
        case 'database':
            loadDatabaseInfo();
            break;
    }
}

// 加载系统概览
async function loadOverview() {
    try {
        // 加载健康状态
        const healthRes = await fetch(`${API_BASE}/admin/system/health`);
        const healthData = await healthRes.json();
        if (healthData.code === 200) {
            displayHealthStatus(healthData.data);
        }

        // 加载统计信息
        const statsRes = await fetch(`${API_BASE}/admin/stats/overview`);
        const statsData = await statsRes.json();
        if (statsData.code === 200) {
            displayStats(statsData.data);
        }

        // 加载系统信息
        const infoRes = await fetch(`${API_BASE}/admin/system/info`);
        const infoData = await infoRes.json();
        if (infoData.code === 200) {
            document.getElementById('app-name').textContent = infoData.data.app_name;
            document.getElementById('app-version').textContent = `v${infoData.data.version}`;
            document.getElementById('stat-environment').textContent = infoData.data.environment;
        }
    } catch (error) {
        console.error('加载概览数据失败:', error);
        showToast('加载数据失败', 'error');
    }
}

// 显示健康状态
function displayHealthStatus(data) {
    const container = document.getElementById('health-status');
    const statusClass = data.status === 'healthy' ? 'healthy' : 'unhealthy';
    const dbStatus = data.database?.status || 'unknown';
    const dbHealthy = data.database?.healthy || false;

    container.innerHTML = `
        <div class="status-badge ${statusClass}">
            <span class="status-dot"></span>
            <span>系统状态: ${data.status === 'healthy' ? '健康' : '异常'}</span>
        </div>
        <div class="status-badge ${dbHealthy ? 'healthy' : 'unhealthy'}">
            <span class="status-dot"></span>
            <span>数据库: ${dbStatus === 'connected' ? '已连接' : '未连接'}</span>
        </div>
    `;
}

// 显示统计信息
function displayStats(data) {
    document.getElementById('stat-users-total').textContent = data.users?.total || 0;
    document.getElementById('stat-users-active').textContent = data.users?.active || 0;
    document.getElementById('stat-db-status').textContent = data.database?.connected ? '已连接' : '未连接';
}

// 加载用户列表
async function loadUsers(page = 1, pageSize = 10) {
    try {
        const url = `${API_BASE}/users?page=${page}&page_size=${pageSize}`;
        const res = await fetch(url);
        const data = await res.json();

        if (data.code === 200) {
            displayUsers(data.data);
            displayPagination(data.data, 'users');
            currentUserPage = page;
        } else {
            showToast('加载用户列表失败', 'error');
        }
    } catch (error) {
        console.error('加载用户列表失败:', error);
        showToast('加载用户列表失败', 'error');
    }
}

// 显示用户列表
function displayUsers(data) {
    const tbody = document.getElementById('users-table-body');
    
    if (!data.items || data.items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="loading">暂无用户数据</td></tr>';
        return;
    }

    tbody.innerHTML = data.items.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${escapeHtml(user.username || '-')}</td>
            <td>${escapeHtml(user.email || '-')}</td>
            <td>
                <span class="status-badge ${user.is_active ? 'healthy' : 'unhealthy'}">
                    ${user.is_active ? '激活' : '未激活'}
                </span>
            </td>
            <td>${formatDate(user.created_at)}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteUser(${user.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

// 显示分页
function displayPagination(data, type) {
    if (type === 'users') {
        const pagination = document.getElementById('users-pagination');
        if (!data.has_next && !data.has_prev) {
            pagination.innerHTML = '';
            return;
        }

        pagination.innerHTML = `
            <button class="pagination-btn" ${!data.has_prev ? 'disabled' : ''} 
                    onclick="loadUsers(${data.page - 1}, ${data.page_size})">上一页</button>
            <span>第 ${data.page} / ${data.total_pages} 页（共 ${data.total} 条）</span>
            <button class="pagination-btn" ${!data.has_next ? 'disabled' : ''} 
                    onclick="loadUsers(${data.page + 1}, ${data.page_size})">下一页</button>
        `;
    }
}

// 删除用户
async function deleteUser(userId) {
    if (!confirm('确定要删除这个用户吗？')) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/users/${userId}`, {
            method: 'DELETE'
        });
        const data = await res.json();

        if (data.code === 200) {
            showToast('用户删除成功', 'success');
            loadUsers(currentUserPage, currentUserPageSize);
        } else {
            showToast(data.message || '删除失败', 'error');
        }
    } catch (error) {
        console.error('删除用户失败:', error);
        showToast('删除用户失败', 'error');
    }
}

// 加载系统信息
async function loadSystemInfo() {
    try {
        // 加载基本信息
        const infoRes = await fetch(`${API_BASE}/admin/system/info`);
        const infoData = await infoRes.json();
        if (infoData.code === 200) {
            displaySystemInfo(infoData.data);
        }

        // 加载配置信息
        const configRes = await fetch(`${API_BASE}/admin/config/info`);
        const configData = await configRes.json();
        if (configData.code === 200) {
            displayConfigInfo(configData.data);
        }
    } catch (error) {
        console.error('加载系统信息失败:', error);
        showToast('加载系统信息失败', 'error');
    }
}

// 显示系统信息
function displaySystemInfo(data) {
    const grid = document.getElementById('system-info-grid');
    grid.innerHTML = `
        <div class="info-item">
            <div class="info-label">应用名称</div>
            <div class="info-value">${escapeHtml(data.app_name)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">版本</div>
            <div class="info-value">${escapeHtml(data.version)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">运行环境</div>
            <div class="info-value">${escapeHtml(data.environment)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">调试模式</div>
            <div class="info-value">${data.debug ? '开启' : '关闭'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">主机</div>
            <div class="info-value">${escapeHtml(data.host)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">端口</div>
            <div class="info-value">${data.port}</div>
        </div>
        <div class="info-item">
            <div class="info-label">日志级别</div>
            <div class="info-value">${escapeHtml(data.log_level)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">日志格式</div>
            <div class="info-value">${escapeHtml(data.log_format)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">当前时间</div>
            <div class="info-value">${formatDate(data.current_time)}</div>
        </div>
    `;
}

// 显示配置信息
function displayConfigInfo(data) {
    const grid = document.getElementById('config-info-grid');
    grid.innerHTML = `
        <div class="info-item">
            <div class="info-label">数据库 URL</div>
            <div class="info-value">${escapeHtml(data.database_url || '未配置')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Redis URL</div>
            <div class="info-value">${escapeHtml(data.redis_url || '未配置')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Celery Broker</div>
            <div class="info-value">${escapeHtml(data.celery_broker_url || '未配置')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Flower 端口</div>
            <div class="info-value">${data.flower_port || '-'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Flower 认证</div>
            <div class="info-value">${data.has_flower_auth ? '已配置' : '未配置'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">CORS 源</div>
            <div class="info-value">${data.cors_origins?.join(', ') || '-'}</div>
        </div>
    `;
}

// 加载数据库信息
async function loadDatabaseInfo() {
    try {
        // 加载连接状态
        const healthRes = await fetch(`${API_BASE}/admin/system/health`);
        const healthData = await healthRes.json();
        if (healthData.code === 200) {
            displayDatabaseInfo(healthData.data);
        }

        // 加载统计信息
        const statsRes = await fetch(`${API_BASE}/admin/database/stats`);
        const statsData = await statsRes.json();
        if (statsData.code === 200) {
            displayDatabaseStats(statsData.data);
        }
    } catch (error) {
        console.error('加载数据库信息失败:', error);
        showToast('加载数据库信息失败', 'error');
    }
}

// 显示数据库信息
function displayDatabaseInfo(data) {
    const grid = document.getElementById('database-info-grid');
    const dbData = data.database || {};
    
    grid.innerHTML = `
        <div class="info-item">
            <div class="info-label">连接状态</div>
            <div class="info-value">
                <span class="status-badge ${dbData.healthy ? 'healthy' : 'unhealthy'}">
                    <span class="status-dot"></span>
                    ${dbData.status === 'connected' ? '已连接' : dbData.status || '未知'}
                </span>
            </div>
        </div>
        ${dbData.error ? `
        <div class="info-item">
            <div class="info-label">错误信息</div>
            <div class="info-value" style="color: var(--danger-color);">${escapeHtml(dbData.error)}</div>
        </div>
        ` : ''}
    `;
}

// 显示数据库统计
function displayDatabaseStats(data) {
    const grid = document.getElementById('database-stats-grid');
    grid.innerHTML = `
        <div class="info-item">
            <div class="info-label">连接状态</div>
            <div class="info-value">${data.connected ? '已连接' : '未连接'}</div>
        </div>
        <div class="info-item">
            <div class="info-label">数据库类型</div>
            <div class="info-value">${escapeHtml(data.database_type || '未知')}</div>
        </div>
        <div class="info-item">
            <div class="info-label">表数量</div>
            <div class="info-value">${data.tables_count || 0}</div>
        </div>
        ${data.error ? `
        <div class="info-item">
            <div class="info-label">错误信息</div>
            <div class="info-value" style="color: var(--danger-color);">${escapeHtml(data.error)}</div>
        </div>
        ` : ''}
    `;
}

// 工具函数：转义 HTML
function escapeHtml(text) {
    if (text == null) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 工具函数：格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    try {
        const date = new Date(dateString);
        return date.toLocaleString('zh-CN');
    } catch (e) {
        return dateString;
    }
}

// 显示 Toast 消息
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// 用户搜索
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('user-search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const keyword = e.target.value.trim();
            if (keyword.length > 0) {
                searchTimeout = setTimeout(() => {
                    searchUsers(keyword);
                }, 500);
            } else {
                loadUsers();
            }
        });
    }

    // 刷新按钮
    const refreshBtn = document.getElementById('btn-refresh-users');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            loadUsers(currentUserPage, currentUserPageSize);
        });
    }
});

// 搜索用户
async function searchUsers(keyword) {
    try {
        const url = `${API_BASE}/users/search?keyword=${encodeURIComponent(keyword)}&page=1&page_size=${currentUserPageSize}`;
        const res = await fetch(url);
        const data = await res.json();

        if (data.code === 200) {
            displayUsers(data.data);
            displayPagination(data.data, 'users');
        } else {
            showToast('搜索用户失败', 'error');
        }
    } catch (error) {
        console.error('搜索用户失败:', error);
        showToast('搜索用户失败', 'error');
    }
}

// 导出函数供全局使用
window.loadUsers = loadUsers;
window.deleteUser = deleteUser;
