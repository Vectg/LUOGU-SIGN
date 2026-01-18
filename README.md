## Luogu 每日自动打卡

1. [Fork](https://github.com/xcx0902/luogu-auto-punch/fork) 本仓库到个人用户下。
2. 打开[洛谷](https://www.luogu.com.cn)，右击，选择检查，上方选择应用程序，左侧找到 Cookie，点击下方的 `https://www.luogu.com.cn`，找到 `_uid` 和 `__client_id`，记下来。
![img](https://user-images.githubusercontent.com/99001676/223611417-aba0e538-845e-436e-89b4-fdb4767ceaf7.png)
3. 在 New Action Secret 页面（`https://github.com/<username>/luogu-auto-punch/settings/secrets/actions/new`），添加一个名为 `COOKIE` 的 Secret，内容为 `"__client_id=<your __client_id>;_uid=<your _uid>;"`。
4. 在 Action 页（`https://github.com/<username>/luogu-auto-punch/actions`）点击绿色圆角矩形方框。此时每日 8 点到 10 点左右即会自动打卡，如果没有打卡成功请检查你的各项配置。

![img](https://user-images.githubusercontent.com/99001676/224011586-dd93b1c0-471a-45df-8734-d13c83ae5167.png)
