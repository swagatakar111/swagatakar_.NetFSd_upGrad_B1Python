function calculatePercentage(score, total) {
  if (!total || total <= 0) return 0;
  return Math.round((score / total) * 100);
}

function getGrade(percent) {
  if (percent >= 80) return "A";
  else if (percent >= 60) return "B";
  else if (percent >= 40) return "C";
  else return "F";
}

function getPerformanceFeedback(percent) {
  let grade = getGrade(percent);
  switch (grade) {
    case "A":
      return "Outstanding performance! Excellent work!";
    case "B":
      return "Good job! You have a solid understanding.";
    case "C":
      return "Average. Review the material and try again.";
    case "F":
      return "Needs improvement. Please revisit the lessons.";
    default:
      return "Quiz completed.";
  }
}

function getResultStatus(percent) {
  return percent >= 40 ? "Pass" : "Fail";
}