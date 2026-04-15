using AutoMapper;
using ELearningPlatform.DTOs;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Services;

public class UserService : IUserService
{
    private readonly IUserRepository _repo;
    private readonly IMapper _mapper;

    public UserService(IUserRepository repo, IMapper mapper)
    {
        _repo = repo;
        _mapper = mapper;
    }

    public async Task<IEnumerable<UserResponseDto>> GetAllAsync()
    {
        var users = await _repo.GetAllAsync();
        return _mapper.Map<IEnumerable<UserResponseDto>>(users);
    }

    public async Task<UserResponseDto?> GetByIdAsync(int id)
    {
        var user = await _repo.GetByIdAsync(id);
        return user == null ? null : _mapper.Map<UserResponseDto>(user);
    }

    public async Task<UserResponseDto> RegisterAsync(RegisterUserDto dto)
    {
        var existing = await _repo.GetByEmailAsync(dto.Email);
        if (existing != null)
            throw new InvalidOperationException("Email already registered.");

        var user = _mapper.Map<User>(dto);
        user.PasswordHash = BCrypt.Net.BCrypt.HashPassword(dto.Password);
        user.CreatedAt = DateTime.UtcNow;

        var created = await _repo.CreateAsync(user);
        return _mapper.Map<UserResponseDto>(created);
    }

    public async Task<UserResponseDto?> UpdateAsync(int id, UpdateUserDto dto)
    {
        var user = await _repo.GetByIdAsync(id);
        if (user == null) return null;

        user.FullName = dto.FullName;
        user.Email = dto.Email;

        var updated = await _repo.UpdateAsync(user);
        return _mapper.Map<UserResponseDto>(updated);
    }

    public async Task<bool> DeleteAsync(int id) =>
        await _repo.DeleteAsync(id);

    public async Task<UserResponseDto?> LoginAsync(string email, string password)
    {
        var user = await _repo.GetByEmailAsync(email);
        if (user == null) return null;

        bool isValid = BCrypt.Net.BCrypt.Verify(password, user.PasswordHash);
        if (!isValid) return null;

        return _mapper.Map<UserResponseDto>(user);
    }
}