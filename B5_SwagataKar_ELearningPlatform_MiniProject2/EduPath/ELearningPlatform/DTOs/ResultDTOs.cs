namespace ELearningPlatform.DTOs;

public class QuizResultResponseDto
{
    public int ResultId { get; set; }
    public int UserId { get; set; }
    public int QuizId { get; set; }
    public string QuizTitle { get; set; } = string.Empty;
    public string CourseTitle { get; set; } = string.Empty;
    public int Score { get; set; }
    public int TotalQuestions { get; set; }
    public double Percentage { get; set; }
    public string Grade { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string Feedback { get; set; } = string.Empty;
    public DateTime AttemptDate { get; set; }
}