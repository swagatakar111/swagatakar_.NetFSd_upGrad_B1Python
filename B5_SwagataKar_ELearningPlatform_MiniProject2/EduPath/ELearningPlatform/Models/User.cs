using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.Models;

public class User
{
    public int UserId { get; set; }

    [Required, MaxLength(100)]
    public string FullName { get; set; } = string.Empty;

    [Required, EmailAddress, MaxLength(150)]
    public string Email { get; set; } = string.Empty;

    [Required]
    public string PasswordHash { get; set; } = string.Empty;

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    
    public ICollection<Course> Courses { get; set; } = new List<Course>();
    public ICollection<Result> Results { get; set; } = new List<Result>();
}