using ELearningPlatform.Models;

namespace ELearningPlatform.Repositories.Interfaces;

public interface ILessonRepository
{
    Task<IEnumerable<Lesson>> GetByCourseIdAsync(int courseId);
    Task<Lesson?> GetByIdAsync(int id);
    Task<Lesson> CreateAsync(Lesson lesson);
    Task<Lesson> UpdateAsync(Lesson lesson);
    Task<bool> DeleteAsync(int id);
}