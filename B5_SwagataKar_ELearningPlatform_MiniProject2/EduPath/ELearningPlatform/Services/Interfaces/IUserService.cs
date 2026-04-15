using ELearningPlatform.DTOs;

namespace ELearningPlatform.Services.Interfaces;

public interface IUserService
{
    Task<IEnumerable<UserResponseDto>> GetAllAsync();
    Task<UserResponseDto?> GetByIdAsync(int id);
    Task<UserResponseDto> RegisterAsync(RegisterUserDto dto);
    Task<UserResponseDto?> UpdateAsync(int id, UpdateUserDto dto);
    Task<bool> DeleteAsync(int id);
    Task<UserResponseDto?> LoginAsync(string email, string password); // ← ADD THIS
}