document.addEventListener("DOMContentLoaded", () => {
    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('username-display').textContent = username;
    }
});

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

function sendRequest() {
            const text = document.querySelector("#input-chat").value;
            const data = { question: text, config: "" };
            const resLog = document.querySelector("#res-log");
            const selfMsg = document.createElement("div");
            selfMsg.innerText = text;
            selfMsg.className = "self-msg";
            resLog.appendChild(selfMsg);

            fetch("http://127.0.0.1:8080/api/test", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            }).then(response => {
                if (response.ok) {
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder("utf-8");
                    const res = document.querySelector("#res-log");
                    const chatItem = document.createElement("p");
                    const s=document.createElement("span");
                    s.className='sty';
                    chatItem.appendChild(s);
                    res.appendChild(chatItem);

                    function read() {
                        reader.read().then(({ done, value }) => {
                            if (done) {
                                console.log('Stream closed');
                                return;
                            }
                            const chunk = decoder.decode(value, { stream: true });
                            chunk.split('\r\n').forEach(eventString => {
                                s.innerHTML += eventString;
                            });
                            read();
                        }).catch(error => {
                            console.error('Stream error', error);
                        });
                    }

                    read();
                } else {
                    console.error('Network response was not ok.');
                }
            }).catch(error => {
                console.error('Fetch error:', error);
            });
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