# Appium 元素定位規範 v1.1

* 一律依「定位優先順序」選擇定位策略
* 能不用 XPath 就不得使用 XPath
* XPath 僅允許作為最後手段
* 嚴禁 index 型 XPath（如 `EditText[1]`）
* 回覆內容 **只能輸出 JSON，不得夾帶任何說明文字**
* 輸出的 JSON 必須為合法格式（不可多段 JSON 拼接）

#### 輸出格式鎖定（強制）

- locator_spec.md 僅用於規範「定位策略與 selector 撰寫方式」，不得影響最終輸出格式。
- 最終輸出格式必須完全符合「Appium 元素定位規範 v1.1」所定義的 JSON 結構。
- locator_spec.md 不得定義、修改或簡化 JSON 結構（例如不可輸出 { "<頁面>": [...] } 形式）。
- locator_spec.md 不得定義輸出檔名、輸出路徑或寫檔時機，僅遵循 v1.1 規範第 9 章。

---

## 1. 定位優先順序（必須遵守）

### 1.1 iOS（由高到低）

1. accessibility id（accessibilityIdentifier）
2. iOS Class Chain
3. iOS Predicate
4. name / id（僅限非顯示文字）
5. XPath（最後手段）

### 1.2 Android（由高到低）

1. accessibility id（content-desc）
2. resource-id（AppiumBy.ID）
3. Android UIAutomator
4. XPath（最後手段）

---

## 2. XPath 強制規範（違反即錯）

### 2.1 禁止寫法（嚴禁）

以下為禁止寫法範例：

```xpath
//android.widget.EditText[1]

//XCUIElementTypeTextField[2]
```

* 任何僅使用「class + index」的 XPath 一律禁止

---

### 2.2 強制寫法規則（必須）

* XPath **必須使用「Anchor + 相對定位」**
* Anchor 僅能為：

    * 標題
    * label
    * 描述文字
* 必須限制搜尋範圍：

    * 同容器優先
    * 優先使用 `parent::`、`following-sibling::`
* 若元素已有 accessibility id / resource-id，仍使用 XPath 視為錯誤
* 使用 XPath 時，`note` 欄位 **必須說明原因**

---

### 2.3 標準 XPath 範例（必須遵循）

#### Android

```xpath
//*[contains(@text,"使用者密碼")]
  /parent::*
  //android.widget.EditText
```

#### iOS

```xpath
//XCUIElementTypeStaticText[@name="使用者密碼"]
  /parent::*
  //XCUIElementTypeSecureTextField
```

---

## 3. name 命名規範（用途型中文，必須遵守）

* `name` 必須為：`<動作 / 用途><元件類型>`

### 3.1 範例

* 登入按鈕
* 返回按鈕
* 企業戶ID輸入框
* 密碼輸入框
* 錯誤提示文字
* Slogan文字
* 畫面提示文字
* 標題文字

### 3.2 禁止事項

* 程式命名（如 `userNameTextView`）
* 英文命名
* 無用途的直譯名稱 ( 如：`文字1`、`按鈕A`)

---

## 4. 任務輸出規格（必須）

### 4.1 輸入內容

每個元素至少包含：

* 頁面名稱（page）
* 元素用途描述
* 可能的錨點文字（僅 XPath 使用）

### 4.2 輸出內容

* 必須為每個元素產出對應的 locator
* locator 必須依「頁面（page）」分組
* 除 JSON 外，不得輸出任何文字

### 4.3 多頁累積輸出規則（強制）

- 測試流程中，每當進入一個新的 page，必須產出該 page 的完整 locator 清單。
- 多個 page 的 locator 必須「累積」輸出至同一份 JSON，不得清空或覆蓋先前 page 的結果。
- `pages[pageName]` 不存在時才建立；已存在時必須 append 或 merge。
- 最終寫檔內容必須包含「所有已執行 page」的 locator 結果。

### 4.4 pageName 來源與唯一性（強制）

- pageName 必須為穩定且具唯一性的畫面名稱（例如：登入頁、總覽頁、明細頁）。
- 同一測試流程中，不同畫面不得使用相同 pageName，避免 pages key 被覆蓋。
- 若無法由 App 自動判斷 pageName，必須以 testcase.md 中定義的頁面名稱為準。


---

## 5. 輸出格式

### 5.1 結構規則

* 最外層為 JSON Object
* 第一層固定 Key：platforms
* 第二層 Key：Android / iOS
* 第三層固定 Key：pages
* 第四層 Key：頁面名稱（page）
* 第五層 Value：locator 陣列

**規則**：platform 不再出現在 locator 內，平台由結構本身表示。

### 5.2 locator 必備欄位

* `name`：用途型中文
* `strategy`：**必須使用 AppiumBy.XXX（禁止 By.ID、By.XPATH）**
* `selector`：字串
* `note`：XPath 原因（無則空字串）
* `validation`：執行期驗證結果

---

### 5.3 JSON Schema（概念）

