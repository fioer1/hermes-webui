# Hermes 双仓库同步指南

本文档记录 `Hermes Agent` 与 `Hermes WebUI` 在双机协作时的 Git 规则、远端角色和安全更新方式。目标是让这台机器与另一台机器上的人类开发者、AI 助手都能快速判断当前状态，避免把 fork、upstream 和软件 update 混在一起。

## 适用仓库

1. `Hermes Agent`
2. `Hermes WebUI`

两个仓库各自独立，必须跟踪各自的官方源头。

## 总原则

### 1. `origin` 是共享 fork

用于两台机器同步自己的定制。

### 2. `upstream` 是官方上游

用于吸收官方更新。

### 3. 两个仓库不要互相借分支策略

- `Hermes Agent` 主分支是 `main`
- `Hermes WebUI` 当前主分支是 `master`

### 4. 历史重写前必须先做备份

任何 `rebase`、`reset --hard`、`push --force-with-lease` 之前，先留备份分支。

## 仓库一：Hermes WebUI

### 仓库身份

- 本地目录：`G:\hermes-webui`
- 官方上游：`https://github.com/nesquena/hermes-webui.git`
- 个人 fork：`https://github.com/fioer1/hermes-webui.git`

### 远端角色

```bash
origin   = https://github.com/fioer1/hermes-webui.git
upstream = https://github.com/nesquena/hermes-webui.git
```

### 当前状态（记录于 2026-04-29）

该仓库已经完成历史整理：

- 原先存在断开的 `master` 历史
- 已创建备份：`backup/disconnected-master-2026-04-29`
- 已基于 `upstream/master` 重建干净主线
- 已把本地定制重新落在官方主线上
- 已推送到 `origin/master`

可用以下命令确认 `master` 仍然建立在官方主线上：

```bash
git merge-base --is-ancestor upstream/master master
```

### WebUI 的日常更新方式

```bash
git fetch upstream origin
git checkout master
git rebase upstream/master
git push --force-with-lease origin master
```

### 另一台机器如何安全同步 WebUI

如果没有本地未提交改动：

```bash
git fetch origin
git checkout master
git reset --hard origin/master
```

如果有本地修改：

1. 先提交或另建备份分支
2. 再执行 `reset --hard`

### WebUI 最小验证

至少跑这组回归测试：

```bash
python -m pytest tests/test_updates.py tests/test_pwa_manifest_sw.py tests/test_auto_title_setting.py tests/test_perf_fast_ui.py tests/test_prompt_cache_toggle.py -q
```

## 仓库二：Hermes Agent

### 仓库身份

- 本地目录：`G:\Hermes Agent`
- 官方上游：`https://github.com/NousResearch/hermes-agent.git`
- 个人 fork：`https://github.com/fioer1/hermes-agent.git`

### 远端角色

```bash
origin   = https://github.com/fioer1/hermes-agent.git
upstream = https://github.com/NousResearch/hermes-agent.git
```

### 当前状态（记录于 2026-04-29）

`Hermes Agent` 已完成远端角色调整，但主线还没有做最终历史收敛。

当时的状态是：

```bash
main...origin/main   => ahead 5, behind 8
main...upstream/main => ahead 5, behind 8
```

这表示：

- 远端结构已经清晰
- 但本地 `main` 仍然和官方主线分叉
- 另一台机器上的 AI 不应在没检查前直接 `git pull`

### 当前本地独有提交

```text
a29f95f0b Merge branch 'main' of https://github.com/NousResearch/hermes-agent
1b89ba839 chore: ignore pytest local artifacts
7a9ac1de1 chore: add remaining local artifacts
1aceb9bf5 fix: stabilize gateway, MCP, and hindsight behavior
c514aabcb fix(ACP): 修复 Windows 路径与本地 shell 兼容性
```

### Agent 仓库后续整理建议

1. 备份当前主线：

```bash
git checkout main
git branch backup/pre-clean-main-YYYY-MM-DD
```

2. 抓取最新远端：

```bash
git fetch upstream origin
```

3. 以 `upstream/main` 为底，重放真正要保留的本地提交  
推荐用 `rebase` 或新建清理分支后 `cherry-pick`。

4. 验证后再推到 fork：

```bash
git push --force-with-lease origin main
```

### Agent 仓库验证入口

优先使用仓库自带测试脚本：

```bash
scripts/run_tests.sh
```

## 双机协作规则

### 每次操作前先确认现场

```bash
git remote -v
git status --short --branch
```

如果要判断是否可以安全同步，再看：

```bash
git rev-list --left-right --count origin/<branch>...HEAD
git rev-list --left-right --count upstream/<branch>...HEAD
```

### 默认用 `--force-with-lease`

不要裸用 `--force`。

### 任何历史重写前先备份

建议命名：

```text
backup/<用途>-YYYY-MM-DD
```

### 软件 update 与 Git 工作区不要混着改

如果一个目录已经承担 Git 同步职责，就优先走 Git。  
如果一个目录主要承担“安装目录 / 软件运行目录”职责，就不要在上面堆长期源码定制。

## 给 AI 助手的直接指令

如果你是另一台机器上的 AI 助手，请按下面顺序操作：

1. 先读本文件
2. 再读当前仓库根目录下的 `AGENTS.md`
3. 运行：

```bash
git remote -v
git status --short --branch
```

4. 如果涉及同步，再运行：

```bash
git rev-list --left-right --count origin/<branch>...HEAD
git rev-list --left-right --count upstream/<branch>...HEAD
```

5. 没确认历史关系前，不要直接 `pull`
6. 没建备份分支前，不要直接改写历史

## 最后更新

- 更新时间：2026-04-29
- 更新人：OpenAI Codex
