<div align="center">

# 🌱 WorkBuddy Daily

**WorkBuddy 成长中心 · 全能签到脚本 · 单文件自包含**

🔐 Token 永续 · ✅ 35 项自动化任务 · 🏫 开学季活动 · 📱 小程序任务 · 🖥️ 桌面换血 · 🎮 8 项玩法 · 💰 三类查询 · 🎁 自动领奖 · 📊 全中文报告 · 📢 三渠道推送 · 🐧 青龙友好 · ☁️ GitHub Actions

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20%E9%9D%92%E9%BE%99-4EAA25?style=for-the-badge&logo=linux&logoColor=white" />
<img src="https://img.shields.io/badge/Deploy-%E9%9D%92%E9%BE%99%20%7C%20GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/Deps-requests%20only-A78BFA?style=for-the-badge&logo=pypi&logoColor=white" />
<img src="https://img.shields.io/badge/Self--contained-1%20file-FFC75F?style=for-the-badge&logo=files&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-F472B6?style=for-the-badge" />

</div>

---

## ✨ 这是什么

一个脚本搞定 **WorkBuddy 成长中心 + 开学季活动 + 小程序任务** 的全部自动化：**Token 自动续期 → 积分/用量/成长查询 → 18 项成长任务（17 全自动）→ 8 项互动玩法 → 5 项开学季任务 + 大转盘抽奖 → 5 项小程序任务 → 自动领奖 → 中文报告推送**，全流程无人值守，重复运行只补缺口、不重复领取。

> 🎯 一句话：**配一个刷新令牌，剩下交给它。**
>
> 📦 **单文件自包含**：无需任何配套模块（专家市场数据、推送通知全部内置），青龙上传一个 `workbuddy_daily.py` 即可运行。
>
> ☁️ **云端部署**：除了青龙，也支持直接跑在 **GitHub Actions** 上，零服务器、定时自动执行。

---

## 🚀 部署方式一：青龙面板（三步）

| 步骤 | 操作 |
| :---: | :--- |
| **1️⃣ 上传脚本** | 把 `workbuddy_daily.py` 放到脚本目录 |
| **2️⃣ 设置变量** | `WORKBUDDY_REFRESH_TOKEN` = 每行一个 `手机号:AT:RT`（多账号换行分隔） |
| **3️⃣ 定时任务** | 日常 `0 7,12 * * *` · 夜猫子窗口 `30 23 * * *`（**青龙用本地时间**） |

> 🌙 **为什么需要单独的夜猫定时？** 夜猫子任务只在 **23:00–08:00** 期间计入进度，且要求**真实对话**（不能指纹伪造）。
> 日常的 7 点、12 点都不在窗口内，所以必须有 `30 23 * * *` 这个专门的窗口定时，否则夜猫子永远跑不了。
>
> 📌 官方规则是「**每天 1 次 × 累计 3 天**」，脚本有响应即停，不会一晚空跑多次。

```bash
# 依赖（仅一个）
pip3 install requests
```

---

## ☁️ 部署方式二：GitHub Actions（零服务器 · 推荐）

> 本仓库已内置工作流 [`.github/workflows/workbuddy.yml`](.github/workflows/workbuddy.yml)，**Fork 或直接使用本仓库**即可开启云端定时签到。

### 第 1 步：添加 Secrets（仓库 → Settings → Secrets and variables → Actions）

| Secret 名称 | 必填 | 值 |
| :--- | :---: | :--- |
| `WORKBUDDY_REFRESH_TOKEN` | ✅ | 每行一个 `手机号:AT:RT`（多账号换行分隔） |
| `PUSHPLUS_TOKEN` | ⬜ | 可选，PushPlus 推送令牌 |
| `BARK_URL` | ⬜ | 可选，Bark 推送（iOS），如 `https://api.day.app/xxxxxxxx` |
| `WECOM_WEBHOOK` | ⬜ | 可选，企业微信群机器人 webhook（或仅 key） |

> 点 **New repository secret**，Name 填上面的名称，Secret 粘贴对应的值，保存。

### 第 2 步：开启 Actions
进入仓库 **Actions** 标签页，若提示需要启用，点 **I understand my workflows, go ahead and enable them**。

### 第 3 步：手动跑一次验证
Actions → 左侧选 **🌱 WorkBuddy Daily** → **Run workflow** → 选 `main` 分支 → 运行。看到 ✅ 即部署成功。

### 内置定时（北京时间）
| 时间 | UTC cron | 说明 |
| :---: | :---: | :--- |
| 07:00 | `0 23 * * *` | 日常全流程 |
| 12:00 | `0 4 * * *` | 日常全流程 |
| 23:30 | `30 15 * * *` | 夜猫子活动窗口 |

