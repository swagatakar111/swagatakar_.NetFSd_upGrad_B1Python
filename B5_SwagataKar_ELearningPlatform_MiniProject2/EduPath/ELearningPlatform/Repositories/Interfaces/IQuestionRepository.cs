using ELearningPlatform.Models;

namespace ELearningPlatform.Repositories.Interfaces;

public interface IQuestionRepository
{
    Task<IEnumerable<Question>> GetByQuizIdAsync(int quizId);
    Task<Question?> GetByIdAsync(int id);
    Task<Question> CreateAsync(Question question);
}