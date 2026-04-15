using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.Models;

public class Quiz
{
    public int QuizId { get; set; }

    public int CourseId { get; set; }

    [Required, MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    public Course? Course { get; set; }
    public ICollection<Question> Questions { get; set; } = new List<Question>();
    public ICollection<Result> Results { get; set; } = new List<Result>();
}