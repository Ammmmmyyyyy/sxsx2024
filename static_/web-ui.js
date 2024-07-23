document.querySelector("#btn-fold-in").addEventListener("click", (e) => {
    const sidebar = document.querySelector(".sidebar");
    sidebar.style.width = 0

    const btnFoldOut = document.querySelector("#btn-fold-out");
    btnFoldOut.style.display = "inline-block"
})

document.querySelector("#input-send").addEventListener("click", (e) => {
    sendRequest()
})

document.querySelector("#input-chat").addEventListener("keydown", (e) => {
    if(e.keyCode === 13) { 
        sendRequest()
    }
})

document.querySelector("#btn-fold-out").addEventListener("click", (e) => {
    const sidebar = document.querySelector(".sidebar");
    sidebar.style.width = "260px"

    e.target.style.display = "none"
})

function sendRequest(){
    const inputChat = document.querySelector("#input-chat");
    const text = inputChat.value;
    processInput(text);
    inputChat.value = '';
}

const mbtiTypes = {
    "INTJ": "INTJ是具有策略性和计划性的“建筑师”，他们善于制定长远计划并致力于实现目标。他们通常是创新者，擅长逻辑分析和解决复杂问题。INTJ在工作中通常表现出色，尤其是在需要独立思考和长期战略的领域。",
    "INTP": "INTP是具有深刻思想和好奇心的“逻辑学家”，他们喜欢探索理论和抽象概念，致力于发现宇宙的基本真理。INTP通常是学术研究者和科学家，享受独立工作和深入思考。",
    "ENTJ": "ENTJ是果断和自信的“指挥官”，他们擅长领导团队实现宏伟目标。ENTJ通常是自然的领导者，在商业和管理领域表现突出，他们喜欢挑战并能在高压力环境中茁壮成长。",
    "ENTP": "ENTP是好奇、探究和机智的“辩论家”，擅长发现问题的新可能性和解决方案。他们灵活适应、善于追求自己感兴趣的事物，以及因热情和辩论能力而闻名。ENTP通常对生活采取多面化的方式，并对一个观点进行全面探索，而不是专攻一方面。他们是天生的领导者，在商业或作为企业家方面经常取得成功。",
    "INFJ": "INFJ是具有深刻洞察力和同情心的“提倡者”，他们致力于帮助他人并追求意义和目的。INFJ通常是理想主义者，擅长理解复杂的情感和人际关系。",
    "INFP": "INFP是具有强烈理想和创意的“调停者”，他们追求和谐与自我表达。INFP通常是艺术家和作家，喜欢探索人类体验和情感的深度。",
    "ENFJ": "ENFJ是充满热情和魅力的“导师”，他们善于鼓舞和引导他人实现潜力。ENFJ通常是出色的沟通者和组织者，在社会和教育领域表现突出。",
    "ENFP": "ENFP是充满活力和创意的“竞选者”，他们喜欢探索新想法并激励他人。ENFP通常是创新者和激励者，擅长在人际互动中展现魅力。",
    "ISTJ": "ISTJ是可靠和实际的“后勤专家”，他们擅长组织和执行计划。ISTJ通常是细节导向的工作者，确保任务按时完成并达到高标准。",
    "ISFJ": "ISFJ是关怀和细心的“守护者”，他们致力于照顾他人并维护传统。ISFJ通常是细心的支持者和可靠的团队成员，在需要耐心和同理心的领域表现出色。",
    "ESTJ": "ESTJ是实际和果断的“管理者”，他们擅长领导团队实现具体目标。ESTJ通常是组织者和管理员，确保事情有序进行并达到预期效果。",
    "ESFJ": "ESFJ是温暖和合作的“领事”，他们重视和谐和人际关系。ESFJ通常是社交能手和支持者，擅长在团队中创造积极的氛围。",
    "ISTP": "ISTP是冷静和务实的“工匠”，他们擅长解决实际问题并掌握各种工具。ISTP通常是技术专家和工程师，喜欢通过实际操作来理解世界。",
    "ISFP": "ISFP是敏感和好奇的“探险家”，他们追求美丽和自我表达。ISFP通常是艺术家和音乐家，喜欢通过创作表达情感。",
    "ESTP": "ESTP是大胆和实际的“企业家”，他们喜欢冒险并迅速适应新情况。ESTP通常是行动导向的领导者，擅长在动态环境中作出决策。",
    "ESFP": "ESFP是充满活力和热情的“表演者”，他们喜欢享受生活并与他人分享快乐。ESFP通常是社交能手和娱乐专家，擅长通过互动带来欢乐。"
};

function processInput(text) {
    const userInput = text.toUpperCase();
    const resLog = document.querySelector("#res-log");

    // 显示用户输入的内容
    const selfMsg = document.createElement("div");
    selfMsg.innerText = text;
    selfMsg.className = "self-msg";
    resLog.appendChild(selfMsg);

    const matchedType = Object.keys(mbtiTypes).find(type => userInput.includes(type));
    const resultDiv = document.createElement('div');
    resultDiv.className = "result";

    if (userInput.includes("测试")) {
        resultDiv.innerHTML = `请点击如下链接测试你的人格：<a href="https://www.16personalities.com/" target="_blank">https://www.16personalities.com/</a>`;
    } else if (matchedType) {
        resultDiv.innerHTML = 
            `<div class="text">
                ${mbtiTypes[matchedType]} 想了解更多请点击下面网页：
                <a href="${matchedType.toLowerCase()}/${matchedType.toLowerCase()}.html" target="_blank">Go to ${matchedType} page</a>
            </div>`;
    } else {
        resultDiv.textContent = 'No MBTI type found in the input';
    }

    // 显示生成的链接或提示信息
    const llmMsg = document.createElement("div");
    llmMsg.className = "llm-msg";
    llmMsg.appendChild(resultDiv);
    resLog.appendChild(llmMsg);
}
document.querySelector("#btn-model1").addEventListener("click", () => {
            window.location.href = "test.html";
        });

        document.querySelector("#btn-model2").addEventListener("click", () => {
            window.location.href = "tarot.html";
        });

        document.querySelector("#btn-model3").addEventListener("click", () => {
            window.location.href = "constellation2.html";
        });

        document.querySelector("#btn-model4").addEventListener("click", () => {
            window.location.href = "constellation.html";
        });

