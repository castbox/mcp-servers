# Google API 凭证生成指南

本指南将帮助你创建和配置Google API服务账号，获取必要的凭证文件（credentials.json），以便使用Google Sheets MCP工具。

## 前提条件

1. 拥有Google账号
2. 能够访问[Google Cloud Console](https://console.cloud.google.com/)

## 步骤一：创建Google Cloud项目

1. 访问[Google Cloud Console](https://console.cloud.google.com/)
2. 点击页面顶部的项目下拉菜单，然后点击"新建项目"
3. 输入项目名称（例如"Google-Sheets-MCP"）
4. 点击"创建"按钮
5. 等待项目创建完成，系统会自动切换到新项目

## 步骤二：启用必要的API

1. 在Google Cloud Console左侧菜单中，导航至"API和服务" > "库"
2. 搜索并启用以下API：
   - Google Sheets API
   - Google Drive API
   - Google Docs API
3. 对于每个API，点击"启用"按钮

## 步骤三：创建服务账号

1. 在Google Cloud Console左侧菜单中，导航至"API和服务" > "凭证"
2. 点击页面顶部的"创建凭证"按钮，选择"服务账号"
3. 输入服务账号名称（例如"sheets-service-account"）
4. （可选）添加服务账号描述
5. 点击"创建并继续"
6. 在"授予此服务账号对项目的访问权限"部分，选择"编辑者"角色
7. 点击"继续"，然后点击"完成"

## 步骤四：创建并下载服务账号密钥

1. 在"凭证"页面，找到刚刚创建的服务账号，点击右侧的操作菜单（三个点）
2. 选择"管理密钥"
3. 点击"添加密钥" > "创建新密钥"
4. 选择"JSON"格式
5. 点击"创建"按钮
6. 系统会自动下载JSON密钥文件到你的计算机
7. 将此文件重命名为`credentials.json`并移动到项目根目录

## 步骤五：共享Google文档给服务账号

要让服务账号访问你的Google文档，你需要与服务账号的电子邮件地址共享这些文档：

1. 打开`credentials.json`文件，找到`client_email`字段的值（格式类似于`service-account-name@project-id.iam.gserviceaccount.com`）
2. 打开你想要访问的Google Sheets或Docs文档
3. 点击"共享"按钮
4. 在输入框中粘贴服务账号的电子邮件地址
5. 设置适当的权限（对于只读操作选择"查看者"，对于需要编辑的操作选择"编辑者"）
6. 取消勾选"通知用户"选项（可选）
7. 点击"发送"或"共享"按钮

## 步骤六：配置项目

1. 在项目根目录中，确保`credentials.json`文件已就位
2. 编辑`config.py`文件，根据需要修改配置参数
3. 特别注意更新`SPREADSHEET_ID`为你的Google Sheets文档ID（可以从URL中获取）

## 安全注意事项

- **不要**将`credentials.json`文件提交到公共代码库
- **不要**在多人共享的环境中暴露此文件
- 考虑使用环境变量来存储敏感信息
- 定期轮换服务账号密钥，特别是在怀疑凭证可能泄露时
- 仅授予服务账号所需的最小权限

## 故障排除

### 403 Forbidden 错误

如果遇到"403 Forbidden"错误，可能是由于以下原因：

1. 未启用相应的API（Google Sheets API、Google Drive API或Google Docs API）
2. 未与服务账号共享目标文档
3. 服务账号没有足够的权限
4. API配额已用尽

### 身份验证失败

如果遇到身份验证失败，请检查：

1. `credentials.json`文件是否位于正确的位置
2. 文件内容是否完整且格式正确
3. 服务账号是否仍然有效（未被删除或禁用）

## 其他资源

- [Google Sheets API 文档](https://developers.google.com/sheets/api)
- [Google Drive API 文档](https://developers.google.com/drive)
- [Google Docs API 文档](https://developers.google.com/docs)
- [Google Cloud 服务账号文档](https://cloud.google.com/iam/docs/service-accounts)
