using AutoMapper;
using ELearningPlatform.DTOs;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Services;

public class CourseService : ICourseService
{
    private readonly ICourseRepository _repo;
    private readonly IMapper _mapper;

    public CourseService(ICourseRepository repo, IMapper mapper)
    {
        _repo = repo;
        _mapper = mapper;
    }

    public async Task<IEnumerable<CourseResponseDto>> GetAllAsync()
    {
        var courses = await _repo.GetAllAsync();
        return _mapper.Map<IEnumerable<CourseResponseDto>>(courses);
    }

    public async Task<CourseResponseDto?> GetByIdAsync(int id)
    {
        var course = await _repo.GetByIdAsync(id);
        return course == null ? null : _mapper.Map<CourseResponseDto>(course);
    }

    public async Task<CourseResponseDto> CreateAsync(CreateCourseDto dto)
    {
        var course = _mapper.Map<Course>(dto);
        course.CreatedAt = DateTime.UtcNow;
        var created = await _repo.CreateAsync(course);
        var withDetails = await _repo.GetByIdAsync(created.CourseId);
        return _mapper.Map<CourseResponseDto>(withDetails!);
    }

    public async Task<CourseResponseDto?> UpdateAsync(int id, UpdateCourseDto dto)
    {
        var course = await _repo.GetByIdAsync(id);
        if (course == null) return null;

        course.Title = dto.Title;
        course.Description = dto.Description;

        await _repo.UpdateAsync(course);
        var updated = await _repo.GetByIdAsync(id);
        return _mapper.Map<CourseResponseDto>(updated!);
    }

    public async Task<bool> DeleteAsync(int id) =>
        await _repo.DeleteAsync(id);
}