document.addEventListener("DOMContentLoaded", () => {
    let keyBuff = [];
    let keyPresses = [];
    let keyPressHistory = [];
    let hadKeyUp = true;
    const listenFor = [
        {
            shortcut: [["g"], ["g"]],
            handle(){
                console.log("gg");
            }
        },
    ];
    document.addEventListener(
        "keydown",
        (event) => {
            if (hadKeyUp || keyBuff.slice(-1) != event.key) {
                if (keyBuff.length == 0) {
                    keyPresses = [];
                }
                keyBuff.push(event.key);
                hadKeyUp = false;
            }
        },
        false,
    );
    document.addEventListener(
        "keyup",
        (event) => {
            keyPresses.push(Array.from(keyBuff));
            const keyIndex = keyBuff.indexOf(event.key);
            keyBuff.splice(keyIndex, 1);
            if (keyBuff.length == 0) {
                keyBuff = [];
                keyPressHistory.push(Array.from(keyPresses));
                for (const k = 0; k < listenFor.length; k++) {
                    console.log(`${listenFor[k].shortcut}`);
                }
            }
            hadKeyUp = true;
        },
        false,
    );

});
