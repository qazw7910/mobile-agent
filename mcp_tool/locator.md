# Appium 元素定位規範（必須遵守）

- 一律依「定位優先順序」選擇定位策略
- 能不用 XPath 就不得使用 XPath
- XPath 僅允許作為最後手段
- 嚴禁 index 型 XPath（如 `EditText[1]`）
- 回覆內容 只能輸出 JSON，不得夾帶說明文字
- 輸出的 JSON 必須為合法格式（不可多段 JSON 拼接）

---

# 1. 定位優先順序（必須遵守）

## iOS（由高到低）
1. accessibility id（accessibilityIdentifier）
2. iOS Class Chain
3. iOS Predicate
4. name / id（僅限非顯示文字）
5. XPath（最後手段）

## Android（由高到低）
1. accessibility id（content-desc）
2. resource-id（AppiumBy.ID）
3. Android UIAutomator
4. XPath（最後手段）

---

# 2. XPath 強制規範（違反即錯）

## 2.1 禁止寫法（嚴禁）
以下為禁止寫法範例：
```
//android.widget.EditText[1]

//XCUIElementTypeTextField[2]
```
- 任何僅使用「class + index」的 XPath 都禁止。

## 2.2 強制寫法規則（必須）
- XPath 必須使用「Anchor + 相對定位」
- Anchor 必須為：
  - 標題
  - label
  - 描述文字
- 必須限制搜尋範圍：
  - 同容器優先
  - 優先使用 `parent::`、`following-sibling::`
- 若元素已有 accessibility id / resource-id，仍使用 XPath 視為錯誤
- 使用 XPath 時，`note` 欄位必須說明原因

## 2.3 標準 XPath 範例（必須遵循）

### Android 範例：
```
//*[contains(@text,"使用者密碼")]
  /parent::*
  //android.widget.EditText
```

### iOS 範例：
```
//XCUIElementTypeStaticText[@name="使用者密碼"]
  /parent::*
  //XCUIElementTypeSecureTextField
```

---

# 3. name 命名規範（用途型，必須遵守）

- name 必須為：`<動作 / 用途><元件類型>`
- 範例：
  - `登入按鈕`
  - `返回按鈕`
  - `企業戶ID輸入框`
  - `密碼輸入框`
  - `錯誤提示文字`
  - `Slogan文字`
  - `畫面提示文字`
  - `標題文字`
- 標題文字
- 禁止事項：
  - 程式命名（如 `userNameTextView`）
  - 英文
  - 無用途的直譯名稱

---

# 4. 任務輸出規格（必須）

## 4.1 輸入內容
你會取得測試執行所需的元素資訊，每個元素至少包含：
- 頁面名稱（page）
- 元素用途描述
- 可能的錨點文字（僅 XPath 使用）

## 4.2 輸出內容
- 必須為每個元素產出對應的 locator
- locator 必須依「頁面（page）」分組
- 除 JSON 外，不得輸出任何文字

---

# 5. 輸出格式

- 最外層為 JSON Object
- Key = 頁面名稱（page）
- Value = locator 陣列

每個 locator 必須包含：
- name：用途型中文
- platform：Android / iOS
- strategy 須使用 AppiumBy.XXX（禁止使用 By.ID、By.XPATH）
- selector：字串
- note：XPath 原因（無則空字串）

## 5.1 JSON Schema（概念）
```json
{
  "<頁面名稱>": [
    {
      "name": "<用途型中文>",
      "platform": "Android | iOS",
      "strategy": "AppiumBy.XXX",
      "selector": "<字串>",
      "note": ""
    }
  ]
}
```

## 5.2 輸出範例
```json
{
  "登入頁": [
    {
      "name": "登入企網銀按鈕",
      "platform": "Android",
      "strategy": "AppiumBy.ACCESSIBILITY_ID",
      "selector": "登入企網銀",
      "note": ""
    },
    {
      "name": "企業戶ID輸入框",
      "platform": "Android",
      "strategy": "AppiumBy.ID",
      "selector": "com.cathaybk.geb.cubuat:id/companyIdEditText",
      "note": ""
    }
  ],
  "總覽頁": [
    {
      "name": "登出按鈕",
      "platform": "Android",
      "strategy": "AppiumBy.ID",
      "selector": "com.cathaybk.geb.cubuat:id/logoutButton",
      "note": ""
    }
  ]
}
```

---

# 6. 輸出檔案（必須）