> 需要改时间，编辑 `workbuddy.yml` 里的 `cron`（**注意是 UTC，北京时间 − 8 小时**）。
>
> 🕐 工作流已设置 `TZ: Asia/Shanghai`——否则 runner 默认 UTC，会导致**日志时间显示错误**和**补签日期算错一天**。脚本内部也用 `beijing_now()` / `beijing_today()` 强制北京时间，双保险。

### ⚠️ 令牌状态与安全（重要）
- 脚本每次续期都会**轮换刷新令牌**并写入 `wb_refresh_tokens.json`。
- 工作流内置安全判断：**仅在「私有仓库」中**把 `wb_refresh_tokens.json` 提交回仓库；**公开仓库会自动跳过**，避免 RT 泄露。
- **强烈建议**：如果你 Fork 本仓库用于部署，**请把 Fork 后的仓库设为 Private**（Settings → General → 拉到底 → Change visibility → Private），这样令牌才能安全持久化，续期不中断。
- 若使用公开仓库，令牌不会持久化，**每次运行都依赖 `WORKBUDDY_REFRESH_TOKEN` 这个 Secret 提供最新 RT**——需自行保证其不过期。

---

## 🔐 登录工具：短信验证码获取 Token

> 没有 AT/RT？用这个工具**一条命令**拿到。

```bash
python workbuddy_login.py                    # 交互式登录（推荐）
python workbuddy_login.py 13800000000        # 指定手机号
python workbuddy_login.py 13800000000 123456 # 指定手机号+验证码（跳过等待）
python workbuddy_login.py --verify           # 登录后额外验证 RT 是否可用
```

**流程**：输入手机号 → 自动发送短信验证码 → 输入收到的验证码 → 服务端直接下发 Token → 输出 `手机号:AT:RT`。

```
╔══════════════════════════════════════════════╗
║ 🔐 WorkBuddy 短信验证码登录工具 (插件接口版)   ║
╚══════════════════════════════════════════════╝
[1/5] 准备登录...
  ✅ 目标: https://www.workbuddy.cn
[2/5] 发送短信验证码到 13800000000 ...
  ✅ 验证码已发送 (有效期 300 秒)
  📱 请输入收到的验证码: ******
[3/5] 提交登录...
  ✅ 登录成功!
[4/5] 解析凭据...
  ✅ 身份: 13800000000 | AT 过期: 2026-12-11 08:30
[5/5] 完成!

════════════════════════════════════════════════════════════
✅ 将下面的值追加到 WORKBUDDY_REFRESH_TOKEN 变量
════════════════════════════════════════════════════════════
13800000000:eyJhbGciOiJSUzI1NiIs...很长...:eyJhbGciOiJIUzUxMiIs...也很长...
════════════════════════════════════════════════════════════
📁 结果已保存到: wb_login_result.json
```

**输出**：结果同时保存到 `wb_login_result.json`（已被 `.gitignore` 屏蔽，不会提交）。

> 💡 拿到这行 `手机号:AT:RT` 后，直接粘贴到青龙的 `WORKBUDDY_REFRESH_TOKEN` 变量或 GitHub Secrets 即可，主脚本会自动续期、永不过期。
>
> 🛠️ **实现说明**：走官方**插件登录接口** `/v2/plugin/login/send-sms` 与 `/v2/plugin/login/token`，由服务端直接下发 `accessToken` / `refreshToken`，**不再解析 Keycloak 登录页表单**——这是解决"验证码正确却提示验证码错误"的关键。

---
## 🔑 如何获取变量值（首次必看）

> 从桌面端认证文件中取 `AT` 和 `RT`，拼成 `手机号:AT:RT`。

1. **安装并登录** WorkBuddy 桌面端
2. 用记事本打开下面这个文件（`AppData` 是隐藏文件夹，地址栏直接粘贴路径）：
   ```
   C:/Users/你的用户名/AppData/Local/CodeBuddyExtension/Data/Public/auth/workbuddy-desktop.info
   ```
3. 在文件里搜索 `accessToken` 和 `refreshToken`，各自后面跟一串 **`eyJ` 开头**的长字符串，那就是 **AT** 和 **RT**
4. 按格式拼一行，多账号写多行：
   ```
   1XXXXXXXXXX:eyJhbGciOiJSUzI1NiIs...很长...:eyJhbGciOiJIUzUxMiIs...也很长...
   ```

