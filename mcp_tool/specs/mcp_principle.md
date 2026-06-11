# MCP 核心原則

> 本文件定義測試生成時的核心規則與分層設計。
> AI 必須遵守本文件，但行為流程以 agent.md 為準。
> 本文件僅定義規則，不定義流程。

---

## 優先順序（強制）

1. framework_spec.md（最高優先）
2. locator_spec.md
3. testcase.md

當規則衝突時：

- 必須直接捨棄低優先序內容
- 不得融合或自創折衷方案

---

## 分層規則（核心）

### TestCase

負責：

- 呼叫 Page
- 驗證結果

禁止：

- 使用 locator
- 使用 driver
- 使用 wait
- 定義 UI element

---

### Page

負責：

- 定義 locator
- 封裝 wait
- 回傳 Component

禁止：

- 撰寫 assert
- 撰寫測試流程
- 封裝業務流程（如 login / submit）

---

### Navigator

負責：

- 提供 Page 存取入口

規則：

- 單裝置：property
- 多裝置：*_mu(role)

---

## 單裝置 / 多裝置（強制）

### 單裝置

- Page 必須使用：

```python
def __init__(self):
````

* 不得傳入 role

---

### 多裝置

* Page 必須使用：

```python
def __init__(self, role=None):
```

* role 必須由 TestCase 決定
* Page 不得判斷 role

---

## Locator 原則（強制）

* 必須完全遵守 locator_spec.md
* 不得自行產生或推測 locator
* 只能使用 MCP 執行收集的結果

---

## 畫面判斷與 screenshot 規則（強制）

### 畫面判斷優先順序

1. locator（id / accessibility / UIAutomator）
2. page_source
3. screenshot（最後手段）

---

### screenshot 使用限制

- screenshot 僅可作為最後手段
- 不得在每一步操作後呼叫 screenshot
- 同一畫面最多只允許一次 screenshot
- 不可連續呼叫 screenshot
- 若已取得 page_source，不得再以 screenshot 作為主要判斷依據

---

### 錯誤處理（與 screenshot 相關）

- 若 element 查找失敗：
    - 不得直接重試 screenshot
    - 不得以 screenshot 取代畫面判斷
    - 必須重新確認畫面狀態（locator 或 page_source）

---

## 輸出物（不可缺）

必須產出：

1. Page
2. Navigator 更新
3. TestCase
4. locator JSON

---

## 錯誤處理（強制）

若發生以下情況，必須停止：

* testcase 無法唯一識別
* 測試資料不足
* 無法依 framework 正確產碼
* locator 資訊不足

回覆：

* 需要補充測試案例細節
  或
* 需要補充設定

---

## 規則一致性（強制）

* 所有規則必須來自 spec
* 不得在 prompt 重複定義規則
* 若 spec 未定義，必須停止，不得自行補充

---

## 多裝置 Phase 執行規則（強制）

### Phase 判斷

- 若 testcase 步驟中出現 `[PHASEn-ROLE]`，視為 multi_device phase testcase
- ROLE 不分大小寫，解析後一律轉小寫
    - OLD → old
    - NEW → new

---

### Phase 執行原則

1. 必須依 PHASE 編號順序執行（PHASE1 → PHASE2 → PHASE3）
2. 每次只允許執行一個 Phase
3. 每個 Phase 只能操作該 ROLE 對應裝置
4. 不得同時操作多個裝置（old / new）

---

### 多裝置 Session 規則

- Phase 間不得重啟 Appium session
- Phase 間不得 reset app
- Phase 間不得 close app
- Phase 間不得重新建立 driver

---

### Locator 規則（Phase）

- 多裝置 Phase 執行期間：
    - locator 僅允許在執行過程中累積（記憶 / context）
    - 不得在 Phase 結束時寫入 JSON 檔案
    - 不得產生任何中間 locator 檔案（包含 locator_phaseX.json）

- 所有 Phase 完成後：
    - 必須一次性將所有 locator 寫入：
      mcp_tool/locator/locator_output.json

- 禁止行為：
    - 禁止在 Phase 結束時寫入 locator_output.json
    - 禁止先建立 phase locator 再合併
    - 禁止分段寫入 JSON

---

### Phase 停止機制

每個 Phase 完成後，必須：

1. 停止執行
2. 回報已完成 Phase
3. 詢問 user 是否繼續

---

### TestCase 產出規則

- 所有 Phase 完成前：
    - 禁止產生 TestCase
- 所有 Phase 完成後：
    - 產生一份完整 TestCase