using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.DTOs;

public class CreateCourseDto
{
    [Required] 
    public string Title { get; set; } = string.Empty;
    
    public string Description { get; set; } = string.Empty;
    
    [Required] 
    public int CreatedBy { get; set; }
}

public class UpdateCourseDto
{
    [Required] 
    public string Title { get; set; } = string.Empty;
    
    public string Description { get; set; } = string.Empty;
}

public class CourseResponseDto
{
    public int CourseId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public int CreatedBy { get; set; }
    public string CreatorName { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    public int LessonCount { get; set; }
    public int QuizCount { get; set; }
}