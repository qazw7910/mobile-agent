/// 2026-0310

# 自動化測試腳本撰寫指南

> 本文件描述自動化測試框架的架構與使用方式。
>
> 命名規則（Page / TestCase / Navigator page_key 等）由 `mcp_principle.md` 統一定義。
> 本文件中的示例若與 `mcp_principle.md` 衝突，應以 `mcp_principle.md` 為準。

## 專案架構概覽
> 所有路徑皆以「專案根目錄（repo root）」為基準。
> 文件中的目錄結構僅為相對路徑示意，不得寫死專案名稱（例如 mobile-framework）。

```

├── page/           # 頁面物件層 (Page Object)
├── module/         # 核心模組層
├── testcase/       # 測試案例層
├── framework/      # 框架工具層
└── data/          # 測試資料層
```

## 三層架構職責分工

### 1. Page 層 - 頁面元素定義
**職責：** 定義頁面元素與基本操作

**核心功能：**
- 元素定位器定義
- 基本元素操作封裝
- 頁面狀態檢查

**撰寫規範：**
```python
class LoginPage(BaseObject):
    def __init__(self):
        super().__init__()
        self.set_remark("GMB 登入頁")
        self.driver = DeviceManager.get_driver()
    
    def login_btn(self):
        return BasicComponent(
            lambda: WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, 'name == "登入"'))
            ),
            remark=f"{self.remark()} > 登入按鈕"
        )
```

**重點原則：**
- 每個元素都要有明確的 remark 說明
- 使用 BasicComponent 封裝元素操作
- 包含等待機制確保元素可操作
- 只定義元素與等待，不包含業務流程或測試流程方法

### 2. Navigator 層 - 業務流程導航
**職責：** 統一管理頁面物件與流程導航

**架構設計：**
```python
Navigator().ios.zh.login_page.login_btn().click()
```

**層級結構：**
- `Navigator` → 平台選擇 (`android`/`ios`)
- 平台 → 語言選擇 (`zh`)
- 語言 → 頁面物件存取

**核心功能：**
- 頁面物件統一管理
- 跨頁面流程協調
- 平台與語言切換

### 3. TestCase 層 - 測試案例實現
**職責：** 實現具體測試場景與驗證邏輯

**撰寫結構：**
```python
@pytest.mark.overview
@allure.epic("iOS")
@allure.feature("總覽")
@allure.title('經辦登入流程')
@pytest.mark.parametrize("user_role,id_number,username,password", data, ids=ids)
def test_login(user_role, id_number, username, password):
    # 1. 測試準備
    navigator = Navigator().ios.zh
    
    # 2. 執行操作
    navigator.login_page.login_slogan().assert_visible()
    navigator.login_page.id_input().click()
    
    # 3. 結果驗證
    assert navigator.overview_page.to_do_list().is_visible()
```

## 單裝置 vs 多裝置差異

### Page 層差異

**單裝置寫法：**
```python
class LoginPage(BaseObject):
    def __init__(self):
        super().__init__()
        self.driver = DeviceManager.get_driver()  # 無需傳入 role
```

**多裝置寫法：**
```python
class MUOtpPage(BaseObject):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        # 傳入 role 以取得對應裝置的 driver
        self.driver = DeviceManager.get_driver(role=self.role)
```

### Navigator 層差異

**單裝置模式：**
- 直接使用 `Navigator().ios.zh`
- DeviceManager 自動偵測連接的裝置
- 無需額外配置

**多裝置模式：**
- 需要先載入 `devices.json` 配置檔
- 透過 role 參數區分不同裝置
- 支援同時操作多個裝置

**Navigator 內部實作差異：**

```python
class NavigatoriOSZh:
    def __init__(self, role=None):
        self.role = role
        self.__otp_page_mu = {}  # 多裝置頁面物件快取
        self.__keyboard_mu = {}      # 多裝置鍵盤物件快取
    
    # 單裝置頁面物件
    @property
    def login_page(self) -> LoginPage:
        if self.__login_page is None:
            self.__login_page = LoginPage()  # 無role參數
        return self.__login_page
    
    # 多裝置頁面物件
    def otp_page_mu(self, role: str) -> MUOtpPage:
        if role not in self.__otp_page_mu:
            self.__otp_page_mu[role] = MUOtpPage(role=role)  # 傳入role
        return self.__otp_page_mu[role]
```

**使用方式差異：**

