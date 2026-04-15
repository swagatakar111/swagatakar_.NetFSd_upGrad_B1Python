



async function loadDashboard() {
  const tbody = document.getElementById("courseTable");
  const progressBar = document.getElementById("progressBar");
  const progressLabel = document.getElementById("progressLabel");
  if (!tbody) return;

  try {
    const userId = localStorage.getItem("userId");
    const [courses, results] = await Promise.all([
      API.getCourses(),
      userId ? API.getResults(userId) : Promise.resolve([])
    ]);

    let total = 0;
    tbody.innerHTML = "";

    for (const course of courses) {
      const quizzes = await API.getQuizzesByCourse(course.courseId);
      const doneCount = results.filter(r =>
        quizzes.some(q => q.quizId === r.quizId)).length;
      const percent = quizzes.length > 0
        ? Math.round((doneCount / quizzes.length) * 100) : 0;
      total += percent;

      tbody.innerHTML += `
        <tr>
          <td>${course.title}</td>
          <td>${percent}%</td>
          <td><progress value="${percent}" max="100"></progress></td>
        </tr>
      `;
    }

    const avg = courses.length > 0 ? total / courses.length : 0;
    if (progressBar) progressBar.value = avg;
    if (progressLabel) progressLabel.textContent = Math.round(avg) + "% complete";

  } catch (err) {
    console.error("Dashboard load error:", err);
    tbody.innerHTML = `<tr><td colspan="3">Failed to load courses.</td></tr>`;
  }
}


async function renderCourseList() {
  const list = document.getElementById("courseList");
  if (!list) return;

  list.innerHTML = "<p>Loading courses...</p>";

  try {
    const userId = localStorage.getItem("userId");
    const [courses, results] = await Promise.all([
      API.getCourses(),
      userId ? API.getResults(userId) : Promise.resolve([])
    ]);

    list.innerHTML = "";

    for (const course of courses) {
      const [lessons, quizzes] = await Promise.all([
        API.getLessons(course.courseId),
        API.getQuizzesByCourse(course.courseId)
      ]);

      const completedQuizIds = results.map(r => r.quizId);
      const allDone = quizzes.length > 0 &&
        quizzes.every(q => completedQuizIds.includes(q.quizId));
      const nextQuiz = quizzes.find(q => !completedQuizIds.includes(q.quizId));

      let buttonHTML = allDone
        ? `<button disabled>✅ Completed</button>`
        : nextQuiz
          ? `<button onclick="startQuizFromCourses(${course.courseId})">Start Quiz</button>`
          : `<button disabled>No Quiz Yet</button>`;

      let marksHTML = results.some(r =>
        quizzes.some(q => q.quizId === r.quizId))
        ? `<button onclick="showMarks(${course.courseId})">Show Marks</button>`
        : "";

      let lessonHTML = lessons.map(l => `
        <li>
          <strong>${l.orderIndex}. ${l.title}</strong>
          <ul><li>${l.content}</li></ul>
        </li>
      `).join("");

      list.innerHTML += `
        <div class="course-card">
          <h3>${course.title}</h3>
          <p>${course.description}</p>

          <div class="lesson-toggle" onclick="toggleLesson(${course.courseId})">
            📋 View Lesson Plan <span id="icon-${course.courseId}">▼</span>
          </div>

          <div class="lesson-plan" id="lesson-${course.courseId}" style="display:none">
            <ol>${lessonHTML || '<li>No lessons added yet.</li>'}</ol>
          </div>

          <div style="margin-top:12px">
            ${buttonHTML}
            ${marksHTML}
          </div>
          <div id="marks-${course.courseId}"></div>
        </div>
      `;
    }

  } catch (err) {
    console.error("Courses load error:", err);
    list.innerHTML = "<p>Failed to load courses. Make sure the API is running.</p>";
  }
}

function toggleLesson(courseId) {
  const plan = document.getElementById("lesson-" + courseId);
  const icon = document.getElementById("icon-" + courseId);
  if (plan.style.display === "none") {
    plan.style.display = "block";
    icon.textContent = "▲";
  } else {
    plan.style.display = "none";
    icon.textContent = "▼";
  }
}

