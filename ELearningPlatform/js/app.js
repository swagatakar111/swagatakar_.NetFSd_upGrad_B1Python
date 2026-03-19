
function getCourseProgress(courseId) {
  let progress = JSON.parse(localStorage.getItem("progress_" + courseId)) || {};
  let percent = 0;
  if (progress.quiz1) percent += 50;
  if (progress.quiz2) percent += 50;
  return percent;
}

function getQuizResults(courseId) {
  return JSON.parse(localStorage.getItem("results_" + courseId)) || {};
}

if (document.getElementById("courseTable")) {
  let tbody = document.getElementById("courseTable");
  let total = 0;

  courses.forEach(c => {
    let progress = getCourseProgress(c.id);
    total += progress;
    tbody.innerHTML += `
      <tr>
        <td>${c.name}</td>
        <td>${progress}%</td>
        <td>
          <progress value="${progress}" max="100"></progress>
        </td>
      </tr>
    `;
  });

  let avg = courses.length > 0 ? total / courses.length : 0;
  let overallBar = document.getElementById("progressBar");
  if (overallBar) overallBar.value = avg;
}


if (document.getElementById("courseList")) {
  renderCourseList();
}

function renderCourseList() {
  let list = document.getElementById("courseList");
  if (!list) return;

  list.innerHTML = "";

  courses.forEach(c => {
    let progress = JSON.parse(localStorage.getItem("progress_" + c.id)) || {};
    let nextQuiz = !progress.quiz1 ? "quiz1" : !progress.quiz2 ? "quiz2" : null;

    let buttonHTML = nextQuiz
      ? `<button onclick="startQuizFromCourses(${c.id})">Start Quiz</button>`
      : `<button disabled>Completed</button>`;

    let marksHTML = progress.quiz1
      ? `<button onclick="showMarks(${c.id})">Show Marks</button>`
      : "";

    // 5-day lesson plan using <ol> (requirement)
    let lessonHTML = c.lessons.map(l => `
      <li>
        <strong>Day ${l.day}: ${l.title}</strong>
        <ul>${l.topics.map(t => `<li>${t}</li>`).join("")}</ul>
      </li>
    `).join("");

    list.innerHTML += `
      <div class="course-card">
        <h3>${c.name}</h3>

        <div class="lesson-toggle" onclick="toggleLesson(${c.id})">
          📋 View Lesson Plan <span id="icon-${c.id}">▼</span>
        </div>

        <div class="lesson-plan" id="lesson-${c.id}" style="display:none">
          <ol>${lessonHTML}</ol>
        </div>

        <div style="margin-top:12px">
          ${buttonHTML}
          ${marksHTML}
        </div>
        <div id="marks-${c.id}"></div>
      </div>
    `;
  });
}

function toggleLesson(courseId) {
  let plan = document.getElementById("lesson-" + courseId);
  let icon = document.getElementById("icon-" + courseId);
  if (plan.style.display === "none") {
    plan.style.display = "block";
    icon.textContent = "▲";
  } else {
    plan.style.display = "none";
    icon.textContent = "▼";
  }
}

function startQuizFromCourses(courseId) {
  let progress = JSON.parse(localStorage.getItem("progress_" + courseId)) || {};
  let nextQuiz = !progress.quiz1 ? "quiz1" : !progress.quiz2 ? "quiz2" : null;

  if (!nextQuiz) {
    alert("All quizzes completed for this course!");
    return;
  }

  window.location.href = `quiz.html?courseId=${courseId}&quizKey=${nextQuiz}`;
}



function showMarks(courseId) {
  let results = getQuizResults(courseId);
  let progress = JSON.parse(localStorage.getItem("progress_" + courseId)) || {};
  let div = document.getElementById("marks-" + courseId);
  if (!div) return;

  let html = "";

  if (results.quiz1) {
    let r = results.quiz1;
    html += `<p>QUIZ1 → Score: ${r.score}/5 | ${r.percent}% | Grade: ${r.grade} | ${r.status}</p>`;
  } else {
    html += `<p>QUIZ1 → Not attempted</p>`;
  }

  if (progress.quiz1) {
    if (results.quiz2) {
      let r = results.quiz2;
      html += `<p>QUIZ2 → Score: ${r.score}/5 | ${r.percent}% | Grade: ${r.grade} | ${r.status}</p>`;
    } else {
      html += `<p>QUIZ2 → Not attempted yet</p>`;
    }
  }

  div.innerHTML = html;
}



if (document.getElementById("completedCourses")) {
  let ul = document.getElementById("completedCourses");
  ul.innerHTML = "";

  courses.forEach(c => {
    let progress = getCourseProgress(c.id);
    if (progress === 100) {
      ul.innerHTML += `<li>${c.name} ✅ Completed</li>`;
    }
  });
}