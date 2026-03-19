let selectedCourse = null;
let selectedQuiz = null;
let questions = [];
let userAnswers = {};


function loadCourses() {
  let div = document.getElementById("courseSelection");
  if (!div) return;

  div.innerHTML = "";
  courses.forEach(c => {
    div.innerHTML += `
      <button class="course-btn" onclick="selectCourse(${c.id}, this)">
        ${c.name}
      </button>
    `;
  });
}


function selectCourse(id, btn) {
  selectedCourse = id;
  selectedQuiz = null;

  document.querySelectorAll(".course-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");

  document.getElementById("quizContainer").innerHTML = "";
  document.getElementById("result").innerHTML = "";
  document.getElementById("submitBtn").style.display = "none";

  showQuizOptions();
}

function showQuizOptions() {
  let div = document.getElementById("quizSelection");
  if (!div) return;

  let progress = JSON.parse(localStorage.getItem("progress_" + selectedCourse)) || {};

  let quiz2Btn = progress.quiz1
    ? `<button class="quiz-btn" onclick="startQuiz('quiz2')">Quiz 2</button>`
    : `<button class="quiz-btn" disabled title="Complete Quiz 1 first">Quiz 2 🔒</button>`;

  div.innerHTML = `
    <h3>Select Quiz</h3>
    <button class="quiz-btn" onclick="startQuiz('quiz1')">Quiz 1</button>
    ${quiz2Btn}
  `;
}


async function startQuiz(quizKey) {
  if (!selectedCourse) return;

  let progress = JSON.parse(localStorage.getItem("progress_" + selectedCourse)) || {};

  if (quizKey === "quiz2" && !progress.quiz1) {
    document.getElementById("quizContainer").innerHTML =
      "<p style='color:orange;'>You must complete Quiz 1 before attempting Quiz 2.</p>";
    document.getElementById("submitBtn").style.display = "none";
    return;
  }

  if (progress[quizKey]) {
    document.getElementById("quizContainer").innerHTML =
      "<p style='color:red;'>You have already completed this quiz. Retake not allowed.</p>";
    document.getElementById("submitBtn").style.display = "none";
    return;
  }

  selectedQuiz = quizKey;
  questions = quizData[selectedCourse][quizKey];
  userAnswers = {};

  document.getElementById("quizContainer").innerHTML = "<p>Loading questions...</p>";
  await new Promise(res => setTimeout(res, 500));

  renderQuiz();
  document.getElementById("submitBtn").style.display = "block";
  document.getElementById("result").innerHTML = "";
}


function renderQuiz() {
  let container = document.getElementById("quizContainer");
  container.innerHTML = "";

  questions.forEach((q, i) => {
    let html = `<p><strong>${i + 1}. ${q.question}</strong></p>`;

    q.options.forEach((opt, j) => {
      html += `
        <label>
          <input type="radio" name="q${i}" onchange="selectAnswer(${i}, ${j})">
          ${opt}
        </label><br>
      `;
    });

    container.innerHTML += `<div class="question-block" style="margin-bottom:1rem">${html}</div>`;
  });
}


function selectAnswer(q, opt) {
  userAnswers[q] = opt;
}


function submitQuiz() {
  if (Object.keys(userAnswers).length < questions.length) {
    if (!confirm("You haven't answered all questions. Submit anyway?")) return;
  }

  let score = 0;
  questions.forEach((q, i) => {
    if (userAnswers[i] === q.answer) score++;
  });

  let percent = calculatePercentage(score, questions.length);
  let grade = getGrade(percent);
  let status = getResultStatus(percent);
  let feedback = getPerformanceFeedback(percent); 

  document.getElementById("result").innerHTML = `
    <p>Score: ${score}/${questions.length}</p>
    <p>Percentage: ${percent}%</p>
    <p>Grade: ${grade}</p>
    <p>Result: ${status}</p>
    <p>${feedback}</p>
  `;

  let progress = JSON.parse(localStorage.getItem("progress_" + selectedCourse)) || {};
  progress[selectedQuiz] = true;
  localStorage.setItem("progress_" + selectedCourse, JSON.stringify(progress));

  let results = JSON.parse(localStorage.getItem("results_" + selectedCourse)) || {};
  results[selectedQuiz] = { score, percent, grade, status, feedback };
  localStorage.setItem("results_" + selectedCourse, JSON.stringify(results));

  document.getElementById("submitBtn").style.display = "none";

  showQuizOptions();
}

document.addEventListener("DOMContentLoaded", function () {
  loadCourses();

  const params = new URLSearchParams(window.location.search);
  const courseIdFromURL = params.get("courseId");
  const quizKeyFromURL = params.get("quizKey");

  if (courseIdFromURL && quizKeyFromURL) {
    selectedCourse = parseInt(courseIdFromURL);

    document.querySelectorAll(".course-btn").forEach(btn => {
      if (btn.getAttribute("onclick") === `selectCourse(${selectedCourse}, this)`) {
        btn.classList.add("active");
      }
    });

    showQuizOptions();
    startQuiz(quizKeyFromURL);
  }
});