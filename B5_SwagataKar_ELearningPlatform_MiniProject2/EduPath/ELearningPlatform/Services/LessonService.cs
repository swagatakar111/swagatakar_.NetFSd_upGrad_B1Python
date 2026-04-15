using AutoMapper;
using ELearningPlatform.DTOs;
using ELearningPlatform.Models;
using ELearningPlatform.Repositories.Interfaces;
using ELearningPlatform.Services.Interfaces;

namespace ELearningPlatform.Services;

public class LessonService : ILessonService
{
    private readonly ILessonRepository _repo;
    private readonly IMapper _mapper;

    public LessonService(ILessonRepository repo, IMapper mapper)
    {
        _repo = repo;
        _mapper = mapper;
    }

    public async Task<IEnumerable<LessonResponseDto>> GetByCourseIdAsync(int courseId)
    {
        var lessons = await _repo.GetByCourseIdAsync(courseId);
        return _mapper.Map<IEnumerable<LessonResponseDto>>(lessons);
    }

    public async Task<LessonResponseDto> CreateAsync(CreateLessonDto dto)
    {
        var lesson = _mapper.Map<Lesson>(dto);
        var created = await _repo.CreateAsync(lesson);
        return _mapper.Map<LessonResponseDto>(created);
    }

    public async Task<LessonResponseDto?> UpdateAsync(int id, UpdateLessonDto dto)
    {
        var lesson = await _repo.GetByIdAsync(id);
        if (lesson == null) return null;

        lesson.Title = dto.Title;
        lesson.Content = dto.Content;
        lesson.OrderIndex = dto.OrderIndex;

        var updated = await _repo.UpdateAsync(lesson);
        return _mapper.Map<LessonResponseDto>(updated);
    }

    public async Task<bool> DeleteAsync(int id) =>
        await _repo.DeleteAsync(id);
}