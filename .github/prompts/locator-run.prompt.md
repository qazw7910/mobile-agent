---
description: 使用 MCP 在裝置上執行 testcase 並收集 locator
---

platform: {platform}
capabilities: {capabilities}
testcase: {testcase}

請依既有規範執行 testcase，並收集 locator。
---

## 多裝置 Phase 執行限制

若 testcase 步驟中包含 `[PHASEn-ROLE]`：

- Agent 必須依 Phase 編號順序解析目前尚未完成的第一個 Phase。
- 每次只允許執行一個 Phase。
- 僅執行目前 Phase 的步驟。
- 僅操作目前 Phase 標記的 ROLE 裝置。
- ROLE 不分大小寫，解析後一律轉小寫。
- 不得執行其他 Phase。
- 不得同時操作其他裝置。
- Phase 完成後必須停止。
- Phase 完成後詢問 user 是否繼續下一個 Phase。
- 所有 Phase 完成前，不得產生測試腳本。

---

## Locator 累積規則

- 多裝置 Phase 執行期間：

  - locator 僅允許在執行過程中累積（context 中保存）
  - 不得寫入任何 JSON 檔案
  - 不得產生 locator_phaseX.json
  - 不得寫入 locator_output.json

- 所有 Phase 完成後：

  - 才允許輸出：

    mcp_tool/locator/locator_output.json

- 禁止：

  - Phase 結束即寫 JSON
  - 分段寫入 JSON
  - 建立任何暫存 locator JSON
---

## 執行要求（強制）

### 畫面判斷順序

- 優先使用 locator（id / accessibility / UIAutomator）
- 次選 page_source
- screenshot 僅作為最後手段

---

### screenshot 使用規則

- 不得在每一步操作後呼叫 screenshot
- 同一畫面最多只允許一次 screenshot
- 不可連續呼叫 screenshot
- 若已取得 page_source，不可再使用 screenshot 判斷畫面

---

### 元素查找規則

- 進入新畫面後，必須先等待畫面穩定
- 不可使用 wait=0
- 必須依 locator_spec.md 優先順序查找元素

---

### 查找失敗處理

- 若 element 找不到：
- 不得直接重試
- 不得立即呼叫 screenshot
- 必須重新判斷畫面（locator 或 page_source）

---

### 禁止行為

- 不得以 screenshot 作為主要流程判斷
- 不得連續 screenshot
- 不得暴力重試（find → screenshot → find）
- 不得跳過等待直接操作

---

限制：

- 僅可使用 MCP 執行取得的資訊
- 不得自行推測 locator

禁止輸出：

- planning
- reasoning
- 說明文字
