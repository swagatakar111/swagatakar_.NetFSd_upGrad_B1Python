

checkAuth();

let selectedCourseId = null;
let selectedQuizId = null;
let questions = [];
let userAnswers = {};

async function loadCourses() {
  const div = document.getElementById("courseSelection");
  if (!div) return;

  try {
    const courses = await API.getCourses();
    div.innerHTML = "";
    courses.forEach(c => {
      div.innerHTML += `
        <button class="course-btn"
          onclick="selectCourse(${c.courseId}, this)">
          ${c.title}
        </button>
      `;
    });
  } catch (err) {
    div.innerHTML = "<p>Failed to load courses.</p>";
  }
}

async function selectCourse(courseId, btn) {
  selectedCourseId = courseId;
  selectedQuizId = null;

  document.querySelectorAll(".course-btn")
    .forEach(b => b.classList.remove("active"));
  btn.classList.add("active");

  document.getElementById("quizContainer").innerHTML = "";
  document.getElementById("result").innerHTML = "";
  document.getElementById("submitBtn").style.display = "none";

  await showQuizOptions();
}

async function showQuizOptions() {
  const div = document.getElementById("quizSelection");
  if (!div) return;

  try {
    const userId = localStorage.getItem("userId");
    const [quizzes, results] = await Promise.all([
      API.getQuizzesByCourse(selectedCourseId),
      userId ? API.getResults(userId) : Promise.resolve([])
    ]);

    const completedQuizIds = results.map(r => r.quizId);
    div.innerHTML = `<h3>Select Quiz</h3>`;

    quizzes.forEach((quiz, index) => {
      const isDone = completedQuizIds.includes(quiz.quizId);
      const isLocked = index > 0 &&
        !completedQuizIds.includes(quizzes[index - 1].quizId);

      if (isDone) {
        div.innerHTML += `
          <button class="quiz-btn active" disabled>
            ${quiz.title} ✅
          </button>`;
      } else if (isLocked) {
        div.innerHTML += `
          <button class="quiz-btn" disabled
            title="Complete previous quiz first">
            ${quiz.title} 🔒
          </button>`;
      } else {
        div.innerHTML += `
          <button class="quiz-btn"
            onclick="startQuiz(${quiz.quizId})">
            ${quiz.title}
          </button>`;
      }
    });

    if (!quizzes.length) {
      div.innerHTML += "<p>No quizzes available for this course.</p>";
    }

  } catch (err) {
    div.innerHTML = "<p>Failed to load quizzes.</p>";
  }
}

async function startQuiz(quizId) {
  selectedQuizId = quizId;
  userAnswers = {};

  const container = document.getElementById("quizContainer");
  container.innerHTML = "<p>Loading questions...</p>";

  try {
    questions = await API.getQuestions(quizId);

    if (!questions.length) {
      container.innerHTML =
        "<p style='color:orange;'>This quiz has no questions yet.</p>";
      document.getElementById("submitBtn").style.display = "none";
      return;
    }

    renderQuiz();
    document.getElementById("submitBtn").style.display = "block";
    document.getElementById("result").innerHTML = "";

  } catch (err) {
    container.innerHTML =
      "<p style='color:red;'>Failed to load questions.</p>";
  }
}

function renderQuiz() {
  const container = document.getElementById("quizContainer");
  container.innerHTML = "";

  questions.forEach((q, i) => {
    const options = [q.optionA, q.optionB, q.optionC, q.optionD];
    const letters = ["A", "B", "C", "D"];

    let html = `<p><strong>${i + 1}. ${q.questionText}</strong></p>`;

    options.forEach((opt, j) => {
      html += `
        <label>
          <input type="radio" name="q${i}"
            onchange="selectAnswer(${q.questionId}, '${letters[j]}')">
          ${letters[j]}. ${opt}
        </label><br>
      `;
    });

    container.innerHTML += `
      <div class="question-block" style="margin-bottom:1rem">
        ${html}
      </div>`;
  });
}

function selectAnswer(questionId, letter) {
  userAnswers[questionId] = letter;
}

async function submitQuiz() {
  if (Object.keys(userAnswers).length < questions.length) {
    if (!confirm("You haven't answered all questions. Submit anyway?"))
      return;
  }

  const userId = localStorage.getItem("userId");
  if (!userId) {
    alert("Please login first.");
    window.location.href = "login.html";
    return;
  }

  try {
    const result = await API.submitQuiz(
      selectedQuizId,
      parseInt(userId),
      userAnswers
    );

    document.getElementById("result").innerHTML = `
      <p>Score: ${result.score}/${result.totalQuestions}</p>
      <p>Percentage: ${result.percentage}%</p>
      <p>Grade: ${result.grade}</p>
      <p>Result: ${result.status}</p>
      <p>${result.feedback}</p>
    `;

    document.getElementById("submitBtn").style.display = "none";
    await showQuizOptions();

  } catch (err) {
    alert("Failed to submit quiz. Please try again.");
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", async function () {
  await loadCourses();

  const params = new URLSearchParams(window.location.search);
  const quizIdFromURL = params.get("quizId");
  const courseIdFromURL = params.get("courseId");

  if (courseIdFromURL) {
    selectedCourseId = parseInt(courseIdFromURL);

    document.querySelectorAll(".course-btn").forEach(btn => {
      if (btn.getAttribute("onclick")
        ?.includes(`selectCourse(${selectedCourseId}`)) {
        btn.classList.add("active");
      }
    });

    await showQuizOptions();

    if (quizIdFromURL) {
      await startQuiz(parseInt(quizIdFromURL));
    }
  }
});