async function startQuizFromCourses(courseId) {
  const userId = localStorage.getItem("userId");
  const [quizzes, results] = await Promise.all([
    API.getQuizzesByCourse(courseId),
    userId ? API.getResults(userId) : Promise.resolve([])
  ]);

  if (!quizzes.length) {
    alert("No quizzes available for this course.");
    return;
  }

  const completedIds = results.map(r => r.quizId);
  const nextQuiz = quizzes.find(q => !completedIds.includes(q.quizId));

  if (!nextQuiz) {
    alert("All quizzes completed for this course!");
    return;
  }

  window.location.href = `quiz.html?quizId=${nextQuiz.quizId}&courseId=${courseId}`;
}

async function showMarks(courseId) {
  const userId = localStorage.getItem("userId");
  if (!userId) return;

  const div = document.getElementById("marks-" + courseId);
  if (!div) return;

  const [quizzes, results] = await Promise.all([
    API.getQuizzesByCourse(courseId),
    API.getResults(userId)
  ]);

  const courseResults = results.filter(r =>
    quizzes.some(q => q.quizId === r.quizId));

  let html = "";
  courseResults.forEach((r, i) => {
    html += `
      <p>Quiz ${i + 1} → 
        Score: ${r.score}/${r.totalQuestions} | 
        ${r.percentage}% | 
        Grade: ${r.grade} | 
        ${r.status}
      </p>`;
  });

  div.innerHTML = html || "<p>No results yet.</p>";
}


async function loadProfile() {
  const userId = localStorage.getItem("userId");
  if (!userId) return;

  try {
    const [user, courses, results] = await Promise.all([
      API.getUser(userId),
      API.getCourses(),
      API.getResults(userId)
    ]);

   
    document.getElementById("profileName").textContent = user.fullName;
    document.getElementById("avatarLetter").textContent =
      user.fullName.charAt(0).toUpperCase();
    document.getElementById("infoFullName").textContent = user.fullName;
    document.getElementById("infoEmail").textContent = user.email;
    document.getElementById("infoCreatedAt").textContent =
      new Date(user.createdAt).toLocaleDateString();

   
    document.getElementById("statEnrolled").textContent = courses.length;
    document.getElementById("statQuizzes").textContent = results.length;

  
    const completedCourses = [];
    for (const course of courses) {
      const quizzes = await API.getQuizzesByCourse(course.courseId);
      const done = results.filter(r =>
        quizzes.some(q => q.quizId === r.quizId));
      if (quizzes.length > 0 && done.length >= quizzes.length) {
        completedCourses.push(course);
      }
    }

    document.getElementById("statCompleted").textContent = completedCourses.length;

    const ul = document.getElementById("completedCourses");
    if (completedCourses.length === 0) {
      ul.innerHTML = '<p class="no-completed">No courses completed yet. Keep going! 💪</p>';
    } else {
      ul.innerHTML = completedCourses
        .map(c => `<li>${c.title} ✅ Completed</li>`)
        .join("");
    }

    
    const perfDiv = document.getElementById("quizPerformance");
    if (results.length === 0) {
      perfDiv.innerHTML = '<p class="no-completed">No quizzes attempted yet.</p>';
    } else {
      perfDiv.innerHTML = results.map(r => `
        <div class="info-row">
          <div>
            <p class="info-label">${r.courseTitle} — ${r.quizTitle}</p>
            <div class="info-value">
              Score: ${r.score}/${r.totalQuestions} | 
              ${r.percentage}% | 
              Grade: ${r.grade} | 
              ${r.status}
            </div>
          </div>
        </div>
      `).join("");
    }

  } catch (err) {
    console.error("Profile load error:", err);
  }
}


document.addEventListener("DOMContentLoaded", () => {
  checkAuth(); 

  if (document.getElementById("courseTable")) loadDashboard();
  if (document.getElementById("courseList")) renderCourseList();
  if (document.getElementById("profileName")) loadProfile();
});