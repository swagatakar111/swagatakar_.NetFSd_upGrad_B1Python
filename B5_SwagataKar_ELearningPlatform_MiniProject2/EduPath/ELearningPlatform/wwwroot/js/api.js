
const API_BASE = '/api';

const API = {

  

  register: (fullName, email, password) =>
    fetch(`${API_BASE}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fullName, email, password })
    }).then(r => r.json()),

  login: (email, password) =>
    fetch(`${API_BASE}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    }).then(r => r.json()),

  getUser: (userId) =>
    fetch(`${API_BASE}/users/${userId}`)
      .then(r => r.json()),

  updateUser: (userId, fullName, email) =>
    fetch(`${API_BASE}/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fullName, email })
    }).then(r => r.json()),

 

  getCourses: () =>
    fetch(`${API_BASE}/courses`)
      .then(r => r.json()),

  getCourse: (courseId) =>
    fetch(`${API_BASE}/courses/${courseId}`)
      .then(r => r.json()),

  createCourse: (title, description, createdBy) =>
    fetch(`${API_BASE}/courses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, createdBy })
    }).then(r => r.json()),

  updateCourse: (courseId, title, description) =>
    fetch(`${API_BASE}/courses/${courseId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description })
    }).then(r => r.json()),

  deleteCourse: (courseId) =>
    fetch(`${API_BASE}/courses/${courseId}`, {
      method: 'DELETE'
    }),

  

  getLessons: (courseId) =>
    fetch(`${API_BASE}/courses/${courseId}/lessons`)
      .then(r => r.json()),

  

  getQuizzesByCourse: (courseId) =>
    fetch(`${API_BASE}/quizzes/${courseId}`)
      .then(r => r.json()),

  getQuestions: (quizId) =>
    fetch(`${API_BASE}/quizzes/${quizId}/questions`)
      .then(r => r.json()),

  submitQuiz: (quizId, userId, answers) =>
    fetch(`${API_BASE}/quizzes/${quizId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, answers })
    }).then(r => r.json()),

  

  getResults: (userId) =>
    fetch(`${API_BASE}/results/${userId}`)
      .then(r => r.json()),
};