using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.DTOs;

public class CreateLessonDto
{
    [Required] 
    public int CourseId { get; set; }
    
    [Required] 
    public string Title { get; set; } = string.Empty;
    
    public string Content { get; set; } = string.Empty;
    
    public int OrderIndex { get; set; }
}

public class UpdateLessonDto
{
    [Required] 
    public string Title { get; set; } = string.Empty;
    
    public string Content { get; set; } = string.Empty;
    
    public int OrderIndex { get; set; }
}

public class LessonResponseDto
{
    public int LessonId { get; set; }
    public int CourseId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public int OrderIndex { get; set; }
}