using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.Models;

public class Question
{
    public int QuestionId { get; set; }

    public int QuizId { get; set; }

    [Required]
    public string QuestionText { get; set; } = string.Empty;

    [Required] public string OptionA { get; set; } = string.Empty;
    [Required] public string OptionB { get; set; } = string.Empty;
    [Required] public string OptionC { get; set; } = string.Empty;
    [Required] public string OptionD { get; set; } = string.Empty;

    [Required, MaxLength(1)]
    public string CorrectAnswer { get; set; } = string.Empty; // "A", "B", "C" or "D"

    
    public Quiz? Quiz { get; set; }
}