> ⚠️ AT 和 RT 之间用**英文冒号 `:`** 分隔；等号后面的引号不要带
> ⚠️ **RT 是你唯一的续期凭据，泄露了别人就能操作你的账号**

---

## ⌨️ 命令行参数

```bash
python workbuddy_daily.py                # 全流程：续期 → 查询 → 任务 → 开学季 → 领奖
python workbuddy_daily.py --refresh      # 仅刷新所有账号 Token
python workbuddy_daily.py --query        # 仅查询积分/用量/成长
python workbuddy_daily.py --no-desktop   # 跳过桌面任务（非 Windows 默认走指纹上报，此参数可彻底跳过）
python workbuddy_daily.py --no-school    # 跳过开学季活动
python workbuddy_daily.py --school-only  # 只跑开学季活动（不做成长中心任务）
python workbuddy_daily.py --only 3       # 只跑第 3 个账号
python workbuddy_daily.py --gap 2.0      # 写动作间隔秒数（默认 1.5，最低 1.0）
```

---

## 🔧 环境变量

| 变量 | 必填 | 说明 |
| :--- | :---: | :--- |
| `WORKBUDDY_REFRESH_TOKEN` | ✅ | 多账号刷新令牌，换行分隔，格式 `手机号:AT:RT`（AT 可留空）。首次运行自动生成 `wb_refresh_tokens.json` 并持续维护 |
| `PUSHPLUS_TOKEN` | ⬜ | 可选，内置 PushPlus 推送，运行结果推到微信 |
| `BARK_URL` | ⬜ | 可选，Bark 推送（iOS），如 `https://api.day.app/xxxxxxxx`（自建服务器换域名即可） |
| `WECOM_WEBHOOK` | ⬜ | 可选，企业微信群机器人。填完整 webhook URL，或只填 key（自动补全域名） |

---

## 📦 任务清单

> 总计 **37 项任务**（35 项全自动 + 2 项需人工），其中仅 1 项完全无法自动完成（公益捐款需真实转账）。
>
> 📌 另有 **微信公众号关注任务**（`wb_wechat_oa_subscribe_task`）——需真人扫码关注，脚本会检测并提示，不自动完成。

### ☁️ 成长中心任务（18 项 · 17 项全自动）

| # | 任务 | 说明 |
| :-: | :--- | :--- |
| 1 | 设计创意模式 | 造画布事件上报 |
| 2 | 探索优秀灵感 | playbook 事件上报 |
| 3 | 桌面端对话 | Windows 真实桌面 / 非 Windows 指纹上报（**无需真实桌面端**） |
| 4 | 尝鲜热门技能 | Windows 真实桌面 / 非 Windows 指纹上报（**无需真实桌面端**） |
| 5 | 体验资料库 | web 域点击事件 |
| 6 | 腾讯轻量云专家 | expert 事件上报 |
| 7 | 和平精英主题 | 主题切换 API + 遥测 |
| 8 | 发现应用 | Buddy 五连事件链 |
| 9 | 企鹅教师助手 | Buddy 五连事件链 |
| 10 | GLM-5.2模型对话 | 真实 AI 对话 |
| 11 | 和AI聊天5次 | 真实 AI 对话 |
| 12 | 夜猫子活动 | 真实对话 + 23:00-08:00 窗口 · **每日1次×累计3天** |
| 13 | 召唤3次专家团 | 真实团队对话 + 遥测 |
| 14 | 召唤5次专家 | expert 事件上报 |
| 15 | 使用5个模板 | 批量遥测上报 |
| 16 | 设置自动化任务 | automation 事件上报 |
| 17 | 领取Buddy | 领养链路（+300c+8e） |
| 18 | ~~公益专家~~ | ❌ **需真实捐款，脚本不做** |
| — | ~~工作台搭建师~~ | ⚠️ **服务端已下线**（脚本仍兼容，出现时会自动处理） |

### 🏫 开学季活动（5 项 · 4 项全自动 + 幸运大转盘）

| # | 任务 | 说明 |
| :-: | :--- | :--- |
| 1 | 分享活动给好友 | `share-complete` 点亮 |
| 2 | 与 AI 对话 3 次 | 小程序域事件上报 |
| 3 | 桌面端对话 1 次 | 桌面 6 连事件（copilot 域） |
| 4 | 召唤开学季专家 | BackToSchool 专家事件 |
| 5 | ~~学生认证~~ | ❌ 微信实名认证，人工环节 |