```json
{
  "platforms": {
    "Android": {
      "pages": {
        "<頁面名稱>": [
          {
            "name": "<用途型中文>",
            "strategy": "AppiumBy.XXX",
            "selector": "<字串>",
            "note": "",
            "validation": {}
          }
        ]
      }
    },
    "iOS": {
      "pages": {
        "<頁面名稱>": [
          {
            "name": "<用途型中文>",
            "strategy": "AppiumBy.XXX",
            "selector": "<字串>",
            "note": "",
            "validation": {}
          }
        ]
      }
    }
  }
}

```

---

## 6. 執行期元素驗證（Runtime Validation，必須）

### 6.1 驗證時機（明確）

* 進入 page 時：驗證該 page 內 **所有 locator**
* 測試步驟執行後：驗證目前所在 page
* 不得跨 page 驗證
* **不得只驗證有被測試案例操作的元素**
* **不得跨平台驗證**（Android 測試時不得驗 iOS 區塊，反之亦然）

### 6.2 驗證項目（全部必做）

* `found_count`：使用 locator 找到的元素數量
* `is_visible`：是否 displayed
* `is_enabled`：是否 enabled
* `value`：是否可讀取文字

### 6.3 可互動元件額外驗證

* `is_clickable`：

    * 不得實際 click
    * 判定規則：`is_visible && is_enabled`

### 6.4 驗證狀態判定

* `found_count == 0` → **FAIL**
* `found_count > 1` → **WARN**
* 使用 XPath：

    * `note` 必須非空
* 若 FAIL，`validation.error` 必須填寫原因

---

## 7. 文字取值規則（必須）

### 7.1 Android（依序嘗試）

1. `element.text`
2. `get_attribute("text")`
3. `get_attribute("content-desc")`
4. `get_attribute("resource-id")`（僅記錄用）

### 7.2 iOS（依序嘗試）

1. `get_attribute("value")`
2. `get_attribute("label")`
3. `get_attribute("name")`
4. `element.text`

---

## 8. 回填輸出格式（必須）

* MCP 最終輸出仍為「page 分組」JSON
* 每個 locator **必須新增 `validation` 欄位**

### 8.1 validation 欄位結構（固定）

* `status`：PASS | WARN | FAIL
* `found_count`：number
* `is_visible`：boolean
* `is_enabled`：boolean
* `is_clickable`：boolean
* `value`：{ "source": "text|value|label|name|attr", "text": "<string>" }
* `actions`：[]（未操作也必須存在；有操作則紀錄如 ["click"]）
* `error`：string
  *規則*：所有 locator 都必須回填 validation，即使未做任何動作也必須產生結果（actions 為空陣列）。

---

### 8.2 回填範例

```json

{
  "platforms": {
    "Android": {
      "pages": {
        "登入頁": [
          {
            "name": "登入企網銀按鈕",
            "strategy": "AppiumBy.ACCESSIBILITY_ID",
            "selector": "登入企網銀",
            "note": "",
            "validation": {
              "status": "PASS",
              "found_count": 1,
              "is_visible": true,
              "is_enabled": true,
              "is_clickable": true,
              "value": {
                "source": "text",
                "text": "登入企網銀"
              },
              "actions": [],
              "error": ""
            }
          }
        ]
      }
    }
  }
}

```

---

## 9. 輸出檔案（必須）
> 所有路徑皆以「專案根目錄（repo root）」為基準。
> 禁止寫死專案名稱（例如 mobile-framework）。

### 檔案名稱
`locator_output.json`

### 輸出路徑
`mcp_tool/locator/`

### 完整路徑
`mcp_tool/locator/locator_output.json`

### 規則

- MCP / Copilot 每次執行 locator 擷取時 **只允許產出一個 JSON 檔案**
- 若檔案已存在，必須 **覆蓋舊檔**
- 檔案內容必須與回覆 JSON **完全一致**
- **禁止產生多個 locator JSON**
---

## 10. 判錯規則（強制）

* 未依定位優先順序選策略 = 錯誤
* XPath 未使用 Anchor + 相對定位 = 錯誤
* 出現 index 型 XPath = 錯誤
* 有 accessibility id / resource-id 卻使用 XPath = 錯誤
* 任一 locator 缺少 `validation` = 錯誤


### 10.1 結構相關

* 缺少 `platforms` 或 `pages` = 錯誤
* `platforms` 下缺少 Android / iOS（應有至少一個）= 錯誤
* locator 內出現 `platform `欄位 = 錯誤
* JSON 非合法格式 = 錯誤
* JSON 以外出現任何文字 = 錯誤

### 10.2 validation 相關

* 任一 locator 缺少 `validation` 欄位 = 錯誤
* `validation.actions` 未提供或不是陣列 = 錯誤
* 使用 XPath 但 `note` 為空 = 錯誤
* 使用 XPath 且 `validation.status` 為 **FAIL**，但 `validation.error` 為**空** = 錯誤

---