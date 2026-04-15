using ELearningPlatform.DTOs;

namespace ELearningPlatform.Services.Interfaces;

public interface ILessonService
{
    Task<IEnumerable<LessonResponseDto>> GetByCourseIdAsync(int courseId);
    Task<LessonResponseDto> CreateAsync(CreateLessonDto dto);
    Task<LessonResponseDto?> UpdateAsync(int id, UpdateLessonDto dto);
    Task<bool> DeleteAsync(int id);
}