const btn = document.getElementById("analyzeBtn");
const form = document.getElementsByClassName("f")[0];
const hiddenSec = document.querySelector(".sec.hidden");

const ta = document.getElementById("ta");
const totalInput = document.getElementById("totalMarks");

let animationDone = false;

btn.addEventListener("click", () => {

    const marksText = ta.value;
    const totalMarks = totalInput.value;

    if (!marksText.trim() || !totalMarks.trim()) {
        alert("Please enter marks and total marks");
        return;
    }

    fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            marks_text: marksText,
            total_marks: totalMarks
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        // update results EVERY time
        document.querySelector(".ab95").innerText = data.above_95;
        document.querySelector(".bet90_95").innerText = data.between_90_95;
        document.querySelector(".bet80_90").innerText = data.between_80_90;
        document.querySelector(".bet70_80").innerText = data.between_70_80;
        document.querySelector(".bet60_70").innerText = data.between_60_70;
        document.querySelector(".bel60").innerText = data.below_60;
        document.querySelector(".totalStudents").innerText = data.total_students;
        document.querySelector(".highestMarks").innerText = data.highest_marks;
        document.querySelector(".lowestMarks").innerText = data.lowest_marks;
        document.querySelector(".avgMarks").innerText = data.avg_marks;
        document.querySelector(".fullMarks").innerText = data.full_marks;


        // animation ONLY once
        if (!animationDone) {
            animationDone = true;

            form.classList.add("animate-once");

            setTimeout(() => {
                hiddenSec.classList.add("show");
            }, 1000);
        }
    });
});
