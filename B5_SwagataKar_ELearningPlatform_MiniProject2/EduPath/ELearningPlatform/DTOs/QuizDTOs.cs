using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.DTOs;

public class CreateQuizDto
{
    [Required] 
    public int CourseId { get; set; }
    
    [Required] 
    public string Title { get; set; } = string.Empty;
}

public class QuizResponseDto
{
    public int QuizId { get; set; }
    public int CourseId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string CourseTitle { get; set; } = string.Empty;
    public int QuestionCount { get; set; }
}

public class CreateQuestionDto
{
    [Required] 
    public int QuizId { get; set; }
    
    [Required] 
    public string QuestionText { get; set; } = string.Empty;
    
    [Required] public string OptionA { get; set; } = string.Empty;
    [Required] public string OptionB { get; set; } = string.Empty;
    [Required] public string OptionC { get; set; } = string.Empty;
    [Required] public string OptionD { get; set; } = string.Empty;
    
    [Required, RegularExpression("^[ABCD]$")] 
    public string CorrectAnswer { get; set; } = string.Empty;
}

public class QuestionResponseDto
{
    public int QuestionId { get; set; }
    public int QuizId { get; set; }
    public string QuestionText { get; set; } = string.Empty;
    public string OptionA { get; set; } = string.Empty;
    public string OptionB { get; set; } = string.Empty;
    public string OptionC { get; set; } = string.Empty;
    public string OptionD { get; set; } = string.Empty;
    
}

public class SubmitQuizDto
{
    [Required] 
    public int UserId { get; set; }
    
    [Required] 
    public Dictionary<int, string> Answers { get; set; } = new();
    
}