const fs = require('fs');

async function getUpSchoolInfo(uid) {
    const url = `https://m.bilibili.com/space/${uid}`;
    const headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    };

    try {
        // 获取用户主页HTML
        const response = await fetch(url, { headers });
        const htmlContent = await response.text();

        // 使用正则表达式提取JSON数据
        const pattern = /window\.__INITIAL_STATE__=(.*?);\(function\(\)/;
        const match = htmlContent.match(pattern);
        if (!match) {
            console.log("未找到用户数据");
            return null;
        }

        // 解析JSON数据
        const jsonStr = match[1];
        const userData = JSON.parse(jsonStr);

        // 从JSON中提取学校信息
        if (userData.space && userData.space.info && userData.space.info.school) {
            const schoolInfo = userData.space.info.school.name;
            if (schoolInfo) {
                return schoolInfo;
            }
        }

        return null;

    } catch (error) {
        console.error(`请求失败: ${error.message}`);
        return null;
    }
}

// 示例使用
(async () => {
    // const uid = "395939636";  // 测试UID：华东理工大学
    const uid = "245645656";  // 测试UID：清华大学
    // const uid = "5415414";
    const schoolInfo = await getUpSchoolInfo(uid);

    if (schoolInfo) {
        console.log(`该UP主的学校: ${schoolInfo}`);
    } else {
        console.log("未找到该UP主的学校信息");
    }
})();