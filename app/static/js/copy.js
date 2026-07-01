document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".copybox").forEach(function (box) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-action";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      const text = box.innerText || box.textContent || "";
      navigator.clipboard.writeText(text.trim()).then(function () {
        btn.textContent = "Copied";
        setTimeout(function(){ btn.textContent = "Copy"; }, 1200);
      }).catch(function () {
        btn.textContent = "Select text";
        setTimeout(function(){ btn.textContent = "Copy"; }, 1600);
      });
    });
    box.parentNode.insertBefore(btn, box);
  });
});