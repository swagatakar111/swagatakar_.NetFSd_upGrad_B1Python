using System.ComponentModel.DataAnnotations;

namespace ELearningPlatform.DTOs;

public class RegisterUserDto
{
    [Required] 
    public string FullName { get; set; } = string.Empty;
    
    [Required, EmailAddress] 
    public string Email { get; set; } = string.Empty;
    
    [Required, MinLength(6)] 
    public string Password { get; set; } = string.Empty;
}

public class UpdateUserDto
{
    [Required] 
    public string FullName { get; set; } = string.Empty;
    
    [Required, EmailAddress] 
    public string Email { get; set; } = string.Empty;
}

public class UserResponseDto
{
    public int UserId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}


public class LoginUserDto
{
    [Required, EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required]
    public string Password { get; set; } = string.Empty;
}