```python
# 單裝置使用
navigator = Navigator().ios.zh
navigator.login_page.login_btn().click()

# 多裝置使用
navigator = Navigator().ios.zh
navigator.otp_page_mu("old").login_btn().click()  # 舊裝置
navigator.otp_page_mu("new").login_btn().click()  # 新裝置
```

### 配置檔結構 (devices.json)
```json
{
  "defaultRole": "old",
  "devices": {
    "new": {
      "platform": "ios",
      "udid": "1C023E72-72E7-4A64-91A0-15484676A023",
      "wdaLocalPort": 8103,
      "bundleId": "com.cathaybk.geb",
      "appiumPort": "4723"
    },
    "old": {
      "platform": "ios", 
      "udid": "00008150-00154C6C0E46401C",
      "wdaLocalPort": 8102,
      "bundleId": "com.cathaybk.geb",
      "appiumPort": "4801"
    }
  }
}
```

### TestCase 層差異

**單裝置測試：**
```python
def test_single_device():
    navigator = Navigator().ios.zh
    navigator.login_page.login_btn().click()
```

**多裝置測試：**
```python
def test_multi_device():
    
    navigator = Navigator().ios.zh
    # 裝置1操作
    navigator.otp_page_mu("old").login_btn().click()
    # 裝置2操作
    navigator.otp_page_mu("new").login_btn().click() # 自動切換到第二個裝置

```

### DeviceManager 運作機制

**自動模式切換：**
- 傳入 `role` → 自動啟用多裝置模式
- 未傳入 `role` → 使用單裝置模式
- 首次使用多裝置時自動載入 JSON 配置

**Driver 管理：**
```python
# 單裝置
driver = DeviceManager.get_driver()  # 回傳預設 driver

# 多裝置
driver_old = DeviceManager.get_driver(role="old")  # 舊裝置
driver_new = DeviceManager.get_driver(role="new")  # 新裝置
```

## 元件操作方法

### BasicComponent 核心方法
- `click()` - 點擊操作
- `send_keys(text)` - 文字輸入
- `clear()` - 清除內容
- `is_visible()` - 可見性檢查
- `assert_visible()` - 可見性斷言
- `text` - 取得文字內容
- `value` - 取得元素值

### 斷言方法
- `assert_visible()` - 元素必須可見
- `assert_invisible()` - 元素必須不可見
- `assert_clickable()` - 元素必須可點擊
- `assert_selected()` - 元素必須被選中

## 測試案例撰寫規範

### 1. 測試標記與分類
```python
@pytest.mark.overview          # 功能標記
@allure.epic("iOS")           # 測試史詩
@allure.feature("總覽")        # 功能特性
@allure.title('經辦登入流程')   # 測試標題
```

### 2. 參數化測試
```python
data = [("經辦", "65141474", "user001", "Ab123456")]
ids = [f"case : {i}" for i in range(1, len(data)+1)]
@pytest.mark.parametrize("user_role,id_number,username,password", data, ids=ids)
```

### 3. 異常處理模式
```python
# 條件性彈窗處理
if navigator.login_page.dialog_common_message().is_visible():
    navigator.login_page.dialog_login_btn().click()

# 信任裝置彈窗處理
if navigator.login_page.truest_device_dialog().is_visible():
    navigator.login_page.next_time_btn().click()
```

### 4. 截圖與報告
```python
navigator.overview_page.save_screenshot(
    case='photo', 
    name='輸入使用者資訊', 
    attach_jpg=True, 
    remove=True
)
```

## 最佳實踐

### Page 層
- 元素定位器使用明確的等待策略
- 每個方法只負責單一元素操作
- 統一使用 BasicComponent 封裝
- **多裝置：** 建構子必須支援 role 參數

### Navigator 層
- 提供清晰的頁面物件存取路徑
- 支援多平台多語言切換
- 集中管理頁面物件實例
- **多裝置：** 自動偵測並載入配置檔

### TestCase 層
- 測試步驟清晰分離：準備→執行→驗證
- 使用參數化支援多組測試資料
- 包含完整的異常處理邏輯
- 適當的截圖與日誌記錄
- **多裝置：** 明確區分不同裝置的操作流程

### 通用原則
- 所有操作都要有明確的 remark 說明
- 使用斷言確保測試可靠性
- 遵循 AAA 模式 (Arrange-Act-Assert)
- 保持測試案例的獨立性與可重複性
- **多裝置：** 確保 JSON 配置檔的 udid 與 port 不衝突