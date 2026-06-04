const el = document.querySelector("#greeting");
const text = el ? el.textContent.trim() : null;
console.log("deferred app sees:", text);
