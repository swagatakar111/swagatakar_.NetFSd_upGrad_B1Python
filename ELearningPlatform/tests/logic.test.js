const { calculatePercentage, getGrade, getResultStatus } = require('../js/utils');
 
test("Percentage calculation", () => {
  expect(calculatePercentage(5, 10)).toBe(50);
});
 
test("Grade calculation", () => {
  expect(getGrade(85)).toBe("A");
});
 
test("Pass Fail determination", () => {
  expect(getResultStatus(30)).toBe("Fail");
});
 