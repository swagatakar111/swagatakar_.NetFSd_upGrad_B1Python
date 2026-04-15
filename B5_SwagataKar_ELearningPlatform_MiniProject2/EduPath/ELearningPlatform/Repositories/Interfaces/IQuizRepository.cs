using ELearningPlatform.Models;

namespace ELearningPlatform.Repositories.Interfaces;

public interface IQuizRepository
{
    Task<IEnumerable<Quiz>> GetByCourseIdAsync(int courseId);
    Task<Quiz?> GetByIdAsync(int id);
    Task<Quiz?> GetWithQuestionsAsync(int id);
    Task<Quiz> CreateAsync(Quiz quiz);
    Task<bool> ExistsAsync(int id);
}