> 🔗 **专家任务**：召唤 4 事件链（点击 → 召唤 → 使用 → 对话），与官方小程序埋点同构。
>
> 🎰 **幸运大转盘**：查余额 → 循环抽奖到 0
> 奖品：6 积分 / 66 积分 / 瑞幸 15 元券 / KFC OK 餐券 / KFC 冰淇淋券 / 酷狗会员月卡

### 📱 小程序成长任务（5 项 · 全自动 · +800c+25e）

| # | 任务 | 奖励 | 说明 |
| :-: | :--- | :--- | :--- |
| 1 | `Sequential_Tasks_1` 完成 1 次对话 | +100 积分 +5 能量 | |
| 2 | `Sequential_Tasks_2` 选中专家并完成对话 | +200 积分 +5 能量 | mp 指纹 `expert_actual_use` |
| 3 | `Sequential_Tasks_3` 完成 5 次对话 | +300 积分 +5 能量 | 逐条累加，自动补差额 |
| 4 | `Sequential_Tasks_4` 创建 1 个定时任务 | +100 积分 +5 能量 | 复用桌面口径 automation 事件 |
| 5 | `school_season` 参与校园日有奖活动 | +100 积分 +5 能量 | 需 `activityId` |

> 🔗 Tasks_1~7 是**链式任务**：完成一环后次日零点解锁下一环（`task locked until <日期>`），脚本每次运行自动检测并推进。

> 💡 这三项需 `X-Client-Platform: miniprogram` 请求头才下发（查询/接受/领奖三处都要），脚本已自动处理。
> 💡 判据上报走小程序指纹头族（`X-Client-Platform: mp-weixin` + `X-Client-Product: workbuddy-mp`），对齐官方 appservice 埋点。

### 🎮 互动玩法（8 项）

抽奖 · 盲盒 · Buddy 信息 · 派猫猫旅行 · 连签兑换 · 补签卡 · 礼包补偿 · 徽章

### 🔹 其他

每日签到（`/v2/billing/meter/daily-checkin`，独立于成长任务，自动完成）

---

### 📊 汇总

| 分类 | 总数 | 全自动 | 人工/不可做 |
| :--- | :-: | :-: | :-: |
| 成长中心任务 | 18 | 17 | 1（公益专家，需捐款） |
| 开学季活动 | 5 | 4 | 1（学生认证，需实名） |
| 小程序任务 | 5 | 5 | 0 |
| 互动玩法 | 8 | 8 | 0 |
| 每日签到 | 1 | 1 | 0 |
| **合计** | **37** | **35** | **2** |

> ℹ️ 成长中心任务会随活动更新。脚本内置**未覆盖任务检测**：遇到没适配的新任务会在日志中明确提示。

---

## 🧠 智能特性

- **📊 全中文报告**：任务代码自动翻译成中文（如 `skill_1` → 尝鲜热门技能），每账号独立分块 + 总计 + 待办分布，一目了然。
- **🔍 未覆盖任务检测**：每次运行扫描成长任务列表，发现脚本尚未适配的新任务会打印 ⚠️ 提示，方便及时更新脚本。
- **♻️ 幂等补缺**：所有任务先查进度再执行，已完成 / 已领取直接跳过，重复运行零副作用。
- **⏰ 智能续期**：距上次刷新 > 10 天或 AT 7 天内过期才刷新，避免无谓轮换。
- **🔄 API 重试**：网络错误 / 5xx 自动指数退避重试 3 次；`--gap` 可调写动作间隔防频控。
- **🔗 稳定设备指纹**：每账号 md5 派生固定 machineId/sessionId，桌面事件指纹与真实客户端对齐。
- **📡 多域上报**：桌面域 + Web 域 + 小程序域三通道事件上报，完整覆盖所有任务类型。
- **📋 进度感知**：只上报缺口数量的事件，不重复提交已完成的进度。
- **✅ accept 双重校验**：解析接口逐任务状态 + 回读验证 + 未落账自动逐个重试（服务端存在「请求成功但未登记」的形态）。
- **🏫 开学季活动**：自动执行开学季限时任务（分享 / 对话 / 专家）+ 幸运大转盘抽奖。
- **🌙 夜猫子规则对齐**：官方为「每日 1 次 × 累计 3 天」，脚本有响应即停，不会一晚空跑多次。
- **🎁 自动补领奖**：扫描到 `completed` 但未领取的任务会自动补领，不会因中途异常漏掉奖励。
- **📱 小程序协议对齐**：四事件专家链（`expert_summon_click` → `expert_summoned` → `expert_actual_use` → `chat_request_send`）+ 小程序指纹头族，与官方小程序埋点一致。
- **📢 三渠道推送**：PushPlus（微信）+ Bark（iOS）+ 企业微信群机器人，可同时配置互不影响。
  企业微信只需一个 webhook（群设置 → 群机器人 → 添加 → 复制 URL）。

