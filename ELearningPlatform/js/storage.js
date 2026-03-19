function saveCourse(id) {
  let data = JSON.parse(localStorage.getItem("completed")) || [];

  if (!data.includes(id)) {
    data.push(id);
  }

  localStorage.setItem("completed", JSON.stringify(data));
}

function getCourses() {
  return JSON.parse(localStorage.getItem("completed")) || [];
}