- 檔名：`locator_output_當前時間與日期.json`
- 路徑：`/mobile-framework/mcp_tool/locator/locator_output.json`
- 檔案內容必須與回覆 JSON 完全一致

---

# 7. 判錯規則（強制）

- 未依定位優先順序選擇策略 = 錯誤
- XPath 未使用 Anchor + 相對定位 = 錯誤
- 出現 index 型 XPath = 錯誤
- 有 accessibility id / resource-id 卻使用 XPath = 錯誤
- 回覆內容非合法 JSON = 錯誤
- JSON 以外出現任何文字 = 錯誤
- 任一 locator 缺少 `validation` 欄位 = 錯誤
- `validation.actions` 未提供（或不是陣列）= 錯誤




---
# 8. 執行期驗證（Runtime Validation，必須）
# 8. 元素驗證規範（必須）
在執行測試案例的每個步驟後（或每次切換 page 後），MCP 必須對「當前 page」的所有 locator 逐一驗證。

每個 locator 的驗證項目（全部必做）：
- found_count：使用 locator 查找元素數量
- is_visible：元素是否可見（displayed）
- is_enabled：元素是否 enabled
- readable_value：嘗試讀取元素可讀值（依平台採用不同來源）

額外驗證（僅針對按鈕類 / 可互動元件）：
- is_clickable：不得真的點擊（避免副作用），以 is_visible && is_enabled 視為 clickable 判斷

驗證結果判定規則：
- 若 found_count == 0 → 該元素驗證狀態為 FAIL
- 若 found_count > 1 → 該元素驗證狀態為 WARN（除非該元素明確允許多個，否則視為問題）
- 若使用 XPath：
  - note 必須非空
  - note 必須說明為何不能用 accessibility id / resource-id
- validation.status 若為 FAIL，validation.error 必須填寫原因

---

## 8.1 文字取值規則（必須）
Android 取值順序（依序嘗試，第一個非空即採用）：
1. element.text
2. get_attribute("text")
3. get_attribute("content-desc")
4. get_attribute("resource-id")（僅做記錄用，不視為文字內容）

iOS 取值順序（依序嘗試，第一個非空即採用）：
1. get_attribute("value")
2. get_attribute("label")
3. get_attribute("name")
4. element.text

說明：
- MCP 的「結合輸出」：在原本 locator 上回填 validation 欄位（見下節格式）。

---

# 9. 回填輸出格式（必須）
MCP 最終輸出仍為「page 分組」JSON（使用上方格式 B），每個 locator 物件新增 validation 欄位（不得改掉原欄位）。

validation 欄位格式（固定）：
- status: PASS | WARN | FAIL
- found_count: number
- is_visible: boolean
- is_enabled: boolean
- is_clickable: boolean（用 is_visible && is_enabled 計算，不實際 click）
- value: { "source": "text|value|label|name|attr", "text": "<string>" }
- error: string（失敗才填）
- timestamp: ISO8601（含時區）

## 9.1 回填範例（同一筆 locator 內含驗證結果）
```json
{
  "登入頁": [
    {
      "name": "登入企網銀按鈕",
      "platform": "Android",
      "strategy": "AppiumBy.ACCESSIBILITY_ID",
      "selector": "登入企網銀",
      "note": "",
      "validation": {
        "status": "PASS",
        "found_count": 1,
        "is_visible": true,
        "is_enabled": true,
        "is_clickable": true,
        "value": { "source": "text", "text": "登入企網銀" },
        "error": "",
        "timestamp": "2026-01-14T13:40:21+08:00"
      }
    }
  ]
}
```

---

# 10. 執行期輸出檔案（必須）
MCP 必須將「回填後的 JSON」存成檔案：
- 檔名：`locator_output_當前時間與日期.json`（例如 `locator_output_2026-01-14_13:14.json`）
- 路徑：`/mobile-framework/mcp_tool/locator/locator_output_當前時間與日期.json`
- 檔案內容必須與回覆 JSON 完全一致

---

# 附錄：注意事項總整理
- 所有 XPath 必須符合「Anchor + 相對定位」並限制範圍，且 note 欄位需說明理由
- 若元素可使用 accessibility id 或 resource-id，絕對不可使用 XPath；若仍使用 XPath 必須在 note 中說明「為何無法使用 accessibility id / resource-id」
- 執行期每次 page 切換或步驟後，必須對該 page 全部 locator 做驗證並回填 validation
- 所有輸出最終均為 JSON（頁面分組），且輸出檔案需存放於指定路徑，檔名依規定命名