---

## ⚙️ 特别之处

- **📦 单文件自包含**：专家市场数据、PushPlus 推送全部内置，**无需任何外部模块**，部署零负担
- **☁️ 多云部署**：青龙面板 / GitHub Actions / 本地 Windows 均可运行
- **🏪 内置专家市场**：直接拉取专家团 / 普通专家 / 模板场景，网络异常时自动使用内置兜底数据
- **📊 全中文报告**：任务代码自动翻译为中文名称，每个账号独立分块 + 总计 + 待办分布
- **🔄 续期节奏**：距上次刷新 > 10 天 或 AT 7 天内过期 → 自动刷新（离线会话 30 天失效）
- **♻️ RT 轮换**：每次刷新都会换发新令牌并立即保存，形成**永续循环**
- **🖥️ 桌面换血**：自动备份并切换桌面端认证文件，跑完还原，全程无需人工
- **🧩 幂等安全**：重复运行只补缺口，不重复领取
- **📁 数据文件**：见下方「数据文件说明」
- **➕ 新增账号**：变量末尾追加一行 `手机号:AT:RT`，下次运行自动并入

---

## 🗂️ 数据文件说明

| 文件 | 说明 | 提交 |
| :--- | :--- | :---: |
| `wb_refresh_tokens.json` | 账号令牌库（RT / AT + 续期时间），**自动生成与维护** | ❌ 已屏蔽 |
| `WORKBUDDY_ACCESS_TOKEN.txt` | 由令牌库重建的 AT 文件（`@` 分隔） | ❌ 已屏蔽 |
| `wb_login_result.json` | `workbuddy_login.py` 登录结果（含真实 Token） | ❌ 已屏蔽 |
| `_meta.json` / `_skillhub_meta.json` | 桌面端技能本地元数据（`~/.workbuddy/skills`） | 仅本机 |
| `*.log` | 运行日志 | ❌ 已屏蔽 |

---

## 📊 推送报告示例

```
📊 各账号运行报告

👤 账号1  账号1
   💰 主套餐剩余980积分(共1000,已用20)
   📊 共12类资源，本月已使用3456次
   🌱 等级3 | 连签7天 | 能量120
   ⏳ 未完成: 桌面端对话、尝鲜热门技能

👤 账号2  账号2
   💰 主套餐剩余500积分(共1000,已用500)
   📊 共12类资源，本月已使用1200次
   🌱 等级5 | 连签30天 | 能量300
   ✅ 全部完成！

📊 ══ 总计 ══
👥 共2个账号，任务完成 34/36 项

   · 桌面端对话（1个账号待完成）
   · 尝鲜热门技能（1个账号待完成）

🕐 2026-09-12 07:05
```

---

## 📁 目录结构

```
WorkBuddy-Daily/
├── .github/
│   └── workflows/
│       └── workbuddy.yml    # GitHub Actions 定时工作流
├── workbuddy_daily.py       # 主脚本（签到/任务/玩法，单文件自包含）
├── workbuddy_login.py       # 登录工具（短信验证码换 Token）
├── requirements.txt         # 依赖（仅 requests）
├── .gitignore               # 屏蔽凭据/运行数据
├── LICENSE                  # MIT 许可证
└── README.md
```

---

## 🔒 隐私说明

脚本**不含任何账号、手机号、Token 或设备信息**，所有凭据均由环境变量（或 GitHub Secrets）注入。请妥善保管你的 `wb_refresh_tokens.json`、`WORKBUDDY_ACCESS_TOKEN.txt`、`wb_login_result.json`——这些文件均已被 `.gitignore` 屏蔽，**切勿手动提交**。

---

## ⚠️ 免责声明

本项目仅供 **学习与个人自动化** 使用。请遵守 WorkBuddy 服务条款，使用风险自负。

---

## 💬 反馈与贡献

遇到问题、有功能建议，或者发现了更好的实现方式，欢迎：

- 提交 [Issue](https://github.com/L0NE-6/WorkBuddy-Daily/issues) —— 报 bug、提需求
- 发起 [Pull Request](https://github.com/L0NE-6/WorkBuddy-Daily/pulls) —— 直接贡献代码

> 提 Issue 时如果能附上**运行日志**和**复现步骤**，定位会快很多 🙏

---

<div align="center">
  <sub>🌱 如果这个脚本帮到你，点个 <b>Star</b> 支持一下 ✨</sub>
</div>
